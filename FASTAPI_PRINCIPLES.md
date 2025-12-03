# FastAPI 核心原理深度解析

## 目录

1. [ASGI 和异步编程](#asgi-和异步编程)
2. [类型系统和 Pydantic](#类型系统和-pydantic)
3. [依赖注入系统](#依赖注入系统)
4. [请求处理流程](#请求处理流程)
5. [自动文档生成](#自动文档生成)
6. [性能优化原理](#性能优化原理)

## ASGI 和异步编程

### 什么是 ASGI？

ASGI (Asynchronous Server Gateway Interface) 是 Python 异步 Web 服务器和应用程序之间的标准接口。

**WSGI vs ASGI:**

```python
# WSGI (同步)
def application(environ, start_response):
    # 处理请求
    return [b"Hello World"]

# ASGI (异步)
async def application(scope, receive, send):
    # 异步处理请求
    await send({
        'type': 'http.response.start',
        'status': 200,
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello World',
    })
```

### 异步优势

1. **高并发**: 单线程处理多个请求
2. **I/O 密集型优化**: 网络请求、数据库查询等
3. **资源利用**: 更少的内存和 CPU 使用

### FastAPI 异步示例

```python
from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()

@app.get("/sync")
def sync_endpoint():
    """同步端点 - 阻塞执行"""
    time.sleep(1)  # 阻塞整个线程
    return {"message": "Sync"}

@app.get("/async")
async def async_endpoint():
    """异步端点 - 非阻塞执行"""
    await asyncio.sleep(1)  # 不阻塞，可处理其他请求
    return {"message": "Async"}

@app.get("/external-api")
async def call_external_api():
    """异步调用外部 API"""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

### 何时使用异步？

**适合异步:**
- 网络请求（API 调用）
- 数据库查询（使用异步驱动）
- 文件 I/O
- WebSocket 连接

**不适合异步:**
- CPU 密集型计算
- 同步库调用
- 简单的内存操作

## 类型系统和 Pydantic

### Python 类型提示

FastAPI 完全基于 Python 3.6+ 的类型提示。

```python
from typing import List, Optional, Dict, Union

# 基础类型
def greet(name: str) -> str:
    return f"Hello {name}"

# 复杂类型
def process_items(items: List[Dict[str, Union[int, str]]]) -> None:
    for item in items:
        print(item)

# 可选类型
def get_user(user_id: int) -> Optional[User]:
    return db.get(user_id)  # 可能返回 None
```

### Pydantic 核心原理

Pydantic 使用 Python 类型提示进行运行时数据验证。

**工作流程:**

```
输入数据 → 类型检查 → 数据转换 → 自定义验证 → 验证成功/失败
```

**示例:**

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """用户模型"""
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    age: Optional[int] = Field(None, ge=0, le=150)
    created_at: datetime = Field(default_factory=datetime.now)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        """自定义验证器"""
        assert v.isalnum(), 'must be alphanumeric'
        return v
    
    @validator('email')
    def email_valid(cls, v):
        """邮箱验证"""
        assert '@' in v, 'invalid email'
        return v

# 使用
try:
    user = User(
        id=1,
        username="john123",
        email="john@example.com",
        age=30
    )
    print(user)
except ValidationError as e:
    print(e.json())
```

### Pydantic 高级特性

#### 1. Config 类

```python
class User(BaseModel):
    id: int
    name: str
    
    class Config:
        # 从 ORM 模型创建
        from_attributes = True
        
        # 不允许额外字段
        extra = 'forbid'
        
        # 字段别名
        fields = {
            'name': 'username'
        }
        
        # JSON 编码器
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### 2. 模型继承

```python
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    """创建用户 - 需要密码"""
    password: str

class UserResponse(UserBase):
    """响应用户 - 不包含密码"""
    id: int
    created_at: datetime
```

#### 3. 泛型模型

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    """通用响应模型"""
    code: int
    message: str
    data: Optional[T] = None

# 使用
user_response: Response[User] = Response(
    code=200,
    message="success",
    data=User(...)
)
```

## 依赖注入系统

### 依赖注入原理

依赖注入 (Dependency Injection) 是一种设计模式，用于管理对象之间的依赖关系。

**核心概念:**
- **依赖**: 函数或类需要的外部资源
- **注入**: 自动提供这些资源
- **容器**: 管理依赖的创建和生命周期

### FastAPI 依赖注入

#### 1. 基础依赖

```python
from fastapi import Depends

def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    """通用查询参数"""
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    """commons 自动注入"""
    return commons
```

#### 2. 类作为依赖

```python
class CommonQueryParams:
    """查询参数类"""
    def __init__(self, q: str = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
def read_items(commons: CommonQueryParams = Depends()):
    """自动实例化 CommonQueryParams"""
    return commons
```

#### 3. 依赖链

依赖可以依赖其他依赖。

```python
from sqlalchemy.orm import Session

def get_db():
    """数据库会话依赖"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)):
    """当前用户依赖（依赖于 db）"""
    # 从 token 获取用户
    user = db.query(User).first()
    return user

@app.get("/me")
def read_current_user(user: User = Depends(get_current_user)):
    """依赖链: get_current_user -> get_db"""
    return user
```

#### 4. 依赖缓存

同一请求中，依赖只执行一次。

```python
from fastapi import Depends

def expensive_dependency():
    """耗时的依赖"""
    print("Computing...")
    return "result"

@app.get("/test")
def test(
    dep1: str = Depends(expensive_dependency),
    dep2: str = Depends(expensive_dependency)
):
    """expensive_dependency 只执行一次"""
    return {"dep1": dep1, "dep2": dep2}
```

#### 5. 全局依赖

```python
app = FastAPI(dependencies=[Depends(verify_token)])

# 所有路由都会执行 verify_token
```

### 依赖注入的优势

1. **代码复用**: 共享的逻辑只写一次
2. **测试友好**: 易于 mock 依赖
3. **关注点分离**: 业务逻辑与基础设施分离
4. **自动文档**: 依赖自动出现在文档中

## 请求处理流程

### 完整的请求处理流程

```
1. 客户端发送请求
   ↓
2. Uvicorn (ASGI Server) 接收请求
   ↓
3. 中间件预处理 (Middleware Stack)
   ├─ CORS
   ├─ Logging
   └─ Custom Middleware
   ↓
4. FastAPI 路由匹配
   ├─ 路径匹配
   └─ HTTP 方法匹配
   ↓
5. 依赖注入解析
   ├─ 解析所有依赖
   ├─ 执行依赖函数
   └─ 缓存依赖结果
   ↓
6. 请求参数解析和验证
   ├─ 路径参数 (Path)
   ├─ 查询参数 (Query)
   ├─ 请求头 (Header)
   ├─ Cookie
   └─ 请求体 (Body)
   ↓
7. Pydantic 数据验证
   ├─ 类型检查
   ├─ 约束验证
   └─ 自定义验证器
   ↓
8. 执行路由处理函数
   ├─ 业务逻辑
   └─ 数据库操作
   ↓
9. 响应数据序列化
   ├─ Pydantic 模型转换
   └─ JSON 序列化
   ↓
10. 中间件后处理
    └─ 添加响应头
   ↓
11. 返回响应给客户端
```

### 详细示例

```python
from fastapi import FastAPI, Depends, Header, Query, Body
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI()

# 中间件
@app.middleware("http")
async def log_requests(request, call_next):
    """1. 中间件预处理"""
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response

# 依赖
def get_db():
    """2. 依赖注入"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token(authorization: str = Header(...)):
    """3. 验证令牌"""
    if authorization != "Bearer valid-token":
        raise HTTPException(status_code=401)
    return authorization

# 路由
@app.post("/users/")
def create_user(
    # 4. 查询参数
    notify: bool = Query(False),
    # 5. 请求体（Pydantic 验证）
    user: UserCreate = Body(...),
    # 6. 依赖注入
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    """
    完整的请求处理:
    1. 验证 token (依赖)
    2. 验证 user 数据 (Pydantic)
    3. 创建用户 (业务逻辑)
    4. 返回响应 (序列化)
    """
    # 7. 业务逻辑
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 8. 响应序列化
    return UserResponse.from_orm(db_user)
```

## 自动文档生成

### OpenAPI 规范

FastAPI 自动生成符合 OpenAPI 3.0 规范的文档。

**包含的信息:**
- 端点路径和方法
- 请求参数（路径、查询、请求体）
- 响应格式
- 数据模型
- 认证方式

### 文档定制

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API 描述",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "用户管理操作",
        },
        {
            "name": "items",
            "description": "物品管理操作",
        }
    ]
)

@app.post(
    "/users/",
    tags=["users"],
    summary="创建用户",
    description="创建一个新用户账户",
    response_description="创建的用户信息",
    responses={
        200: {
            "description": "成功",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "john"}
                }
            }
        },
        400: {"description": "错误的请求"},
        409: {"description": "用户已存在"}
    }
)
def create_user(user: UserCreate):
    """
    创建用户详细说明:
    
    - **username**: 唯一用户名
    - **email**: 用户邮箱
    - **password**: 强密码
    """
    return user
```

### 文档示例

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe"
            }
        }
```

## 性能优化原理

### 1. 异步数据库操作

```python
from databases import Database

database = Database("postgresql://...")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.get("/users/")
async def read_users():
    """异步数据库查询"""
    query = "SELECT * FROM users"
    users = await database.fetch_all(query)
    return users
```

### 2. 后台任务

不阻塞响应，在后台执行任务。

```python
from fastapi import BackgroundTasks

def send_email(email: str):
    """耗时的邮件发送"""
    time.sleep(5)
    print(f"Email sent to {email}")

@app.post("/register/")
def register(
    email: str,
    background_tasks: BackgroundTasks
):
    """注册后在后台发送邮件"""
    # 立即返回响应
    background_tasks.add_task(send_email, email)
    return {"message": "User registered"}
```

### 3. 响应缓存

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.get("/users/")
@cache(expire=60)  # 缓存 60 秒
async def read_users():
    """结果会被缓存"""
    return await fetch_users_from_db()
```

### 4. 流式响应

```python
from fastapi.responses import StreamingResponse

def generate_data():
    """生成器函数"""
    for i in range(1000):
        yield f"data {i}\n"

@app.get("/stream")
def stream():
    """流式响应，减少内存使用"""
    return StreamingResponse(
        generate_data(),
        media_type="text/plain"
    )
```

### 5. 连接池优化

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,           # 连接池大小
    max_overflow=40,        # 额外连接数
    pool_pre_ping=True,     # 连接前检查
    pool_recycle=3600,      # 连接回收时间
    echo_pool=True          # 调试连接池
)
```

### 6. 并发处理

```python
import asyncio

@app.get("/multi-api")
async def call_multiple_apis():
    """并发调用多个 API"""
    results = await asyncio.gather(
        fetch_api_1(),
        fetch_api_2(),
        fetch_api_3()
    )
    return results
```

## 总结

FastAPI 的核心原理包括:

1. **ASGI**: 异步服务器网关接口，支持高并发
2. **类型系统**: 基于 Python 类型提示和 Pydantic
3. **依赖注入**: 灵活的依赖管理系统
4. **自动文档**: 基于 OpenAPI 规范
5. **性能优化**: 异步、缓存、连接池等

理解这些原理有助于:
- 编写高性能的 API
- 设计良好的架构
- 解决实际问题
- 优化应用性能

**关键要点:**
- 适当使用异步（I/O 密集型）
- 利用类型提示和 Pydantic 验证
- 善用依赖注入提高代码质量
- 关注性能优化技术

# 架构设计文档

## 系统架构概览

本项目采用分层架构设计，将应用程序分为多个独立的层，每层负责特定的功能。

```
┌─────────────────────────────────────────┐
│           API Layer (FastAPI)           │  ← HTTP 请求/响应
│  ┌────────────┐      ┌───────────────┐  │
│  │  Users API │      │ Products API  │  │
│  └────────────┘      └───────────────┘  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Schema Layer (Pydantic)         │  ← 数据验证和序列化
│  ┌────────────┐      ┌───────────────┐  │
│  │UserSchemas │      │ProductSchemas │  │
│  └────────────┘      └───────────────┘  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Business Logic Layer (DAL)         │  ← 业务逻辑处理
│  ┌────────────┐      ┌───────────────┐  │
│  │  UserDAL   │      │  ProductDAL   │  │
│  └────────────┘      └───────────────┘  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Data Layer (SQLAlchemy ORM)        │  ← 数据持久化
│  ┌────────────┐      ┌───────────────┐  │
│  │ User Model │      │Product Model  │  │
│  └────────────┘      └───────────────┘  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          Database (MySQL)               │  ← 数据存储
│  ┌────────────┐      ┌───────────────┐  │
│  │users 表    │      │products 表    │  │
│  └────────────┘      └───────────────┘  │
└─────────────────────────────────────────┘
```

## 各层详解

### 1. API Layer（API 层）

**职责：**
- 处理 HTTP 请求和响应
- 路由管理
- 请求验证
- 响应格式化

**组件：**
- `app/api/v1/users.py` - 用户相关端点
- `app/api/v1/products.py` - 产品相关端点

**特点：**
- RESTful API 设计
- 统一的响应格式
- 完整的错误处理
- 自动生成 API 文档

### 2. Schema Layer（模式层）

**职责：**
- 请求数据验证
- 响应数据序列化
- 数据格式定义

**组件：**
- `app/schemas/user.py` - 用户数据模型
- `app/schemas/product.py` - 产品数据模型
- `app/schemas/common.py` - 通用数据模型

**特点：**
- 基于 Pydantic
- 自动类型验证
- 自定义验证器
- 模型继承和复用

### 3. Business Logic Layer（业务逻辑层）

**职责：**
- 封装业务逻辑
- 数据访问抽象
- 事务管理
- 复杂查询

**组件：**
- `app/dal/base.py` - 基础 DAL 类
- `app/dal/user_dal.py` - 用户数据访问
- `app/dal/product_dal.py` - 产品数据访问

**特点：**
- DAL（数据访问层）模式
- 泛型编程
- 可测试性高
- 代码复用

### 4. Data Layer（数据层）

**职责：**
- ORM 模型定义
- 数据库表映射
- 关系定义

**组件：**
- `app/models/base.py` - 基础模型
- `app/models/user.py` - 用户模型
- `app/models/product.py` - 产品模型

**特点：**
- SQLAlchemy ORM
- 声明式映射
- 关系管理
- 自动生成表结构

### 5. Database Layer（数据库层）

**职责：**
- 数据持久化
- 事务支持
- 数据完整性

**组件：**
- MySQL 数据库
- 表结构
- 索引
- 外键约束

## 数据流

### 请求流程（以创建用户为例）

```
1. HTTP POST /api/v1/users/
   ↓
2. FastAPI 路由匹配 → users.create_user()
   ↓
3. Pydantic 验证请求体 → UserCreate
   ↓
4. 依赖注入数据库会话 → get_db()
   ↓
5. 创建 DAL 实例 → UserDAL(db)
   ↓
6. 调用 DAL 方法 → user_dal.create()
   ↓
7. ORM 操作 → User(**data)
   ↓
8. SQL 执行 → INSERT INTO users ...
   ↓
9. 数据库返回 → 新用户记录
   ↓
10. ORM 映射 → User 对象
   ↓
11. Pydantic 序列化 → UserResponse
   ↓
12. 响应格式化 → ResponseModel
   ↓
13. JSON 响应 → 客户端
```

### 查询流程（以获取用户列表为例）

```
1. HTTP GET /api/v1/users/?skip=0&limit=10
   ↓
2. FastAPI 路由匹配 → users.get_users()
   ↓
3. 查询参数验证 → Query()
   ↓
4. 依赖注入数据库会话 → get_db()
   ↓
5. 创建 DAL 实例 → UserDAL(db)
   ↓
6. 调用 DAL 方法 → user_dal.get_multi()
   ↓
7. SQLAlchemy 查询 → query().offset().limit()
   ↓
8. SQL 执行 → SELECT * FROM users LIMIT 10 OFFSET 0
   ↓
9. 数据库返回 → 用户记录列表
   ↓
10. ORM 映射 → List[User]
   ↓
11. Pydantic 序列化 → List[UserResponse]
   ↓
12. 响应格式化 → ResponseModel[UserList]
   ↓
13. JSON 响应 → 客户端
```

## 核心设计模式

### 1. Repository Pattern（仓储模式）

通过 DAL 实现，将数据访问逻辑集中管理。

```python
class BaseDAL(Generic[ModelType]):
    def create(self, obj_in: Dict) -> ModelType:
        ...
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        ...
    
    def update(self, id: int, obj_in: Dict) -> Optional[ModelType]:
        ...
    
    def delete(self, id: int) -> bool:
        ...
```

### 2. Dependency Injection（依赖注入）

FastAPI 的核心特性，用于管理依赖关系。

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    ...
```

### 3. Factory Pattern（工厂模式）

SessionLocal 作为会话工厂，创建数据库会话。

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

### 4. Middleware Pattern（中间件模式）

处理横切关注点，如日志记录、CORS 等。

```python
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # 前置处理
        response = await call_next(request)
        # 后置处理
        return response
```

## 数据库设计

### 表结构

#### users 表

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    age INT,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);
```

#### products 表

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    stock INT DEFAULT 0,
    category VARCHAR(50),
    owner_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_category (category),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 关系设计

- **一对多关系**: User → Products
  - 一个用户可以拥有多个产品
  - 使用外键 `owner_id` 关联

## 安全考虑

### 1. SQL 注入防护

使用 ORM 参数化查询，自动防止 SQL 注入。

```python
# 安全的查询
db.query(User).filter(User.username == username).first()

# 避免字符串拼接
# "SELECT * FROM users WHERE username = '" + username + "'"  # 危险！
```

### 2. 密码安全

- 永远不存储明文密码
- 使用强哈希算法（bcrypt, argon2）
- 加盐处理

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = pwd_context.hash(password)
verified = pwd_context.verify(password, hashed_password)
```

### 3. 输入验证

Pydantic 自动验证所有输入数据。

```python
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # 自动验证邮箱格式
    age: int = Field(..., ge=0, le=150)  # 范围验证
```

### 4. CORS 配置

生产环境应该限制允许的源。

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 不要使用 "*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## 性能优化

### 1. 连接池

配置适当的连接池大小。

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # 基本连接数
    max_overflow=20,     # 额外连接数
    pool_pre_ping=True,  # 连接前检查
)
```

### 2. 索引优化

在常用查询字段上创建索引。

```python
username = Column(String(50), unique=True, index=True)
email = Column(String(100), unique=True, index=True)
category = Column(String(50), index=True)
```

### 3. 查询优化

使用 `joinedload` 或 `selectinload` 减少查询次数。

```python
# 避免 N+1 查询问题
from sqlalchemy.orm import joinedload

users = db.query(User).options(joinedload(User.products)).all()
```

### 4. 分页

始终对大型结果集进行分页。

```python
query.offset(skip).limit(limit).all()
```

## 错误处理

### 全局异常处理器

```python
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "Internal Server Error"}
    )
```

### 业务异常

使用 HTTPException 抛出业务异常。

```python
if not user:
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
```

## 测试策略

### 1. 单元测试

测试独立的函数和类。

```python
def test_user_dal_create():
    user_dal = UserDAL(db)
    user = user_dal.create({"username": "test"})
    assert user.username == "test"
```

### 2. 集成测试

测试多个组件的交互。

```python
def test_create_user_endpoint():
    response = client.post("/api/v1/users/", json={...})
    assert response.status_code == 201
```

### 3. 端到端测试

测试完整的用户流程。

## 部署建议

### 1. 环境变量

使用环境变量管理配置。

```bash
export DB_HOST=localhost
export DB_PASSWORD=secret
```

### 2. Docker 容器化

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. 反向代理

使用 Nginx 作为反向代理。

```nginx
location / {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 监控和日志

### 1. 日志记录

使用 Python logging 模块。

```python
import logging

logger = logging.getLogger(__name__)
logger.info("User created: %s", user.username)
```

### 2. 性能监控

记录请求处理时间。

```python
response.headers["X-Process-Time"] = str(process_time)
```

### 3. 健康检查

提供健康检查端点。

```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

## 总结

本架构设计遵循以下原则：

1. **关注点分离**: 每层负责特定功能
2. **高内聚低耦合**: 模块独立，接口清晰
3. **可扩展性**: 易于添加新功能
4. **可测试性**: 便于编写测试
5. **可维护性**: 代码结构清晰，易于维护

通过这种架构，我们实现了一个健壮、可扩展、易维护的 FastAPI 应用程序。

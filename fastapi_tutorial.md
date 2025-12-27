# Python FastAPI 详解与实战

## 目录

1. [FastAPI 简介](#1-fastapi-简介)
2. [安装与环境配置](#2-安装与环境配置)
3. [核心概念](#3-核心概念)
4. [路由与请求处理](#4-路由与请求处理)
5. [请求参数详解](#5-请求参数详解)
6. [Pydantic 数据模型](#6-pydantic-数据模型)
7. [依赖注入系统](#7-依赖注入系统)
8. [中间件与异常处理](#8-中间件与异常处理)
9. [数据库集成](#9-数据库集成)
10. [认证与授权](#10-认证与授权)
11. [异步编程](#11-异步编程)
12. [测试](#12-测试)
13. [部署](#13-部署)
14. [实战项目](#14-实战项目)

---

## 1. FastAPI 简介

### 1.1 什么是 FastAPI？

FastAPI 是一个现代、快速（高性能）的 Python Web 框架，用于构建 API。它基于 Python 3.7+ 的类型提示特性，具有以下核心优势：

| 特性 | 说明 |
|------|------|
| **高性能** | 与 NodeJS 和 Go 相当的性能（得益于 Starlette 和 Pydantic） |
| **快速开发** | 提高开发速度约 200% 到 300% |
| **更少的 Bug** | 减少约 40% 的人为错误 |
| **直观** | 强大的编辑器支持，自动补全 |
| **简单** | 易于学习和使用 |
| **标准化** | 基于 OpenAPI 和 JSON Schema |
| **自动文档** | 自动生成交互式 API 文档 |

### 1.2 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │    Starlette    │    │           Pydantic              │ │
│  │  (Web 框架核心)  │    │  (数据验证和序列化)              │ │
│  │  - 路由系统      │    │  - 类型验证                     │ │
│  │  - 请求/响应     │    │  - 数据模型                     │ │
│  │  - 中间件       │    │  - JSON Schema                  │ │
│  │  - WebSocket    │    │  - 自动文档生成                 │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                      ASGI Server                            │
│            (Uvicorn / Hypercorn / Daphne)                   │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 与其他框架对比

| 特性 | FastAPI | Flask | Django | Express |
|------|---------|-------|--------|---------|
| 异步支持 | ✅ 原生 | ⚠️ 需扩展 | ⚠️ 部分 | ✅ 原生 |
| 类型检查 | ✅ 内置 | ❌ | ❌ | ❌ |
| 自动文档 | ✅ 内置 | ❌ | ❌ | ❌ |
| 数据验证 | ✅ 内置 | ❌ | ⚠️ 部分 | ❌ |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| 学习曲线 | 低 | 低 | 高 | 低 |

---

## 2. 安装与环境配置

### 2.1 基础安装

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装 FastAPI 和 ASGI 服务器
pip install fastapi
pip install uvicorn[standard]

# 或一次性安装所有推荐依赖
pip install "fastapi[all]"
```

### 2.2 项目依赖文件 (requirements.txt)

```txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
sqlalchemy>=2.0.0
aiosqlite>=0.19.0
httpx>=0.26.0
pytest>=7.4.0
pytest-asyncio>=0.23.0
```

### 2.3 第一个 FastAPI 应用

```python
# main.py
from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI(
    title="My First API",
    description="这是我的第一个 FastAPI 应用",
    version="1.0.0"
)

# 定义路由
@app.get("/")
def read_root():
    """根路径端点"""
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """获取指定 ID 的项目"""
    return {"item_id": item_id, "query": q}
```

### 2.4 运行应用

```bash
# 开发模式（自动重载）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2.5 访问自动文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 3. 核心概念

### 3.1 ASGI vs WSGI

```
WSGI (同步)                          ASGI (异步)
┌─────────────┐                     ┌─────────────┐
│   Request   │                     │   Request   │
└──────┬──────┘                     └──────┬──────┘
       │                                   │
       ▼                                   ▼
┌─────────────┐                     ┌─────────────┐
│   Worker    │ ─ 等待 I/O ─        │   Worker    │ ─ 不等待，切换任务 ─
└─────────────┘                     └─────────────┘
       │                                   │
       ▼                                   ▼
┌─────────────┐                     ┌─────────────┐
│  Response   │                     │  Response   │
└─────────────┘                     └─────────────┘

特点：一个请求占用一个线程         特点：单线程处理多个并发请求
```

### 3.2 类型提示与自动验证

```python
from fastapi import FastAPI, Query, Path
from typing import Optional, List
from pydantic import BaseModel, Field

app = FastAPI()

# 类型提示自动生效
@app.get("/items/{item_id}")
async def read_item(
    item_id: int,                          # 路径参数，自动转换为 int
    q: Optional[str] = None,               # 可选查询参数
    skip: int = 0,                         # 带默认值的查询参数
    limit: int = Query(default=10, le=100) # 使用 Query 进行额外验证
):
    return {
        "item_id": item_id,
        "q": q,
        "skip": skip,
        "limit": limit
    }
```

### 3.3 请求-响应生命周期

```
客户端请求
    │
    ▼
┌─────────────────────────────────────┐
│         Uvicorn (ASGI Server)        │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           中间件 (Middleware)        │
│  - CORS                              │
│  - 认证                              │
│  - 日志                              │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           依赖注入 (Dependencies)    │
│  - 数据库会话                        │
│  - 当前用户                          │
│  - 权限检查                          │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           路由处理函数               │
│  - 参数验证                          │
│  - 业务逻辑                          │
│  - 返回响应                          │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           响应模型验证               │
│  - 数据序列化                        │
│  - 字段过滤                          │
└──────────────────┬──────────────────┘
                   │
                   ▼
              客户端响应
```

---

## 4. 路由与请求处理

### 4.1 HTTP 方法装饰器

```python
from fastapi import FastAPI

app = FastAPI()

# GET - 获取资源
@app.get("/items")
async def list_items():
    return {"items": []}

# POST - 创建资源
@app.post("/items")
async def create_item():
    return {"message": "Item created"}

# PUT - 完整更新资源
@app.put("/items/{item_id}")
async def update_item(item_id: int):
    return {"message": f"Item {item_id} updated"}

# PATCH - 部分更新资源
@app.patch("/items/{item_id}")
async def partial_update_item(item_id: int):
    return {"message": f"Item {item_id} partially updated"}

# DELETE - 删除资源
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}

# OPTIONS - 获取支持的方法
@app.options("/items")
async def options_items():
    return {"methods": ["GET", "POST"]}

# HEAD - 获取响应头
@app.head("/items")
async def head_items():
    return None
```

### 4.2 路由组织 - APIRouter

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def list_users():
    return {"users": []}

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@router.post("/")
async def create_user():
    return {"message": "User created"}

# routers/items.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/")
async def list_items():
    return {"items": []}

# main.py
from fastapi import FastAPI
from routers import users, items

app = FastAPI()

# 注册路由器
app.include_router(users.router)
app.include_router(items.router)

# 可以添加全局前缀
app.include_router(
    users.router,
    prefix="/api/v1"
)
```

### 4.3 路径操作配置

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

@app.post(
    "/items/",
    response_model=ItemResponse,           # 响应模型
    status_code=status.HTTP_201_CREATED,   # 响应状态码
    tags=["items"],                         # 文档标签
    summary="创建新项目",                    # 简短描述
    description="创建一个新的项目，需要提供名称和价格", # 详细描述
    response_description="成功创建的项目",   # 响应描述
    deprecated=False,                        # 是否弃用
    operation_id="create_item_custom_id"    # 操作 ID
)
async def create_item(item: Item):
    """
    创建项目，包含以下信息：
    
    - **name**: 项目名称（必填）
    - **price**: 项目价格（必填）
    """
    return ItemResponse(id=1, **item.model_dump())
```

### 4.4 路径参数详解

```python
from fastapi import FastAPI, Path
from enum import Enum

app = FastAPI()

# 枚举路径参数
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    return {"model_name": model_name}

# 路径参数验证
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        ...,                    # ... 表示必填
        title="项目 ID",
        description="要获取的项目的 ID",
        ge=1,                   # 大于等于 1
        le=1000,                # 小于等于 1000
        example=42
    )
):
    return {"item_id": item_id}

# 文件路径参数
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

---

## 5. 请求参数详解

### 5.1 查询参数 (Query Parameters)

```python
from fastapi import FastAPI, Query
from typing import Optional, List, Annotated

app = FastAPI()

# 基础查询参数
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# 使用 Query 进行验证
@app.get("/items/search")
async def search_items(
    # 必填查询参数
    q: Annotated[str, Query(min_length=3, max_length=50)] = ...,
    
    # 可选参数，带默认值
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    
    # 正则表达式验证
    code: Annotated[Optional[str], Query(pattern="^[A-Z]{2}[0-9]{4}$")] = None,
    
    # 列表参数
    tags: Annotated[List[str], Query()] = [],
    
    # 弃用参数
    old_param: Annotated[Optional[str], Query(deprecated=True)] = None
):
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
        "code": code,
        "tags": tags
    }

# 隐藏参数（不在文档中显示）
@app.get("/items/hidden")
async def hidden_query(
    visible: str,
    hidden: Annotated[Optional[str], Query(include_in_schema=False)] = None
):
    return {"visible": visible, "hidden": hidden}
```

### 5.2 请求体 (Request Body)

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional, Annotated

app = FastAPI()

# 基础请求体模型
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item

# 多个请求体参数
class User(BaseModel):
    username: str
    email: str

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(ge=1, le=5)]  # 单独的 Body 参数
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }

# 嵌入请求体
@app.post("/items/embedded")
async def create_item_embedded(
    item: Annotated[Item, Body(embed=True)]  # {"item": {...}}
):
    return item

# 使用 Field 进行字段验证
class ItemWithValidation(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Laptop"]
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="项目描述"
    )
    price: float = Field(
        ...,
        gt=0,
        description="价格必须大于零"
    )
    tax: Optional[float] = Field(
        None,
        ge=0,
        le=0.5,
        description="税率 (0-50%)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Laptop",
                    "description": "A high-performance laptop",
                    "price": 999.99,
                    "tax": 0.1
                }
            ]
        }
    }
```

### 5.3 请求头和 Cookie

```python
from fastapi import FastAPI, Header, Cookie
from typing import Optional, Annotated, List

app = FastAPI()

# 请求头参数
@app.get("/items/")
async def read_items(
    # 自动将 user_agent 转换为 User-Agent
    user_agent: Annotated[Optional[str], Header()] = None,
    
    # 自定义头名称
    x_token: Annotated[Optional[str], Header(alias="X-Token")] = None,
    
    # 重复的头（如多个 X-Token）
    x_tokens: Annotated[Optional[List[str]], Header()] = None
):
    return {
        "User-Agent": user_agent,
        "X-Token": x_token,
        "X-Tokens": x_tokens
    }

# Cookie 参数
@app.get("/items/cookie")
async def read_items_cookie(
    session_id: Annotated[Optional[str], Cookie()] = None,
    tracking_id: Annotated[Optional[str], Cookie(alias="tracking-id")] = None
):
    return {
        "session_id": session_id,
        "tracking_id": tracking_id
    }
```

### 5.4 表单数据和文件上传

```python
from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated, List

app = FastAPI()

# 表单数据
@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    return {"username": username}

# 文件上传 - 小文件
@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File(description="小文件作为 bytes")]
):
    return {"file_size": len(file)}

# 文件上传 - 大文件（推荐）
@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile  # 异步读取，不会一次性加载到内存
):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

# 多文件上传
@app.post("/uploadfiles/")
async def create_upload_files(
    files: List[UploadFile]
):
    return {"filenames": [f.filename for f in files]}

# 文件和表单数据混合
@app.post("/items/with-file/")
async def create_item_with_file(
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    file: UploadFile
):
    return {
        "name": name,
        "description": description,
        "filename": file.filename
    }
```

---

## 6. Pydantic 数据模型

### 6.1 基础模型定义

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# 枚举类型
class ItemStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

# 基础模型
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    tax: Optional[float] = Field(None, ge=0, le=1)
    status: ItemStatus = ItemStatus.draft
    tags: List[str] = []

# 创建时使用的模型
class ItemCreate(ItemBase):
    pass

# 更新时使用的模型（所有字段可选）
class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    tax: Optional[float] = Field(None, ge=0, le=1)
    status: Optional[ItemStatus] = None
    tags: Optional[List[str]] = None

# 数据库模型（包含 ID 和时间戳）
class ItemInDB(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# API 响应模型
class ItemResponse(ItemBase):
    id: int
    
    model_config = {
        "from_attributes": True  # 允许从 ORM 对象创建
    }
```

### 6.2 字段验证器

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
import re

class User(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    age: Optional[int] = None

    # 单字段验证器
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('用户名必须是字母数字')
        return v.lower()  # 转换为小写

    @field_validator('email')
    @classmethod
    def email_valid(cls, v: str) -> str:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, v):
            raise ValueError('无效的邮箱格式')
        return v.lower()

    @field_validator('age')
    @classmethod
    def age_valid(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 0 or v > 150):
            raise ValueError('年龄必须在 0-150 之间')
        return v

    # 模型级别验证器（验证多个字段）
    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('两次密码输入不一致')
        return self


class Product(BaseModel):
    name: str
    price: float
    discount_price: Optional[float] = None

    @model_validator(mode='after')
    def check_prices(self):
        if self.discount_price is not None:
            if self.discount_price >= self.price:
                raise ValueError('折扣价必须小于原价')
        return self
```

### 6.3 嵌套模型

```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class ContactInfo(BaseModel):
    email: str
    phone: Optional[str] = None

class OrderItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price

class Order(BaseModel):
    id: int
    customer_name: str
    contact: ContactInfo
    shipping_address: Address
    billing_address: Optional[Address] = None
    items: List[OrderItem]
    created_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "customer_name": "张三",
                    "contact": {
                        "email": "zhangsan@example.com",
                        "phone": "13800138000"
                    },
                    "shipping_address": {
                        "street": "中关村大街1号",
                        "city": "北京",
                        "country": "中国",
                        "postal_code": "100080"
                    },
                    "items": [
                        {
                            "product_id": 1,
                            "product_name": "笔记本电脑",
                            "quantity": 1,
                            "unit_price": 5999.00
                        }
                    ]
                }
            ]
        }
    }
```

### 6.4 响应模型控制

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional, List

app = FastAPI()

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool = True
    
    model_config = {"from_attributes": True}

class UserWithPassword(UserResponse):
    hashed_password: str

# 模拟数据库数据
fake_users_db = {
    1: {
        "id": 1,
        "email": "user@example.com",
        "username": "john",
        "hashed_password": "secret_hash",
        "is_active": True
    }
}

# response_model 过滤响应
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    # 即使返回的数据包含 hashed_password，也不会在响应中出现
    return fake_users_db[user_id]

# response_model_exclude 排除字段
@app.get(
    "/users/{user_id}/with-email",
    response_model=UserResponse,
    response_model_exclude={"email"}  # 排除 email
)
async def get_user_without_email(user_id: int):
    return fake_users_db[user_id]

# response_model_include 只包含指定字段
@app.get(
    "/users/{user_id}/minimal",
    response_model=UserResponse,
    response_model_include={"id", "username"}  # 只包含这些字段
)
async def get_user_minimal(user_id: int):
    return fake_users_db[user_id]

# response_model_exclude_unset 排除未设置的字段
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

@app.patch(
    "/items/{item_id}",
    response_model=ItemUpdate,
    response_model_exclude_unset=True  # 不返回值为 None 的字段
)
async def update_item(item_id: int, item: ItemUpdate):
    return item
```

---

## 7. 依赖注入系统

### 7.1 基础依赖

```python
from fastapi import FastAPI, Depends, Query
from typing import Annotated, Optional

app = FastAPI()

# 函数依赖
def common_parameters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
) -> dict:
    return {"skip": skip, "limit": limit}

# 类型别名简化
CommonParams = Annotated[dict, Depends(common_parameters)]

@app.get("/items/")
async def list_items(commons: CommonParams):
    return {"skip": commons["skip"], "limit": commons["limit"]}

@app.get("/users/")
async def list_users(commons: CommonParams):
    return {"skip": commons["skip"], "limit": commons["limit"]}
```

### 7.2 类作为依赖

```python
from fastapi import FastAPI, Depends, Query
from typing import Annotated, Optional

app = FastAPI()

# 使用类作为依赖
class Pagination:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量")
    ):
        self.page = page
        self.page_size = page_size
        self.skip = (page - 1) * page_size
        self.limit = page_size

@app.get("/items/")
async def list_items(pagination: Annotated[Pagination, Depends()]):
    return {
        "page": pagination.page,
        "page_size": pagination.page_size,
        "skip": pagination.skip,
        "limit": pagination.limit
    }
```

### 7.3 依赖链

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Annotated, Optional

app = FastAPI()

# 第一层依赖：获取 token
async def get_token(authorization: Annotated[Optional[str], Header()] = None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供认证信息")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证格式")
    
    return authorization.replace("Bearer ", "")

# 第二层依赖：验证 token 并获取用户
async def get_current_user(token: Annotated[str, Depends(get_token)]) -> dict:
    # 模拟 token 验证
    if token == "valid_token":
        return {"id": 1, "username": "john", "role": "user"}
    elif token == "admin_token":
        return {"id": 2, "username": "admin", "role": "admin"}
    
    raise HTTPException(status_code=401, detail="无效的 token")

# 第三层依赖：检查管理员权限
async def get_admin_user(
    user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user

# 使用依赖链
@app.get("/users/me")
async def read_current_user(user: Annotated[dict, Depends(get_current_user)]):
    return user

@app.get("/admin/dashboard")
async def admin_dashboard(admin: Annotated[dict, Depends(get_admin_user)]):
    return {"message": f"欢迎管理员 {admin['username']}"}
```

### 7.4 带 yield 的依赖（资源管理）

```python
from fastapi import FastAPI, Depends
from typing import Generator, Annotated
from contextlib import contextmanager

app = FastAPI()

# 模拟数据库会话
class DatabaseSession:
    def __init__(self):
        self.connected = False
    
    def connect(self):
        print("连接数据库...")
        self.connected = True
    
    def disconnect(self):
        print("断开数据库连接...")
        self.connected = False
    
    def query(self, sql: str):
        if not self.connected:
            raise RuntimeError("数据库未连接")
        return f"执行查询: {sql}"

# 使用 yield 的依赖
async def get_db() -> Generator[DatabaseSession, None, None]:
    db = DatabaseSession()
    db.connect()
    try:
        yield db  # 提供给路由函数使用
    finally:
        db.disconnect()  # 请求结束后执行清理

@app.get("/items/")
async def list_items(db: Annotated[DatabaseSession, Depends(get_db)]):
    result = db.query("SELECT * FROM items")
    return {"result": result}

# 带异常处理的 yield 依赖
async def get_db_with_transaction() -> Generator[DatabaseSession, None, None]:
    db = DatabaseSession()
    db.connect()
    try:
        yield db
        print("提交事务...")
    except Exception:
        print("回滚事务...")
        raise
    finally:
        db.disconnect()
```

### 7.5 全局依赖和路由依赖

```python
from fastapi import FastAPI, Depends, APIRouter, HTTPException, Header
from typing import Annotated

# 全局依赖
async def verify_api_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != "secret_api_key":
        raise HTTPException(status_code=403, detail="无效的 API Key")

# 应用全局依赖
app = FastAPI(dependencies=[Depends(verify_api_key)])

@app.get("/")
async def root():
    return {"message": "已通过 API Key 验证"}

# 路由器级别依赖
async def verify_admin_token(x_admin_token: Annotated[str, Header()]):
    if x_admin_token != "admin_secret":
        raise HTTPException(status_code=403, detail="需要管理员权限")

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_admin_token)]
)

@admin_router.get("/users")
async def list_admin_users():
    return {"users": ["admin1", "admin2"]}

@admin_router.get("/settings")
async def get_settings():
    return {"debug": False}

app.include_router(admin_router)
```

---

## 8. 中间件与异常处理

### 8.1 中间件

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
import logging

app = FastAPI()

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 信任主机中间件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "example.com", "*.example.com"]
)

# GZip 压缩中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 自定义中间件 - 请求计时
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 自定义中间件 - 请求日志
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"请求: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"响应: {response.status_code}")
    return response

# 自定义中间件类
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_name: str, header_value: str):
        super().__init__(app)
        self.header_name = header_name
        self.header_value = header_value

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers[self.header_name] = self.header_value
        return response

app.add_middleware(
    CustomHeaderMiddleware,
    header_name="X-Custom-Header",
    header_value="MyValue"
)
```

### 8.2 异常处理

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
from typing import Optional

app = FastAPI()

# 内置 HTTPException
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Item does not exist"}
        )
    return {"item_id": item_id}

# 自定义异常类
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

class InsufficientStockError(Exception):
    def __init__(self, item_id: int, requested: int, available: int):
        self.item_id = item_id
        self.requested = requested
        self.available = available

# 注册自定义异常处理器
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "item_not_found",
            "message": f"Item with id {exc.item_id} not found",
            "item_id": exc.item_id
        }
    )

@app.exception_handler(InsufficientStockError)
async def insufficient_stock_handler(request: Request, exc: InsufficientStockError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "insufficient_stock",
            "message": f"Not enough stock for item {exc.item_id}",
            "requested": exc.requested,
            "available": exc.available
        }
    )

# 覆盖验证错误处理
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "请求数据验证失败",
            "details": errors
        }
    )

# 全局异常处理（捕获所有未处理的异常）
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "服务器内部错误",
            "detail": str(exc)  # 生产环境中应该移除
        }
    )

# 使用自定义异常
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    if product_id == 0:
        raise ItemNotFoundError(item_id=product_id)
    return {"product_id": product_id}

@app.post("/orders/")
async def create_order(item_id: int, quantity: int):
    available = 5  # 模拟库存
    if quantity > available:
        raise InsufficientStockError(
            item_id=item_id,
            requested=quantity,
            available=available
        )
    return {"item_id": item_id, "quantity": quantity}
```

---

## 9. 数据库集成

### 9.1 SQLAlchemy 配置

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库 URL
# SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# PostgreSQL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
# MySQL
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # 仅 SQLite 需要
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话的依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 9.2 定义模型

```python
# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    items = relationship("Item", back_populates="owner")
    orders = relationship("Order", back_populates="user")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    owner = relationship("User", back_populates="items")
    order_items = relationship("OrderItem", back_populates="item")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    # 关系
    order = relationship("Order", back_populates="items")
    item = relationship("Item", back_populates="order_items")
```

### 9.3 Pydantic Schemas

```python
# schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}

# Item Schemas
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

# Order Schemas
class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    unit_price: float
    
    model_config = {"from_attributes": True}

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]
    
    model_config = {"from_attributes": True}
```

### 9.4 CRUD 操作

```python
# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
import models
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User CRUD
class UserCRUD:
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.email == email).first()
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.username == username).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
        return db.query(models.User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, user: schemas.UserCreate) -> models.User:
        hashed_password = pwd_context.hash(user.password)
        db_user = models.User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
        db_user = UserCRUD.get_by_id(db, user_id)
        if not db_user:
            return None
        
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        db_user = UserCRUD.get_by_id(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

# Item CRUD
class ItemCRUD:
    @staticmethod
    def get_by_id(db: Session, item_id: int) -> Optional[models.Item]:
        return db.query(models.Item).filter(models.Item.id == item_id).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> List[models.Item]:
        query = db.query(models.Item)
        
        if owner_id is not None:
            query = query.filter(models.Item.owner_id == owner_id)
        if is_active is not None:
            query = query.filter(models.Item.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, item: schemas.ItemCreate, owner_id: int) -> models.Item:
        db_item = models.Item(**item.model_dump(), owner_id=owner_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def update(db: Session, item_id: int, item: schemas.ItemUpdate) -> Optional[models.Item]:
        db_item = ItemCRUD.get_by_id(db, item_id)
        if not db_item:
            return None
        
        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def delete(db: Session, item_id: int) -> bool:
        db_item = ItemCRUD.get_by_id(db, item_id)
        if not db_item:
            return False
        
        db.delete(db_item)
        db.commit()
        return True
```

### 9.5 异步数据库（SQLAlchemy 2.0 + async）

```python
# async_database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 异步数据库 URL
DATABASE_URL = "sqlite+aiosqlite:///./async_app.db"
# PostgreSQL: "postgresql+asyncpg://user:password@localhost/dbname"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 打印 SQL 语句
)

# 创建异步会话工厂
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# 异步获取数据库会话
async def get_async_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# async_crud.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class AsyncItemCRUD:
    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: int):
        result = await db.execute(
            select(models.Item).where(models.Item.id == item_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(models.Item).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def create(db: AsyncSession, item: schemas.ItemCreate, owner_id: int):
        db_item = models.Item(**item.model_dump(), owner_id=owner_id)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item
```

---

## 10. 认证与授权

### 10.1 密码哈希

```python
# auth/password.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """对密码进行哈希处理"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)
```

### 10.2 JWT Token

```python
# auth/jwt.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel

# 配置
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    scopes: list[str] = []

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[TokenData]:
    """解码令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        username: str = payload.get("username")
        scopes: list = payload.get("scopes", [])
        
        if user_id is None:
            return None
        
        return TokenData(user_id=user_id, username=username, scopes=scopes)
    except JWTError:
        return None
```

### 10.3 OAuth2 认证流程

```python
# auth/oauth2.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from database import get_db
from auth.jwt import decode_token, create_access_token, create_refresh_token, Token
from auth.password import verify_password
import crud
import models

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scopes={
        "read": "读取权限",
        "write": "写入权限",
        "admin": "管理员权限"
    }
)

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> models.User:
    """获取当前用户"""
    
    # 构建认证异常
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": authenticate_value}
    )
    
    # 解码 token
    token_data = decode_token(token)
    if token_data is None:
        raise credentials_exception
    
    # 获取用户
    user = crud.UserCRUD.get_by_id(db, token_data.user_id)
    if user is None:
        raise credentials_exception
    
    # 检查权限范围
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足",
                headers={"WWW-Authenticate": authenticate_value}
            )
    
    return user

async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> models.User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user

# auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    """用户登录"""
    # 验证用户
    user = crud.UserCRUD.get_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # 确定用户权限
    scopes = ["read", "write"]
    if user.username == "admin":
        scopes.append("admin")
    
    # 创建令牌
    token_data = {
        "sub": user.id,
        "username": user.username,
        "scopes": scopes
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Annotated[Session, Depends(get_db)]
):
    """刷新令牌"""
    token_data = decode_token(refresh_token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    user = crud.UserCRUD.get_by_id(db, token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    # 创建新令牌
    new_token_data = {
        "sub": user.id,
        "username": user.username,
        "scopes": token_data.scopes
    }
    
    new_access_token = create_access_token(new_token_data)
    new_refresh_token = create_refresh_token(new_token_data)
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )
```

### 10.4 使用认证的路由

```python
from fastapi import APIRouter, Depends, Security
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])

# 需要登录
@router.get("/me")
async def read_current_user(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user

# 需要特定权限
@router.get("/items")
async def read_own_items(
    current_user: Annotated[
        models.User,
        Security(get_current_active_user, scopes=["read"])
    ],
    db: Annotated[Session, Depends(get_db)]
):
    return crud.ItemCRUD.get_all(db, owner_id=current_user.id)

# 需要管理员权限
@router.get("/admin/users")
async def read_all_users(
    current_user: Annotated[
        models.User,
        Security(get_current_active_user, scopes=["admin"])
    ],
    db: Annotated[Session, Depends(get_db)]
):
    return crud.UserCRUD.get_all(db)
```

---

## 11. 异步编程

### 11.1 async/await 基础

```python
from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()

# 同步函数 vs 异步函数
@app.get("/sync")
def sync_endpoint():
    """同步端点 - 会阻塞线程"""
    import time
    time.sleep(1)  # 阻塞
    return {"message": "同步完成"}

@app.get("/async")
async def async_endpoint():
    """异步端点 - 不会阻塞"""
    await asyncio.sleep(1)  # 非阻塞
    return {"message": "异步完成"}

# 并发执行多个异步任务
@app.get("/concurrent")
async def concurrent_requests():
    """并发执行多个 HTTP 请求"""
    async with httpx.AsyncClient() as client:
        # 并发发送多个请求
        tasks = [
            client.get("https://httpbin.org/delay/1"),
            client.get("https://httpbin.org/delay/1"),
            client.get("https://httpbin.org/delay/1"),
        ]
        
        # 等待所有请求完成
        responses = await asyncio.gather(*tasks)
        
        return {
            "message": "并发完成",
            "status_codes": [r.status_code for r in responses]
        }
```

### 11.2 后台任务

```python
from fastapi import FastAPI, BackgroundTasks
from typing import Annotated

app = FastAPI()

# 后台任务函数
def write_log(message: str):
    """写入日志（同步）"""
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

async def send_email(email: str, message: str):
    """发送邮件（异步模拟）"""
    import asyncio
    await asyncio.sleep(2)  # 模拟发送
    print(f"邮件已发送到 {email}: {message}")

async def process_data(data: dict):
    """处理数据"""
    import asyncio
    await asyncio.sleep(5)  # 模拟耗时处理
    print(f"数据处理完成: {data}")

# 使用后台任务
@app.post("/items/")
async def create_item(
    background_tasks: BackgroundTasks,
    name: str
):
    # 添加后台任务（立即返回响应）
    background_tasks.add_task(write_log, f"创建了项目: {name}")
    background_tasks.add_task(send_email, "admin@example.com", f"新项目: {name}")
    
    return {"message": f"项目 {name} 已创建，后台任务正在处理"}

# 依赖中的后台任务
async def log_request(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(write_log, message)
    return message

@app.get("/items/{item_id}")
async def read_item(
    item_id: int,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"访问了项目 {item_id}")
    return {"item_id": item_id}
```

### 11.3 异步上下文管理器

```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import httpx

# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动和关闭时的处理"""
    # 启动时执行
    print("应用启动...")
    app.state.http_client = httpx.AsyncClient()
    
    yield  # 应用运行中
    
    # 关闭时执行
    print("应用关闭...")
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/external")
async def call_external_api():
    """使用共享的 HTTP 客户端"""
    client = app.state.http_client
    response = await client.get("https://api.github.com")
    return {"status": response.status_code}

# 自定义异步上下文管理器依赖
class AsyncDatabaseConnection:
    async def connect(self):
        print("连接数据库...")
        return self
    
    async def disconnect(self):
        print("断开数据库连接...")
    
    async def query(self, sql: str):
        return f"Result of: {sql}"

@asynccontextmanager
async def get_async_db() -> AsyncGenerator[AsyncDatabaseConnection, None]:
    db = AsyncDatabaseConnection()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

@app.get("/data")
async def get_data():
    async with get_async_db() as db:
        result = await db.query("SELECT * FROM users")
        return {"result": result}
```

---

## 12. 测试

### 12.1 基础测试

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

def test_read_item():
    """测试获取项目"""
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["item_id"] == 1

def test_read_item_with_query():
    """测试带查询参数"""
    response = client.get("/items/1?q=test")
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == 1
    assert data["query"] == "test"

def test_create_item():
    """测试创建项目"""
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.5}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"

def test_validation_error():
    """测试验证错误"""
    response = client.post(
        "/items/",
        json={"name": "", "price": -1}  # 无效数据
    )
    assert response.status_code == 422
```

### 12.2 异步测试

```python
# test_async.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
async def async_client():
    """异步测试客户端 fixture"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_async_root(async_client: AsyncClient):
    """异步测试根路径"""
    response = await async_client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_async_create_item(async_client: AsyncClient):
    """异步测试创建项目"""
    response = await async_client.post(
        "/items/",
        json={"name": "Async Item", "price": 25.0}
    )
    assert response.status_code == 201
```

### 12.3 数据库测试

```python
# test_database.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 测试数据库依赖
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 覆盖依赖
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    """每个测试前创建表，测试后清理"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_user():
    """测试创建用户"""
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data  # 密码不应返回

def test_create_duplicate_user():
    """测试创建重复用户"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    
    # 第一次创建
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    
    # 重复创建
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
```

### 12.4 认证测试

```python
# test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    """获取认证头"""
    # 先注册用户
    client.post(
        "/users/",
        json={
            "email": "auth@example.com",
            "username": "authuser",
            "password": "authpass123"
        }
    )
    
    # 登录获取 token
    response = client.post(
        "/auth/login",
        data={
            "username": "authuser",
            "password": "authpass123"
        }
    )
    tokens = response.json()
    
    return {"Authorization": f"Bearer {tokens['access_token']}"}

def test_protected_route_without_auth():
    """测试未认证访问保护路由"""
    response = client.get("/users/me")
    assert response.status_code == 401

def test_protected_route_with_auth(auth_headers):
    """测试认证后访问保护路由"""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "authuser"

def test_invalid_token():
    """测试无效 token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401
```

---

## 13. 部署

### 13.1 Uvicorn 生产配置

```python
# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "FastAPI App"
    debug: bool = False
    
    # 数据库配置
    database_url: str = "sqlite:///./app.db"
    
    # JWT 配置
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS 配置
    cors_origins: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

```bash
# 生产启动命令
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --loop uvloop \
    --http h11 \
    --no-access-log
```

### 13.2 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

### 13.3 Nginx 配置

```nginx
# nginx.conf
upstream fastapi {
    server web:8000;
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /app/static;
        expires 30d;
    }
}
```

---

## 14. 实战项目

### 14.1 项目结构

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库配置
│   ├── models/              # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # Pydantic 模式
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── crud/                # CRUD 操作
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── api/                 # API 路由
│   │   ├── __init__.py
│   │   ├── deps.py          # 依赖
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── users.py
│   │       └── items.py
│   ├── core/                # 核心功能
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── exceptions.py
│   └── utils/               # 工具函数
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── alembic/                 # 数据库迁移
│   ├── versions/
│   └── env.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

完整实战代码请参考 `examples/` 目录。

---

## 总结

FastAPI 是一个功能强大、易于使用的现代 Python Web 框架。本教程涵盖了：

1. **基础概念**：FastAPI 架构、ASGI、类型提示
2. **路由系统**：HTTP 方法、路由组织、参数处理
3. **数据验证**：Pydantic 模型、字段验证、嵌套模型
4. **依赖注入**：函数依赖、类依赖、依赖链、资源管理
5. **中间件**：CORS、自定义中间件、异常处理
6. **数据库**：SQLAlchemy 集成、CRUD 操作、异步数据库
7. **认证授权**：JWT、OAuth2、权限控制
8. **异步编程**：async/await、后台任务、生命周期管理
9. **测试**：同步测试、异步测试、数据库测试
10. **部署**：Docker、Nginx、生产配置

FastAPI 的核心优势在于其优秀的开发体验和高性能，非常适合构建现代 API 服务。

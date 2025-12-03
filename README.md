# FastAPI 原理与实战 + ORM + MySQL DAL

这是一个完整的 FastAPI 应用示例，展示了 FastAPI 的核心原理和最佳实践，包括 SQLAlchemy ORM、MySQL 数据库集成和数据访问层（DAL）模式。

## 📚 项目特点

### 🎯 核心技术栈
- **FastAPI**: 现代、高性能的 Python Web 框架
- **SQLAlchemy**: 强大的 Python ORM
- **MySQL**: 关系型数据库
- **Pydantic**: 数据验证和设置管理
- **Uvicorn**: ASGI 服务器

### 🏗️ 架构设计
- **分层架构**: API层、业务逻辑层、数据访问层
- **DAL模式**: 数据访问层封装所有数据库操作
- **依赖注入**: FastAPI 的依赖注入系统
- **中间件**: 日志记录、CORS 配置
- **异常处理**: 统一的异常处理机制

## 📁 项目结构

```
.
├── app/                        # 应用程序包
│   ├── api/                    # API 路由
│   │   └── v1/                 # API 版本 1
│   │       ├── users.py        # 用户路由
│   │       └── products.py     # 产品路由
│   ├── core/                   # 核心功能
│   │   └── database.py         # 数据库配置和连接
│   ├── dal/                    # 数据访问层
│   │   ├── base.py             # 基础 DAL
│   │   ├── user_dal.py         # 用户 DAL
│   │   └── product_dal.py      # 产品 DAL
│   ├── middleware/             # 中间件
│   │   ├── logging.py          # 日志中间件
│   │   └── cors.py             # CORS 配置
│   ├── models/                 # ORM 模型
│   │   ├── base.py             # 基础模型
│   │   ├── user.py             # 用户模型
│   │   └── product.py          # 产品模型
│   └── schemas/                # Pydantic 模型
│       ├── common.py           # 通用模型
│       ├── user.py             # 用户模型
│       └── product.py          # 产品模型
├── config.py                   # 配置文件
├── main.py                     # 应用入口
├── requirements.txt            # 依赖列表
├── .env.example                # 环境变量示例
└── README.md                   # 项目文档
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=fastapi_demo

# 应用配置
APP_NAME=FastAPI Demo
APP_VERSION=1.0.0
DEBUG=True
```

### 5. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE fastapi_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. 运行应用

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. 访问 API 文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📖 核心概念详解

### 1. FastAPI 基础

FastAPI 是一个现代、快速（高性能）的 Web 框架，用于构建 API。

**主要特点：**
- 基于标准的 Python 类型提示
- 自动生成 API 文档
- 数据验证（基于 Pydantic）
- 异步支持
- 依赖注入系统

**示例：**

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    # item_id 自动验证为整数
    # db 通过依赖注入获取
    return {"item_id": item_id}
```

### 2. SQLAlchemy ORM

ORM（对象关系映射）允许使用 Python 类和对象来操作数据库。

**示例：**

```python
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
```

**原理：**
- 每个类对应一张表
- 每个类属性对应一列
- 类实例对应表中的一行

### 3. 数据访问层（DAL）模式

DAL 模式将数据库操作封装到专门的类中。

**优点：**
- 分离关注点
- 提高可测试性
- 便于维护和复用

**示例：**

```python
class UserDAL(BaseDAL[User]):
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
```

### 4. Pydantic 数据验证

Pydantic 提供数据验证和设置管理。

**示例：**

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)
```

**自动验证：**
- 类型检查
- 长度限制
- 范围验证
- 自定义验证器

### 5. 依赖注入

FastAPI 的依赖注入系统允许声明代码所需的依赖。

**示例：**

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    # db 自动注入
    pass
```

## 🔧 API 端点

### 用户管理

- `POST /api/v1/users/` - 创建用户
- `GET /api/v1/users/` - 获取用户列表
- `GET /api/v1/users/{user_id}` - 获取用户详情
- `PUT /api/v1/users/{user_id}` - 更新用户
- `DELETE /api/v1/users/{user_id}` - 删除用户
- `GET /api/v1/users/search/by-name` - 搜索用户

### 产品管理

- `POST /api/v1/products/` - 创建产品
- `GET /api/v1/products/` - 获取产品列表
- `GET /api/v1/products/{product_id}` - 获取产品详情
- `PUT /api/v1/products/{product_id}` - 更新产品
- `DELETE /api/v1/products/{product_id}` - 删除产品
- `GET /api/v1/products/search/by-name` - 搜索产品
- `GET /api/v1/products/price-range/query` - 价格区间查询
- `PATCH /api/v1/products/{product_id}/stock` - 更新库存
- `GET /api/v1/products/statistics/by-category` - 分类统计

## 📝 使用示例

### 创建用户

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secret123",
    "full_name": "John Doe",
    "age": 30
  }'
```

### 获取用户列表

```bash
curl "http://localhost:8000/api/v1/users/?skip=0&limit=10"
```

### 创建产品

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "description": "最新款苹果手机",
    "price": 7999.00,
    "stock": 100,
    "category": "电子产品"
  }'
```

### 价格区间查询

```bash
curl "http://localhost:8000/api/v1/products/price-range/query?min_price=5000&max_price=10000"
```

## 🎓 学习要点

### 1. FastAPI 核心原理

- **ASGI 框架**: 异步网关接口，支持异步处理
- **类型提示**: 利用 Python 类型提示进行验证和文档生成
- **依赖注入**: 灵活的依赖管理系统
- **自动文档**: 基于 OpenAPI 和 JSON Schema

### 2. SQLAlchemy ORM 原理

- **会话管理**: Session 对象管理数据库事务
- **查询构建**: 链式调用构建 SQL 查询
- **关系映射**: relationship() 定义表之间的关系
- **懒加载/急加载**: 控制关联对象的加载方式

### 3. 数据库连接池

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,      # 连接池大小
    max_overflow=20,   # 最大溢出连接数
    pool_pre_ping=True # 连接前检查有效性
)
```

### 4. 事务管理

```python
db = SessionLocal()
try:
    # 执行数据库操作
    db.add(obj)
    db.commit()  # 提交事务
except Exception:
    db.rollback()  # 回滚事务
finally:
    db.close()  # 关闭会话
```

## 🔐 最佳实践

### 1. 安全性

- 密码哈希（使用 bcrypt 或 passlib）
- JWT 认证
- HTTPS 加密
- SQL 注入防护（ORM 自动处理）
- XSS 防护

### 2. 性能优化

- 连接池配置
- 索引优化
- 查询优化（使用 select_related 等）
- 缓存策略
- 异步处理

### 3. 代码质量

- 类型提示
- 文档注释
- 单元测试
- 代码格式化（black, isort）
- 静态类型检查（mypy）

### 4. 项目结构

- 分层架构
- 关注点分离
- 模块化设计
- 配置管理
- 日志记录

## 🧪 测试

### 单元测试示例

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123"
        }
    )
    assert response.status_code == 201
    assert response.json()["data"]["username"] == "testuser"
```

## 📊 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
# 初始化
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head

# 回滚
alembic downgrade -1
```

## 🐛 常见问题

### 1. 数据库连接失败

检查：
- MySQL 服务是否运行
- 配置文件中的数据库信息
- 防火墙设置
- 数据库用户权限

### 2. 导入错误

确保：
- 虚拟环境已激活
- 所有依赖已安装
- Python 版本 >= 3.7

### 3. 端口被占用

更改端口：
```bash
uvicorn main:app --port 8001
```

## 📚 扩展学习

### 推荐资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [MySQL 文档](https://dev.mysql.com/doc/)

### 进阶主题

- JWT 认证和授权
- WebSocket 实时通信
- 后台任务（Celery）
- 缓存（Redis）
- 微服务架构
- Docker 容器化
- CI/CD 自动化部署

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

Created with ❤️ for learning FastAPI, ORM, and MySQL DAL patterns.

---

**Happy Coding! 🚀**

# FastAPI 实战项目示例

这是一个完整的 FastAPI 项目示例，展示了如何构建一个生产就绪的 API 服务。

## 功能特性

- 🔐 **用户认证**: JWT Token 认证，支持访问令牌和刷新令牌
- 👥 **用户管理**: 用户注册、登录、个人信息管理、管理员功能
- 📦 **商品管理**: 完整的 CRUD 操作、标签系统、搜索功能
- 🗄️ **数据库**: SQLAlchemy ORM，支持 SQLite/PostgreSQL
- 📚 **自动文档**: Swagger UI 和 ReDoc
- 🧪 **测试**: 完整的单元测试和集成测试
- 🐳 **Docker**: 容器化部署支持

## 项目结构

```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库配置
│   ├── models/              # SQLAlchemy 模型
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # Pydantic 模式
│   │   ├── user.py
│   │   ├── item.py
│   │   └── token.py
│   ├── crud/                # CRUD 操作
│   │   ├── user.py
│   │   └── item.py
│   ├── api/                 # API 路由
│   │   ├── deps.py          # 依赖
│   │   └── v1/
│   │       ├── router.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       └── items.py
│   ├── core/                # 核心功能
│   │   ├── security.py      # 安全相关
│   │   └── exceptions.py    # 自定义异常
│   └── utils/               # 工具函数
│       └── pagination.py
├── tests/                   # 测试
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_items.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
# 安装 uv (如果尚未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装依赖 (使用 uv，比 pip 快 10-100 倍)
uv pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件，修改必要的配置
```

### 3. 运行应用

```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload

# 或使用 Python 直接运行
python -m app.main
```

### 4. 访问文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Docker 部署

### 使用 Docker Compose

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 单独使用 Docker

```bash
# 构建镜像
docker build -t fastapi-app .

# 运行容器
docker run -d -p 8000:8000 --name fastapi-app fastapi-app
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_auth.py

# 显示详细输出
pytest -v

# 显示覆盖率
pytest --cov=app --cov-report=html
```

## API 端点

### 认证

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/login | 用户登录 |
| POST | /api/v1/auth/refresh | 刷新令牌 |

### 用户

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| GET | /api/v1/users/me | 获取当前用户 | 认证 |
| PUT | /api/v1/users/me | 更新当前用户 | 认证 |
| GET | /api/v1/users | 获取用户列表 | 管理员 |
| GET | /api/v1/users/{id} | 获取指定用户 | 管理员 |
| PUT | /api/v1/users/{id} | 更新指定用户 | 管理员 |
| DELETE | /api/v1/users/{id} | 删除用户 | 超级管理员 |

### 商品

| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| GET | /api/v1/items | 获取商品列表 | 公开 |
| GET | /api/v1/items/my | 获取我的商品 | 认证 |
| GET | /api/v1/items/{id} | 获取商品详情 | 公开 |
| POST | /api/v1/items | 创建商品 | 写入 |
| PUT | /api/v1/items/{id} | 更新商品 | 写入 |
| DELETE | /api/v1/items/{id} | 删除商品 | 写入 |
| POST | /api/v1/items/{id}/stock | 更新库存 | 写入 |
| GET | /api/v1/items/tags | 获取标签列表 | 公开 |
| POST | /api/v1/items/tags | 创建标签 | 写入 |

## 使用示例

### 注册用户

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "TestPass123",
    "full_name": "Test User"
  }'
```

### 登录

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=TestPass123"
```

### 创建商品

```bash
curl -X POST "http://localhost:8000/api/v1/items" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "description": "Apple 最新款智能手机",
    "price": 7999.00,
    "stock": 100
  }'
```

## 配置说明

| 变量 | 描述 | 默认值 |
|------|------|--------|
| APP_NAME | 应用名称 | FastAPI Demo |
| DEBUG | 调试模式 | false |
| DATABASE_URL | 数据库连接 URL | sqlite:///./app.db |
| SECRET_KEY | JWT 密钥 | - |
| ACCESS_TOKEN_EXPIRE_MINUTES | 访问令牌过期时间 | 30 |
| CORS_ORIGINS | CORS 允许的源 | ["http://localhost:3000"] |

## 许可证

MIT License

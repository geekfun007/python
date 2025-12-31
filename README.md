# FastAPI 实战项目

一个完整的 FastAPI 实战项目，包含用户认证、CRUD 操作、中间件、Docker 部署等功能。

## 🚀 功能特性

- **用户认证**: JWT 令牌认证，支持访问令牌和刷新令牌
- **用户管理**: 注册、登录、用户 CRUD 操作
- **物品管理**: 完整的物品 CRUD、搜索、分页功能
- **中间件**: 日志记录、请求追踪、计时统计、错误处理
- **数据库**: PostgreSQL + SQLAlchemy 异步 ORM
- **缓存**: Redis 缓存支持
- **容器化**: Docker Compose 一键部署
- **反向代理**: Nginx 负载均衡和静态资源服务

## 📁 项目结构

```
.
├── app/
│   ├── api/                    # API 路由
│   │   ├── v1/                 # V1 版本 API
│   │   │   ├── auth.py         # 认证 API
│   │   │   ├── users.py        # 用户 API
│   │   │   ├── items.py        # 物品 API
│   │   │   └── health.py       # 健康检查 API
│   │   └── router.py           # 路由汇总
│   ├── core/                   # 核心配置
│   │   ├── config.py           # 应用配置
│   │   ├── security.py         # 安全相关（JWT、密码哈希）
│   │   └── exceptions.py       # 自定义异常
│   ├── db/                     # 数据库
│   │   ├── base.py             # 基础模型
│   │   └── session.py          # 数据库会话
│   ├── middlewares/            # 中间件
│   │   ├── auth.py             # 认证中间件
│   │   ├── logging.py          # 日志中间件
│   │   ├── request_id.py       # 请求ID中间件
│   │   ├── timing.py           # 计时中间件
│   │   └── error_handler.py    # 错误处理中间件
│   ├── models/                 # ORM 模型
│   │   ├── user.py             # 用户模型
│   │   └── item.py             # 物品模型
│   ├── repositories/           # 数据访问层 (DAL)
│   │   ├── base.py             # 基础仓库
│   │   ├── user.py             # 用户仓库
│   │   └── item.py             # 物品仓库
│   ├── schemas/                # Pydantic 模型 (API Schema)
│   │   ├── base.py             # 基础 Schema
│   │   ├── user.py             # 用户 Schema
│   │   └── item.py             # 物品 Schema
│   ├── thrift_gen/             # Thrift IDL 加载和转换
│   │   ├── __init__.py         # 动态加载 Thrift 模块
│   │   └── converters.py       # 类型转换器
│   ├── services/               # 业务逻辑层
│   │   ├── auth.py             # 认证服务
│   │   ├── user.py             # 用户服务
│   │   └── item.py             # 物品服务
│   └── main.py                 # 应用入口
├── idl/                        # Thrift IDL 定义
│   ├── common.thrift           # 通用类型定义
│   ├── user.thrift             # 用户服务 IDL
│   ├── item.thrift             # 物品服务 IDL
│   └── README.md               # IDL 文档
├── nginx/                      # Nginx 配置
│   ├── nginx.conf              # 主配置
│   └── conf.d/                 # 站点配置
├── scripts/                    # 脚本
│   ├── init-db.sql             # 数据库初始化
│   └── gen_thrift.sh           # Thrift 代码生成脚本
├── tests/                      # 测试
├── docker-compose.yml          # 生产环境配置
├── docker-compose.dev.yml      # 开发环境配置
├── Dockerfile                  # Docker 镜像
├── requirements.txt            # Python 依赖
└── README.md                   # 项目文档
```

## 🛠 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.11+ | 编程语言 |
| FastAPI | 0.109.0 | Web 框架 |
| SQLAlchemy | 2.0.25 | ORM |
| PostgreSQL | 15 | 数据库 |
| Redis | 7 | 缓存 |
| Nginx | Alpine | 反向代理 |
| Docker | 24+ | 容器化 |
| Thrift | IDL | 接口定义语言 |
| thriftpy2 | 0.5.0 | Thrift 动态加载 |

## 🚀 快速开始

### 环境要求

- Docker 24+
- Docker Compose 2.0+

### 开发环境

1. **克隆项目**

```bash
git clone <repository-url>
cd fastapi-demo
```

2. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，修改配置
```

3. **启动开发环境**

```bash
docker-compose -f docker-compose.dev.yml up -d
```

4. **访问服务**

- API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
- Adminer (数据库管理): http://localhost:8080
- Redis Commander: http://localhost:8081

### 生产环境

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📖 API 文档

启动服务后访问:
- Swagger UI: http://localhost/docs
- ReDoc: http://localhost/redoc

### 主要 API 端点

#### 认证

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/register` | 用户注册 |
| POST | `/api/v1/auth/login` | 用户登录 |
| POST | `/api/v1/auth/refresh` | 刷新令牌 |
| GET | `/api/v1/auth/me` | 获取当前用户 |
| POST | `/api/v1/auth/change-password` | 修改密码 |

#### 用户

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/users` | 获取用户列表 |
| GET | `/api/v1/users/{id}` | 获取用户详情 |
| PUT | `/api/v1/users/{id}` | 更新用户 |
| DELETE | `/api/v1/users/{id}` | 删除用户 |

#### 物品

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/items` | 获取物品列表 |
| POST | `/api/v1/items` | 创建物品 |
| GET | `/api/v1/items/{id}` | 获取物品详情 |
| PUT | `/api/v1/items/{id}` | 更新物品 |
| DELETE | `/api/v1/items/{id}` | 删除物品 |
| POST | `/api/v1/items/{id}/publish` | 上架物品 |
| POST | `/api/v1/items/{id}/unpublish` | 下架物品 |

## 🏗 架构设计

### 分层架构

```
┌─────────────────────────────────────────┐
│           API Layer (Routes)            │
├─────────────────────────────────────────┤
│         Service Layer (Business)        │
├─────────────────────────────────────────┤
│      Repository Layer (DAL/CRUD)        │
├─────────────────────────────────────────┤
│        Model Layer (ORM/Schema)         │
├─────────────────────────────────────────┤
│         Database (PostgreSQL)           │
└─────────────────────────────────────────┘
```

### Thrift IDL 架构

```
┌─────────────────────────────────────────┐
│          .thrift IDL 文件               │
│  (common.thrift, user.thrift, item.thrift)
├─────────────────────────────────────────┤
│         thriftpy2 动态加载              │
├─────────────────────────────────────────┤
│           类型转换器                    │
│    (Thrift ↔ Pydantic ↔ ORM)           │
├─────────────────────────────────────────┤
│         FastAPI 路由层                  │
└─────────────────────────────────────────┘
```

### 中间件链

```
Request → RequestID → Timing → Logging → CORS → Route Handler
                                                     ↓
Response ← RequestID ← Timing ← Logging ← CORS ← Response
```

## 🔒 安全特性

- **密码哈希**: 使用 bcrypt 算法
- **JWT 认证**: 访问令牌 + 刷新令牌
- **CORS**: 跨域请求保护
- **请求限流**: Nginx 层面限流
- **安全头**: XSS、CSRF 保护

## 🧪 测试

```bash
# 运行测试
pytest

# 带覆盖率
pytest --cov=app --cov-report=html
```

## 📝 开发指南

### 添加新的 API

1. 在 `idl/` 中定义 Thrift IDL（可选，用于跨语言）
2. 在 `app/schemas/` 中定义 Pydantic 请求/响应模型
3. 在 `app/models/` 中定义 ORM 模型（如需要）
4. 在 `app/repositories/` 中实现数据访问
5. 在 `app/services/` 中实现业务逻辑
6. 在 `app/api/v1/` 中定义路由
7. 在 `app/api/router.py` 中注册路由

### Thrift IDL 使用

```python
# 导入 Thrift 类型
from app.thrift_gen import (
    UserInfo,
    ItemInfo,
    ErrorCode,
    build_success_response,
)

# 使用转换器
from app.thrift_gen.converters import UserConverter, ItemConverter

# ORM -> Thrift
user_thrift = UserConverter.orm_to_thrift(user_orm)

# Thrift -> Dict
user_dict = UserConverter.thrift_to_dict(user_thrift)
```

### 代码规范

```bash
# 格式化代码
black app/

# 排序导入
isort app/

# 类型检查
mypy app/
```

## 📊 监控

### 健康检查

- 应用健康: `GET /api/health`
- 数据库健康: `GET /api/health/db`
- Nginx 健康: `GET /nginx-health`

### 日志

日志文件位于 `logs/` 目录，支持:
- 按文件大小轮转 (10MB)
- 保留 7 天
- 自动压缩

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

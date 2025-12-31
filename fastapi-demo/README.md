# FastAPI 详解 & 实战项目

一个完整的 FastAPI 项目示例，包含企业级架构设计和最佳实践。

## 📚 目录

- [项目特性](#项目特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [架构详解](#架构详解)
- [API 文档](#api-文档)
- [部署指南](#部署指南)

## 🚀 项目特性

- ✅ **Thrift 类型定义** - 使用 Thrift IDL 定义数据类型和服务接口
- ✅ **MySQL 数据库** - 完整的数据库 Schema 设计
- ✅ **SQLAlchemy ORM** - 异步 ORM 模型和关系映射
- ✅ **DAL 数据访问层** - 清晰的数据访问层封装
- ✅ **Router & Controller** - RESTful API 路由和控制器
- ✅ **Middleware 中间件** - 日志、限流、CORS、错误处理
- ✅ **Docker Compose** - 完整的容器化部署方案
- ✅ **Nginx 反向代理** - 负载均衡和安全配置

## 🛠 技术栈

| 组件 | 技术 |
|------|------|
| Web 框架 | FastAPI 0.115+ |
| ORM | SQLAlchemy 2.0 (异步) |
| 数据库 | MySQL 8.0 |
| 缓存 | Redis 7 |
| 认证 | JWT (python-jose) |
| 验证 | Pydantic 2.0 |
| 类型定义 | Apache Thrift |
| 容器化 | Docker & Docker Compose |
| 反向代理 | Nginx |
| 日志 | Loguru |

## 📁 项目结构

```
fastapi-demo/
├── app/                        # 应用主目录
│   ├── api/                    # API 路由
│   │   └── v1/                 # API v1 版本
│   │       ├── auth.py         # 认证路由
│   │       ├── users.py        # 用户路由
│   │       ├── articles.py     # 文章路由
│   │       ├── categories.py   # 分类路由
│   │       └── tags.py         # 标签路由
│   ├── core/                   # 核心配置
│   │   ├── config.py           # 应用配置
│   │   ├── database.py         # 数据库配置
│   │   └── security.py         # 安全配置
│   ├── dal/                    # 数据访问层
│   │   ├── base_dal.py         # DAL 基类
│   │   ├── user_dal.py         # 用户 DAL
│   │   ├── article_dal.py      # 文章 DAL
│   │   └── interaction_dal.py  # 互动 DAL
│   ├── middleware/             # 中间件
│   │   ├── cors.py             # CORS 中间件
│   │   ├── error_handler.py    # 错误处理
│   │   ├── logging_middleware.py # 日志中间件
│   │   └── rate_limiter.py     # 限流中间件
│   ├── models/                 # ORM 模型
│   │   ├── user.py             # 用户模型
│   │   ├── article.py          # 文章模型
│   │   └── interaction.py      # 互动模型
│   ├── schemas/                # Pydantic 模式
│   │   ├── user.py             # 用户模式
│   │   ├── article.py          # 文章模式
│   │   └── interaction.py      # 互动模式
│   ├── services/               # 业务逻辑层
│   │   ├── auth_service.py     # 认证服务
│   │   ├── user_service.py     # 用户服务
│   │   └── article_service.py  # 文章服务
│   ├── utils/                  # 工具函数
│   └── main.py                 # 应用入口
├── thrift/                     # Thrift IDL 定义
│   ├── user.thrift             # 用户类型定义
│   ├── article.thrift          # 文章类型定义
│   └── common.thrift           # 通用类型定义
├── sql/                        # SQL 脚本
│   ├── 001_create_database.sql # 建表脚本
│   └── 002_seed_data.sql       # 测试数据
├── nginx/                      # Nginx 配置
│   ├── nginx.conf              # 主配置
│   └── conf.d/                 # 站点配置
├── tests/                      # 测试文件
├── docker-compose.yml          # 开发环境
├── docker-compose.prod.yml     # 生产环境
├── Dockerfile                  # Docker 镜像
└── requirements.txt            # Python 依赖
```

## 🚀 快速开始

### 1. 克隆项目

```bash
cd fastapi-demo
```

### 2. 环境配置

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑配置（可选）
vim .env
```

### 3. 使用 Docker Compose 启动（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

### 4. 本地开发（不使用 Docker）

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问服务

- API 文档 (Swagger): http://localhost/docs
- API 文档 (ReDoc): http://localhost/redoc
- 健康检查: http://localhost/health

## 🏗 架构详解

### 1. Thrift 类型定义

使用 Apache Thrift IDL 定义数据类型和服务接口，提供跨语言的类型定义。

```thrift
// thrift/user.thrift
enum UserStatus {
    INACTIVE = 0,
    ACTIVE = 1,
    BANNED = 2,
}

struct UserResponse {
    1: required i64 id,
    2: required string username,
    3: required string email,
    4: required UserStatus status,
}

service UserService {
    UserResponse createUser(1: UserCreateRequest request),
    UserResponse getUser(1: i64 user_id),
}
```

### 2. SQLAlchemy ORM 模型

使用 SQLAlchemy 2.0 异步模式定义数据模型：

```python
# app/models/user.py
class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(SmallInteger, default=UserStatus.INACTIVE)
    
    # 关系定义
    articles = relationship("Article", back_populates="author")
```

### 3. DAL 数据访问层

封装所有数据库操作，提供统一的数据访问接口：

```python
# app/dal/user_dal.py
class UserDAL(BaseDAL[User]):
    async def create_user(self, username, email, password) -> User:
        user_data = {
            "username": username,
            "email": email,
            "password_hash": get_password_hash(password),
        }
        return await self.create(user_data)
    
    async def authenticate(self, email, password) -> Optional[User]:
        user = await self.get_by_email(email)
        if user and verify_password(password, user.password_hash):
            return user
        return None
```

### 4. Router & Controller

使用 FastAPI 的依赖注入实现路由和控制器：

```python
# app/api/v1/users.py
@router.get("/{user_id}", response_model=ResponseModel[UserResponse])
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_user(user_id)
    return ResponseModel.success(data=UserResponse.model_validate(user))
```

### 5. Middleware 中间件

实现多种中间件处理横切关注点：

```python
# 日志中间件
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(f"[{request_id}] {request.method} {request.url.path} - {response.status_code}")
        
        return response

# 限流中间件
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        client_ip = self._get_client_ip(request)
        
        if not self._is_allowed(client_ip):
            return JSONResponse(status_code=429, content={"message": "请求过于频繁"})
        
        return await call_next(request)
```

### 6. Docker Compose 部署

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mysql
      - redis
    
  mysql:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
      - ./sql:/docker-entrypoint-initdb.d
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - api
```

### 7. Nginx 配置

```nginx
# 负载均衡
upstream fastapi_backend {
    least_conn;
    server api:8000;
}

# 反向代理
location /api/ {
    limit_req zone=api_limit burst=20;
    proxy_pass http://fastapi_backend;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 📖 API 文档

### 认证 API

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/v1/auth/register` | 用户注册 |
| POST | `/api/v1/auth/login` | 用户登录 |
| GET | `/api/v1/auth/me` | 获取当前用户 |
| POST | `/api/v1/auth/refresh` | 刷新令牌 |

### 用户 API

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/users` | 获取用户列表 |
| GET | `/api/v1/users/{id}` | 获取用户详情 |
| PUT | `/api/v1/users/{id}` | 更新用户信息 |
| DELETE | `/api/v1/users/{id}` | 删除用户 |

### 文章 API

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/articles` | 获取文章列表 |
| POST | `/api/v1/articles` | 创建文章 |
| GET | `/api/v1/articles/{id}` | 获取文章详情 |
| PUT | `/api/v1/articles/{id}` | 更新文章 |
| DELETE | `/api/v1/articles/{id}` | 删除文章 |
| POST | `/api/v1/articles/{id}/publish` | 发布文章 |
| POST | `/api/v1/articles/{id}/like` | 点赞文章 |
| POST | `/api/v1/articles/{id}/favorite` | 收藏文章 |

## 🚢 部署指南

### 开发环境

```bash
docker-compose up -d
```

### 生产环境

```bash
# 设置环境变量
export DB_PASSWORD=your_secure_password
export SECRET_KEY=your_secret_key
export JWT_SECRET_KEY=your_jwt_secret

# 使用生产配置启动
docker-compose -f docker-compose.prod.yml up -d
```

### 环境变量

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `DEBUG` | 调试模式 | `false` |
| `DB_HOST` | 数据库主机 | `mysql` |
| `DB_PORT` | 数据库端口 | `3306` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | - |
| `DB_NAME` | 数据库名 | `fastapi_demo` |
| `REDIS_HOST` | Redis 主机 | `redis` |
| `SECRET_KEY` | 应用密钥 | - |
| `JWT_SECRET_KEY` | JWT 密钥 | - |

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_api.py

# 显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=app --cov-report=html
```

## 📝 开发规范

### 代码风格

- 使用 Python 3.11+
- 遵循 PEP 8 规范
- 使用类型提示
- 使用 async/await 异步编程

### Git 提交规范

```
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代码格式（不影响功能）
refactor: 代码重构
test: 测试相关
chore: 构建/工具相关
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

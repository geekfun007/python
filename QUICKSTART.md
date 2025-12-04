# 快速开始指南

## 5分钟快速上手

### 前置要求

- Python 3.7+
- MySQL 8.0+
- pip

### 步骤 1: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2: 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env`，修改数据库配置：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=fastapi_demo
```

### 步骤 3: 创建数据库

登录 MySQL 并创建数据库：

```sql
CREATE DATABASE fastapi_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 步骤 4: 初始化数据库

运行初始化脚本：

```bash
python init_db.py
```

这将：
- 创建所有表
- 插入示例数据
- 验证数据

### 步骤 5: 启动应用

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --reload
```

### 步骤 6: 访问 API

打开浏览器访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API**: http://localhost:8000/api/v1/

## 使用 Docker（推荐）

### 步骤 1: 启动服务

```bash
docker-compose up -d
```

这将启动：
- MySQL 数据库
- FastAPI 应用

### 步骤 2: 访问应用

等待几秒钟后，访问：
- http://localhost:8000/docs

### 停止服务

```bash
docker-compose down
```

## 测试 API

运行测试脚本：

```bash
python test_api.py
```

## 使用 Makefile（推荐）

项目提供了 Makefile 简化命令：

```bash
# 查看所有命令
make help

# 安装依赖
make install

# 初始化数据库
make init-db

# 运行应用
make run

# 测试 API
make test-api

# 代码格式化
make format

# 代码检查
make lint

# 清理缓存
make clean
```

## 示例请求

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

### 获取产品列表

```bash
curl "http://localhost:8000/api/v1/products/?skip=0&limit=10"
```

## 项目结构

```
.
├── app/                    # 应用程序包
│   ├── api/               # API 路由
│   ├── core/              # 核心功能
│   ├── dal/               # 数据访问层
│   ├── models/            # ORM 模型
│   ├── schemas/           # Pydantic 模型
│   └── middleware/        # 中间件
├── main.py                # 应用入口
├── config.py              # 配置文件
├── init_db.py            # 数据库初始化
├── test_api.py           # API 测试
├── requirements.txt       # 依赖列表
└── README.md             # 项目文档
```

## 常见问题

### 1. 数据库连接失败

检查：
- MySQL 服务是否运行
- 数据库是否存在
- 用户名和密码是否正确
- `.env` 配置是否正确

### 2. 端口被占用

更改端口：
```bash
uvicorn main:app --port 8001
```

### 3. 依赖安装失败

使用镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 下一步

- 阅读 [README.md](README.md) 了解详细功能
- 查看 [ARCHITECTURE.md](ARCHITECTURE.md) 了解架构设计
- 阅读 [FASTAPI_PRINCIPLES.md](FASTAPI_PRINCIPLES.md) 学习 FastAPI 原理
- 参考 [DATABASE_GUIDE.md](DATABASE_GUIDE.md) 深入了解数据库操作

## 获取帮助

如有问题，请查看文档或提交 Issue。

**祝你使用愉快！ 🚀**

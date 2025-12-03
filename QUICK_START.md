# Flask 原理与实战 - 快速开始

## 🚀 快速安装和运行

### 1. 克隆项目（如果使用 Git）

```bash
git clone <repository-url>
cd flask-principles-and-practice
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行示例

#### 基础示例

```bash
# Hello World
python examples/01_basic/hello_world.py

# 路由系统
python examples/01_basic/routing.py

# 模板系统
python examples/01_basic/templates.py

# 请求和响应
python examples/01_basic/request_response.py

# 静态文件
python examples/01_basic/static_files.py
```

访问 http://127.0.0.1:5000/

#### 进阶示例

```bash
# 表单处理
python examples/02_intermediate/forms.py

# 数据库集成
python examples/02_intermediate/database.py

# 用户认证
python examples/02_intermediate/authentication.py
```

#### 高级示例

```bash
# 蓝图系统
python examples/03_advanced/blueprints.py

# RESTful API
python examples/03_advanced/restful_api.py
```

#### 实战项目 - 博客系统

```bash
cd projects/blog
python app.py
```

**测试账号：**
- 管理员: `admin` / `Admin123!`
- 普通用户: `demo` / `Demo123!`

---

## 📚 学习路径

### 初学者（1-2周）

1. 阅读 `README.md` 中的 Flask 原理部分
2. 运行并理解 `examples/01_basic/` 中的所有示例
3. 阅读 `docs/principles.md` 深入理解原理

**目标：** 理解 Flask 的基本概念和工作原理

### 中级（2-3周）

1. 学习 `examples/02_intermediate/` 中的示例
2. 阅读 `docs/best_practices.md`
3. 尝试修改示例代码，添加新功能

**目标：** 掌握表单、数据库、认证等核心功能

### 高级（3-4周）

1. 研究 `examples/03_advanced/` 中的高级示例
2. 分析 `projects/blog/` 博客系统的实现
3. 阅读 `docs/deployment.md` 学习部署

**目标：** 能够构建完整的 Flask 应用并部署

### 实战（持续）

1. 完成博客系统的扩展功能
2. 构建自己的 Flask 项目
3. 参与开源项目

**目标：** 成为 Flask 开发专家

---

## 🛠️ 常用命令

### 开发

```bash
# 运行开发服务器
flask run

# 启用调试模式
flask run --debug

# 指定端口
flask run --port 8000

# 监听所有网络接口
flask run --host 0.0.0.0
```

### 数据库

```bash
# 初始化数据库迁移
flask db init

# 创建迁移
flask db migrate -m "描述"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

### 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_basics.py

# 显示覆盖率
pytest --cov=app tests/

# 生成 HTML 覆盖率报告
pytest --cov=app --cov-report=html tests/
```

---

## 📖 文档目录

- **README.md** - 项目总览和 Flask 原理
- **QUICK_START.md** - 本文件，快速开始指南
- **docs/principles.md** - Flask 原理详解
- **docs/best_practices.md** - 最佳实践
- **docs/deployment.md** - 部署指南

---

## 🎯 示例说明

### 基础示例（examples/01_basic/）

| 文件 | 内容 | 难度 |
|------|------|------|
| hello_world.py | 最基础的 Flask 应用 | ⭐ |
| routing.py | 路由系统和 URL 构建 | ⭐⭐ |
| templates.py | Jinja2 模板引擎 | ⭐⭐ |
| request_response.py | 请求和响应处理 | ⭐⭐ |
| static_files.py | 静态文件服务 | ⭐⭐ |

### 进阶示例（examples/02_intermediate/）

| 文件 | 内容 | 难度 |
|------|------|------|
| forms.py | 表单处理和验证 | ⭐⭐⭐ |
| database.py | SQLAlchemy 数据库集成 | ⭐⭐⭐ |
| authentication.py | 用户认证和会话管理 | ⭐⭐⭐ |

### 高级示例（examples/03_advanced/）

| 文件 | 内容 | 难度 |
|------|------|------|
| blueprints.py | 蓝图和应用模块化 | ⭐⭐⭐⭐ |
| restful_api.py | RESTful API 设计 | ⭐⭐⭐⭐ |

### 实战项目（projects/）

| 项目 | 内容 | 难度 |
|------|------|------|
| blog/ | 完整的博客系统 | ⭐⭐⭐⭐⭐ |

---

## 🐛 故障排除

### 问题：端口已被占用

```bash
# Linux/Mac: 查找占用端口的进程
lsof -i :5000

# Windows: 查找占用端口的进程
netstat -ano | findstr :5000

# 使用其他端口
flask run --port 8000
```

### 问题：模块未找到

```bash
# 确保虚拟环境已激活
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 重新安装依赖
pip install -r requirements.txt
```

### 问题：数据库错误

```bash
# 删除数据库文件重新创建
rm *.db

# 重新初始化
flask db init
flask db migrate
flask db upgrade
```

---

## 💡 提示

1. **始终使用虚拟环境** - 避免依赖冲突
2. **阅读代码注释** - 每个示例都有详细的中英文注释
3. **动手实践** - 不要只看代码，要亲自运行和修改
4. **循序渐进** - 按照学习路径一步步来
5. **善用文档** - 遇到问题先查看文档

---

## 📞 获取帮助

- 查看 [Flask 官方文档](https://flask.palletsprojects.com/)
- 查看 [Flask 中文文档](https://dormousehole.readthedocs.io/)
- 阅读项目中的详细文档
- GitHub Issues（如果项目在 GitHub 上）

---

## 🎉 开始你的 Flask 之旅！

现在你已经准备好开始学习 Flask 了。祝你学习愉快！

```bash
# 运行第一个示例
python examples/01_basic/hello_world.py
```

访问 http://127.0.0.1:5000/ 查看结果！

# Flask 最佳实践 (Best Practices)

这份文档总结了 Flask 开发中的最佳实践和常见模式。

## 目录

1. [项目结构](#项目结构)
2. [配置管理](#配置管理)
3. [数据库](#数据库)
4. [错误处理](#错误处理)
5. [安全性](#安全性)
6. [性能优化](#性能优化)
7. [测试](#测试)
8. [日志](#日志)

---

## 项目结构

### 小型项目

```
myapp/
├── app.py              # 主应用文件
├── requirements.txt    # 依赖列表
├── .env               # 环境变量（不提交到git）
├── .gitignore
├── README.md
├── templates/         # 模板目录
│   ├── base.html
│   └── index.html
└── static/           # 静态文件
    ├── css/
    ├── js/
    └── images/
```

### 中大型项目（推荐）

```
myproject/
├── app/                    # 应用包
│   ├── __init__.py        # 应用工厂
│   ├── models.py          # 数据库模型
│   ├── forms.py           # 表单定义
│   ├── email.py           # 邮件功能
│   ├── main/              # 主蓝图
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── errors.py
│   ├── api/               # API 蓝图
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── posts.py
│   ├── auth/              # 认证蓝图
│   │   ├── __init__.py
│   │   └── views.py
│   ├── templates/
│   └── static/
├── migrations/            # 数据库迁移
├── tests/                 # 测试
│   ├── __init__.py
│   ├── test_basics.py
│   └── test_api.py
├── venv/                  # 虚拟环境
├── requirements.txt
├── config.py              # 配置文件
├── manage.py              # 管理脚本
└── .env
```

---

## 配置管理

### ✅ 使用配置类

```python
# config.py
import os

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev.db'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """生产环境配置"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        # 发送错误邮件给管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None):
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

### ✅ 使用环境变量

```python
# .env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Python 代码
from dotenv import load_dotenv
load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

### ❌ 避免硬编码敏感信息

```python
# ❌ 错误示例
app.config['SECRET_KEY'] = '123456'
app.config['DATABASE_URL'] = 'postgresql://user:password@localhost/db'

# ✅ 正确示例
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

---

## 数据库

### ✅ 使用应用工厂模式

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
    return app
```

### ✅ 使用数据库迁移

```bash
# 初始化迁移
flask db init

# 创建迁移
flask db migrate -m "initial migration"

# 应用迁移
flask db upgrade
```

### ✅ 使用模型方法

```python
class User(db.Model):
    # ... 字段定义 ...
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    
    @staticmethod
    def create_user(username, email, password):
        """创建用户的工厂方法"""
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
```

### ✅ 使用索引

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)  # 添加索引
    slug = db.Column(db.String(200), unique=True, index=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
```

### ✅ 使用查询优化

```python
# ❌ N+1 查询问题
posts = Post.query.all()
for post in posts:
    print(post.author.username)  # 每次都查询数据库

# ✅ 使用 join 或 eager loading
posts = Post.query.options(db.joinedload('author')).all()
for post in posts:
    print(post.author.username)  # 只查询一次
```

---

## 错误处理

### ✅ 自定义错误页面

```python
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # 回滚数据库事务
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403
```

### ✅ 使用异常处理

```python
from werkzeug.exceptions import NotFound, BadRequest

@app.route('/post/<int:id>')
def show_post(id):
    post = Post.query.get(id)
    if not post:
        raise NotFound('Post not found')
    return render_template('post.html', post=post)

# 或使用 get_or_404
@app.route('/post/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)
```

### ✅ API 错误响应

```python
class APIError(Exception):
    def __init__(self, message, status_code=400, payload=None):
        self.message = message
        self.status_code = status_code
        self.payload = payload

@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        'error': error.message,
        'status_code': error.status_code
    }
    if error.payload:
        response['details'] = error.payload
    return jsonify(response), error.status_code

# 使用
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        raise APIError('User not found', status_code=404)
    return jsonify(user.to_dict())
```

---

## 安全性

### ✅ 使用 CSRF 保护

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
csrf.init_app(app)
```

### ✅ 密码安全

```python
from werkzeug.security import generate_password_hash, check_password_hash

# 存储密码
password_hash = generate_password_hash('user_password')

# 验证密码
is_valid = check_password_hash(password_hash, 'user_input')
```

### ✅ SQL 注入防护

```python
# ❌ 不安全
username = request.args.get('username')
query = f"SELECT * FROM users WHERE username = '{username}'"

# ✅ 使用 ORM
user = User.query.filter_by(username=username).first()

# ✅ 或使用参数化查询
query = text("SELECT * FROM users WHERE username = :username")
result = db.engine.execute(query, username=username)
```

### ✅ XSS 防护

```python
# Jinja2 自动转义 HTML
{{ user_input }}  # 自动转义

# 如果需要渲染 HTML（确保内容安全）
from flask import Markup
safe_html = Markup('<b>Bold</b>')

# 或在模板中
{{ content | safe }}
```

### ✅ HTTPS

```python
# 强制 HTTPS
from flask_talisman import Talisman

Talisman(app, force_https=True)
```

### ✅ 限流

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # 登录逻辑
    pass
```

---

## 性能优化

### ✅ 使用缓存

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@app.route('/expensive')
@cache.cached(timeout=300)  # 缓存 5 分钟
def expensive_operation():
    # 耗时操作
    result = heavy_computation()
    return result

# 缓存参数化路由
@app.route('/user/<int:user_id>')
@cache.cached(timeout=300, key_prefix='user_view_%s')
def user_view(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)
```

### ✅ 数据库连接池

```python
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
```

### ✅ 异步任务

```python
from celery import Celery

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

@celery.task
def send_email(to, subject, body):
    # 发送邮件
    pass

# 在视图中调用
@app.route('/register', methods=['POST'])
def register():
    # ... 注册逻辑 ...
    send_email.delay(user.email, 'Welcome', 'Welcome to our site!')
    return redirect(url_for('index'))
```

### ✅ 压缩响应

```python
from flask_compress import Compress

Compress(app)
```

### ✅ 使用 CDN

```python
# 配置静态文件 CDN
app.config['CDN_DOMAIN'] = 'https://cdn.example.com'

# 在模板中使用
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

---

## 测试

### ✅ 单元测试

```python
import unittest
from app import create_app, db
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password_setter(self):
        u = User(username='test')
        u.set_password('cat')
        self.assertTrue(u.password_hash is not None)
    
    def test_password_verification(self):
        u = User(username='test')
        u.set_password('cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))
```

### ✅ API 测试

```python
class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_get_users(self):
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('users', data)
    
    def test_create_user(self):
        response = self.client.post('/api/users', 
            json={'username': 'test', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 201)
```

### ✅ 使用测试覆盖率

```bash
pip install pytest pytest-cov

# 运行测试并生成覆盖率报告
pytest --cov=app tests/
```

---

## 日志

### ✅ 配置日志

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')
```

### ✅ 使用日志

```python
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        
        app.logger.info(f'New user created: {user.username}')
        return jsonify(user.to_dict()), 201
        
    except Exception as e:
        app.logger.error(f'Error creating user: {str(e)}')
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
```

---

## 部署建议

### ✅ 使用环境变量

```bash
export FLASK_APP=app
export FLASK_ENV=production
export SECRET_KEY=production-secret-key
```

### ✅ 使用生产级服务器

```bash
# 安装 gunicorn
pip install gunicorn

# 运行
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### ✅ 使用反向代理

```nginx
# Nginx 配置
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/app/static;
    }
}
```

---

## 总结

遵循这些最佳实践可以帮助你：

1. ✅ 编写更安全的代码
2. ✅ 提高应用性能
3. ✅ 提升代码可维护性
4. ✅ 减少 bug 和错误
5. ✅ 更容易扩展应用

记住：**始终优先考虑安全性和可维护性！**

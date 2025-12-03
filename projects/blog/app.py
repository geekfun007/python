"""
Flask 实战项目: 博客系统
Flask Practical Project: Blog System

一个功能完整的博客系统，包含用户认证、文章管理、评论、标签等功能。
A full-featured blog system with user authentication, post management, comments, tags, etc.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os
import secrets

# ============================================
# 应用配置 (App Configuration)
# ============================================

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "blog.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ============================================
# 数据库模型 (Database Models)
# ============================================

# 文章-标签关联表
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(200), default='/static/default-avatar.png')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """文章模型"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    slug = db.Column(db.String(200), unique=True, index=True)
    views = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # 关系
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Post {self.title}>'


class Category(db.Model):
    """分类模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    # 关系
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    """标签模型"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Tag {self.name}>'


class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id}>'


# ============================================
# 初始化数据库和示例数据
# ============================================

def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        
        # 检查是否已有数据
        if User.query.count() == 0:
            # 创建管理员
            admin = User(
                username='admin',
                email='admin@blog.com',
                bio='博客管理员',
                is_admin=True
            )
            admin.set_password('Admin123!')
            db.session.add(admin)
            
            # 创建测试用户
            user = User(
                username='demo',
                email='demo@blog.com',
                bio='演示用户账号'
            )
            user.set_password('Demo123!')
            db.session.add(user)
            
            # 创建分类
            categories = [
                Category(name='技术', slug='tech', description='技术相关文章'),
                Category(name='生活', slug='life', description='生活感悟'),
                Category(name='随笔', slug='essay', description='随笔杂谈'),
            ]
            for cat in categories:
                db.session.add(cat)
            
            # 创建标签
            tags = [
                Tag(name='Python', slug='python'),
                Tag(name='Flask', slug='flask'),
                Tag(name='Web开发', slug='web-dev'),
                Tag(name='教程', slug='tutorial'),
            ]
            for tag in tags:
                db.session.add(tag)
            
            db.session.commit()
            
            # 创建示例文章
            posts = [
                Post(
                    title='欢迎来到 Flask 博客系统',
                    content='这是一个使用 Flask 构建的完整博客系统。它包含了用户认证、文章管理、评论、标签等功能。\n\n## 功能特性\n\n- 用户注册和登录\n- 文章发布和编辑\n- Markdown 支持\n- 评论系统\n- 标签和分类\n- 搜索功能\n\n开始探索吧！',
                    summary='Flask 博客系统简介',
                    slug='welcome-to-flask-blog',
                    user_id=1,
                    category_id=1,
                    published=True
                ),
                Post(
                    title='Flask 开发最佳实践',
                    content='在开发 Flask 应用时，有一些最佳实践可以让你的代码更加优雅和易维护。\n\n1. 使用蓝图组织代码\n2. 使用配置对象管理配置\n3. 使用装饰器进行权限控制\n4. 合理使用缓存\n5. 编写单元测试',
                    summary='Flask 开发技巧和最佳实践',
                    slug='flask-best-practices',
                    user_id=1,
                    category_id=1,
                    published=True
                ),
            ]
            
            for post in posts:
                db.session.add(post)
            
            db.session.commit()
            
            # 为文章添加标签
            post1 = Post.query.get(1)
            post1.tags.extend([Tag.query.get(1), Tag.query.get(2)])
            
            post2 = Post.query.get(2)
            post2.tags.extend([Tag.query.get(2), Tag.query.get(4)])
            
            # 添加示例评论
            comment = Comment(
                content='很棒的文章！期待更多内容。',
                user_id=2,
                post_id=1
            )
            db.session.add(comment)
            
            db.session.commit()
            
            print("✅ 数据库初始化完成！")
            print("📝 测试账号:")
            print("   管理员: admin / Admin123!")
            print("   用户: demo / Demo123!")


# ============================================
# 装饰器 (Decorators)
# ============================================

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('需要管理员权限', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """获取当前登录用户"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


# ============================================
# 模板基础布局
# ============================================

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask 博客系统{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f7fa;
        }
        
        /* 导航栏 */
        nav {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        nav .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        nav .logo {
            font-size: 1.5rem;
            font-weight: bold;
            text-decoration: none;
            color: white;
        }
        
        nav .nav-links {
            display: flex;
            gap: 1.5rem;
            align-items: center;
        }
        
        nav a {
            color: white;
            text-decoration: none;
            transition: opacity 0.3s;
        }
        
        nav a:hover {
            opacity: 0.8;
        }
        
        /* 主容器 */
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 20px;
        }
        
        /* Flash 消息 */
        .flash-messages {
            margin: 1rem 0;
        }
        
        .flash {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            border-left: 4px solid;
        }
        
        .flash.success {
            background: #d4edda;
            border-color: #28a745;
            color: #155724;
        }
        
        .flash.error {
            background: #f8d7da;
            border-color: #dc3545;
            color: #721c24;
        }
        
        .flash.warning {
            background: #fff3cd;
            border-color: #ffc107;
            color: #856404;
        }
        
        .flash.info {
            background: #d1ecf1;
            border-color: #17a2b8;
            color: #0c5460;
        }
        
        /* 按钮 */
        .btn {
            display: inline-block;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1rem;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
        }
        
        .btn-danger {
            background: #e74c3c;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c0392b;
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        /* 卡片 */
        .card {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        /* 页脚 */
        footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: 4rem;
        }
        
        {% block extra_css %}{% endblock %}
    </style>
</head>
<body>
    <nav>
        <div class="container">
            <a href="/" class="logo">📝 Flask 博客</a>
            <div class="nav-links">
                <a href="/">首页</a>
                <a href="/posts">文章</a>
                {% if current_user %}
                    <a href="/posts/new">写文章</a>
                    <a href="/profile">{{ current_user.username }}</a>
                    {% if current_user.is_admin %}
                    <a href="/admin">管理</a>
                    {% endif %}
                    <a href="/logout">退出</a>
                {% else %}
                    <a href="/login">登录</a>
                    <a href="/register">注册</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
    
    <footer>
        <p>&copy; 2024 Flask 博客系统 | 使用 Flask 构建</p>
    </footer>
</body>
</html>
'''


# ============================================
# 路由 (Routes)
# ============================================

@app.route('/')
def index():
    """首页"""
    # 获取最新文章
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).limit(10).all()
    
    # 获取统计信息
    stats = {
        'posts': Post.query.filter_by(published=True).count(),
        'users': User.query.count(),
        'comments': Comment.query.count(),
        'categories': Category.query.count(),
    }
    
    template = BASE_TEMPLATE + '''
    {% block content %}
    <style>
        .welcome {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .welcome h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stat-card h3 {
            font-size: 2rem;
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        
        .posts-grid {
            display: grid;
            gap: 1.5rem;
        }
        
        .post-card {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .post-card:hover {
            transform: translateY(-5px);
        }
        
        .post-card h2 {
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .post-card h2 a {
            color: inherit;
            text-decoration: none;
        }
        
        .post-meta {
            color: #6c757d;
            font-size: 0.9rem;
            margin: 1rem 0;
        }
        
        .post-meta span {
            margin-right: 1rem;
        }
        
        .tags {
            margin-top: 1rem;
        }
        
        .tag {
            display: inline-block;
            background: #e8f4f8;
            color: #2980b9;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.85rem;
            margin-right: 0.5rem;
        }
    </style>
    
    <div class="welcome">
        <h1>🎉 欢迎来到 Flask 博客系统</h1>
        <p>一个功能完整的博客平台，展示 Flask 的强大功能</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>{{ stats.posts }}</h3>
            <p>篇文章</p>
        </div>
        <div class="stat-card">
            <h3>{{ stats.users }}</h3>
            <p>位用户</p>
        </div>
        <div class="stat-card">
            <h3>{{ stats.comments }}</h3>
            <p>条评论</p>
        </div>
        <div class="stat-card">
            <h3>{{ stats.categories }}</h3>
            <p>个分类</p>
        </div>
    </div>
    
    <h2>📄 最新文章</h2>
    <div class="posts-grid">
        {% for post in posts %}
        <div class="post-card">
            <h2><a href="/posts/{{ post.id }}">{{ post.title }}</a></h2>
            <div class="post-meta">
                <span>👤 {{ post.author.username }}</span>
                <span>📅 {{ post.created_at.strftime('%Y-%m-%d') }}</span>
                <span>👁️ {{ post.views }} 次浏览</span>
                <span>💬 {{ post.comments.count() }} 条评论</span>
            </div>
            {% if post.summary %}
            <p>{{ post.summary }}</p>
            {% else %}
            <p>{{ post.content[:200] }}...</p>
            {% endif %}
            {% if post.tags %}
            <div class="tags">
                {% for tag in post.tags %}
                <span class="tag">{{ tag.name }}</span>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% endblock %}
    '''
    
    return render_template_string(template, 
                                 current_user=get_current_user(),
                                 posts=posts,
                                 stats=stats)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            if remember:
                session.permanent = True
            flash(f'欢迎回来，{username}！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'error')
    
    template = BASE_TEMPLATE + '''
    {% block content %}
    <style>
        .login-container {
            max-width: 500px;
            margin: 3rem auto;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
    </style>
    
    <div class="login-container">
        <div class="card">
            <h1>🔑 用户登录</h1>
            <form method="POST">
                <div class="form-group">
                    <label>用户名</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>密码</label>
                    <input type="password" name="password" required>
                </div>
                <div class="form-group checkbox-group">
                    <input type="checkbox" name="remember" id="remember">
                    <label for="remember" style="margin: 0;">记住我</label>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">登录</button>
            </form>
            <p style="margin-top: 1rem; text-align: center;">
                还没有账号？<a href="/register">立即注册</a>
            </p>
            <div style="background: #f8f9fa; padding: 1rem; margin-top: 1rem; border-radius: 5px;">
                <strong>测试账号：</strong><br>
                admin / Admin123! (管理员)<br>
                demo / Demo123! (普通用户)
            </div>
        </div>
    </div>
    {% endblock %}
    '''
    
    return render_template_string(template, current_user=get_current_user())


@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        errors = []
        
        if User.query.filter_by(username=username).first():
            errors.append('用户名已存在')
        if User.query.filter_by(email=email).first():
            errors.append('邮箱已被注册')
        if password != confirm_password:
            errors.append('两次输入的密码不一致')
        if len(password) < 6:
            errors.append('密码至少需要6个字符')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('注册成功！请登录', 'success')
            return redirect(url_for('login'))
    
    template = BASE_TEMPLATE + '''
    {% block content %}
    <style>
        .register-container {
            max-width: 500px;
            margin: 3rem auto;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        input[type="text"],
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
        }
    </style>
    
    <div class="register-container">
        <div class="card">
            <h1>📝 用户注册</h1>
            <form method="POST">
                <div class="form-group">
                    <label>用户名</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>邮箱</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>密码</label>
                    <input type="password" name="password" required>
                </div>
                <div class="form-group">
                    <label>确认密码</label>
                    <input type="password" name="confirm_password" required>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">注册</button>
            </form>
            <p style="margin-top: 1rem; text-align: center;">
                已有账号？<a href="/login">立即登录</a>
            </p>
        </div>
    </div>
    {% endblock %}
    '''
    
    return render_template_string(template, current_user=get_current_user())


@app.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('index'))


# 初始化数据库
init_db()


if __name__ == '__main__':
    print("🚀 Starting Flask Blog System...")
    print("📍 访问 http://127.0.0.1:5000/")
    print("\n📝 测试账号:")
    print("  管理员: admin / Admin123!")
    print("  用户: demo / Demo123!")
    app.run(debug=True, host='0.0.0.0', port=5000)

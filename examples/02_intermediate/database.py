"""
Flask 进阶示例 2: 数据库集成
Flask Intermediate Example 2: Database Integration

演示使用 SQLAlchemy 进行数据库操作。
Demonstrates database operations using SQLAlchemy.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)


# ============================================
# 数据库模型 (Database Models)
# ============================================

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系：一个用户可以有多篇文章
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'posts_count': self.posts.count()
        }


class Post(db.Model):
    """文章模型"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键：关联到用户
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 关系：一篇文章可以有多个标签
    tags = db.relationship('Tag', secondary='post_tags', backref='posts', lazy='dynamic')
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.username,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'tags': [tag.name for tag in self.tags]
        }


class Tag(db.Model):
    """标签模型"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Tag {self.name}>'


# 多对多关系表：文章-标签
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


# ============================================
# 初始化数据库
# ============================================

with app.app_context():
    # 创建所有表
    db.create_all()
    
    # 插入示例数据（仅在首次运行时）
    if User.query.count() == 0:
        # 创建示例用户
        users = [
            User(username='admin', email='admin@example.com', bio='系统管理员'),
            User(username='alice', email='alice@example.com', bio='Python 开发者'),
            User(username='bob', email='bob@example.com', bio='全栈工程师'),
        ]
        for user in users:
            db.session.add(user)
        
        # 创建示例标签
        tags = [
            Tag(name='Python'),
            Tag(name='Flask'),
            Tag(name='Database'),
            Tag(name='Web Development'),
            Tag(name='Tutorial'),
        ]
        for tag in tags:
            db.session.add(tag)
        
        db.session.commit()
        
        # 创建示例文章
        posts = [
            Post(
                title='Flask 数据库入门',
                content='这篇文章介绍如何在 Flask 中使用 SQLAlchemy...',
                user_id=1
            ),
            Post(
                title='Python Web 开发最佳实践',
                content='本文总结了 Python Web 开发的最佳实践...',
                user_id=2
            ),
            Post(
                title='数据库设计原则',
                content='良好的数据库设计是应用成功的关键...',
                user_id=3
            ),
        ]
        for post in posts:
            db.session.add(post)
        
        db.session.commit()
        
        # 为文章添加标签
        post1 = Post.query.get(1)
        post1.tags.append(Tag.query.filter_by(name='Flask').first())
        post1.tags.append(Tag.query.filter_by(name='Database').first())
        post1.tags.append(Tag.query.filter_by(name='Tutorial').first())
        
        post2 = Post.query.get(2)
        post2.tags.append(Tag.query.filter_by(name='Python').first())
        post2.tags.append(Tag.query.filter_by(name='Web Development').first())
        
        post3 = Post.query.get(3)
        post3.tags.append(Tag.query.filter_by(name='Database').first())
        
        db.session.commit()
        
        print("✅ 示例数据已创建")


# ============================================
# 路由
# ============================================

@app.route('/')
def index():
    """主页"""
    users_count = User.query.count()
    posts_count = Post.query.count()
    tags_count = Tag.query.count()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask 数据库示例</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { color: #667eea; }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .stat-card h3 {
                margin: 0;
                font-size: 36px;
            }
            .stat-card p {
                margin: 10px 0 0 0;
            }
            .nav-links {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .nav-link {
                display: block;
                padding: 15px;
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                text-decoration: none;
                color: #333;
                border-radius: 5px;
                transition: all 0.3s;
            }
            .nav-link:hover {
                background: #e9ecef;
                transform: translateX(5px);
            }
            .feature {
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 5px;
            }
            pre {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗄️ Flask 数据库集成示例</h1>
            <h2>SQLAlchemy ORM</h2>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>{{ users_count }}</h3>
                    <p>👤 用户</p>
                </div>
                <div class="stat-card">
                    <h3>{{ posts_count }}</h3>
                    <p>📝 文章</p>
                </div>
                <div class="stat-card">
                    <h3>{{ tags_count }}</h3>
                    <p>🏷️ 标签</p>
                </div>
            </div>
            
            <h3>📋 功能导航</h3>
            <div class="nav-links">
                <a href="/users" class="nav-link">👥 用户列表</a>
                <a href="/posts" class="nav-link">📄 文章列表</a>
                <a href="/tags" class="nav-link">🏷️ 标签列表</a>
                <a href="/users/new" class="nav-link">➕ 创建用户</a>
                <a href="/posts/new" class="nav-link">✏️ 创建文章</a>
                <a href="/api/users" class="nav-link">🔌 API: 用户</a>
                <a href="/api/posts" class="nav-link">🔌 API: 文章</a>
            </div>
            
            <div class="feature">
                <h3>💡 数据库特性</h3>
                <ul>
                    <li><strong>ORM (对象关系映射):</strong> 使用 SQLAlchemy</li>
                    <li><strong>关系:</strong> 一对多 (用户-文章), 多对多 (文章-标签)</li>
                    <li><strong>查询:</strong> 过滤、排序、分页</li>
                    <li><strong>级联删除:</strong> 删除用户时自动删除其文章</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>📚 模型定义示例</h3>
                <pre><code>class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    posts = db.relationship('Post', backref='author')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))</code></pre>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, 
                                 users_count=users_count,
                                 posts_count=posts_count,
                                 tags_count=tags_count)


# ============================================
# 用户相关路由
# ============================================

@app.route('/users')
def users_list():
    """用户列表"""
    # 查询所有用户，按创建时间排序
    users = User.query.order_by(User.created_at.desc()).all()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户列表</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .user-card {
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
                border-left: 4px solid #3498db;
            }
            .user-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .user-actions {
                display: flex;
                gap: 10px;
            }
            .btn {
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                color: white;
                cursor: pointer;
            }
            .btn-view { background: #3498db; }
            .btn-edit { background: #f39c12; }
            .btn-delete { background: #e74c3c; }
            .btn:hover { opacity: 0.9; }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👥 用户列表</h1>
            <p>共有 {{ users|length }} 位用户</p>
            
            {% for user in users %}
            <div class="user-card">
                <div class="user-header">
                    <div>
                        <h3>{{ user.username }}</h3>
                        <p><strong>邮箱:</strong> {{ user.email }}</p>
                        {% if user.bio %}
                        <p><strong>简介:</strong> {{ user.bio }}</p>
                        {% endif %}
                        <p><strong>文章数:</strong> {{ user.posts.count() }}</p>
                        <p><small>注册时间: {{ user.created_at.strftime('%Y-%m-%d %H:%M') }}</small></p>
                    </div>
                    <div class="user-actions">
                        <a href="/users/{{ user.id }}" class="btn btn-view">查看</a>
                        <a href="/users/{{ user.id }}/edit" class="btn btn-edit">编辑</a>
                        <a href="/users/{{ user.id }}/delete" class="btn btn-delete" 
                           onclick="return confirm('确定要删除用户 {{ user.username }} 吗？')">删除</a>
                    </div>
                </div>
            </div>
            {% endfor %}
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, users=users)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """用户详情"""
    # 查询用户或返回 404
    user = User.query.get_or_404(user_id)
    # 获取用户的文章
    posts = user.posts.order_by(Post.created_at.desc()).all()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ user.username }} - 用户详情</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .user-info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
            .post-card {
                background: #fff;
                padding: 15px;
                margin: 15px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .post-card h3 {
                margin-top: 0;
                color: #3498db;
            }
            .tags {
                margin-top: 10px;
            }
            .tag {
                display: inline-block;
                background: #e8f4f8;
                color: #2980b9;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                margin-right: 5px;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👤 {{ user.username }}</h1>
            
            <div class="user-info">
                <p><strong>邮箱:</strong> {{ user.email }}</p>
                {% if user.bio %}
                <p><strong>简介:</strong> {{ user.bio }}</p>
                {% endif %}
                <p><strong>注册时间:</strong> {{ user.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</p>
                <p><strong>文章数:</strong> {{ posts|length }}</p>
            </div>
            
            <h2>📝 文章列表</h2>
            {% if posts %}
                {% for post in posts %}
                <div class="post-card">
                    <h3><a href="/posts/{{ post.id }}">{{ post.title }}</a></h3>
                    <p>{{ post.content[:200] }}{% if post.content|length > 200 %}...{% endif %}</p>
                    <p><small>发布时间: {{ post.created_at.strftime('%Y-%m-%d %H:%M') }}</small></p>
                    {% if post.tags %}
                    <div class="tags">
                        {% for tag in post.tags %}
                        <span class="tag">{{ tag.name }}</span>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            {% else %}
                <p>该用户还没有发布文章。</p>
            {% endif %}
            
            <a href="/users" class="back-link">← 返回用户列表</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, user=user, posts=posts)


@app.route('/users/new', methods=['GET', 'POST'])
def user_create():
    """创建用户"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        bio = request.form.get('bio', '')
        
        # 验证
        errors = []
        if not username:
            errors.append('用户名不能为空')
        elif User.query.filter_by(username=username).first():
            errors.append('用户名已存在')
        
        if not email:
            errors.append('邮箱不能为空')
        elif User.query.filter_by(email=email).first():
            errors.append('邮箱已被注册')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            # 创建新用户
            new_user = User(username=username, email=email, bio=bio)
            db.session.add(new_user)
            db.session.commit()
            
            flash(f'✅ 用户 {username} 创建成功！', 'success')
            return redirect(url_for('users_list'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>创建用户</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .form-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #555;
            }
            input[type="text"],
            input[type="email"],
            textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            textarea {
                resize: vertical;
                min-height: 100px;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background: #2980b9;
            }
            .flash {
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
            }
            .flash.error {
                background: #f8d7da;
                color: #721c24;
            }
            .flash.success {
                background: #d4edda;
                color: #155724;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>➕ 创建新用户</h1>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST">
                <div class="form-group">
                    <label for="username">用户名 *</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="email">邮箱 *</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label for="bio">个人简介</label>
                    <textarea id="bio" name="bio" placeholder="介绍一下自己..."></textarea>
                </div>
                
                <button type="submit">创建用户</button>
            </form>
            
            <a href="/users" class="back-link">← 返回用户列表</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


@app.route('/users/<int:user_id>/delete')
def user_delete(user_id):
    """删除用户"""
    user = User.query.get_or_404(user_id)
    username = user.username
    
    # 删除用户（会级联删除文章）
    db.session.delete(user)
    db.session.commit()
    
    flash(f'✅ 用户 {username} 已删除', 'success')
    return redirect(url_for('users_list'))


# ============================================
# 文章相关路由
# ============================================

@app.route('/posts')
def posts_list():
    """文章列表"""
    # 支持分页
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # 查询并分页
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>文章列表</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .post-card {
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
            }
            .post-card h3 {
                margin-top: 0;
                color: #3498db;
            }
            .post-card h3 a {
                color: #3498db;
                text-decoration: none;
            }
            .post-card h3 a:hover {
                text-decoration: underline;
            }
            .post-meta {
                color: #666;
                font-size: 14px;
                margin: 10px 0;
            }
            .tags {
                margin-top: 10px;
            }
            .tag {
                display: inline-block;
                background: #e8f4f8;
                color: #2980b9;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                margin-right: 5px;
            }
            .pagination {
                margin: 30px 0;
                text-align: center;
            }
            .pagination a {
                display: inline-block;
                padding: 8px 12px;
                margin: 0 5px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .pagination a:hover {
                background: #2980b9;
            }
            .pagination .current {
                background: #2c3e50;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 文章列表</h1>
            <p>共有 {{ pagination.total }} 篇文章 (第 {{ pagination.page }} / {{ pagination.pages }} 页)</p>
            
            {% for post in posts %}
            <div class="post-card">
                <h3><a href="/posts/{{ post.id }}">{{ post.title }}</a></h3>
                <div class="post-meta">
                    作者: <a href="/users/{{ post.author.id }}">{{ post.author.username }}</a> | 
                    发布时间: {{ post.created_at.strftime('%Y-%m-%d %H:%M') }}
                </div>
                <p>{{ post.content[:200] }}{% if post.content|length > 200 %}...{% endif %}</p>
                {% if post.tags %}
                <div class="tags">
                    {% for tag in post.tags %}
                    <span class="tag">{{ tag.name }}</span>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
            {% endfor %}
            
            {% if pagination.pages > 1 %}
            <div class="pagination">
                {% if pagination.has_prev %}
                <a href="?page={{ pagination.prev_num }}">← 上一页</a>
                {% endif %}
                
                {% for p in pagination.iter_pages() %}
                    {% if p %}
                        {% if p == pagination.page %}
                        <a href="?page={{ p }}" class="current">{{ p }}</a>
                        {% else %}
                        <a href="?page={{ p }}">{{ p }}</a>
                        {% endif %}
                    {% else %}
                    <span>...</span>
                    {% endif %}
                {% endfor %}
                
                {% if pagination.has_next %}
                <a href="?page={{ pagination.next_num }}">下一页 →</a>
                {% endif %}
            </div>
            {% endif %}
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, posts=posts, pagination=pagination)


@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    """文章详情"""
    post = Post.query.get_or_404(post_id)
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ post.title }}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 15px;
            }
            .post-meta {
                color: #666;
                margin: 20px 0;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 5px;
            }
            .post-content {
                line-height: 1.8;
                margin: 30px 0;
            }
            .tags {
                margin-top: 20px;
            }
            .tag {
                display: inline-block;
                background: #e8f4f8;
                color: #2980b9;
                padding: 5px 15px;
                border-radius: 15px;
                margin-right: 10px;
            }
            .back-link {
                display: inline-block;
                margin-top: 30px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{{ post.title }}</h1>
            
            <div class="post-meta">
                <p>
                    <strong>作者:</strong> <a href="/users/{{ post.author.id }}">{{ post.author.username }}</a><br>
                    <strong>发布时间:</strong> {{ post.created_at.strftime('%Y-%m-%d %H:%M:%S') }}<br>
                    <strong>更新时间:</strong> {{ post.updated_at.strftime('%Y-%m-%d %H:%M:%S') }}
                </p>
            </div>
            
            <div class="post-content">
                {{ post.content }}
            </div>
            
            {% if post.tags %}
            <div class="tags">
                <strong>标签:</strong>
                {% for tag in post.tags %}
                <span class="tag">{{ tag.name }}</span>
                {% endfor %}
            </div>
            {% endif %}
            
            <a href="/posts" class="back-link">← 返回文章列表</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, post=post)


# ============================================
# API 端点
# ============================================

@app.route('/api/users')
def api_users():
    """用户 API"""
    users = User.query.all()
    return {
        'total': len(users),
        'users': [user.to_dict() for user in users]
    }


@app.route('/api/posts')
def api_posts():
    """文章 API"""
    posts = Post.query.all()
    return {
        'total': len(posts),
        'posts': [post.to_dict() for post in posts]
    }


if __name__ == '__main__':
    print("🚀 Starting Flask Database Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    print(f"💾 数据库文件: {os.path.join(basedir, 'database.db')}")
    app.run(debug=True, host='0.0.0.0', port=5000)

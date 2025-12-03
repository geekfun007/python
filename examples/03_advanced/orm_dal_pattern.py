"""
Flask 高级示例: ORM + DAL 模式
Flask Advanced Example: ORM + DAL Pattern

演示如何使用数据访问层（DAL）模式封装数据库操作，实现业务逻辑与数据访问的分离。
Demonstrates how to use Data Access Layer (DAL) pattern to encapsulate database operations,
separating business logic from data access.
"""

from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
import os

# ============================================
# 应用配置
# ============================================

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "dal_example.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ============================================
# ORM 模型层 (Models)
# ============================================

class User(db.Model):
    """
    用户模型 - Active Record 模式
    User Model - Active Record Pattern
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'posts_count': self.posts.count()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """文章模型"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'status': self.status,
            'views': self.views,
            'author': self.author.username if self.author else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f'<Post {self.title}>'


# ============================================
# 数据访问层接口 (DAL Interface)
# ============================================

class BaseRepository(ABC):
    """
    基础仓储接口 - 定义通用的 CRUD 操作
    Base Repository Interface - Defines common CRUD operations
    """
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Any]:
        """根据 ID 获取实体"""
        pass
    
    @abstractmethod
    def get_all(self, **filters) -> List[Any]:
        """获取所有实体"""
        pass
    
    @abstractmethod
    def create(self, **kwargs) -> Any:
        """创建实体"""
        pass
    
    @abstractmethod
    def update(self, id: int, **kwargs) -> Optional[Any]:
        """更新实体"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """删除实体"""
        pass
    
    @abstractmethod
    def count(self, **filters) -> int:
        """统计数量"""
        pass


# ============================================
# 用户数据访问层 (User DAL)
# ============================================

class UserRepository(BaseRepository):
    """
    用户仓储 - 封装所有用户相关的数据库操作
    User Repository - Encapsulates all user-related database operations
    """
    
    def __init__(self):
        self.model = User
    
    def get_by_id(self, id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        return self.model.query.get(id)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.model.query.filter_by(username=username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.model.query.filter_by(email=email).first()
    
    def get_all(self, active_only: bool = False, **filters) -> List[User]:
        """
        获取所有用户
        
        Args:
            active_only: 只返回活跃用户
            **filters: 其他过滤条件
        """
        query = self.model.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        if filters:
            query = query.filter_by(**filters)
        
        return query.all()
    
    def create(self, username: str, email: str, **kwargs) -> User:
        """
        创建用户
        
        Args:
            username: 用户名
            email: 邮箱
            **kwargs: 其他字段
        
        Returns:
            创建的用户对象
        
        Raises:
            ValueError: 如果用户名或邮箱已存在
        """
        # 验证用户名和邮箱唯一性
        if self.get_by_username(username):
            raise ValueError(f'Username "{username}" already exists')
        
        if self.get_by_email(email):
            raise ValueError(f'Email "{email}" already exists')
        
        # 创建用户
        user = self.model(username=username, email=email, **kwargs)
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def update(self, id: int, **kwargs) -> Optional[User]:
        """
        更新用户
        
        Args:
            id: 用户 ID
            **kwargs: 要更新的字段
        
        Returns:
            更新后的用户对象，如果用户不存在返回 None
        """
        user = self.get_by_id(id)
        if not user:
            return None
        
        # 更新字段
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return user
    
    def delete(self, id: int) -> bool:
        """
        删除用户
        
        Args:
            id: 用户 ID
        
        Returns:
            删除成功返回 True，用户不存在返回 False
        """
        user = self.get_by_id(id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    def deactivate(self, id: int) -> Optional[User]:
        """停用用户（软删除）"""
        return self.update(id, is_active=False)
    
    def activate(self, id: int) -> Optional[User]:
        """激活用户"""
        return self.update(id, is_active=True)
    
    def count(self, active_only: bool = False, **filters) -> int:
        """统计用户数量"""
        query = self.model.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        if filters:
            query = query.filter_by(**filters)
        
        return query.count()
    
    def search(self, keyword: str, limit: int = 10) -> List[User]:
        """
        搜索用户
        
        Args:
            keyword: 搜索关键词
            limit: 返回结果数量限制
        """
        return self.model.query.filter(
            db.or_(
                self.model.username.ilike(f'%{keyword}%'),
                self.model.email.ilike(f'%{keyword}%'),
                self.model.full_name.ilike(f'%{keyword}%')
            )
        ).limit(limit).all()
    
    def get_with_posts(self, id: int) -> Optional[User]:
        """获取用户及其文章（预加载）"""
        return self.model.query.options(
            db.joinedload('posts')
        ).get(id)
    
    def paginate(self, page: int = 1, per_page: int = 10, **filters):
        """
        分页查询
        
        Args:
            page: 页码
            per_page: 每页数量
            **filters: 过滤条件
        
        Returns:
            分页对象
        """
        query = self.model.query
        
        if filters:
            query = query.filter_by(**filters)
        
        return query.paginate(page=page, per_page=per_page, error_out=False)


# ============================================
# 文章数据访问层 (Post DAL)
# ============================================

class PostRepository(BaseRepository):
    """
    文章仓储 - 封装所有文章相关的数据库操作
    Post Repository - Encapsulates all post-related database operations
    """
    
    def __init__(self):
        self.model = Post
    
    def get_by_id(self, id: int) -> Optional[Post]:
        """根据 ID 获取文章"""
        return self.model.query.get(id)
    
    def get_all(self, status: Optional[str] = None, **filters) -> List[Post]:
        """获取所有文章"""
        query = self.model.query
        
        if status:
            query = query.filter_by(status=status)
        
        if filters:
            query = query.filter_by(**filters)
        
        return query.order_by(self.model.created_at.desc()).all()
    
    def create(self, title: str, content: str, user_id: int, **kwargs) -> Post:
        """创建文章"""
        post = self.model(
            title=title,
            content=content,
            user_id=user_id,
            **kwargs
        )
        db.session.add(post)
        db.session.commit()
        return post
    
    def update(self, id: int, **kwargs) -> Optional[Post]:
        """更新文章"""
        post = self.get_by_id(id)
        if not post:
            return None
        
        for key, value in kwargs.items():
            if hasattr(post, key):
                setattr(post, key, value)
        
        db.session.commit()
        return post
    
    def delete(self, id: int) -> bool:
        """删除文章"""
        post = self.get_by_id(id)
        if not post:
            return False
        
        db.session.delete(post)
        db.session.commit()
        return True
    
    def count(self, status: Optional[str] = None, **filters) -> int:
        """统计文章数量"""
        query = self.model.query
        
        if status:
            query = query.filter_by(status=status)
        
        if filters:
            query = query.filter_by(**filters)
        
        return query.count()
    
    def get_by_user(self, user_id: int, status: Optional[str] = None) -> List[Post]:
        """获取指定用户的文章"""
        query = self.model.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(self.model.created_at.desc()).all()
    
    def get_published(self, limit: Optional[int] = None) -> List[Post]:
        """获取已发布的文章"""
        query = self.model.query.filter_by(status='published')
        query = query.order_by(self.model.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def increment_views(self, id: int) -> Optional[Post]:
        """增加文章浏览次数"""
        post = self.get_by_id(id)
        if not post:
            return None
        
        post.views += 1
        db.session.commit()
        return post
    
    def publish(self, id: int) -> Optional[Post]:
        """发布文章"""
        return self.update(id, status='published')
    
    def archive(self, id: int) -> Optional[Post]:
        """归档文章"""
        return self.update(id, status='archived')
    
    def search(self, keyword: str, limit: int = 10) -> List[Post]:
        """搜索文章"""
        return self.model.query.filter(
            db.or_(
                self.model.title.ilike(f'%{keyword}%'),
                self.model.content.ilike(f'%{keyword}%')
            )
        ).limit(limit).all()
    
    def get_popular(self, limit: int = 10) -> List[Post]:
        """获取热门文章（按浏览量排序）"""
        return self.model.query.filter_by(status='published') \
            .order_by(self.model.views.desc()) \
            .limit(limit).all()


# ============================================
# 业务逻辑层 (Service Layer)
# ============================================

class UserService:
    """
    用户服务 - 封装用户相关的业务逻辑
    User Service - Encapsulates user-related business logic
    """
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.post_repo = PostRepository()
    
    def register_user(self, username: str, email: str, full_name: str = None) -> Dict[str, Any]:
        """
        注册用户
        
        Returns:
            包含用户信息的字典
        
        Raises:
            ValueError: 如果验证失败
        """
        try:
            user = self.user_repo.create(
                username=username,
                email=email,
                full_name=full_name
            )
            return {
                'success': True,
                'user': user.to_dict(),
                'message': f'User {username} registered successfully'
            }
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """获取用户资料（包含文章统计）"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        # 获取用户的文章统计
        total_posts = self.post_repo.count(user_id=user_id)
        published_posts = self.post_repo.count(user_id=user_id, status='published')
        draft_posts = self.post_repo.count(user_id=user_id, status='draft')
        
        profile = user.to_dict()
        profile['statistics'] = {
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts
        }
        
        return profile
    
    def deactivate_user(self, user_id: int) -> Dict[str, Any]:
        """停用用户"""
        user = self.user_repo.deactivate(user_id)
        if user:
            return {
                'success': True,
                'message': f'User {user.username} deactivated'
            }
        return {
            'success': False,
            'error': 'User not found'
        }


class PostService:
    """
    文章服务 - 封装文章相关的业务逻辑
    Post Service - Encapsulates post-related business logic
    """
    
    def __init__(self):
        self.post_repo = PostRepository()
        self.user_repo = UserRepository()
    
    def create_post(self, title: str, content: str, user_id: int, 
                    status: str = 'draft') -> Dict[str, Any]:
        """创建文章"""
        # 验证用户存在
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return {
                'success': False,
                'error': 'User not found'
            }
        
        # 验证用户是活跃状态
        if not user.is_active:
            return {
                'success': False,
                'error': 'User is not active'
            }
        
        # 创建文章
        post = self.post_repo.create(
            title=title,
            content=content,
            user_id=user_id,
            status=status
        )
        
        return {
            'success': True,
            'post': post.to_dict(),
            'message': 'Post created successfully'
        }
    
    def get_post_detail(self, post_id: int, increment_view: bool = True) -> Optional[Dict[str, Any]]:
        """获取文章详情（并增加浏览次数）"""
        if increment_view:
            post = self.post_repo.increment_views(post_id)
        else:
            post = self.post_repo.get_by_id(post_id)
        
        if not post:
            return None
        
        return post.to_dict()
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """获取仪表板统计信息"""
        return {
            'total_posts': self.post_repo.count(),
            'published_posts': self.post_repo.count(status='published'),
            'draft_posts': self.post_repo.count(status='draft'),
            'archived_posts': self.post_repo.count(status='archived'),
            'total_users': UserRepository().count(),
            'active_users': UserRepository().count(active_only=True)
        }


# ============================================
# 初始化数据库和示例数据
# ============================================

def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        
        # 检查是否已有数据
        if User.query.count() == 0:
            # 初始化仓储
            user_repo = UserRepository()
            post_repo = PostRepository()
            
            # 创建示例用户
            try:
                user1 = user_repo.create(
                    username='alice',
                    email='alice@example.com',
                    full_name='Alice Johnson'
                )
                
                user2 = user_repo.create(
                    username='bob',
                    email='bob@example.com',
                    full_name='Bob Smith'
                )
                
                # 创建示例文章
                post_repo.create(
                    title='Understanding ORM Pattern',
                    content='ORM (Object-Relational Mapping) is a technique...',
                    user_id=user1.id,
                    status='published'
                )
                
                post_repo.create(
                    title='Data Access Layer Best Practices',
                    content='The DAL pattern helps separate business logic from data access...',
                    user_id=user1.id,
                    status='published'
                )
                
                post_repo.create(
                    title='Draft Article',
                    content='This is a draft article...',
                    user_id=user2.id,
                    status='draft'
                )
                
                print("✅ 示例数据已创建")
            except Exception as e:
                print(f"❌ 创建示例数据失败: {e}")


# ============================================
# 路由 (Routes)
# ============================================

@app.route('/')
def index():
    """首页"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ORM + DAL 模式示例</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { color: #667eea; }
            .section {
                background: #f8f9fa;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .api-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .api-card {
                background: white;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #e0e0e0;
            }
            .api-card h4 {
                margin-top: 0;
                color: #667eea;
            }
            .method {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                color: white;
            }
            .get { background: #27ae60; }
            .post { background: #3498db; }
            .put { background: #f39c12; }
            .delete { background: #e74c3c; }
            a {
                color: #667eea;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            pre {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }
            .stat-card h3 {
                margin: 0;
                font-size: 32px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗄️ ORM + DAL 模式示例</h1>
            <h2>Data Access Layer Pattern</h2>
            
            <div class="section">
                <h3>💡 什么是 DAL？</h3>
                <p><strong>数据访问层（Data Access Layer, DAL）</strong>是一种设计模式，用于将数据访问逻辑与业务逻辑分离。</p>
                <ul>
                    <li><strong>ORM (Object-Relational Mapping)</strong>: 对象关系映射，将数据库表映射为 Python 类</li>
                    <li><strong>Repository 模式</strong>: 封装数据访问操作，提供统一的接口</li>
                    <li><strong>Service 层</strong>: 封装业务逻辑，协调多个 Repository</li>
                </ul>
            </div>
            
            <div class="section">
                <h3>📊 系统统计</h3>
                <div class="stats" id="stats">
                    <div class="stat-card">
                        <h3>-</h3>
                        <p>用户总数</p>
                    </div>
                    <div class="stat-card">
                        <h3>-</h3>
                        <p>文章总数</p>
                    </div>
                    <div class="stat-card">
                        <h3>-</h3>
                        <p>已发布</p>
                    </div>
                    <div class="stat-card">
                        <h3>-</h3>
                        <p>草稿</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>🔌 API 端点</h3>
                
                <h4>用户 API (User API)</h4>
                <div class="api-grid">
                    <div class="api-card">
                        <h4><span class="method get">GET</span> <a href="/api/users">/api/users</a></h4>
                        <p>获取所有用户</p>
                    </div>
                    <div class="api-card">
                        <h4><span class="method get">GET</span> <a href="/api/users/1">/api/users/:id</a></h4>
                        <p>获取用户详情</p>
                    </div>
                    <div class="api-card">
                        <h4><span class="method post">POST</span> /api/users</h4>
                        <p>创建用户</p>
                    </div>
                    <div class="api-card">
                        <h4><span class="method get">GET</span> <a href="/api/users/1/posts">/api/users/:id/posts</a></h4>
                        <p>获取用户的文章</p>
                    </div>
                </div>
                
                <h4>文章 API (Post API)</h4>
                <div class="api-grid">
                    <div class="api-card">
                        <h4><span class="method get">GET</span> <a href="/api/posts">/api/posts</a></h4>
                        <p>获取所有文章</p>
                    </div>
                    <div class="api-card">
                        <h4><span class="method get">GET</span> <a href="/api/posts/1">/api/posts/:id</a></h4>
                        <p>获取文章详情</p>
                    </div>
                    <div class="api-card">
                        <h4><span class="method post">POST</span> /api/posts</h4>
                        <p>创建文章</p>
                    </div>
                    <div class="api-card">
                        <h4><span class="method get">GET</span> <a href="/api/posts/published">/api/posts/published</a></h4>
                        <p>获取已发布文章</p>
                    </div>
                </div>
                
                <h4>统计 API (Stats API)</h4>
                <div class="api-grid">
                    <div class="api-card">
                        <h4><span class="method get">GET</span> <a href="/api/stats">/api/stats</a></h4>
                        <p>获取系统统计</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>🏗️ 架构示例</h3>
                <pre><code># 1. ORM 模型（数据库映射）
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

# 2. Repository（数据访问层）
class UserRepository:
    def get_by_id(self, id):
        return User.query.get(id)
    
    def create(self, username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

# 3. Service（业务逻辑层）
class UserService:
    def __init__(self):
        self.repo = UserRepository()
    
    def register_user(self, username, email):
        # 业务逻辑：验证、创建用户等
        return self.repo.create(username, email)</code></pre>
            </div>
            
            <div class="section">
                <h3>🧪 测试 API</h3>
                <p>使用 curl 或 Postman 测试 API：</p>
                <pre><code># 获取所有用户
curl http://127.0.0.1:5000/api/users

# 创建新用户
curl -X POST http://127.0.0.1:5000/api/users \\
  -H "Content-Type: application/json" \\
  -d '{"username":"john","email":"john@example.com","full_name":"John Doe"}'

# 获取用户详情
curl http://127.0.0.1:5000/api/users/1

# 创建文章
curl -X POST http://127.0.0.1:5000/api/posts \\
  -H "Content-Type: application/json" \\
  -d '{"title":"New Post","content":"Content...","user_id":1}'</code></pre>
            </div>
        </div>
        
        <script>
            // 加载统计数据
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    const stats = document.querySelectorAll('.stat-card h3');
                    stats[0].textContent = data.total_users;
                    stats[1].textContent = data.total_posts;
                    stats[2].textContent = data.published_posts;
                    stats[3].textContent = data.draft_posts;
                });
        </script>
    </body>
    </html>
    '''
    return render_template_string(template)


# ============================================
# API 路由 - 用户
# ============================================

@app.route('/api/users', methods=['GET'])
def api_get_users():
    """获取所有用户"""
    repo = UserRepository()
    users = repo.get_all()
    return jsonify({
        'success': True,
        'count': len(users),
        'users': [user.to_dict() for user in users]
    })


@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    """获取用户详情"""
    service = UserService()
    profile = service.get_user_profile(user_id)
    
    if not profile:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    return jsonify({'success': True, 'user': profile})


@app.route('/api/users', methods=['POST'])
def api_create_user():
    """创建用户"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required fields: username, email'
        }), 400
    
    service = UserService()
    result = service.register_user(
        username=data['username'],
        email=data['email'],
        full_name=data.get('full_name')
    )
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@app.route('/api/users/<int:user_id>/posts', methods=['GET'])
def api_get_user_posts(user_id):
    """获取用户的文章"""
    repo = PostRepository()
    posts = repo.get_by_user(user_id)
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'count': len(posts),
        'posts': [post.to_dict() for post in posts]
    })


# ============================================
# API 路由 - 文章
# ============================================

@app.route('/api/posts', methods=['GET'])
def api_get_posts():
    """获取所有文章"""
    repo = PostRepository()
    status = request.args.get('status')
    posts = repo.get_all(status=status)
    
    return jsonify({
        'success': True,
        'count': len(posts),
        'posts': [post.to_dict() for post in posts]
    })


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def api_get_post(post_id):
    """获取文章详情"""
    service = PostService()
    post = service.get_post_detail(post_id)
    
    if not post:
        return jsonify({'success': False, 'error': 'Post not found'}), 404
    
    return jsonify({'success': True, 'post': post})


@app.route('/api/posts', methods=['POST'])
def api_create_post():
    """创建文章"""
    data = request.get_json()
    
    required_fields = ['title', 'content', 'user_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {", ".join(required_fields)}'
        }), 400
    
    service = PostService()
    result = service.create_post(
        title=data['title'],
        content=data['content'],
        user_id=data['user_id'],
        status=data.get('status', 'draft')
    )
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@app.route('/api/posts/published', methods=['GET'])
def api_get_published_posts():
    """获取已发布的文章"""
    repo = PostRepository()
    limit = request.args.get('limit', type=int)
    posts = repo.get_published(limit=limit)
    
    return jsonify({
        'success': True,
        'count': len(posts),
        'posts': [post.to_dict() for post in posts]
    })


@app.route('/api/posts/popular', methods=['GET'])
def api_get_popular_posts():
    """获取热门文章"""
    repo = PostRepository()
    limit = request.args.get('limit', 10, type=int)
    posts = repo.get_popular(limit=limit)
    
    return jsonify({
        'success': True,
        'count': len(posts),
        'posts': [post.to_dict() for post in posts]
    })


# ============================================
# API 路由 - 统计
# ============================================

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """获取系统统计"""
    service = PostService()
    stats = service.get_dashboard_stats()
    return jsonify(stats)


# ============================================
# 初始化
# ============================================

init_db()


if __name__ == '__main__':
    print("🚀 Starting ORM + DAL Pattern Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    print("\n💡 架构说明:")
    print("  ✅ ORM 层: User, Post 模型")
    print("  ✅ DAL 层: UserRepository, PostRepository")
    print("  ✅ Service 层: UserService, PostService")
    print("\n🔌 API 端点:")
    print("  GET  /api/users")
    print("  GET  /api/users/:id")
    print("  POST /api/users")
    print("  GET  /api/posts")
    print("  POST /api/posts")
    print("  GET  /api/stats")
    app.run(debug=True, host='0.0.0.0', port=5000)

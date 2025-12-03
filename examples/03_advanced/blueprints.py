"""
Flask 高级示例 1: 蓝图 (Blueprints)
Flask Advanced Example 1: Blueprints

演示如何使用蓝图组织大型应用。
Demonstrates how to organize large applications using Blueprints.
"""

from flask import Flask, render_template_string, Blueprint

app = Flask(__name__)


# ============================================
# 蓝图 1: 主页模块
# ============================================

main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    """主页"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask 蓝图示例</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1000px;
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
            .nav-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .nav-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                transition: all 0.3s;
            }
            .nav-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .nav-card h3 {
                margin-top: 0;
                color: #667eea;
            }
            .nav-card a {
                color: #3498db;
                text-decoration: none;
                display: inline-block;
                margin-top: 10px;
            }
            .nav-card a:hover {
                text-decoration: underline;
            }
            .feature {
                background: #f8f9fa;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
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
            <h1>🧩 Flask 蓝图 (Blueprints)</h1>
            <h2>模块化应用架构</h2>
            
            <div class="feature">
                <h3>💡 什么是蓝图？</h3>
                <p>蓝图是 Flask 提供的一种组织应用的方式，可以将应用分解为多个模块。每个蓝图可以有自己的路由、模板、静态文件等。</p>
                <ul>
                    <li><strong>模块化:</strong> 将大型应用分解为小模块</li>
                    <li><strong>可重用:</strong> 蓝图可以在不同应用中重用</li>
                    <li><strong>URL前缀:</strong> 每个蓝图可以有自己的URL前缀</li>
                    <li><strong>独立性:</strong> 蓝图可以有独立的错误处理器和钩子函数</li>
                </ul>
            </div>
            
            <h3>📋 示例模块导航</h3>
            <div class="nav-grid">
                <div class="nav-card">
                    <h3>👤 用户模块</h3>
                    <p>处理用户相关的功能</p>
                    <a href="/users/">用户列表</a><br>
                    <a href="/users/profile/admin">查看用户资料</a>
                </div>
                
                <div class="nav-card">
                    <h3>📝 博客模块</h3>
                    <p>博客文章管理</p>
                    <a href="/blog/">文章列表</a><br>
                    <a href="/blog/post/1">文章详情</a>
                </div>
                
                <div class="nav-card">
                    <h3>🔌 API 模块</h3>
                    <p>RESTful API 接口</p>
                    <a href="/api/">API 首页</a><br>
                    <a href="/api/v1/users">API: 用户</a>
                </div>
                
                <div class="nav-card">
                    <h3>⚙️ 管理模块</h3>
                    <p>后台管理功能</p>
                    <a href="/admin/">管理首页</a><br>
                    <a href="/admin/settings">系统设置</a>
                </div>
            </div>
            
            <div class="feature">
                <h3>📚 蓝图定义示例</h3>
                <pre><code># 创建蓝图
from flask import Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/users')

# 定义路由
@users_bp.route('/')
def user_list():
    return 'User List'

@users_bp.route('/&lt;username&gt;')
def user_profile(username):
    return f'Profile: {username}'

# 在主应用中注册蓝图
app.register_blueprint(users_bp)</code></pre>
            </div>
            
            <div class="feature">
                <h3>🏗️ 典型的蓝图应用结构</h3>
                <pre><code>myapp/
├── app.py              # 主应用
├── blueprints/         # 蓝图目录
│   ├── __init__.py
│   ├── users/          # 用户模块
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── models.py
│   ├── blog/           # 博客模块
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── models.py
│   └── api/            # API模块
│       ├── __init__.py
│       └── views.py
├── templates/          # 模板
│   ├── users/
│   └── blog/
└── static/            # 静态文件</code></pre>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


# ============================================
# 蓝图 2: 用户模块
# ============================================

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def user_list():
    """用户列表"""
    users = [
        {'id': 1, 'username': 'admin', 'email': 'admin@example.com'},
        {'id': 2, 'username': 'alice', 'email': 'alice@example.com'},
        {'id': 3, 'username': 'bob', 'email': 'bob@example.com'},
    ]
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户列表</title>
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
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #3498db; }
            .info-box {
                background: #e8f4f8;
                padding: 15px;
                border-left: 4px solid #3498db;
                margin: 20px 0;
                border-radius: 5px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background: #3498db;
                color: white;
            }
            tr:hover {
                background: #f5f5f5;
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
            <h1>👤 用户列表</h1>
            
            <div class="info-box">
                <strong>📌 蓝图信息:</strong><br>
                Blueprint Name: <code>users</code><br>
                URL Prefix: <code>/users</code>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>用户名</th>
                        <th>邮箱</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td><a href="/users/profile/{{ user.username }}">查看</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, users=users)


@users_bp.route('/profile/<username>')
def user_profile(username):
    """用户资料"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户资料 - {{ username }}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 700px;
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
            h1 { color: #3498db; }
            .profile-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
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
            <h1>👤 用户资料</h1>
            <div class="profile-card">
                <h2>{{ username }}</h2>
                <p><strong>URL:</strong> <code>{{ request.url }}</code></p>
                <p><strong>Blueprint:</strong> <code>{{ request.blueprint }}</code></p>
                <p><strong>Endpoint:</strong> <code>{{ request.endpoint }}</code></p>
            </div>
            <a href="/users/" class="back-link">← 返回用户列表</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, username=username)


# ============================================
# 蓝图 3: 博客模块
# ============================================

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

@blog_bp.route('/')
def blog_list():
    """博客列表"""
    posts = [
        {'id': 1, 'title': 'Flask 蓝图入门', 'author': 'admin'},
        {'id': 2, 'title': 'Python Web 开发', 'author': 'alice'},
        {'id': 3, 'title': '模块化应用设计', 'author': 'bob'},
    ]
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>博客列表</title>
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
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #e74c3c; }
            .info-box {
                background: #fef5e7;
                padding: 15px;
                border-left: 4px solid #e74c3c;
                margin: 20px 0;
                border-radius: 5px;
            }
            .post-card {
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
                border-left: 4px solid #e74c3c;
            }
            .post-card h3 {
                margin-top: 0;
                color: #e74c3c;
            }
            .post-card a {
                color: #3498db;
                text-decoration: none;
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
            <h1>📝 博客列表</h1>
            
            <div class="info-box">
                <strong>📌 蓝图信息:</strong><br>
                Blueprint Name: <code>blog</code><br>
                URL Prefix: <code>/blog</code>
            </div>
            
            {% for post in posts %}
            <div class="post-card">
                <h3><a href="/blog/post/{{ post.id }}">{{ post.title }}</a></h3>
                <p>作者: {{ post.author }}</p>
            </div>
            {% endfor %}
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, posts=posts)


@blog_bp.route('/post/<int:post_id>')
def blog_detail(post_id):
    """博客详情"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>文章详情</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 700px;
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
            h1 { color: #e74c3c; }
            .post-content {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
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
            <h1>📄 文章 #{{ post_id }}</h1>
            <div class="post-content">
                <p><strong>URL:</strong> <code>{{ request.url }}</code></p>
                <p><strong>Blueprint:</strong> <code>{{ request.blueprint }}</code></p>
                <p><strong>Endpoint:</strong> <code>{{ request.endpoint }}</code></p>
            </div>
            <a href="/blog/" class="back-link">← 返回博客列表</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, post_id=post_id)


# ============================================
# 蓝图 4: API 模块
# ============================================

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def api_index():
    """API 首页"""
    return {
        'name': 'Flask Blueprint API',
        'version': '1.0',
        'endpoints': {
            'users': '/api/v1/users',
            'posts': '/api/v1/posts',
        }
    }


@api_bp.route('/v1/users')
def api_users():
    """API: 用户列表"""
    return {
        'blueprint': 'api',
        'endpoint': 'users',
        'data': [
            {'id': 1, 'username': 'admin'},
            {'id': 2, 'username': 'alice'},
            {'id': 3, 'username': 'bob'},
        ]
    }


@api_bp.route('/v1/posts')
def api_posts():
    """API: 文章列表"""
    return {
        'blueprint': 'api',
        'endpoint': 'posts',
        'data': [
            {'id': 1, 'title': 'Flask 蓝图入门'},
            {'id': 2, 'title': 'Python Web 开发'},
        ]
    }


# ============================================
# 蓝图 5: 管理模块
# ============================================

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_index():
    """管理首页"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>管理后台</title>
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
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #9b59b6; }
            .info-box {
                background: #f4ecf7;
                padding: 15px;
                border-left: 4px solid #9b59b6;
                margin: 20px 0;
                border-radius: 5px;
            }
            .menu {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .menu-item {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border: 2px solid #9b59b6;
            }
            .menu-item a {
                color: #9b59b6;
                text-decoration: none;
                font-weight: bold;
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
            <h1>⚙️ 管理后台</h1>
            
            <div class="info-box">
                <strong>📌 蓝图信息:</strong><br>
                Blueprint Name: <code>admin</code><br>
                URL Prefix: <code>/admin</code>
            </div>
            
            <h3>管理菜单</h3>
            <div class="menu">
                <div class="menu-item">
                    <a href="/admin/users">👥 用户管理</a>
                </div>
                <div class="menu-item">
                    <a href="/admin/settings">⚙️ 系统设置</a>
                </div>
                <div class="menu-item">
                    <a href="/admin/logs">📊 日志查看</a>
                </div>
            </div>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


@admin_bp.route('/settings')
def admin_settings():
    """系统设置"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>系统设置</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 700px;
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
            h1 { color: #9b59b6; }
            .settings-group {
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
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
            <h1>⚙️ 系统设置</h1>
            <div class="settings-group">
                <p><strong>Blueprint:</strong> {{ request.blueprint }}</p>
                <p><strong>Endpoint:</strong> {{ request.endpoint }}</p>
                <p><strong>URL:</strong> {{ request.url }}</p>
            </div>
            <a href="/admin/" class="back-link">← 返回管理首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


# ============================================
# 注册所有蓝图
# ============================================

app.register_blueprint(main_bp)
app.register_blueprint(users_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)


# ============================================
# 显示所有注册的蓝图和路由
# ============================================

@app.route('/debug/routes')
def show_routes():
    """显示所有路由"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': ', '.join(rule.methods - {'OPTIONS', 'HEAD'}),
            'rule': rule.rule
        })
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>所有路由</title>
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
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background: #2c3e50;
                color: white;
            }
            tr:hover {
                background: #f5f5f5;
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
            <h1>🗺️ 所有注册的路由</h1>
            <p>共有 {{ routes|length }} 个路由</p>
            <table>
                <thead>
                    <tr>
                        <th>Endpoint</th>
                        <th>Methods</th>
                        <th>URL Rule</th>
                    </tr>
                </thead>
                <tbody>
                    {% for route in routes %}
                    <tr>
                        <td><code>{{ route.endpoint }}</code></td>
                        <td>{{ route.methods }}</td>
                        <td><code>{{ route.rule }}</code></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, routes=routes)


if __name__ == '__main__':
    print("🚀 Starting Flask Blueprints Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    print("\n📋 注册的蓝图:")
    for blueprint_name, blueprint in app.blueprints.items():
        print(f"  - {blueprint_name}: {blueprint.url_prefix or '/'}")
    print("\n💡 查看所有路由: http://127.0.0.1:5000/debug/routes")
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
Flask 进阶示例 3: 用户认证和会话管理
Flask Intermediate Example 3: Authentication and Session Management

演示用户登录、注册、会话管理和权限控制。
Demonstrates user login, registration, session management, and authorization.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # 生成安全的密钥
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 会话有效期

# 模拟用户数据库
users_db = {
    'admin': {
        'id': 1,
        'username': 'admin',
        'password': generate_password_hash('Admin123!'),  # 密码: Admin123!
        'email': 'admin@example.com',
        'role': 'admin',
        'created_at': datetime.now()
    },
    'user': {
        'id': 2,
        'username': 'user',
        'password': generate_password_hash('User123!'),  # 密码: User123!
        'email': 'user@example.com',
        'role': 'user',
        'created_at': datetime.now()
    }
}


# ============================================
# 装饰器：登录验证
# ============================================

def login_required(f):
    """要求用户登录"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """要求管理员权限"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        
        user = get_current_user()
        if not user or user.get('role') != 'admin':
            flash('需要管理员权限', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================
# 辅助函数
# ============================================

def get_current_user():
    """获取当前登录用户"""
    if 'user_id' in session:
        for user in users_db.values():
            if user['id'] == session['user_id']:
                return user
    return None


# ============================================
# 路由
# ============================================

@app.route('/')
def index():
    """主页"""
    user = get_current_user()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask 认证示例</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 900px;
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
            .user-info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
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
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                text-align: center;
                transition: all 0.3s;
            }
            .nav-link:hover {
                background: #2980b9;
                transform: translateY(-2px);
            }
            .nav-link.danger {
                background: #e74c3c;
            }
            .nav-link.danger:hover {
                background: #c0392b;
            }
            .nav-link.success {
                background: #27ae60;
            }
            .nav-link.success:hover {
                background: #229954;
            }
            .feature {
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 5px;
                border-left: 4px solid #667eea;
            }
            .flash {
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
            }
            .flash.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .flash.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .flash.warning {
                background: #fff3cd;
                color: #856404;
                border: 1px solid #ffeeba;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Flask 认证示例</h1>
            <h2>Authentication & Session Management</h2>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            {% if user %}
            <div class="user-info">
                <h3>👤 当前用户信息</h3>
                <p><strong>用户名:</strong> {{ user.username }}</p>
                <p><strong>邮箱:</strong> {{ user.email }}</p>
                <p><strong>角色:</strong> 
                    {% if user.role == 'admin' %}
                        🔑 管理员
                    {% else %}
                        👤 普通用户
                    {% endif %}
                </p>
                <p><strong>登录时间:</strong> {{ session.get('login_time', 'N/A') }}</p>
            </div>
            
            <h3>📋 功能导航</h3>
            <div class="nav-links">
                <a href="/profile" class="nav-link">📋 个人资料</a>
                <a href="/protected" class="nav-link">🔒 受保护页面</a>
                {% if user.role == 'admin' %}
                <a href="/admin" class="nav-link">⚙️ 管理后台</a>
                {% endif %}
                <a href="/logout" class="nav-link danger">🚪 退出登录</a>
            </div>
            
            {% else %}
            <div class="feature">
                <h3>欢迎使用认证系统</h3>
                <p>请登录或注册以访问完整功能</p>
            </div>
            
            <div class="nav-links">
                <a href="/login" class="nav-link">🔑 登录</a>
                <a href="/register" class="nav-link success">📝 注册</a>
            </div>
            
            <div class="feature">
                <h3>🧪 测试账号</h3>
                <p><strong>管理员账号:</strong></p>
                <ul>
                    <li>用户名: admin</li>
                    <li>密码: Admin123!</li>
                </ul>
                <p><strong>普通用户账号:</strong></p>
                <ul>
                    <li>用户名: user</li>
                    <li>密码: User123!</li>
                </ul>
            </div>
            {% endif %}
            
            <div class="feature">
                <h3>💡 功能特性</h3>
                <ul>
                    <li>✅ 用户注册和登录</li>
                    <li>✅ 密码哈希存储 (Werkzeug Security)</li>
                    <li>✅ 会话管理 (Session)</li>
                    <li>✅ 登录装饰器 (@login_required)</li>
                    <li>✅ 权限控制 (基于角色)</li>
                    <li>✅ 记住我功能</li>
                    <li>✅ 自动重定向</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if 'user_id' in session:
        flash('您已登录', 'info')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 验证
        errors = []
        if not username:
            errors.append('用户名不能为空')
        elif username in users_db:
            errors.append('用户名已存在')
        elif len(username) < 3:
            errors.append('用户名至少需要3个字符')
        
        if not email:
            errors.append('邮箱不能为空')
        elif any(u['email'] == email for u in users_db.values()):
            errors.append('邮箱已被注册')
        
        if not password:
            errors.append('密码不能为空')
        elif len(password) < 8:
            errors.append('密码至少需要8个字符')
        elif password != confirm_password:
            errors.append('两次输入的密码不一致')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            # 创建新用户
            user_id = len(users_db) + 1
            users_db[username] = {
                'id': user_id,
                'username': username,
                'password': generate_password_hash(password),
                'email': email,
                'role': 'user',
                'created_at': datetime.now()
            }
            
            flash(f'✅ 注册成功！欢迎 {username}', 'success')
            return redirect(url_for('login'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户注册</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 500px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .form-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { color: #667eea; text-align: center; }
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
            input[type="password"] {
                width: 100%;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
                font-size: 14px;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover {
                background: #764ba2;
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
            .links {
                text-align: center;
                margin-top: 20px;
            }
            .links a {
                color: #667eea;
                text-decoration: none;
            }
            .links a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>📝 用户注册</h1>
            
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
                    <input type="text" id="username" name="username" required 
                           placeholder="至少3个字符" value="{{ request.form.get('username', '') }}">
                </div>
                
                <div class="form-group">
                    <label for="email">邮箱 *</label>
                    <input type="email" id="email" name="email" required 
                           placeholder="your@email.com" value="{{ request.form.get('email', '') }}">
                </div>
                
                <div class="form-group">
                    <label for="password">密码 *</label>
                    <input type="password" id="password" name="password" required 
                           placeholder="至少8个字符">
                </div>
                
                <div class="form-group">
                    <label for="confirm_password">确认密码 *</label>
                    <input type="password" id="confirm_password" name="confirm_password" required 
                           placeholder="再次输入密码">
                </div>
                
                <button type="submit">注册</button>
            </form>
            
            <div class="links">
                <p>已有账号？<a href="/login">立即登录</a></p>
                <p><a href="/">← 返回首页</a></p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if 'user_id' in session:
        flash('您已登录', 'info')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        remember = request.form.get('remember')
        next_page = request.args.get('next')
        
        user = users_db.get(username)
        
        if user and check_password_hash(user['password'], password):
            # 登录成功
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 记住我功能
            if remember:
                session.permanent = True
            
            flash(f'✅ 欢迎回来，{username}！', 'success')
            
            # 重定向到之前的页面或首页
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'error')
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户登录</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 500px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .form-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { color: #667eea; text-align: center; }
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
            input[type="password"] {
                width: 100%;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
                font-size: 14px;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            .checkbox-group {
                display: flex;
                align-items: center;
            }
            .checkbox-group input {
                margin-right: 10px;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover {
                background: #764ba2;
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
            .links {
                text-align: center;
                margin-top: 20px;
            }
            .links a {
                color: #667eea;
                text-decoration: none;
            }
            .links a:hover {
                text-decoration: underline;
            }
            .demo-accounts {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
                font-size: 13px;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>🔑 用户登录</h1>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST">
                <div class="form-group">
                    <label for="username">用户名</label>
                    <input type="text" id="username" name="username" required 
                           placeholder="输入用户名" value="{{ request.form.get('username', '') }}">
                </div>
                
                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" name="password" required 
                           placeholder="输入密码">
                </div>
                
                <div class="form-group checkbox-group">
                    <input type="checkbox" id="remember" name="remember" value="yes">
                    <label for="remember" style="font-weight: normal; margin: 0;">
                        记住我 (7天)
                    </label>
                </div>
                
                <button type="submit">登录</button>
            </form>
            
            <div class="demo-accounts">
                <strong>🧪 测试账号:</strong><br>
                管理员: admin / Admin123!<br>
                普通用户: user / User123!
            </div>
            
            <div class="links">
                <p>还没有账号？<a href="/register">立即注册</a></p>
                <p><a href="/">← 返回首页</a></p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


@app.route('/logout')
def logout():
    """退出登录"""
    username = session.get('username', '用户')
    session.clear()
    flash(f'👋 {username}，您已退出登录', 'success')
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """个人资料（需要登录）"""
    user = get_current_user()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>个人资料</title>
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
            h1 { color: #667eea; }
            .profile-info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
            .profile-info p {
                margin: 10px 0;
            }
            .badge {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            .badge.admin {
                background: #e74c3c;
                color: white;
            }
            .badge.user {
                background: #3498db;
                color: white;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 个人资料</h1>
            
            <div class="profile-info">
                <p><strong>用户 ID:</strong> {{ user.id }}</p>
                <p><strong>用户名:</strong> {{ user.username }}</p>
                <p><strong>邮箱:</strong> {{ user.email }}</p>
                <p><strong>角色:</strong> 
                    {% if user.role == 'admin' %}
                    <span class="badge admin">🔑 管理员</span>
                    {% else %}
                    <span class="badge user">👤 普通用户</span>
                    {% endif %}
                </p>
                <p><strong>注册时间:</strong> {{ user.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</p>
                <p><strong>会话开始:</strong> {{ session.get('login_time', 'N/A') }}</p>
            </div>
            
            <p>这是一个受保护的页面，只有登录用户才能访问。</p>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, user=user)


@app.route('/protected')
@login_required
def protected():
    """受保护的页面"""
    user = get_current_user()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>受保护页面</title>
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
            h1 { color: #27ae60; }
            .success-box {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #27ae60;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔒 受保护的页面</h1>
            
            <div class="success-box">
                <h2>✅ 访问成功！</h2>
                <p>恭喜，{{ user.username }}！您已成功访问受保护的页面。</p>
                <p>这个页面使用了 <code>@login_required</code> 装饰器，只有登录用户才能访问。</p>
            </div>
            
            <h3>💡 装饰器原理：</h3>
            <pre><code>@login_required
def protected():
    # 只有登录用户才能执行这里的代码
    pass</code></pre>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, user=user)


@app.route('/admin')
@admin_required
def admin():
    """管理员后台"""
    user = get_current_user()
    all_users = list(users_db.values())
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>管理后台</title>
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
            h1 { color: #e74c3c; }
            .admin-notice {
                background: #fff3cd;
                border: 1px solid #ffeeba;
                color: #856404;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
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
                background: #e74c3c;
                color: white;
            }
            .badge {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: bold;
            }
            .badge.admin {
                background: #e74c3c;
                color: white;
            }
            .badge.user {
                background: #3498db;
                color: white;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #e74c3c;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚙️ 管理员后台</h1>
            
            <div class="admin-notice">
                <strong>🔑 管理员权限</strong><br>
                这个页面使用了 <code>@admin_required</code> 装饰器，只有管理员才能访问。
            </div>
            
            <h2>👥 所有用户</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>用户名</th>
                        <th>邮箱</th>
                        <th>角色</th>
                        <th>注册时间</th>
                    </tr>
                </thead>
                <tbody>
                    {% for u in users %}
                    <tr>
                        <td>{{ u.id }}</td>
                        <td>{{ u.username }}</td>
                        <td>{{ u.email }}</td>
                        <td>
                            {% if u.role == 'admin' %}
                            <span class="badge admin">管理员</span>
                            {% else %}
                            <span class="badge user">用户</span>
                            {% endif %}
                        </td>
                        <td>{{ u.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, user=user, users=all_users)


if __name__ == '__main__':
    print("🚀 Starting Flask Authentication Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    print("\n🧪 测试账号:")
    print("  管理员: admin / Admin123!")
    print("  普通用户: user / User123!")
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
Flask 高级示例 2: RESTful API
Flask Advanced Example 2: RESTful API

演示如何构建符合 REST 规范的 API。
Demonstrates how to build RESTful APIs following REST conventions.
"""

from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# 模拟数据库
users_db = [
    {'id': 1, 'username': 'admin', 'email': 'admin@example.com', 'created_at': '2024-01-01'},
    {'id': 2, 'username': 'alice', 'email': 'alice@example.com', 'created_at': '2024-01-02'},
    {'id': 3, 'username': 'bob', 'email': 'bob@example.com', 'created_at': '2024-01-03'},
]

posts_db = [
    {'id': 1, 'title': 'Flask RESTful API 教程', 'content': 'REST API 设计原则...', 'user_id': 1, 'created_at': '2024-01-15'},
    {'id': 2, 'title': 'Python Web 开发', 'content': 'Flask 是一个轻量级框架...', 'user_id': 2, 'created_at': '2024-01-16'},
]

next_user_id = 4
next_post_id = 3


# ============================================
# 辅助函数
# ============================================

def api_response(data=None, message=None, status_code=200, errors=None):
    """标准 API 响应格式"""
    response = {
        'success': 200 <= status_code < 300,
        'status_code': status_code,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code


def validate_json(*required_fields):
    """装饰器：验证 JSON 请求数据"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return api_response(
                    message='Content-Type must be application/json',
                    status_code=400
                )
            
            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return api_response(
                    message='Missing required fields',
                    errors={'missing_fields': missing_fields},
                    status_code=400
                )
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


# ============================================
# 主页 - API 文档
# ============================================

@app.route('/')
def index():
    """API 文档主页"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask RESTful API</title>
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
            h2 { color: #2c3e50; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
            .endpoint {
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
                border-left: 4px solid #3498db;
            }
            .method {
                display: inline-block;
                padding: 5px 12px;
                border-radius: 5px;
                font-weight: bold;
                margin-right: 10px;
                color: white;
            }
            .method.get { background: #27ae60; }
            .method.post { background: #3498db; }
            .method.put { background: #f39c12; }
            .method.delete { background: #e74c3c; }
            .url { font-family: 'Courier New', monospace; color: #2c3e50; }
            pre {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
            .feature {
                background: #e8f4f8;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
                border-left: 4px solid #3498db;
            }
            .test-button {
                display: inline-block;
                padding: 8px 15px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 5px;
            }
            .test-button:hover {
                background: #2980b9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔌 Flask RESTful API</h1>
            <p>一个符合 REST 规范的 API 示例</p>
            
            <div class="feature">
                <h3>✨ REST API 设计原则</h3>
                <ul>
                    <li><strong>资源导向:</strong> URL 代表资源，使用名词而非动词</li>
                    <li><strong>HTTP 方法:</strong> GET (查询), POST (创建), PUT (更新), DELETE (删除)</li>
                    <li><strong>状态码:</strong> 正确使用 HTTP 状态码表示结果</li>
                    <li><strong>统一接口:</strong> 保持 API 接口的一致性</li>
                    <li><strong>无状态:</strong> 每个请求包含所有必要信息</li>
                </ul>
            </div>
            
            <h2>👤 用户 API (Users)</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="url">/api/users</span>
                <p>获取所有用户列表</p>
                <a href="/api/users" class="test-button" target="_blank">测试</a>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="url">/api/users/:id</span>
                <p>获取指定用户信息</p>
                <a href="/api/users/1" class="test-button" target="_blank">测试</a>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <span class="url">/api/users</span>
                <p>创建新用户</p>
                <pre><code>{
  "username": "newuser",
  "email": "newuser@example.com"
}</code></pre>
            </div>
            
            <div class="endpoint">
                <span class="method put">PUT</span>
                <span class="url">/api/users/:id</span>
                <p>更新用户信息</p>
                <pre><code>{
  "username": "updated_name",
  "email": "updated@example.com"
}</code></pre>
            </div>
            
            <div class="endpoint">
                <span class="method delete">DELETE</span>
                <span class="url">/api/users/:id</span>
                <p>删除用户</p>
            </div>
            
            <h2>📝 文章 API (Posts)</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="url">/api/posts</span>
                <p>获取所有文章</p>
                <a href="/api/posts" class="test-button" target="_blank">测试</a>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="url">/api/posts/:id</span>
                <p>获取指定文章</p>
                <a href="/api/posts/1" class="test-button" target="_blank">测试</a>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="url">/api/users/:id/posts</span>
                <p>获取指定用户的所有文章</p>
                <a href="/api/users/1/posts" class="test-button" target="_blank">测试</a>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <span class="url">/api/posts</span>
                <p>创建新文章</p>
                <pre><code>{
  "title": "新文章",
  "content": "文章内容...",
  "user_id": 1
}</code></pre>
            </div>
            
            <h2>🧪 测试 API</h2>
            <p>使用 curl 命令测试：</p>
            <pre><code># 获取所有用户
curl http://127.0.0.1:5000/api/users

# 获取指定用户
curl http://127.0.0.1:5000/api/users/1

# 创建新用户
curl -X POST http://127.0.0.1:5000/api/users \\
  -H "Content-Type: application/json" \\
  -d '{"username":"test","email":"test@example.com"}'

# 更新用户
curl -X PUT http://127.0.0.1:5000/api/users/1 \\
  -H "Content-Type: application/json" \\
  -d '{"username":"updated","email":"updated@example.com"}'

# 删除用户
curl -X DELETE http://127.0.0.1:5000/api/users/1</code></pre>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


# ============================================
# 用户 API
# ============================================

@app.route('/api/users', methods=['GET'])
def get_users():
    """GET /api/users - 获取所有用户"""
    # 支持分页
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_users = users_db[start:end]
    
    return api_response(
        data={
            'users': paginated_users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(users_db),
                'pages': (len(users_db) + per_page - 1) // per_page
            }
        },
        message='Users retrieved successfully'
    )


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET /api/users/:id - 获取指定用户"""
    user = next((u for u in users_db if u['id'] == user_id), None)
    
    if not user:
        return api_response(
            message=f'User {user_id} not found',
            status_code=404
        )
    
    return api_response(
        data={'user': user},
        message='User retrieved successfully'
    )


@app.route('/api/users', methods=['POST'])
@validate_json('username', 'email')
def create_user():
    """POST /api/users - 创建新用户"""
    global next_user_id
    data = request.get_json()
    
    # 验证用户名是否已存在
    if any(u['username'] == data['username'] for u in users_db):
        return api_response(
            message='Username already exists',
            errors={'username': 'This username is already taken'},
            status_code=400
        )
    
    # 创建新用户
    new_user = {
        'id': next_user_id,
        'username': data['username'],
        'email': data['email'],
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    next_user_id += 1
    
    users_db.append(new_user)
    
    return api_response(
        data={'user': new_user},
        message='User created successfully',
        status_code=201
    )


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """PUT /api/users/:id - 更新用户信息"""
    user = next((u for u in users_db if u['id'] == user_id), None)
    
    if not user:
        return api_response(
            message=f'User {user_id} not found',
            status_code=404
        )
    
    if not request.is_json:
        return api_response(
            message='Content-Type must be application/json',
            status_code=400
        )
    
    data = request.get_json()
    
    # 更新用户信息
    if 'username' in data:
        user['username'] = data['username']
    if 'email' in data:
        user['email'] = data['email']
    
    return api_response(
        data={'user': user},
        message='User updated successfully'
    )


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """DELETE /api/users/:id - 删除用户"""
    global users_db
    user = next((u for u in users_db if u['id'] == user_id), None)
    
    if not user:
        return api_response(
            message=f'User {user_id} not found',
            status_code=404
        )
    
    users_db = [u for u in users_db if u['id'] != user_id]
    
    return api_response(
        message='User deleted successfully',
        status_code=200
    )


# ============================================
# 文章 API
# ============================================

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """GET /api/posts - 获取所有文章"""
    return api_response(
        data={'posts': posts_db, 'total': len(posts_db)},
        message='Posts retrieved successfully'
    )


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """GET /api/posts/:id - 获取指定文章"""
    post = next((p for p in posts_db if p['id'] == post_id), None)
    
    if not post:
        return api_response(
            message=f'Post {post_id} not found',
            status_code=404
        )
    
    # 添加作者信息
    author = next((u for u in users_db if u['id'] == post['user_id']), None)
    post_with_author = post.copy()
    post_with_author['author'] = author
    
    return api_response(
        data={'post': post_with_author},
        message='Post retrieved successfully'
    )


@app.route('/api/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """GET /api/users/:id/posts - 获取指定用户的所有文章"""
    user = next((u for u in users_db if u['id'] == user_id), None)
    
    if not user:
        return api_response(
            message=f'User {user_id} not found',
            status_code=404
        )
    
    user_posts = [p for p in posts_db if p['user_id'] == user_id]
    
    return api_response(
        data={
            'user': user,
            'posts': user_posts,
            'total': len(user_posts)
        },
        message='User posts retrieved successfully'
    )


@app.route('/api/posts', methods=['POST'])
@validate_json('title', 'content', 'user_id')
def create_post():
    """POST /api/posts - 创建新文章"""
    global next_post_id
    data = request.get_json()
    
    # 验证用户是否存在
    user = next((u for u in users_db if u['id'] == data['user_id']), None)
    if not user:
        return api_response(
            message='User not found',
            errors={'user_id': f"User {data['user_id']} does not exist"},
            status_code=400
        )
    
    # 创建新文章
    new_post = {
        'id': next_post_id,
        'title': data['title'],
        'content': data['content'],
        'user_id': data['user_id'],
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    next_post_id += 1
    
    posts_db.append(new_post)
    
    return api_response(
        data={'post': new_post},
        message='Post created successfully',
        status_code=201
    )


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """PUT /api/posts/:id - 更新文章"""
    post = next((p for p in posts_db if p['id'] == post_id), None)
    
    if not post:
        return api_response(
            message=f'Post {post_id} not found',
            status_code=404
        )
    
    if not request.is_json:
        return api_response(
            message='Content-Type must be application/json',
            status_code=400
        )
    
    data = request.get_json()
    
    # 更新文章
    if 'title' in data:
        post['title'] = data['title']
    if 'content' in data:
        post['content'] = data['content']
    
    return api_response(
        data={'post': post},
        message='Post updated successfully'
    )


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """DELETE /api/posts/:id - 删除文章"""
    global posts_db
    post = next((p for p in posts_db if p['id'] == post_id), None)
    
    if not post:
        return api_response(
            message=f'Post {post_id} not found',
            status_code=404
        )
    
    posts_db = [p for p in posts_db if p['id'] != post_id]
    
    return api_response(
        message='Post deleted successfully'
    )


# ============================================
# 错误处理
# ============================================

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return api_response(
        message='Resource not found',
        errors={'url': request.url},
        status_code=404
    )


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return api_response(
        message='Internal server error',
        errors={'error': str(error)},
        status_code=500
    )


if __name__ == '__main__':
    print("🚀 Starting Flask RESTful API Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    print("\n📋 API Endpoints:")
    print("  GET    /api/users")
    print("  GET    /api/users/:id")
    print("  POST   /api/users")
    print("  PUT    /api/users/:id")
    print("  DELETE /api/users/:id")
    print("  GET    /api/posts")
    print("  GET    /api/posts/:id")
    print("  POST   /api/posts")
    app.run(debug=True, host='0.0.0.0', port=5000)

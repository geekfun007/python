"""
Flask 基础示例 2: 路由系统
Flask Basic Example 2: Routing System

演示 Flask 的路由功能，包括动态路由、类型转换器和 URL 构建。
Demonstrates Flask routing features including dynamic routes, converters, and URL building.
"""

from flask import Flask, url_for, redirect, request

app = Flask(__name__)


# ============================================
# 1. 基本路由 (Basic Routing)
# ============================================

@app.route('/')
def index():
    """首页 - 显示所有可用路由"""
    html = '<h1>Flask 路由示例 (Flask Routing Examples)</h1><ul>'
    html += '<li><a href="/user/John">动态路由: /user/John</a></li>'
    html += '<li><a href="/post/123">整数路由: /post/123</a></li>'
    html += '<li><a href="/path/folder/subfolder/file.txt">路径路由</a></li>'
    html += '<li><a href="/float/3.14">浮点数路由: /float/3.14</a></li>'
    html += '<li><a href="/redirect-example">重定向示例</a></li>'
    html += '<li><a href="/method-example">HTTP 方法示例</a></li>'
    html += '</ul>'
    return html


# ============================================
# 2. 动态路由 (Dynamic Routing)
# ============================================

@app.route('/user/<username>')
def show_user(username):
    """动态路由 - 字符串参数"""
    return f'''
        <h1>用户资料 (User Profile)</h1>
        <p>用户名 (Username): <strong>{username}</strong></p>
        <a href="/">返回首页 (Back to Home)</a>
    '''


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """
    类型转换器: int
    Type converter: int
    只接受整数，如 /post/123
    """
    return f'''
        <h1>文章详情 (Post Detail)</h1>
        <p>文章 ID (Post ID): <strong>{post_id}</strong></p>
        <p>类型 (Type): {type(post_id)}</p>
        <a href="/">返回首页 (Back to Home)</a>
    '''


@app.route('/float/<float:value>')
def show_float(value):
    """
    类型转换器: float
    Type converter: float
    接受浮点数，如 /float/3.14
    """
    return f'''
        <h1>浮点数示例 (Float Example)</h1>
        <p>值 (Value): <strong>{value}</strong></p>
        <p>平方 (Square): {value ** 2}</p>
        <a href="/">返回首页 (Back to Home)</a>
    '''


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    """
    类型转换器: path
    Type converter: path
    接受包含斜杠的路径，如 /path/folder/subfolder/file.txt
    """
    return f'''
        <h1>路径示例 (Path Example)</h1>
        <p>子路径 (Subpath): <strong>{subpath}</strong></p>
        <a href="/">返回首页 (Back to Home)</a>
    '''


@app.route('/uuid/<uuid:uuid_value>')
def show_uuid(uuid_value):
    """
    类型转换器: uuid
    Type converter: uuid
    接受 UUID 格式，如 /uuid/123e4567-e89b-12d3-a456-426614174000
    """
    return f'''
        <h1>UUID 示例 (UUID Example)</h1>
        <p>UUID: <strong>{uuid_value}</strong></p>
        <p>类型 (Type): {type(uuid_value)}</p>
        <a href="/">返回首页 (Back to Home)</a>
    '''


# ============================================
# 3. URL 构建 (URL Building)
# ============================================

@app.route('/url-building')
def url_building():
    """演示 url_for() 函数的使用"""
    return f'''
        <h1>URL 构建示例 (URL Building Example)</h1>
        <ul>
            <li>index: <code>{url_for('index')}</code></li>
            <li>show_user: <code>{url_for('show_user', username='Alice')}</code></li>
            <li>show_post: <code>{url_for('show_post', post_id=42)}</code></li>
            <li>show_float: <code>{url_for('show_float', value=3.14)}</code></li>
        </ul>
        <p>url_for() 的优势：</p>
        <ul>
            <li>URL 变更时自动更新</li>
            <li>自动处理特殊字符</li>
            <li>支持外部 URL 生成</li>
        </ul>
        <a href="/">返回首页 (Back to Home)</a>
    '''


# ============================================
# 4. 重定向 (Redirects)
# ============================================

@app.route('/redirect-example')
def redirect_example():
    """重定向到首页"""
    return redirect(url_for('index'))


@app.route('/old-page')
def old_page():
    """旧页面重定向到新页面"""
    return redirect(url_for('new_page'), code=301)  # 301 永久重定向


@app.route('/new-page')
def new_page():
    """新页面"""
    return '<h1>这是新页面 (This is the new page)</h1>'


# ============================================
# 5. HTTP 方法 (HTTP Methods)
# ============================================

@app.route('/method-example', methods=['GET', 'POST', 'PUT', 'DELETE'])
def method_example():
    """处理多种 HTTP 方法"""
    method = request.method
    
    responses = {
        'GET': '📖 GET 请求 - 读取数据',
        'POST': '📝 POST 请求 - 创建数据',
        'PUT': '✏️ PUT 请求 - 更新数据',
        'DELETE': '🗑️ DELETE 请求 - 删除数据'
    }
    
    return f'''
        <h1>HTTP 方法示例</h1>
        <p>当前方法 (Current Method): <strong>{method}</strong></p>
        <p>说明: {responses.get(method, '未知方法')}</p>
        <h3>测试命令 (Test Commands):</h3>
        <pre>
# GET
curl http://127.0.0.1:5000/method-example

# POST
curl -X POST http://127.0.0.1:5000/method-example

# PUT
curl -X PUT http://127.0.0.1:5000/method-example

# DELETE
curl -X DELETE http://127.0.0.1:5000/method-example
        </pre>
        <a href="/">返回首页 (Back to Home)</a>
    '''


# ============================================
# 6. 尾部斜杠 (Trailing Slash)
# ============================================

@app.route('/projects/')
def projects():
    """
    带尾部斜杠的路由
    访问 /projects 会自动重定向到 /projects/
    """
    return '<h1>项目列表 (Projects)</h1><p>URL 带尾部斜杠</p>'


@app.route('/about')
def about():
    """
    不带尾部斜杠的路由
    访问 /about/ 会返回 404
    """
    return '<h1>关于 (About)</h1><p>URL 不带尾部斜杠</p>'


# ============================================
# 7. 自定义错误页面 (Custom Error Pages)
# ============================================

@app.errorhandler(404)
def page_not_found(error):
    """404 错误处理"""
    return f'''
        <h1>404 - 页面未找到</h1>
        <p>抱歉，您访问的页面不存在。</p>
        <a href="/">返回首页</a>
    ''', 404


if __name__ == '__main__':
    print("🚀 Starting Flask Routing Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    
    # 显示所有注册的路由
    print("\n📋 注册的路由 (Registered Routes):")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint:30s} {rule.methods} {rule.rule}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

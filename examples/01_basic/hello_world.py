"""
Flask 基础示例 1: Hello World
Flask Basic Example 1: Hello World

这是最简单的 Flask 应用，演示了基本的路由和响应。
This is the simplest Flask application, demonstrating basic routing and response.
"""

from flask import Flask

# 创建 Flask 应用实例
# Create Flask application instance
app = Flask(__name__)


# 基本路由 - 根路径
# Basic route - root path
@app.route('/')
def hello():
    """返回简单的字符串响应"""
    return 'Hello, Flask! 你好，Flask！'


# 路由到 /hello
# Route to /hello
@app.route('/hello')
def hello_page():
    """返回 HTML 响应"""
    return '<h1>Hello, World!</h1><p>这是一个 HTML 响应</p>'


# 返回 JSON 响应
# Return JSON response
@app.route('/api/hello')
def hello_json():
    """返回 JSON 格式的响应"""
    return {
        'message': 'Hello, Flask!',
        'status': 'success',
        'data': {
            'greeting': '你好',
            'language': 'Chinese'
        }
    }


# 多种 HTTP 方法
# Multiple HTTP methods
@app.route('/hello/<name>')
def hello_name(name):
    """
    URL 参数示例
    URL parameter example
    
    访问 /hello/John 会显示 "Hello, John!"
    """
    return f'<h1>Hello, {name}!</h1>'


# 自定义状态码
# Custom status code
@app.route('/not-found')
def not_found():
    """返回自定义状态码"""
    return '这个资源不存在 (This resource does not exist)', 404


if __name__ == '__main__':
    # 运行开发服务器
    # Run development server
    # debug=True 启用调试模式和自动重载
    # debug=True enables debug mode and auto-reload
    print("🚀 Starting Flask application...")
    print("📍 访问 http://127.0.0.1:5000/")
    print("📍 Visit http://127.0.0.1:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)

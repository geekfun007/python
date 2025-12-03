"""
Flask 基础示例 4: 请求和响应处理
Flask Basic Example 4: Request and Response Handling

演示如何处理 HTTP 请求和构建响应。
Demonstrates how to handle HTTP requests and build responses.
"""

from flask import Flask, request, Response, jsonify, make_response, redirect, url_for
import json

app = Flask(__name__)


# ============================================
# 1. 请求对象 (Request Object)
# ============================================

@app.route('/')
def index():
    """首页 - 显示所有示例"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>请求和响应示例</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            a { color: #0066cc; text-decoration: none; display: block; margin: 10px 0; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Flask 请求和响应示例</h1>
        <h2>Request and Response Examples</h2>
        
        <h3>请求示例：</h3>
        <a href="/request-info">📋 请求信息 (Request Info)</a>
        <a href="/query-params?name=张三&age=28">🔍 查询参数 (Query Parameters)</a>
        <a href="/form-demo">📝 表单处理 (Form Handling)</a>
        <a href="/json-demo">📦 JSON 请求 (JSON Request)</a>
        <a href="/headers-demo">📬 请求头 (Headers)</a>
        <a href="/cookies-demo">🍪 Cookies</a>
        
        <h3>响应示例：</h3>
        <a href="/response-types">📤 响应类型 (Response Types)</a>
        <a href="/custom-response">⚙️ 自定义响应 (Custom Response)</a>
        <a href="/download">💾 文件下载 (File Download)</a>
    </body>
    </html>
    '''


@app.route('/request-info')
def request_info():
    """显示当前请求的详细信息"""
    info = {
        '请求方法 (Method)': request.method,
        '请求路径 (Path)': request.path,
        '完整 URL (Full URL)': request.url,
        '基础 URL (Base URL)': request.base_url,
        '主机 (Host)': request.host,
        '远程地址 (Remote Addr)': request.remote_addr,
        '用户代理 (User Agent)': request.user_agent.string,
        '是否 HTTPS (Is Secure)': request.is_secure,
    }
    
    html = '<html><head><style>body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }</style></head><body>'
    html += '<h1>请求信息 (Request Information)</h1>'
    html += '<table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">'
    
    for key, value in info.items():
        html += f'<tr><td><strong>{key}</strong></td><td>{value}</td></tr>'
    
    html += '</table>'
    html += '<p><a href="/">返回首页</a></p>'
    html += '</body></html>'
    
    return html


# ============================================
# 2. 查询参数 (Query Parameters)
# ============================================

@app.route('/query-params')
def query_params():
    """处理 URL 查询参数"""
    # 获取单个参数
    name = request.args.get('name', '未提供')
    age = request.args.get('age', type=int, default=0)
    
    # 获取所有参数
    all_params = request.args.to_dict()
    
    # 获取多个相同名称的参数
    tags = request.args.getlist('tag')
    
    return f'''
    <html>
    <head><style>body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }}</style></head>
    <body>
        <h1>查询参数示例 (Query Parameters)</h1>
        
        <h3>单个参数：</h3>
        <p>姓名 (Name): <strong>{name}</strong></p>
        <p>年龄 (Age): <strong>{age}</strong></p>
        
        <h3>所有参数：</h3>
        <pre>{json.dumps(all_params, indent=2, ensure_ascii=False)}</pre>
        
        <h3>多值参数 (tags)：</h3>
        <p>{tags}</p>
        
        <h3>测试 URL：</h3>
        <ul>
            <li><a href="/query-params?name=张三&age=28">基本参数</a></li>
            <li><a href="/query-params?name=李四&age=32&tag=python&tag=flask&tag=web">多值参数</a></li>
        </ul>
        
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''


# ============================================
# 3. 表单处理 (Form Handling)
# ============================================

@app.route('/form-demo', methods=['GET', 'POST'])
def form_demo():
    """处理 HTML 表单"""
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        message = request.form.get('message')
        newsletter = request.form.get('newsletter')  # 复选框
        
        return f'''
        <html>
        <head><style>body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }}</style></head>
        <body>
            <h1>表单提交成功 (Form Submitted)</h1>
            <h3>提交的数据：</h3>
            <p><strong>用户名:</strong> {username}</p>
            <p><strong>邮箱:</strong> {email}</p>
            <p><strong>消息:</strong> {message}</p>
            <p><strong>订阅:</strong> {'是' if newsletter else '否'}</p>
            <p><a href="/form-demo">返回表单</a> | <a href="/">返回首页</a></p>
        </body>
        </html>
        '''
    
    # GET 请求：显示表单
    return '''
    <html>
    <head>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            form { background: #f5f5f5; padding: 20px; border-radius: 5px; }
            label { display: block; margin: 10px 0 5px; }
            input, textarea { width: 100%; padding: 8px; box-sizing: border-box; }
            button { background: #0066cc; color: white; padding: 10px 20px; border: none; 
                     border-radius: 5px; cursor: pointer; margin-top: 10px; }
            button:hover { background: #0052a3; }
        </style>
    </head>
    <body>
        <h1>表单示例 (Form Example)</h1>
        
        <form method="POST">
            <label>用户名 (Username):</label>
            <input type="text" name="username" required>
            
            <label>邮箱 (Email):</label>
            <input type="email" name="email" required>
            
            <label>消息 (Message):</label>
            <textarea name="message" rows="5"></textarea>
            
            <label>
                <input type="checkbox" name="newsletter" value="yes">
                订阅新闻 (Subscribe to newsletter)
            </label>
            
            <button type="submit">提交 (Submit)</button>
        </form>
        
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''


# ============================================
# 4. JSON 请求和响应 (JSON Request/Response)
# ============================================

@app.route('/json-demo', methods=['GET', 'POST'])
def json_demo():
    """处理 JSON 数据"""
    if request.method == 'POST':
        # 获取 JSON 数据
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '无效的 JSON 数据'}), 400
        
        # 处理数据并返回 JSON 响应
        response = {
            'status': 'success',
            'message': '数据接收成功',
            'received_data': data,
            'timestamp': str(request.headers.get('Date', 'N/A'))
        }
        
        return jsonify(response)
    
    # GET 请求：显示说明和测试表单
    return '''
    <html>
    <head>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
            button { background: #0066cc; color: white; padding: 10px 20px; border: none; 
                     border-radius: 5px; cursor: pointer; margin: 10px 5px; }
            #response { margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>JSON 请求示例 (JSON Request Example)</h1>
        
        <h3>使用 curl 测试：</h3>
        <pre>curl -X POST http://127.0.0.1:5000/json-demo \\
  -H "Content-Type: application/json" \\
  -d '{"name":"张三","age":28,"city":"北京"}'</pre>
        
        <h3>使用 JavaScript 测试：</h3>
        <button onclick="sendJSON()">发送 JSON 数据</button>
        <div id="response"></div>
        
        <script>
        async function sendJSON() {
            const data = {
                name: '张三',
                age: 28,
                city: '北京',
                hobbies: ['编程', '阅读', '旅行']
            };
            
            try {
                const response = await fetch('/json-demo', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                document.getElementById('response').innerHTML = 
                    '<h3>响应:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('response').innerHTML = 
                    '<p style="color: red;">错误: ' + error + '</p>';
            }
        }
        </script>
        
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''


# ============================================
# 5. 请求头 (Headers)
# ============================================

@app.route('/headers-demo')
def headers_demo():
    """显示所有请求头"""
    headers = dict(request.headers)
    
    html = '<html><head><style>body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }</style></head><body>'
    html += '<h1>请求头 (Request Headers)</h1>'
    html += '<table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">'
    html += '<tr><th>Header Name</th><th>Value</th></tr>'
    
    for key, value in headers.items():
        html += f'<tr><td><strong>{key}</strong></td><td>{value}</td></tr>'
    
    html += '</table>'
    html += '<p><a href="/">返回首页</a></p>'
    html += '</body></html>'
    
    return html


# ============================================
# 6. Cookies
# ============================================

@app.route('/cookies-demo')
def cookies_demo():
    """Cookie 示例"""
    # 读取 Cookie
    visit_count = request.cookies.get('visit_count', type=int, default=0)
    username = request.cookies.get('username', '访客')
    
    # 创建响应并设置 Cookie
    response = make_response(f'''
    <html>
    <head><style>body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }}</style></head>
    <body>
        <h1>Cookie 示例</h1>
        <p>欢迎, <strong>{username}</strong>!</p>
        <p>您是第 <strong>{visit_count + 1}</strong> 次访问</p>
        
        <h3>当前 Cookies:</h3>
        <ul>
            <li>username: {username}</li>
            <li>visit_count: {visit_count}</li>
        </ul>
        
        <p><a href="/cookies-demo">刷新页面</a> | <a href="/clear-cookies">清除 Cookies</a> | <a href="/">返回首页</a></p>
    </body>
    </html>
    ''')
    
    # 设置新的 Cookie
    response.set_cookie('visit_count', str(visit_count + 1))
    response.set_cookie('username', username)
    
    return response


@app.route('/clear-cookies')
def clear_cookies():
    """清除 Cookies"""
    response = make_response(redirect(url_for('cookies_demo')))
    response.delete_cookie('visit_count')
    response.delete_cookie('username')
    return response


# ============================================
# 7. 响应类型 (Response Types)
# ============================================

@app.route('/response-types')
def response_types():
    """演示不同类型的响应"""
    response_type = request.args.get('type', 'html')
    
    if response_type == 'json':
        # JSON 响应
        return jsonify({
            'message': 'This is a JSON response',
            'data': {'key': 'value'}
        })
    
    elif response_type == 'text':
        # 纯文本响应
        return Response('This is plain text response', mimetype='text/plain')
    
    elif response_type == 'xml':
        # XML 响应
        xml_data = '''<?xml version="1.0" encoding="UTF-8"?>
        <response>
            <message>This is XML response</message>
            <status>success</status>
        </response>'''
        return Response(xml_data, mimetype='application/xml')
    
    elif response_type == 'csv':
        # CSV 响应
        csv_data = "Name,Age,City\n张三,28,北京\n李四,32,上海"
        return Response(csv_data, mimetype='text/csv',
                       headers={'Content-Disposition': 'attachment; filename=data.csv'})
    
    else:
        # HTML 响应 (默认)
        return '''
        <html>
        <head><style>body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }</style></head>
        <body>
            <h1>响应类型示例 (Response Types)</h1>
            <p>选择不同的响应类型：</p>
            <ul>
                <li><a href="/response-types?type=html">HTML 响应</a></li>
                <li><a href="/response-types?type=json">JSON 响应</a></li>
                <li><a href="/response-types?type=text">纯文本响应</a></li>
                <li><a href="/response-types?type=xml">XML 响应</a></li>
                <li><a href="/response-types?type=csv">CSV 响应</a></li>
            </ul>
            <p><a href="/">返回首页</a></p>
        </body>
        </html>
        '''


# ============================================
# 8. 自定义响应 (Custom Response)
# ============================================

@app.route('/custom-response')
def custom_response():
    """创建自定义响应对象"""
    # 方式 1: 直接返回响应对象
    # return Response('Custom response', status=200, mimetype='text/plain')
    
    # 方式 2: 使用 make_response
    response = make_response('<h1>Custom Response</h1>', 200)
    response.headers['X-Custom-Header'] = 'Custom Value'
    response.headers['X-Powered-By'] = 'Flask'
    
    return response


# ============================================
# 9. 文件下载 (File Download)
# ============================================

@app.route('/download')
def download():
    """提供文件下载"""
    # 创建文件内容
    content = '''Flask 文件下载示例
这是一个动态生成的文本文件。

Flask File Download Example
This is a dynamically generated text file.
'''
    
    # 创建响应
    response = Response(content, mimetype='text/plain')
    response.headers['Content-Disposition'] = 'attachment; filename=example.txt'
    
    return response


if __name__ == '__main__':
    print("🚀 Starting Flask Request/Response Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)

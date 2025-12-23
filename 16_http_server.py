"""
Python HTTP 服务器详解
包含：http.server、socketserver、Flask 基础等
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs


# ============================================
# 1. 简单 HTTP 服务器
# ============================================

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """简单的 HTTP 请求处理器"""
    
    def do_GET(self):
        """处理 GET 请求"""
        # 解析 URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # 路由
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>Hello, World!</h1>')
        
        elif path == '/api/hello':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'Hello from API'}
            self.wfile.write(json.dumps(response).encode())
        
        elif path == '/api/time':
            from datetime import datetime
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'time': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        """处理 POST 请求"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/api/echo':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                data = json.loads(post_data.decode())
                response = {'received': data}
                self.wfile.write(json.dumps(response).encode())
            except:
                self.send_error(400, 'Invalid JSON')
        
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[{self.address_string()}] {format % args}")


def simple_server_demo():
    """简单服务器演示"""
    print("\n=== 简单 HTTP 服务器 ===")
    print("""
    创建服务器:
    
    ```python
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print("服务器运行在 http://localhost:8000")
    server.serve_forever()
    ```
    
    访问:
    - http://localhost:8000/
    - http://localhost:8000/api/hello
    - http://localhost:8000/api/time
    
    POST 请求:
    curl -X POST http://localhost:8000/api/echo \\
         -H "Content-Type: application/json" \\
         -d '{"message": "Hello"}'
    """)


# ============================================
# 2. RESTful API 服务器
# ============================================

class RESTfulHandler(BaseHTTPRequestHandler):
    """RESTful API 处理器"""
    
    # 模拟数据库
    users = {
        1: {'id': 1, 'name': 'Alice', 'age': 25},
        2: {'id': 2, 'name': 'Bob', 'age': 30},
    }
    next_id = 3
    
    def send_json_response(self, status_code, data):
        """发送 JSON 响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        """GET - 获取资源"""
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/users':
            # 获取所有用户
            self.send_json_response(200, list(self.users.values()))
        
        elif parsed.path.startswith('/api/users/'):
            # 获取单个用户
            user_id = int(parsed.path.split('/')[-1])
            if user_id in self.users:
                self.send_json_response(200, self.users[user_id])
            else:
                self.send_json_response(404, {'error': 'User not found'})
        
        else:
            self.send_json_response(404, {'error': 'Not found'})
    
    def do_POST(self):
        """POST - 创建资源"""
        if self.path == '/api/users':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                user = {
                    'id': self.next_id,
                    'name': data['name'],
                    'age': data['age']
                }
                self.users[self.next_id] = user
                self.__class__.next_id += 1
                
                self.send_json_response(201, user)
            except:
                self.send_json_response(400, {'error': 'Invalid data'})
        else:
            self.send_json_response(404, {'error': 'Not found'})
    
    def do_PUT(self):
        """PUT - 更新资源"""
        if self.path.startswith('/api/users/'):
            user_id = int(self.path.split('/')[-1])
            
            if user_id in self.users:
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                
                try:
                    data = json.loads(put_data.decode())
                    self.users[user_id].update(data)
                    self.send_json_response(200, self.users[user_id])
                except:
                    self.send_json_response(400, {'error': 'Invalid data'})
            else:
                self.send_json_response(404, {'error': 'User not found'})
        else:
            self.send_json_response(404, {'error': 'Not found'})
    
    def do_DELETE(self):
        """DELETE - 删除资源"""
        if self.path.startswith('/api/users/'):
            user_id = int(self.path.split('/')[-1])
            
            if user_id in self.users:
                del self.users[user_id]
                self.send_json_response(204, {})
            else:
                self.send_json_response(404, {'error': 'User not found'})
        else:
            self.send_json_response(404, {'error': 'Not found'})


def restful_server_demo():
    """RESTful 服务器演示"""
    print("\n=== RESTful API 服务器 ===")
    print("""
    RESTful API 示例:
    
    GET /api/users          - 获取所有用户
    GET /api/users/1        - 获取用户1
    POST /api/users         - 创建用户
    PUT /api/users/1        - 更新用户1
    DELETE /api/users/1     - 删除用户1
    
    示例请求:
    
    # 获取所有用户
    curl http://localhost:8000/api/users
    
    # 创建用户
    curl -X POST http://localhost:8000/api/users \\
         -H "Content-Type: application/json" \\
         -d '{"name": "Charlie", "age": 35}'
    
    # 更新用户
    curl -X PUT http://localhost:8000/api/users/1 \\
         -H "Content-Type: application/json" \\
         -d '{"age": 26}'
    
    # 删除用户
    curl -X DELETE http://localhost:8000/api/users/1
    """)


# ============================================
# 3. 中间件模式
# ============================================

class MiddlewareHandler(BaseHTTPRequestHandler):
    """带中间件的处理器"""
    
    def __init__(self, *args, **kwargs):
        self.middlewares = [
            self.log_middleware,
            self.auth_middleware,
        ]
        super().__init__(*args, **kwargs)
    
    def log_middleware(self, request):
        """日志中间件"""
        print(f"[LOG] {request['method']} {request['path']}")
        return request
    
    def auth_middleware(self, request):
        """认证中间件"""
        auth_header = self.headers.get('Authorization')
        if not auth_header:
            return {'error': 'No authorization', 'status': 401}
        
        # 简单验证
        if auth_header != 'Bearer secret-token':
            return {'error': 'Invalid token', 'status': 401}
        
        return request
    
    def process_middlewares(self, request):
        """处理中间件"""
        for middleware in self.middlewares:
            result = middleware(request)
            if isinstance(result, dict) and 'error' in result:
                return result
            request = result
        return request
    
    def do_GET(self):
        """处理 GET 请求"""
        request = {'method': 'GET', 'path': self.path}
        result = self.process_middlewares(request)
        
        if isinstance(result, dict) and 'error' in result:
            self.send_response(result.get('status', 400))
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            return
        
        # 正常处理
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Success', 'path': self.path}
        self.wfile.write(json.dumps(response).encode())


def middleware_demo():
    """中间件演示"""
    print("\n=== 中间件模式 ===")
    print("""
    中间件处理流程:
    
    1. 日志中间件 - 记录请求
    2. 认证中间件 - 验证token
    3. 业务处理 - 处理请求
    
    示例:
    
    # 无 token (失败)
    curl http://localhost:8000/api/data
    
    # 有效 token (成功)
    curl http://localhost:8000/api/data \\
         -H "Authorization: Bearer secret-token"
    """)


# ============================================
# 4. 文件服务器
# ============================================

def file_server_demo():
    """文件服务器演示"""
    print("\n=== 文件服务器 ===")
    print("""
    使用内置文件服务器:
    
    ```python
    # 简单文件服务器
    python -m http.server 8000
    
    # 指定目录
    python -m http.server 8000 --directory /path/to/dir
    
    # 绑定地址
    python -m http.server 8000 --bind 0.0.0.0
    ```
    
    自定义文件服务器:
    
    ```python
    from http.server import SimpleHTTPRequestHandler, HTTPServer
    
    class MyFileHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory='/path/to/dir', **kwargs)
    
    server = HTTPServer(('localhost', 8000), MyFileHandler)
    server.serve_forever()
    ```
    """)


# ============================================
# 5. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 完整的 API 服务器示例
    print("""
    完整的 API 服务器示例:
    
    ```python
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json
    from urllib.parse import urlparse, parse_qs
    
    class APIHandler(BaseHTTPRequestHandler):
        # 存储数据
        data_store = {}
        
        def do_GET(self):
            parsed = urlparse(self.path)
            path = parsed.path
            params = parse_qs(parsed.query)
            
            if path == '/api/items':
                self.send_json(200, list(self.data_store.values()))
            elif path.startswith('/api/items/'):
                item_id = path.split('/')[-1]
                item = self.data_store.get(item_id)
                if item:
                    self.send_json(200, item)
                else:
                    self.send_json(404, {'error': 'Not found'})
            else:
                self.send_json(404, {'error': 'Not found'})
        
        def do_POST(self):
            if self.path == '/api/items':
                length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(length))
                
                item_id = str(len(self.data_store) + 1)
                item = {'id': item_id, **data}
                self.data_store[item_id] = item
                
                self.send_json(201, item)
        
        def send_json(self, status, data):
            self.send_response(status)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
    
    if __name__ == '__main__':
        server = HTTPServer(('localhost', 8000), APIHandler)
        print('Server running on http://localhost:8000')
        server.serve_forever()
    ```
    """)


# ============================================
# 6. 最佳实践
# ============================================

def best_practices():
    """最佳实践"""
    print("\n=== 最佳实践 ===")
    
    print("""
    HTTP 服务器最佳实践:
    
    1. 生产环境不要使用
       ✗ http.server (仅用于开发/测试)
       ✓ gunicorn, uwsgi (生产环境)
       ✓ nginx (反向代理)
    
    2. 使用 Web 框架
       - Flask: 轻量级
       - FastAPI: 现代、快速
       - Django: 全功能
    
    3. 错误处理
       - 捕获所有异常
       - 返回适当的状态码
       - 记录错误日志
    
    4. 安全性
       - 验证输入
       - 防止 SQL 注入
       - 使用 HTTPS
       - CORS 设置
    
    5. 日志记录
       - 请求日志
       - 错误日志
       - 性能监控
    
    6. 性能优化
       - 使用连接池
       - 缓存响应
       - 压缩内容
       - 异步处理
    
    7. API 设计
       - RESTful 原则
       - 版本控制
       - 文档化
       - 一致的响应格式
    
    8. 测试
       - 单元测试
       - 集成测试
       - 负载测试
    
    推荐框架:
    
    轻量级:
    - Flask
    - Bottle
    - web.py
    
    现代异步:
    - FastAPI
    - Sanic
    - aiohttp
    
    全功能:
    - Django
    - Pyramid
    
    下一步:
    查看 17_fastapi_demo/ 了解 FastAPI 实战
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python HTTP 服务器详解")
    print("=" * 60)
    
    simple_server_demo()
    restful_server_demo()
    middleware_demo()
    file_server_demo()
    practical_examples()
    best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)
    
    # 取消注释以运行服务器
    # print("\n启动服务器...")
    # server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    # print("服务器运行在 http://localhost:8000")
    # print("按 Ctrl+C 停止")
    # try:
    #     server.serve_forever()
    # except KeyboardInterrupt:
    #     print("\n服务器已停止")


if __name__ == "__main__":
    main()

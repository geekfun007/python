"""
Python HTTP 客户端详解
包含：requests、urllib、httpx、异步HTTP等
"""

import requests
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
import json


# ============================================
# 1. requests 基础
# ============================================

def requests_basics():
    """requests 基础"""
    print("\n=== requests 基础 ===")
    
    # GET 请求
    print("1. GET 请求:")
    try:
        response = requests.get('https://httpbin.org/get')
        print(f"  状态码: {response.status_code}")
        print(f"  内容类型: {response.headers['Content-Type']}")
        print(f"  响应大小: {len(response.content)} 字节")
    except requests.RequestException as e:
        print(f"  请求失败: {e}")
    
    # 带参数的 GET
    print("\n2. 带参数的 GET:")
    try:
        params = {'key1': 'value1', 'key2': 'value2'}
        response = requests.get('https://httpbin.org/get', params=params)
        data = response.json()
        print(f"  参数: {data.get('args')}")
    except:
        print("  请求失败")
    
    # POST 请求
    print("\n3. POST 请求:")
    try:
        data = {'username': 'alice', 'password': 'secret'}
        response = requests.post('https://httpbin.org/post', data=data)
        print(f"  状态码: {response.status_code}")
    except:
        print("  请求失败")
    
    # JSON POST
    print("\n4. JSON POST:")
    try:
        json_data = {'name': 'Alice', 'age': 25}
        response = requests.post('https://httpbin.org/post', json=json_data)
        result = response.json()
        print(f"  发送的JSON: {result.get('json')}")
    except:
        print("  请求失败")


def requests_advanced():
    """requests 高级功能"""
    print("\n=== requests 高级功能 ===")
    
    # 自定义请求头
    print("1. 自定义请求头:")
    try:
        headers = {
            'User-Agent': 'MyApp/1.0',
            'Accept': 'application/json'
        }
        response = requests.get('https://httpbin.org/headers', headers=headers)
        data = response.json()
        print(f"  User-Agent: {data['headers'].get('User-Agent')}")
    except:
        print("  请求失败")
    
    # 超时设置
    print("\n2. 超时设置:")
    try:
        response = requests.get('https://httpbin.org/delay/1', timeout=2)
        print(f"  请求成功: {response.status_code}")
    except requests.Timeout:
        print("  请求超时")
    except:
        print("  请求失败")
    
    # 重试机制
    print("\n3. 重试机制:")
    try:
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.get('https://httpbin.org/status/500')
        print(f"  状态码: {response.status_code}")
    except:
        print("  所有重试均失败")
    
    # Session 保持
    print("\n4. Session:")
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'MyApp/1.0'})
        
        # Cookie 会自动保持
        response = session.get('https://httpbin.org/cookies/set/sessionid/123456')
        response = session.get('https://httpbin.org/cookies')
        data = response.json()
        print(f"  Cookies: {data.get('cookies')}")
    except:
        print("  请求失败")
    
    # 文件上传
    print("\n5. 文件上传:")
    try:
        files = {'file': ('test.txt', 'file content', 'text/plain')}
        response = requests.post('https://httpbin.org/post', files=files)
        data = response.json()
        print(f"  文件已上传: {list(data.get('files', {}).keys())}")
    except:
        print("  上传失败")


def requests_error_handling():
    """requests 错误处理"""
    print("\n=== requests 错误处理 ===")
    
    # HTTP 错误
    print("1. HTTP 错误处理:")
    try:
        response = requests.get('https://httpbin.org/status/404')
        response.raise_for_status()  # 抛出 HTTPError
    except requests.HTTPError as e:
        print(f"  HTTP错误: {e}")
    except:
        pass
    
    # 连接错误
    print("\n2. 连接错误:")
    try:
        response = requests.get('http://invalid-domain-12345.com', timeout=2)
    except requests.ConnectionError as e:
        print(f"  连接错误: 无法连接")
    except:
        pass
    
    # 超时错误
    print("\n3. 超时错误:")
    try:
        response = requests.get('https://httpbin.org/delay/10', timeout=1)
    except requests.Timeout:
        print(f"  超时错误")
    except:
        pass


# ============================================
# 2. urllib - 标准库
# ============================================

def urllib_basics():
    """urllib 基础"""
    print("\n=== urllib 基础 ===")
    
    # GET 请求
    print("1. GET 请求:")
    try:
        with urllib.request.urlopen('https://httpbin.org/get') as response:
            data = response.read()
            print(f"  状态码: {response.status}")
            print(f"  响应大小: {len(data)} 字节")
    except:
        print("  请求失败")
    
    # 带参数的 GET
    print("\n2. 带参数的 GET:")
    try:
        params = {'key1': 'value1', 'key2': 'value2'}
        query_string = urllib.parse.urlencode(params)
        url = f'https://httpbin.org/get?{query_string}'
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            print(f"  参数: {data.get('args')}")
    except:
        print("  请求失败")
    
    # POST 请求
    print("\n3. POST 请求:")
    try:
        data = {'key': 'value'}
        data = urllib.parse.urlencode(data).encode('utf-8')
        
        req = urllib.request.Request('https://httpbin.org/post', data=data)
        with urllib.request.urlopen(req) as response:
            print(f"  状态码: {response.status}")
    except:
        print("  请求失败")
    
    # 自定义请求头
    print("\n4. 自定义请求头:")
    try:
        req = urllib.request.Request('https://httpbin.org/headers')
        req.add_header('User-Agent', 'MyApp/1.0')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(f"  User-Agent: {data['headers'].get('User-Agent')}")
    except:
        print("  请求失败")


# ============================================
# 3. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. API 客户端
    print("1. RESTful API 客户端:")
    
    class APIClient:
        """API 客户端"""
        def __init__(self, base_url):
            self.base_url = base_url
            self.session = requests.Session()
            self.session.headers.update({
                'Content-Type': 'application/json',
                'User-Agent': 'MyApp/1.0'
            })
        
        def get(self, endpoint, **kwargs):
            """GET 请求"""
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response.json()
        
        def post(self, endpoint, data=None, **kwargs):
            """POST 请求"""
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(url, json=data, **kwargs)
            response.raise_for_status()
            return response.json()
    
    try:
        client = APIClient('https://httpbin.org')
        
        # GET
        result = client.get('/get', params={'key': 'value'})
        print(f"  GET: {result.get('args')}")
        
        # POST
        result = client.post('/post', data={'name': 'Alice'})
        print(f"  POST: {result.get('json')}")
    except:
        print("  API 请求失败")
    
    # 2. 下载文件
    print("\n2. 下载文件:")
    
    def download_file(url, filename):
        """下载文件"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            print(f"  下载失败: {e}")
            return False
    
    success = download_file(
        'https://httpbin.org/bytes/1024',
        '/tmp/downloaded.bin'
    )
    if success:
        import os
        size = os.path.getsize('/tmp/downloaded.bin')
        print(f"  文件已下载: {size} 字节")
    
    # 3. 批量请求
    print("\n3. 批量请求:")
    
    urls = [
        'https://httpbin.org/delay/0.1',
        'https://httpbin.org/delay/0.1',
        'https://httpbin.org/delay/0.1',
    ]
    
    def fetch_all(urls):
        """批量获取"""
        results = []
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                results.append(response.status_code)
            except:
                results.append(None)
        return results
    
    try:
        import time
        start = time.time()
        results = fetch_all(urls)
        duration = time.time() - start
        print(f"  完成 {len(results)} 个请求，耗时 {duration:.2f}秒")
        print(f"  状态码: {results}")
    except:
        print("  批量请求失败")
    
    # 4. 认证
    print("\n4. 认证:")
    
    # Basic Auth
    try:
        from requests.auth import HTTPBasicAuth
        response = requests.get(
            'https://httpbin.org/basic-auth/user/pass',
            auth=HTTPBasicAuth('user', 'pass')
        )
        print(f"  Basic Auth: {response.status_code}")
    except:
        print("  认证失败")
    
    # Bearer Token
    try:
        headers = {'Authorization': 'Bearer mytoken123'}
        response = requests.get('https://httpbin.org/headers', headers=headers)
        data = response.json()
        print(f"  Bearer Token: {data['headers'].get('Authorization')}")
    except:
        print("  Token 认证失败")


# ============================================
# 4. 最佳实践
# ============================================

def best_practices():
    """最佳实践"""
    print("\n=== 最佳实践 ===")
    
    print("""
    HTTP 客户端最佳实践:
    
    1. 使用 requests 库
       - 比 urllib 更简单
       - 功能更强大
       - 社区支持好
    
    2. 设置超时
       ✓ requests.get(url, timeout=5)
       ✗ requests.get(url)  # 可能永久挂起
    
    3. 处理异常
       - requests.RequestException
       - requests.HTTPError
       - requests.ConnectionError
       - requests.Timeout
    
    4. 使用 Session
       - 保持连接
       - 共享 cookies
       - 共享配置
    
    5. 重试机制
       - 使用 Retry adapter
       - 指数退避
       - 限制重试次数
    
    6. 流式下载
       - stream=True
       - iter_content()
       - 节省内存
    
    7. 请求头
       - User-Agent
       - Accept
       - Authorization
    
    8. 连接池
       - Session 自动管理
       - 复用连接
       - 提高性能
    
    9. 证书验证
       - verify=True (默认)
       - 使用自签名证书时: verify='/path/to/cert'
    
    10. 异步请求
        - 使用 httpx
        - 或 aiohttp
        - 提高并发性能
    
    性能优化:
    - 使用连接池
    - 启用压缩
    - HTTP/2 支持
    - 缓存响应
    
    安全建议:
    - 验证 SSL 证书
    - 不要硬编码密码
    - 使用环境变量
    - 限制重定向次数
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python HTTP 客户端详解")
    print("=" * 60)
    
    print("\n注意：以下示例需要网络连接")
    print("=" * 60)
    
    try:
        requests_basics()
        requests_advanced()
        requests_error_handling()
        urllib_basics()
        practical_examples()
    except Exception as e:
        print(f"\n网络请求失败: {e}")
        print("请检查网络连接")
    
    best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

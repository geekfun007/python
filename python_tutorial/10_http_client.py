"""
Python HTTP 客户端详解 (with Type Hints)
========================================

本文件涵盖：
- urllib (标准库)
- requests (同步)
- httpx (同步 + 异步)
- aiohttp (异步)
"""

from typing import Any, TypedDict, cast
from dataclasses import dataclass
import json
import urllib.request
import urllib.parse
import urllib.error
from http.client import HTTPResponse
import asyncio

# ============================================================================
# 1. urllib (标准库)
# ============================================================================

class UrllibDemo:
    """urllib 演示（标准库）"""
    
    @staticmethod
    def basic_get() -> dict[str, Any]:
        """基本 GET 请求"""
        url = "https://httpbin.org/get"
        
        # 简单请求
        with urllib.request.urlopen(url) as response:
            resp: HTTPResponse = response
            
            # 响应信息
            print(f"Status: {resp.status}")
            print(f"Headers: {dict(resp.headers)}")
            
            # 读取响应体
            body = resp.read().decode('utf-8')
            data = json.loads(body)
            
        return data
    
    @staticmethod
    def get_with_params() -> dict[str, Any]:
        """带参数的 GET 请求"""
        base_url = "https://httpbin.org/get"
        params = {
            "name": "张三",
            "age": 30,
            "tags": ["python", "http"]
        }
        
        # URL 编码
        query_string = urllib.parse.urlencode(params, doseq=True)
        full_url = f"{base_url}?{query_string}"
        
        print(f"URL: {full_url}")
        
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        return data
    
    @staticmethod
    def post_request() -> dict[str, Any]:
        """POST 请求"""
        url = "https://httpbin.org/post"
        
        # JSON 数据
        payload = {
            "username": "testuser",
            "password": "secret123"
        }
        
        # 创建请求
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Python-urllib/3.x'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
    
    @staticmethod
    def error_handling() -> None:
        """错误处理"""
        try:
            urllib.request.urlopen("https://httpbin.org/status/404")
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            print(f"Response body: {e.read().decode()}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")


# ============================================================================
# 2. requests 库
# ============================================================================

# 注意: 需要安装 requests: pip install requests

class RequestsDemo:
    """requests 库演示"""
    
    @staticmethod
    def basic_get() -> dict[str, Any]:
        """基本 GET 请求"""
        try:
            import requests
        except ImportError:
            print("请安装 requests: pip install requests")
            return {}
        
        response = requests.get("https://httpbin.org/get")
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Encoding: {response.encoding}")
        
        # 自动解析 JSON
        return response.json()
    
    @staticmethod
    def get_with_params() -> dict[str, Any]:
        """带参数的 GET 请求"""
        try:
            import requests
        except ImportError:
            return {}
        
        params = {
            "name": "张三",
            "age": 30,
        }
        
        response = requests.get(
            "https://httpbin.org/get",
            params=params,
            headers={"Accept-Language": "zh-CN"}
        )
        
        print(f"Request URL: {response.url}")
        return response.json()
    
    @staticmethod
    def post_json() -> dict[str, Any]:
        """POST JSON 数据"""
        try:
            import requests
        except ImportError:
            return {}
        
        payload = {
            "title": "测试文章",
            "content": "这是内容",
            "tags": ["python", "http"]
        }
        
        response = requests.post(
            "https://httpbin.org/post",
            json=payload  # 自动序列化为 JSON
        )
        
        return response.json()
    
    @staticmethod
    def post_form() -> dict[str, Any]:
        """POST 表单数据"""
        try:
            import requests
        except ImportError:
            return {}
        
        data = {
            "username": "testuser",
            "password": "secret"
        }
        
        response = requests.post(
            "https://httpbin.org/post",
            data=data  # 自动编码为表单数据
        )
        
        return response.json()
    
    @staticmethod
    def upload_file() -> dict[str, Any]:
        """上传文件"""
        try:
            import requests
        except ImportError:
            return {}
        
        from io import BytesIO
        
        # 模拟文件
        file_content = b"This is file content"
        files = {
            'file': ('test.txt', BytesIO(file_content), 'text/plain')
        }
        
        response = requests.post(
            "https://httpbin.org/post",
            files=files,
            data={"description": "Test file upload"}
        )
        
        return response.json()
    
    @staticmethod
    def session_usage() -> None:
        """使用 Session（保持连接和 cookies）"""
        try:
            import requests
        except ImportError:
            return
        
        with requests.Session() as session:
            # 设置默认头
            session.headers.update({
                "User-Agent": "MyApp/1.0"
            })
            
            # 第一次请求，设置 cookie
            session.get("https://httpbin.org/cookies/set/session_id/abc123")
            
            # 后续请求自动携带 cookie
            response = session.get("https://httpbin.org/cookies")
            print(f"Cookies: {response.json()}")
    
    @staticmethod
    def timeout_and_retry() -> None:
        """超时和重试"""
        try:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
        except ImportError:
            return
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        
        with requests.Session() as session:
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            
            try:
                response = session.get(
                    "https://httpbin.org/get",
                    timeout=(3.0, 10.0)  # (连接超时, 读取超时)
                )
                print(f"Success: {response.status_code}")
            except requests.exceptions.Timeout:
                print("Request timed out")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")


# ============================================================================
# 3. httpx (同步 + 异步)
# ============================================================================

# 注意: 需要安装 httpx: pip install httpx

class HttpxSyncDemo:
    """httpx 同步演示"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        try:
            import httpx
        except ImportError:
            print("请安装 httpx: pip install httpx")
            return
        
        # GET 请求
        response = httpx.get("https://httpbin.org/get")
        print(f"GET Status: {response.status_code}")
        
        # POST 请求
        response = httpx.post(
            "https://httpbin.org/post",
            json={"key": "value"}
        )
        print(f"POST Status: {response.status_code}")
        
        # 使用客户端（连接复用）
        with httpx.Client(base_url="https://httpbin.org") as client:
            r1 = client.get("/get")
            r2 = client.post("/post", json={"data": "test"})
            print(f"Client requests: {r1.status_code}, {r2.status_code}")


class HttpxAsyncDemo:
    """httpx 异步演示"""
    
    @staticmethod
    async def basic_operations() -> None:
        """基本异步操作"""
        try:
            import httpx
        except ImportError:
            print("请安装 httpx: pip install httpx")
            return
        
        # 单个异步请求
        async with httpx.AsyncClient() as client:
            response = await client.get("https://httpbin.org/get")
            print(f"Async GET: {response.status_code}")
    
    @staticmethod
    async def concurrent_requests() -> None:
        """并发请求"""
        try:
            import httpx
        except ImportError:
            return
        
        urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/ip",
            "https://httpbin.org/user-agent",
        ]
        
        async with httpx.AsyncClient() as client:
            # 并发发送所有请求
            tasks = [client.get(url) for url in urls]
            responses = await asyncio.gather(*tasks)
            
            for url, response in zip(urls, responses):
                print(f"{url}: {response.status_code}")
    
    @staticmethod
    async def streaming() -> None:
        """流式响应"""
        try:
            import httpx
        except ImportError:
            return
        
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", "https://httpbin.org/stream/3") as response:
                print("Streaming response:")
                async for line in response.aiter_lines():
                    print(f"  {line[:50]}...")


# ============================================================================
# 4. aiohttp (异步专用)
# ============================================================================

# 注意: 需要安装 aiohttp: pip install aiohttp

class AiohttpDemo:
    """aiohttp 演示"""
    
    @staticmethod
    async def basic_get() -> dict[str, Any]:
        """基本 GET 请求"""
        try:
            import aiohttp
        except ImportError:
            print("请安装 aiohttp: pip install aiohttp")
            return {}
        
        async with aiohttp.ClientSession() as session:
            async with session.get("https://httpbin.org/get") as response:
                print(f"Status: {response.status}")
                print(f"Content-Type: {response.content_type}")
                return await response.json()
    
    @staticmethod
    async def post_json() -> dict[str, Any]:
        """POST JSON"""
        try:
            import aiohttp
        except ImportError:
            return {}
        
        payload = {"key": "value", "number": 42}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://httpbin.org/post",
                json=payload
            ) as response:
                return await response.json()
    
    @staticmethod
    async def concurrent_requests() -> list[dict[str, Any]]:
        """并发请求"""
        try:
            import aiohttp
        except ImportError:
            return []
        
        urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/ip",
            "https://httpbin.org/headers",
        ]
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(asyncio.create_task(
                    AiohttpDemo._fetch(session, url)
                ))
            
            results = await asyncio.gather(*tasks)
            return results
    
    @staticmethod
    async def _fetch(session: Any, url: str) -> dict[str, Any]:
        """辅助函数：获取 URL"""
        async with session.get(url) as response:
            return await response.json()
    
    @staticmethod
    async def with_timeout() -> None:
        """带超时的请求"""
        try:
            import aiohttp
        except ImportError:
            return
        
        timeout = aiohttp.ClientTimeout(total=10)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.get("https://httpbin.org/delay/2") as response:
                    print(f"Response: {response.status}")
            except asyncio.TimeoutError:
                print("Request timed out")
    
    @staticmethod
    async def connection_pool() -> None:
        """连接池"""
        try:
            import aiohttp
        except ImportError:
            return
        
        # 配置连接池
        connector = aiohttp.TCPConnector(
            limit=100,        # 总连接数限制
            limit_per_host=10  # 每个主机连接数限制
        )
        
        async with aiohttp.ClientSession(connector=connector) as session:
            # 并发请求会复用连接
            tasks = [
                session.get("https://httpbin.org/get")
                for _ in range(5)
            ]
            responses = await asyncio.gather(*tasks)
            
            for i, response in enumerate(responses):
                await response.read()
                response.close()
                print(f"Request {i}: {response.status}")


# ============================================================================
# 5. HTTP 客户端最佳实践
# ============================================================================

class HttpClientBestPractices:
    """HTTP 客户端最佳实践"""
    
    @staticmethod
    def create_api_client() -> None:
        """创建 API 客户端"""
        try:
            import httpx
        except ImportError:
            print("需要 httpx")
            return
        
        class APIClient:
            """API 客户端封装"""
            
            def __init__(
                self,
                base_url: str,
                api_key: str | None = None,
                timeout: float = 30.0
            ) -> None:
                self.base_url = base_url
                self.api_key = api_key
                self.timeout = timeout
                self._client: httpx.Client | None = None
            
            def __enter__(self) -> "APIClient":
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                self._client = httpx.Client(
                    base_url=self.base_url,
                    headers=headers,
                    timeout=self.timeout,
                )
                return self
            
            def __exit__(self, *args: Any) -> None:
                if self._client:
                    self._client.close()
            
            def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
                if not self._client:
                    raise RuntimeError("Client not initialized")
                
                response = self._client.get(path, **kwargs)
                response.raise_for_status()
                return response.json()
            
            def post(self, path: str, data: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
                if not self._client:
                    raise RuntimeError("Client not initialized")
                
                response = self._client.post(path, json=data, **kwargs)
                response.raise_for_status()
                return response.json()
        
        # 使用示例
        with APIClient("https://httpbin.org") as client:
            result = client.get("/get", params={"test": "value"})
            print(f"API GET result: {result.get('args')}")
    
    @staticmethod
    async def create_async_api_client() -> None:
        """创建异步 API 客户端"""
        try:
            import httpx
        except ImportError:
            return
        
        class AsyncAPIClient:
            """异步 API 客户端"""
            
            def __init__(self, base_url: str) -> None:
                self.base_url = base_url
                self._client: httpx.AsyncClient | None = None
            
            async def __aenter__(self) -> "AsyncAPIClient":
                self._client = httpx.AsyncClient(base_url=self.base_url)
                return self
            
            async def __aexit__(self, *args: Any) -> None:
                if self._client:
                    await self._client.aclose()
            
            async def get(self, path: str) -> dict[str, Any]:
                if not self._client:
                    raise RuntimeError("Client not initialized")
                response = await self._client.get(path)
                response.raise_for_status()
                return response.json()
        
        # 使用
        async with AsyncAPIClient("https://httpbin.org") as client:
            result = await client.get("/get")
            print(f"Async API result: {result.get('url')}")


# ============================================================================
# 演示运行
# ============================================================================

def run_sync_demos() -> None:
    """运行同步演示"""
    print("=" * 60)
    print("URLLIB DEMO")
    print("=" * 60)
    
    print("\n--- Basic GET ---")
    try:
        result = UrllibDemo.basic_get()
        print(f"Result URL: {result.get('url')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n--- GET with Params ---")
    try:
        result = UrllibDemo.get_with_params()
        print(f"Args: {result.get('args')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n--- POST Request ---")
    try:
        result = UrllibDemo.post_request()
        print(f"JSON received: {result.get('json')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n--- Error Handling ---")
    UrllibDemo.error_handling()
    
    print("\n" + "=" * 60)
    print("REQUESTS DEMO")
    print("=" * 60)
    
    print("\n--- Basic GET ---")
    result = RequestsDemo.basic_get()
    if result:
        print(f"Result URL: {result.get('url')}")
    
    print("\n--- POST JSON ---")
    result = RequestsDemo.post_json()
    if result:
        print(f"JSON received: {result.get('json')}")
    
    print("\n--- Session Usage ---")
    RequestsDemo.session_usage()
    
    print("\n" + "=" * 60)
    print("HTTPX SYNC DEMO")
    print("=" * 60)
    
    HttpxSyncDemo.basic_operations()
    
    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)
    
    HttpClientBestPractices.create_api_client()


async def run_async_demos() -> None:
    """运行异步演示"""
    print("\n" + "=" * 60)
    print("HTTPX ASYNC DEMO")
    print("=" * 60)
    
    print("\n--- Basic Operations ---")
    await HttpxAsyncDemo.basic_operations()
    
    print("\n--- Concurrent Requests ---")
    await HttpxAsyncDemo.concurrent_requests()
    
    print("\n" + "=" * 60)
    print("AIOHTTP DEMO")
    print("=" * 60)
    
    print("\n--- Basic GET ---")
    result = await AiohttpDemo.basic_get()
    if result:
        print(f"Result URL: {result.get('url')}")
    
    print("\n--- Concurrent Requests ---")
    results = await AiohttpDemo.concurrent_requests()
    print(f"Got {len(results)} responses")
    
    print("\n--- Async API Client ---")
    await HttpClientBestPractices.create_async_api_client()


def main() -> None:
    """主函数"""
    run_sync_demos()
    asyncio.run(run_async_demos())


if __name__ == "__main__":
    main()

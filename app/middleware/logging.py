"""
Logging Middleware
日志中间件 - 记录所有请求和响应

中间件原理：
1. 中间件在请求到达路由处理函数之前执行
2. 可以修改请求和响应
3. 按照添加顺序依次执行
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    日志中间件
    
    记录每个请求的：
    - 请求方法和路径
    - 处理时间
    - 响应状态码
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        处理请求
        
        原理：
        1. call_next(request) 调用下一个中间件或路由处理函数
        2. 在调用前后可以执行自定义逻辑
        3. 必须返回Response对象
        """
        # 记录请求开始时间
        start_time = time.time()
        
        # 记录请求信息
        logger.info(f"请求开始: {request.method} {request.url.path}")
        
        # 调用下一个中间件或路由处理函数
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录响应信息
        logger.info(
            f"请求完成: {request.method} {request.url.path} "
            f"- 状态码: {response.status_code} "
            f"- 耗时: {process_time:.3f}秒"
        )
        
        # 添加自定义响应头
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

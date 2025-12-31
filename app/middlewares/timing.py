"""
计时中间件
记录请求处理时间
"""
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):
    """
    计时中间件
    
    记录每个请求的处理时间，并添加到响应头中
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # 记录开始时间
        start_time = time.perf_counter()
        
        # 处理请求
        response = await call_next(request)
        
        # 计算处理时间（毫秒）
        process_time_ms = (time.perf_counter() - start_time) * 1000
        
        # 添加到响应头
        response.headers["X-Response-Time"] = f"{process_time_ms:.2f}ms"
        
        return response

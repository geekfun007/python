"""
日志中间件
记录请求和响应日志
"""
import time
from typing import Callable

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    日志中间件
    
    记录每个请求的详细信息，包括:
    - 请求方法和路径
    - 请求头
    - 响应状态码
    - 处理时间
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # 获取请求信息
        request_id = request.headers.get("X-Request-ID", "-")
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        url = str(request.url)
        user_agent = request.headers.get("User-Agent", "-")
        
        # 记录请求开始
        logger.info(
            f"Request started | "
            f"request_id={request_id} | "
            f"method={method} | "
            f"url={url} | "
            f"client_ip={client_ip} | "
            f"user_agent={user_agent}"
        )
        
        # 记录开始时间
        start_time = time.perf_counter()
        
        # 处理请求
        try:
            response = await call_next(request)
        except Exception as e:
            # 记录异常
            process_time = time.perf_counter() - start_time
            logger.error(
                f"Request failed | "
                f"request_id={request_id} | "
                f"method={method} | "
                f"url={url} | "
                f"error={str(e)} | "
                f"process_time={process_time:.4f}s"
            )
            raise
        
        # 计算处理时间
        process_time = time.perf_counter() - start_time
        
        # 记录请求完成
        logger.info(
            f"Request completed | "
            f"request_id={request_id} | "
            f"method={method} | "
            f"url={url} | "
            f"status_code={response.status_code} | "
            f"process_time={process_time:.4f}s"
        )
        
        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        
        return response

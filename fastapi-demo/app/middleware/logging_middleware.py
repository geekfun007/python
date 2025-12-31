"""
Logging Middleware
请求日志中间件
"""

import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    请求日志中间件
    
    功能:
    - 为每个请求生成唯一的 request_id
    - 记录请求的方法、路径、状态码、耗时
    - 记录客户端 IP 和 User-Agent
    
    日志格式:
        [request_id] METHOD /path - status_code - duration_ms
    """
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # 生成请求ID
        request_id = str(uuid.uuid4())[:8]
        
        # 记录请求开始时间
        start_time = time.time()
        
        # 获取客户端信息
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "unknown")
        
        # 将 request_id 添加到请求状态
        request.state.request_id = request_id
        
        # 记录请求开始
        logger.info(
            f"[{request_id}] Started {request.method} {request.url.path} "
            f"- IP: {client_ip}"
        )
        
        try:
            # 处理请求
            response = await call_next(request)
            
            # 计算处理时间
            process_time = (time.time() - start_time) * 1000
            
            # 添加响应头
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            
            # 记录请求完成
            log_level = "info" if response.status_code < 400 else "warning"
            getattr(logger, log_level)(
                f"[{request_id}] Completed {request.method} {request.url.path} "
                f"- {response.status_code} - {process_time:.2f}ms"
            )
            
            return response
            
        except Exception as e:
            # 计算处理时间
            process_time = (time.time() - start_time) * 1000
            
            # 记录错误
            logger.error(
                f"[{request_id}] Failed {request.method} {request.url.path} "
                f"- {process_time:.2f}ms - Error: {str(e)}"
            )
            raise
    
    def _get_client_ip(self, request: Request) -> str:
        """
        获取客户端真实 IP
        支持代理转发的情况
        """
        # 尝试从 X-Forwarded-For 获取
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        # 尝试从 X-Real-IP 获取
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # 使用直接连接的客户端 IP
        if request.client:
            return request.client.host
        
        return "unknown"

"""
请求ID中间件
为每个请求生成唯一ID
"""
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    请求ID中间件
    
    为每个请求生成或获取唯一的请求ID，用于:
    - 日志追踪
    - 分布式追踪
    - 问题排查
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # 获取或生成请求ID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # 将请求ID存储在request.state中，方便后续使用
        request.state.request_id = request_id
        
        # 处理请求
        response = await call_next(request)
        
        # 在响应头中返回请求ID
        response.headers["X-Request-ID"] = request_id
        
        return response


def get_request_id(request: Request) -> str:
    """
    获取当前请求的ID
    
    Args:
        request: 请求对象
    
    Returns:
        请求ID
    """
    return getattr(request.state, "request_id", str(uuid.uuid4()))

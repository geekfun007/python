"""
Rate Limiter Middleware
请求限流中间件
"""

import time
from typing import Dict, Optional, Callable
from collections import defaultdict
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    简单的内存限流中间件
    
    功能:
    - 基于 IP 的请求限流
    - 滑动窗口算法
    - 可配置限流规则
    
    注意:
    - 此实现仅适用于单实例部署
    - 生产环境建议使用 Redis 实现分布式限流
    
    使用:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=60,
            exclude_paths=["/health", "/docs"]
        )
    """
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_second: int = 10,
        exclude_paths: list = None,
        whitelist_ips: list = None,
    ):
        """
        初始化限流中间件
        
        Args:
            app: FastAPI 应用
            requests_per_minute: 每分钟最大请求数
            requests_per_second: 每秒最大请求数
            exclude_paths: 排除的路径列表
            whitelist_ips: 白名单 IP 列表
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_second = requests_per_second
        self.exclude_paths = exclude_paths or ["/health", "/docs", "/redoc", "/openapi.json"]
        self.whitelist_ips = whitelist_ips or ["127.0.0.1"]
        
        # 请求记录 {ip: [(timestamp, count), ...]}
        self.request_records: Dict[str, list] = defaultdict(list)
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # 检查是否是排除的路径
        if self._is_excluded_path(request.url.path):
            return await call_next(request)
        
        # 获取客户端 IP
        client_ip = self._get_client_ip(request)
        
        # 检查是否在白名单
        if client_ip in self.whitelist_ips:
            return await call_next(request)
        
        # 检查限流
        if not self._is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "code": 429,
                    "message": "请求过于频繁，请稍后重试",
                    "detail": None
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                }
            )
        
        # 记录请求
        self._record_request(client_ip)
        
        # 处理请求
        response = await call_next(request)
        
        # 添加限流信息到响应头
        remaining = self._get_remaining_requests(client_ip)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
    
    def _is_excluded_path(self, path: str) -> bool:
        """检查路径是否被排除"""
        for excluded in self.exclude_paths:
            if path.startswith(excluded):
                return True
        return False
    
    def _get_client_ip(self, request: Request) -> str:
        """获取客户端 IP"""
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _is_allowed(self, client_ip: str) -> bool:
        """检查请求是否允许"""
        now = time.time()
        records = self.request_records[client_ip]
        
        # 清理过期记录（1分钟前的）
        cutoff_minute = now - 60
        self.request_records[client_ip] = [
            r for r in records if r > cutoff_minute
        ]
        
        # 检查每分钟限制
        if len(self.request_records[client_ip]) >= self.requests_per_minute:
            return False
        
        # 检查每秒限制
        cutoff_second = now - 1
        recent_requests = [
            r for r in self.request_records[client_ip] if r > cutoff_second
        ]
        if len(recent_requests) >= self.requests_per_second:
            return False
        
        return True
    
    def _record_request(self, client_ip: str):
        """记录请求"""
        self.request_records[client_ip].append(time.time())
    
    def _get_remaining_requests(self, client_ip: str) -> int:
        """获取剩余请求数"""
        return max(0, self.requests_per_minute - len(self.request_records[client_ip]))


class TokenBucketRateLimiter:
    """
    令牌桶限流算法实现
    
    可用于更精细的限流控制
    
    Example:
        limiter = TokenBucketRateLimiter(
            rate=10,  # 每秒生成10个令牌
            capacity=100  # 桶容量100
        )
        
        if limiter.consume("user_123"):
            # 处理请求
            pass
        else:
            # 拒绝请求
            pass
    """
    
    def __init__(self, rate: float, capacity: int):
        """
        初始化令牌桶
        
        Args:
            rate: 令牌生成速率（每秒）
            capacity: 桶容量
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens: Dict[str, float] = {}
        self.last_time: Dict[str, float] = {}
    
    def consume(self, key: str, tokens: int = 1) -> bool:
        """
        尝试消费令牌
        
        Args:
            key: 标识符（如用户ID或IP）
            tokens: 需要消费的令牌数
        
        Returns:
            是否成功消费
        """
        now = time.time()
        
        # 初始化
        if key not in self.tokens:
            self.tokens[key] = self.capacity
            self.last_time[key] = now
        
        # 计算新增的令牌
        time_passed = now - self.last_time[key]
        self.tokens[key] = min(
            self.capacity,
            self.tokens[key] + time_passed * self.rate
        )
        self.last_time[key] = now
        
        # 尝试消费
        if self.tokens[key] >= tokens:
            self.tokens[key] -= tokens
            return True
        
        return False
    
    def get_tokens(self, key: str) -> float:
        """获取当前令牌数"""
        return self.tokens.get(key, self.capacity)

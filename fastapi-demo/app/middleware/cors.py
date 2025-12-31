"""
CORS Middleware
跨域资源共享中间件
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def setup_cors(app: FastAPI):
    """
    设置 CORS 中间件
    
    CORS (Cross-Origin Resource Sharing) 允许浏览器向不同源的服务器发送请求。
    
    配置项:
    - allow_origins: 允许的源列表，["*"] 表示允许所有源
    - allow_credentials: 是否允许携带凭据（cookies 等）
    - allow_methods: 允许的 HTTP 方法
    - allow_headers: 允许的请求头
    
    注意:
    - 生产环境不建议使用 ["*"] 作为 allow_origins
    - 当 allow_credentials=True 时，allow_origins 不能是 ["*"]
    """
    
    # 获取配置
    origins = settings.CORS_ORIGINS
    
    # 如果允许凭据且源是 *，需要特殊处理
    if settings.CORS_ALLOW_CREDENTIALS and "*" in origins:
        # 生产环境应该明确指定允许的源
        origins = [
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:8080",
            "http://127.0.0.1",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8080",
        ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
        expose_headers=[
            "X-Request-ID",
            "X-Process-Time",
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
        ],
        max_age=600,  # 预检请求缓存时间（秒）
    )


def get_cors_config() -> dict:
    """
    获取 CORS 配置（用于自定义配置）
    
    Returns:
        CORS 配置字典
    """
    return {
        "allow_origins": settings.CORS_ORIGINS,
        "allow_credentials": settings.CORS_ALLOW_CREDENTIALS,
        "allow_methods": settings.CORS_ALLOW_METHODS,
        "allow_headers": settings.CORS_ALLOW_HEADERS,
    }

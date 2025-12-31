"""
FastAPI Application Entry Point
应用主入口
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from loguru import logger
import sys

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1 import api_router
from app.middleware import (
    LoggingMiddleware,
    setup_exception_handlers,
    RateLimitMiddleware,
    setup_cors,
)
from app.middleware.error_handler import setup_business_exception_handler


# 配置 loguru 日志
logger.remove()  # 移除默认处理器
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>",
    level="DEBUG" if settings.DEBUG else "INFO",
)
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level="INFO",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    
    启动时:
    - 初始化数据库连接
    - 执行启动任务
    
    关闭时:
    - 关闭数据库连接
    - 清理资源
    """
    logger.info("Application starting up...")
    
    # 启动时初始化
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    yield
    
    # 关闭时清理
    logger.info("Application shutting down...")
    await close_db()
    logger.info("Database connection closed")


def create_application() -> FastAPI:
    """
    创建 FastAPI 应用实例
    
    Returns:
        FastAPI 应用实例
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="""
## FastAPI 示例项目

这是一个完整的 FastAPI 项目示例，包含：

- 🔐 **用户认证**: JWT Token 认证
- 👤 **用户管理**: 用户注册、登录、信息管理
- 📝 **文章管理**: 文章 CRUD、发布、草稿
- 💬 **评论系统**: 评论、回复
- 👍 **互动功能**: 点赞、收藏
- 🏷️ **分类标签**: 文章分类和标签

### 认证方式

使用 Bearer Token 认证，在 Swagger UI 中点击 **Authorize** 按钮输入令牌。

### API 版本

当前版本: v1

所有 API 路径以 `/api/v1` 开头。
        """,
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # 设置 CORS
    setup_cors(app)
    
    # 添加中间件（注意顺序：后添加的先执行）
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=60,
        requests_per_second=10,
    )
    app.add_middleware(LoggingMiddleware)
    
    # 设置异常处理器
    setup_exception_handlers(app)
    setup_business_exception_handler(app)
    
    # 注册路由
    app.include_router(api_router, prefix="/api/v1")
    
    # 健康检查端点
    @app.get("/health", tags=["健康检查"])
    async def health_check():
        """
        健康检查
        
        用于负载均衡器或 Kubernetes 探针
        """
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
        }
    
    # 根路径
    @app.get("/", tags=["根路径"])
    async def root():
        """
        API 根路径
        
        返回 API 基本信息
        """
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs" if settings.DEBUG else "disabled",
            "api": "/api/v1",
        }
    
    return app


# 创建应用实例
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
    )

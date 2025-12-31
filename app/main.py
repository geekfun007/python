"""
FastAPI 应用入口
配置应用、中间件和路由
"""
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api import api_router
from app.core.config import settings
from app.db.session import close_db, init_db
from app.middlewares import (
    LoggingMiddleware,
    RequestIDMiddleware,
    TimingMiddleware,
)


def setup_logging() -> None:
    """配置日志"""
    # 移除默认处理器
    logger.remove()
    
    # 添加控制台处理器
    logger.add(
        sys.stdout,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        colorize=True,
    )
    
    # 添加文件处理器
    logger.add(
        "logs/app.log",
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    应用生命周期管理
    
    启动时初始化数据库连接
    关闭时释放资源
    """
    # 启动时
    logger.info("Starting application...")
    setup_logging()
    
    # 初始化数据库
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    yield
    
    # 关闭时
    logger.info("Shutting down application...")
    await close_db()
    logger.info("Database connection closed")


def create_app() -> FastAPI:
    """
    创建 FastAPI 应用实例
    
    Returns:
        FastAPI 应用实例
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
## FastAPI 实战项目

这是一个完整的 FastAPI 实战项目，包含以下功能：

- 🔐 用户认证（JWT）
- 👤 用户管理
- 📦 物品管理
- 📝 完整的 CRUD 操作
- 🔍 搜索和分页
- 📊 日志记录
- 🐳 Docker 部署

### 技术栈

- FastAPI
- SQLAlchemy (异步)
- PostgreSQL
- Redis
- Docker & Docker Compose
- Nginx
        """,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    
    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 添加自定义中间件（顺序很重要，先添加的后执行）
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestIDMiddleware)
    
    # 注册路由
    app.include_router(api_router, prefix="/api")
    
    # 根路径
    @app.get("/", tags=["根路径"])
    async def root():
        """根路径，返回欢迎信息"""
        return {
            "message": "Welcome to FastAPI Demo",
            "docs": "/docs",
            "redoc": "/redoc",
        }
    
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )

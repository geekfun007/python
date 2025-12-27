"""FastAPI 应用入口"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import logging

from .config import settings
from .database import create_tables
from .api.v1.router import api_router

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理
    
    - 启动时：创建数据库表
    - 关闭时：清理资源
    """
    # 启动
    logger.info("应用启动中...")
    create_tables()
    logger.info("数据库表已创建")
    
    yield
    
    # 关闭
    logger.info("应用关闭中...")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    description="""
## FastAPI 实战项目示例

这是一个完整的 FastAPI 项目示例，包含：

- 🔐 **用户认证**: JWT Token 认证
- 👥 **用户管理**: 注册、登录、用户信息管理
- 📦 **商品管理**: CRUD 操作、标签、搜索
- 📚 **自动文档**: Swagger UI 和 ReDoc

### 认证说明

大部分接口需要认证，请先：
1. 注册账户 (`POST /api/v1/auth/register`)
2. 登录获取 Token (`POST /api/v1/auth/login`)
3. 在请求头添加 `Authorization: Bearer <token>`
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ==================== 中间件 ====================

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求计时中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间到响应头"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录请求日志"""
    logger.info(f"请求: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"响应: {response.status_code}")
    return response


# ==================== 异常处理 ====================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """自定义验证错误响应"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "请求数据验证失败",
            "details": errors
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.exception(f"未处理的异常: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "服务器内部错误"
        }
    )


# ==================== 路由 ====================

# 注册 API 路由
app.include_router(api_router, prefix=settings.api_v1_prefix)


# 根路径
@app.get("/", tags=["根路径"])
async def root():
    """API 根路径
    
    返回 API 基本信息
    """
    return {
        "message": f"欢迎使用 {settings.app_name}",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_version": "v1",
        "api_prefix": settings.api_v1_prefix
    }


# 健康检查
@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查端点
    
    用于负载均衡器或 Kubernetes 探针
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )

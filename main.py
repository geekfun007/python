"""
FastAPI Main Application
主应用程序入口

FastAPI核心概念：
1. 异步框架 - 基于ASGI，支持高并发
2. 自动API文档 - Swagger UI 和 ReDoc
3. 类型提示 - 完整的类型检查支持
4. 依赖注入 - 灵活的依赖管理系统
5. 数据验证 - 基于Pydantic的自动验证
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config import settings
from app.core.database import init_db
from app.api.v1 import api_router
from app.middleware.logging import LoggingMiddleware
from app.middleware.cors import setup_cors

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## FastAPI 原理与实战示例
    
    这是一个完整的FastAPI应用，演示了：
    
    ### 核心特性
    * **ORM**: SQLAlchemy 对象关系映射
    * **DAL**: 数据访问层模式
    * **依赖注入**: FastAPI的依赖注入系统
    * **数据验证**: Pydantic模型验证
    * **API文档**: 自动生成Swagger UI文档
    
    ### 数据库
    * MySQL数据库
    * 连接池管理
    * 事务管理
    
    ### 架构模式
    * 分层架构（API层、业务逻辑层、数据访问层）
    * RESTful API设计
    * 统一响应格式
    """,
    docs_url="/docs",  # Swagger UI文档路径
    redoc_url="/redoc",  # ReDoc文档路径
    openapi_url="/openapi.json"  # OpenAPI规范路径
)

# 配置CORS
setup_cors(app)

# 添加日志中间件
app.add_middleware(LoggingMiddleware)

# 注册API路由
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """
    应用启动事件
    
    原理：
    - @app.on_event("startup") 装饰器注册启动时执行的函数
    - 可以在这里进行初始化操作
    """
    print("=" * 50)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 启动中...")
    print(f"📝 API文档: http://localhost:8000/docs")
    print(f"📚 ReDoc文档: http://localhost:8000/redoc")
    print("=" * 50)
    
    # 初始化数据库（创建表）
    # 注意：生产环境应该使用Alembic进行数据库迁移
    try:
        init_db()
        print("✅ 数据库初始化成功")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print("\n" + "=" * 50)
    print("👋 应用正在关闭...")
    print("=" * 50)


@app.get("/", tags=["Root"])
async def root():
    """
    根路径
    
    返回API基本信息
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "欢迎使用 FastAPI！",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    健康检查端点
    
    用于监控系统检查服务是否正常运行
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# 全局异常处理器
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    HTTP异常处理器
    
    原理：
    - 捕获所有HTTP异常
    - 统一返回格式
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    请求验证异常处理器
    
    原理：
    - Pydantic验证失败时抛出RequestValidationError
    - 格式化验证错误信息
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "请求参数验证失败",
            "data": {"errors": errors}
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    通用异常处理器
    
    捕获所有未处理的异常
    """
    import traceback
    
    # 打印详细错误信息
    print("=" * 50)
    print("❌ 服务器错误:")
    print(traceback.format_exc())
    print("=" * 50)
    
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": {"detail": str(exc)} if settings.DEBUG else None
        }
    )


if __name__ == "__main__":
    """
    直接运行此文件启动应用
    
    使用uvicorn ASGI服务器
    """
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,  # 开发模式下自动重载
        log_level="info"
    )

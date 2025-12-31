"""
Error Handler Middleware
全局异常处理中间件
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


def setup_exception_handlers(app: FastAPI):
    """
    设置全局异常处理器
    
    处理的异常类型:
    - HTTPException: HTTP 异常（404, 401, 403 等）
    - RequestValidationError: 请求验证错误
    - SQLAlchemyError: 数据库错误
    - Exception: 其他未捕获的异常
    """
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
    ) -> JSONResponse:
        """
        HTTP 异常处理
        
        返回格式:
        {
            "code": status_code,
            "message": "错误信息",
            "detail": null
        }
        """
        request_id = getattr(request.state, "request_id", "unknown")
        
        logger.warning(
            f"[{request_id}] HTTP Exception: {exc.status_code} - {exc.detail}"
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": str(exc.detail),
                "detail": None
            },
            headers=exc.headers,
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        """
        请求验证错误处理
        
        返回格式:
        {
            "code": 422,
            "message": "请求参数验证失败",
            "detail": [
                {
                    "loc": ["body", "field_name"],
                    "msg": "错误信息",
                    "type": "错误类型"
                }
            ]
        }
        """
        request_id = getattr(request.state, "request_id", "unknown")
        
        # 格式化错误信息
        errors = []
        for error in exc.errors():
            errors.append({
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", ""),
            })
        
        logger.warning(
            f"[{request_id}] Validation Error: {errors}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": 422,
                "message": "请求参数验证失败",
                "detail": errors
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError
    ) -> JSONResponse:
        """
        数据库错误处理
        
        在生产环境中，不应该向客户端暴露详细的数据库错误信息
        """
        request_id = getattr(request.state, "request_id", "unknown")
        
        logger.error(
            f"[{request_id}] Database Error: {str(exc)}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 500,
                "message": "数据库操作失败，请稍后重试",
                "detail": None
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """
        通用异常处理
        
        捕获所有未处理的异常，防止敏感信息泄露
        """
        request_id = getattr(request.state, "request_id", "unknown")
        
        logger.exception(
            f"[{request_id}] Unhandled Exception: {str(exc)}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 500,
                "message": "服务器内部错误",
                "detail": None
            }
        )


class BusinessException(Exception):
    """
    业务异常基类
    
    用于抛出业务逻辑相关的异常
    
    Example:
        raise BusinessException(
            code=40001,
            message="用户不存在",
            status_code=404
        )
    """
    
    def __init__(
        self,
        code: int,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: dict = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


def setup_business_exception_handler(app: FastAPI):
    """设置业务异常处理器"""
    
    @app.exception_handler(BusinessException)
    async def business_exception_handler(
        request: Request,
        exc: BusinessException
    ) -> JSONResponse:
        """业务异常处理"""
        request_id = getattr(request.state, "request_id", "unknown")
        
        logger.warning(
            f"[{request_id}] Business Exception: {exc.code} - {exc.message}"
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
                "detail": exc.detail
            }
        )

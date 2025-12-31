"""
全局异常处理中间件
统一处理应用异常
"""
import traceback
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import AppException


async def error_handler_middleware(
    request: Request, call_next: Callable
) -> Response:
    """
    全局异常处理中间件
    
    捕获并处理所有未处理的异常，返回统一的错误响应格式
    
    Args:
        request: 请求对象
        call_next: 下一个中间件或路由处理函数
    
    Returns:
        响应对象
    """
    try:
        return await call_next(request)
    
    except AppException as e:
        # 应用自定义异常
        logger.warning(
            f"Application error | "
            f"code={e.code} | "
            f"message={e.message} | "
            f"details={e.details}"
        )
        return JSONResponse(
            status_code=e.code,
            content={
                "code": e.code,
                "message": e.message,
                "details": e.details,
            },
        )
    
    except ValidationError as e:
        # Pydantic 验证错误
        logger.warning(f"Validation error | errors={e.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": 422,
                "message": "数据验证失败",
                "details": e.errors(),
            },
        )
    
    except SQLAlchemyError as e:
        # 数据库错误
        logger.error(f"Database error | error={str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 500,
                "message": "数据库操作失败",
                "details": None,
            },
        )
    
    except Exception as e:
        # 未知异常
        logger.error(
            f"Unexpected error | "
            f"error={str(e)} | "
            f"traceback={traceback.format_exc()}"
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 500,
                "message": "服务器内部错误",
                "details": str(e) if request.app.debug else None,
            },
        )

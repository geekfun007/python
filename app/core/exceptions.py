"""
自定义异常模块
定义业务异常和HTTP异常处理
"""
from typing import Any, Optional

from fastapi import HTTPException, status


class AppException(Exception):
    """应用基础异常"""
    
    def __init__(
        self,
        message: str,
        code: int = 500,
        details: Optional[Any] = None,
    ):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)


class NotFoundException(HTTPException):
    """资源未找到异常"""
    
    def __init__(self, detail: str = "资源未找到"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(HTTPException):
    """未授权异常"""
    
    def __init__(self, detail: str = "未授权访问"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(HTTPException):
    """禁止访问异常"""
    
    def __init__(self, detail: str = "禁止访问"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestException(HTTPException):
    """请求错误异常"""
    
    def __init__(self, detail: str = "请求参数错误"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ConflictException(HTTPException):
    """资源冲突异常"""
    
    def __init__(self, detail: str = "资源冲突"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ValidationException(HTTPException):
    """验证异常"""
    
    def __init__(self, detail: str = "数据验证失败"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )

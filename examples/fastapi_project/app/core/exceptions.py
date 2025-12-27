"""自定义异常类"""
from fastapi import HTTPException, status


class AppException(HTTPException):
    """应用基础异常类"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict = None
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers
        )


class NotFoundException(AppException):
    """资源未找到异常"""
    
    def __init__(self, detail: str = "资源未找到"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class UnauthorizedException(AppException):
    """未认证异常"""
    
    def __init__(self, detail: str = "未认证"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(AppException):
    """权限不足异常"""
    
    def __init__(self, detail: str = "权限不足"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class BadRequestException(AppException):
    """请求错误异常"""
    
    def __init__(self, detail: str = "请求错误"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class ConflictException(AppException):
    """资源冲突异常"""
    
    def __init__(self, detail: str = "资源已存在"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class InsufficientStockException(AppException):
    """库存不足异常"""
    
    def __init__(self, item_id: int, requested: int, available: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"商品 {item_id} 库存不足：请求 {requested}，可用 {available}"
        )
        self.item_id = item_id
        self.requested = requested
        self.available = available

"""
Common Schemas
通用响应和分页模型
"""

from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel, Field


T = TypeVar("T")


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")
    
    @property
    def offset(self) -> int:
        """计算偏移量"""
        return (self.page - 1) * self.page_size


class PaginationMeta(BaseModel):
    """分页元数据"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")
    has_next: bool = Field(..., description="是否有下一页")
    has_prev: bool = Field(..., description="是否有上一页")
    
    @classmethod
    def create(cls, total: int, page: int, page_size: int) -> "PaginationMeta":
        """创建分页元数据"""
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return cls(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )


class ResponseModel(BaseModel, Generic[T]):
    """
    通用 API 响应模型
    
    Example:
        {
            "code": 0,
            "message": "success",
            "data": {...}
        }
    """
    code: int = Field(default=0, description="状态码，0 表示成功")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    
    @classmethod
    def success(cls, data: T = None, message: str = "success") -> "ResponseModel[T]":
        """成功响应"""
        return cls(code=0, message=message, data=data)
    
    @classmethod
    def error(cls, message: str, code: int = -1, data: T = None) -> "ResponseModel[T]":
        """错误响应"""
        return cls(code=code, message=message, data=data)


class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误信息")
    detail: Optional[Any] = Field(default=None, description="详细错误信息")


class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(default="healthy", description="服务状态")
    version: str = Field(..., description="应用版本")
    database: str = Field(default="connected", description="数据库状态")

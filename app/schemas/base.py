"""
基础 Schema 定义
通用响应格式和分页模型
"""
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """基础Schema配置"""
    
    model_config = ConfigDict(
        from_attributes=True,  # 支持从ORM模型创建
        populate_by_name=True,  # 允许使用别名
        str_strip_whitespace=True,  # 字符串去除首尾空格
    )


class TimestampMixin(BaseModel):
    """时间戳混入"""
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BaseResponse(BaseModel, Generic[T]):
    """
    统一响应格式
    
    示例:
    {
        "code": 200,
        "message": "success",
        "data": {...}
    }
    """
    
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    
    @classmethod
    def success(cls, data: T = None, message: str = "操作成功") -> "BaseResponse[T]":
        """成功响应"""
        return cls(code=200, message=message, data=data)
    
    @classmethod
    def error(cls, message: str = "操作失败", code: int = 400) -> "BaseResponse":
        """错误响应"""
        return cls(code=code, message=message, data=None)


class PaginatedResponse(BaseModel, Generic[T]):
    """
    分页响应格式
    
    示例:
    {
        "items": [...],
        "total": 100,
        "page": 1,
        "page_size": 20,
        "pages": 5
    }
    """
    
    items: List[T] = Field(default_factory=list, description="数据列表")
    total: int = Field(default=0, description="总数量")
    page: int = Field(default=1, ge=1, description="当前页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")
    pages: int = Field(default=0, description="总页数")
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        """创建分页响应"""
        pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )


class QueryParams(BaseModel):
    """通用查询参数"""
    
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")
    order_by: Optional[str] = Field(default=None, description="排序字段")
    order_desc: bool = Field(default=False, description="是否降序")
    search: Optional[str] = Field(default=None, description="搜索关键词")

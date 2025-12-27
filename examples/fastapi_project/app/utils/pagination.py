"""分页工具"""
from fastapi import Query
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')


class Pagination:
    """分页参数类
    
    作为依赖使用，自动计算 skip 和 limit
    
    Example:
        @app.get("/items")
        async def list_items(pagination: Pagination = Depends()):
            return items[pagination.skip:pagination.skip + pagination.limit]
    """
    
    def __init__(
        self,
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(20, ge=1, le=100, description="每页数量")
    ):
        self.page = page
        self.page_size = page_size
        self.skip = (page - 1) * page_size
        self.limit = page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应模型
    
    用于封装分页数据
    """
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ) -> "PaginatedResponse[T]":
        """创建分页响应
        
        Args:
            items: 当前页数据
            total: 总数量
            page: 当前页码
            page_size: 每页数量
            
        Returns:
            分页响应对象
        """
        total_pages = (total + page_size - 1) // page_size
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

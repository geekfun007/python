"""
Pydantic Schemas Package
用于请求验证和响应序列化
"""
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserList
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductList
from app.schemas.common import PaginationParams, ResponseModel

__all__ = [
    "UserCreate",
    "UserUpdate", 
    "UserResponse",
    "UserList",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductList",
    "PaginationParams",
    "ResponseModel",
]

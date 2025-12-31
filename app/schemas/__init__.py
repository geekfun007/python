"""
Schemas (IDL) 模块
定义请求和响应的数据模型
"""
from app.schemas.base import BaseResponse, PaginatedResponse
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenPayload,
)
from app.schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
)

__all__ = [
    # Base
    "BaseResponse",
    "PaginatedResponse",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenPayload",
    # Item
    "ItemCreate",
    "ItemUpdate",
    "ItemResponse",
]

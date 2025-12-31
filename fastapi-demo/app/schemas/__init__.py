"""
Pydantic Schemas
API 请求/响应数据验证模型
"""

from .user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
    LoginRequest,
    LoginResponse,
    TokenPayload,
)
from .article import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleListResponse,
    ArticleFilter,
    CategoryCreate,
    CategoryResponse,
    TagCreate,
    TagResponse,
)
from .interaction import (
    CommentCreate,
    CommentResponse,
    CommentListResponse,
)
from .common import (
    ResponseModel,
    PaginationParams,
    PaginationMeta,
)

__all__ = [
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserListResponse",
    "LoginRequest",
    "LoginResponse",
    "TokenPayload",
    # Article
    "ArticleCreate",
    "ArticleUpdate",
    "ArticleResponse",
    "ArticleListResponse",
    "ArticleFilter",
    "CategoryCreate",
    "CategoryResponse",
    "TagCreate",
    "TagResponse",
    # Interaction
    "CommentCreate",
    "CommentResponse",
    "CommentListResponse",
    # Common
    "ResponseModel",
    "PaginationParams",
    "PaginationMeta",
]

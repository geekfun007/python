"""
API V1 Module
API 版本 1 路由
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .articles import router as articles_router
from .categories import router as categories_router
from .tags import router as tags_router

# 创建 v1 路由器
api_router = APIRouter()

# 注册子路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(users_router, prefix="/users", tags=["用户"])
api_router.include_router(articles_router, prefix="/articles", tags=["文章"])
api_router.include_router(categories_router, prefix="/categories", tags=["分类"])
api_router.include_router(tags_router, prefix="/tags", tags=["标签"])

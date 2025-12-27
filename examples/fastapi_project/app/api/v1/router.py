"""API v1 主路由"""
from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .items import router as items_router

# 创建 v1 路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(users_router, prefix="/users", tags=["用户"])
api_router.include_router(items_router, prefix="/items", tags=["商品"])

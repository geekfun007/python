"""
API 路由汇总
"""
from fastapi import APIRouter

from app.api.v1 import auth, items, users, health

api_router = APIRouter()

# 健康检查
api_router.include_router(health.router, prefix="/health", tags=["健康检查"])

# V1 API
api_router.include_router(auth.router, prefix="/v1/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/v1/users", tags=["用户"])
api_router.include_router(items.router, prefix="/v1/items", tags=["物品"])

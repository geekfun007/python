"""
API Version 1
"""
from fastapi import APIRouter
from app.api.v1 import users, products

# 创建API路由器
api_router = APIRouter()

# 注册子路由
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])

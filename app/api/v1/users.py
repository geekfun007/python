"""
用户 API
处理用户的 CRUD 操作
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.middlewares.auth import get_current_superuser, get_current_user
from app.models.user import User
from app.schemas.base import BaseResponse, PaginatedResponse
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter()


@router.get(
    "",
    response_model=BaseResponse[PaginatedResponse[UserResponse]],
    summary="获取用户列表",
    description="获取用户列表（需要管理员权限）",
)
async def get_users(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    is_active: Optional[bool] = Query(default=None, description="是否激活"),
    current_user: User = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户列表接口
    
    需要管理员权限
    
    - **page**: 页码
    - **page_size**: 每页数量
    - **is_active**: 按激活状态过滤
    """
    user_service = UserService(db)
    result = await user_service.get_users(
        page=page,
        page_size=page_size,
        is_active=is_active,
    )
    return BaseResponse.success(data=result, message="获取成功")


@router.get(
    "/{user_id}",
    response_model=BaseResponse[UserResponse],
    summary="获取用户详情",
    description="根据ID获取用户详情",
)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户详情接口
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    user = await user_service.get_user(user_id)
    return BaseResponse.success(data=user, message="获取成功")


@router.put(
    "/{user_id}",
    response_model=BaseResponse[UserResponse],
    summary="更新用户",
    description="更新用户信息（用户本人或管理员）",
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    更新用户信息接口
    
    用户只能修改自己的信息，管理员可以修改所有用户
    
    - **user_id**: 用户ID
    - **email**: 新邮箱（可选）
    - **username**: 新用户名（可选）
    - **full_name**: 新全名（可选）
    - **password**: 新密码（可选）
    """
    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_data, current_user)
    return BaseResponse.success(data=user, message="更新成功")


@router.delete(
    "/{user_id}",
    response_model=BaseResponse,
    summary="删除用户",
    description="删除用户（需要管理员权限）",
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
):
    """
    删除用户接口
    
    需要管理员权限，不能删除自己
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    await user_service.delete_user(user_id, current_user)
    return BaseResponse.success(message="删除成功")


@router.post(
    "/{user_id}/activate",
    response_model=BaseResponse[UserResponse],
    summary="激活用户",
    description="激活用户（需要管理员权限）",
)
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
):
    """
    激活用户接口
    
    需要管理员权限
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    user = await user_service.activate_user(user_id)
    return BaseResponse.success(data=user, message="激活成功")


@router.post(
    "/{user_id}/deactivate",
    response_model=BaseResponse[UserResponse],
    summary="禁用用户",
    description="禁用用户（需要管理员权限）",
)
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
):
    """
    禁用用户接口
    
    需要管理员权限
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    user = await user_service.deactivate_user(user_id)
    return BaseResponse.success(data=user, message="禁用成功")

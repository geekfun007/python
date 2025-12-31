"""
Users Router
用户相关 API 路由
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import (
    UserResponse, UserUpdate, UserListResponse, PasswordChange
)
from app.schemas.common import ResponseModel
from app.services.user_service import UserService
from app.services.auth_service import get_current_user, get_current_admin_user
from app.models.user import User, UserStatus, UserRole

router = APIRouter()


@router.get(
    "",
    response_model=ResponseModel[UserListResponse],
    summary="获取用户列表",
    description="获取用户列表（需要管理员权限）"
)
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[UserStatus] = Query(None, description="用户状态"),
    role: Optional[UserRole] = Query(None, description="用户角色"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户列表
    
    - 需要管理员权限
    - 支持按状态、角色过滤
    - 支持关键词搜索（用户名、邮箱）
    """
    user_service = UserService(db)
    result = await user_service.get_users(
        page=page,
        page_size=page_size,
        status=status,
        role=role,
        keyword=keyword,
    )
    return ResponseModel.success(data=result)


@router.get(
    "/{user_id}",
    response_model=ResponseModel[UserResponse],
    summary="获取用户信息",
    description="根据用户ID获取用户详细信息"
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户详细信息
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    user = await user_service.get_user(user_id)
    return ResponseModel.success(data=UserResponse.model_validate(user))


@router.put(
    "/{user_id}",
    response_model=ResponseModel[UserResponse],
    summary="更新用户信息",
    description="更新用户信息（只能更新自己的信息，管理员可更新任何用户）"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户信息
    
    - 普通用户只能更新自己的信息
    - 管理员可以更新任何用户的信息
    - 只有管理员可以修改用户状态和角色
    """
    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_data, current_user)
    return ResponseModel.success(data=UserResponse.model_validate(user), message="更新成功")


@router.delete(
    "/{user_id}",
    response_model=ResponseModel,
    summary="删除用户",
    description="删除用户（需要管理员权限）"
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除用户
    
    - 需要管理员权限
    - 不能删除自己
    - 执行软删除（将状态设为 DELETED）
    """
    user_service = UserService(db)
    await user_service.delete_user(user_id, current_user)
    return ResponseModel.success(message="删除成功")


@router.post(
    "/change-password",
    response_model=ResponseModel,
    summary="修改密码",
    description="修改当前用户的密码"
)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    修改密码
    
    - **old_password**: 当前密码
    - **new_password**: 新密码（至少6个字符）
    """
    user_service = UserService(db)
    await user_service.change_password(
        user_id=current_user.id,
        old_password=password_data.old_password,
        new_password=password_data.new_password,
    )
    return ResponseModel.success(message="密码修改成功")


@router.post(
    "/{user_id}/ban",
    response_model=ResponseModel[UserResponse],
    summary="封禁用户",
    description="封禁指定用户（需要管理员权限）"
)
async def ban_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    封禁用户
    
    - 需要管理员权限
    - 将用户状态设为 BANNED
    """
    user_service = UserService(db)
    user = await user_service.update_user(
        user_id,
        UserUpdate(status=UserStatus.BANNED),
        current_user
    )
    return ResponseModel.success(data=UserResponse.model_validate(user), message="用户已封禁")


@router.post(
    "/{user_id}/activate",
    response_model=ResponseModel[UserResponse],
    summary="激活用户",
    description="激活指定用户（需要管理员权限）"
)
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    激活用户
    
    - 需要管理员权限
    - 将用户状态设为 ACTIVE
    """
    user_service = UserService(db)
    user = await user_service.update_user(
        user_id,
        UserUpdate(status=UserStatus.ACTIVE),
        current_user
    )
    return ResponseModel.success(data=UserResponse.model_validate(user), message="用户已激活")

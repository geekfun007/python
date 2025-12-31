"""
认证 API
处理用户注册、登录、令牌刷新等
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.middlewares.auth import get_current_user
from app.models.user import User
from app.schemas.base import BaseResponse
from app.schemas.user import (
    PasswordChange,
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=BaseResponse[UserResponse],
    summary="用户注册",
    description="注册新用户账号",
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    用户注册接口
    
    - **email**: 用户邮箱（唯一）
    - **username**: 用户名（唯一，3-50字符，仅字母数字）
    - **password**: 密码（8-100字符，需包含大小写字母和数字）
    - **full_name**: 全名（可选）
    """
    auth_service = AuthService(db)
    user = await auth_service.register(user_data)
    return BaseResponse.success(data=user, message="注册成功")


@router.post(
    "/login",
    response_model=BaseResponse[Token],
    summary="用户登录",
    description="用户登录获取访问令牌",
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """
    用户登录接口
    
    - **email**: 用户邮箱
    - **password**: 密码
    
    返回访问令牌和刷新令牌
    """
    auth_service = AuthService(db)
    token = await auth_service.login(login_data.email, login_data.password)
    return BaseResponse.success(data=token, message="登录成功")


@router.post(
    "/refresh",
    response_model=BaseResponse[Token],
    summary="刷新令牌",
    description="使用刷新令牌获取新的访问令牌",
)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
):
    """
    刷新令牌接口
    
    - **refresh_token**: 刷新令牌
    
    返回新的访问令牌和刷新令牌
    """
    auth_service = AuthService(db)
    token = await auth_service.refresh_token(refresh_token)
    return BaseResponse.success(data=token, message="令牌刷新成功")


@router.get(
    "/me",
    response_model=BaseResponse[UserResponse],
    summary="获取当前用户",
    description="获取当前登录用户的信息",
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    获取当前用户信息接口
    
    需要认证
    """
    return BaseResponse.success(
        data=UserResponse.model_validate(current_user),
        message="获取成功",
    )


@router.post(
    "/change-password",
    response_model=BaseResponse,
    summary="修改密码",
    description="修改当前用户的密码",
)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    修改密码接口
    
    - **old_password**: 旧密码
    - **new_password**: 新密码（8-100字符，需包含大小写字母和数字）
    """
    auth_service = AuthService(db)
    await auth_service.change_password(
        current_user,
        password_data.old_password,
        password_data.new_password,
    )
    return BaseResponse.success(message="密码修改成功")

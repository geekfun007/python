"""
Auth Router
认证相关 API 路由
"""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import LoginRequest, LoginResponse, UserResponse, UserCreate
from app.schemas.common import ResponseModel
from app.services.auth_service import AuthService, get_current_user
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter()


@router.post(
    "/register",
    response_model=ResponseModel[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="用户注册",
    description="注册新用户账户"
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册
    
    - **username**: 用户名（2-50个字符）
    - **email**: 邮箱地址
    - **password**: 密码（至少6个字符）
    - **phone**: 手机号（可选）
    - **avatar**: 头像URL（可选）
    """
    user_service = UserService(db)
    user = await user_service.create_user(user_data)
    return ResponseModel.success(
        data=UserResponse.model_validate(user),
        message="注册成功"
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="用户登录",
    description="使用邮箱和密码登录"
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录
    
    - **email**: 注册邮箱
    - **password**: 用户密码
    
    返回 JWT 访问令牌
    """
    auth_service = AuthService(db)
    return await auth_service.login(login_data)


@router.post(
    "/login/form",
    response_model=LoginResponse,
    summary="表单登录",
    description="OAuth2 兼容的表单登录（用于 Swagger UI）"
)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    表单登录（OAuth2 兼容）
    
    此端点用于 Swagger UI 的授权功能
    username 字段实际上接收的是邮箱
    """
    auth_service = AuthService(db)
    login_data = LoginRequest(email=form_data.username, password=form_data.password)
    return await auth_service.login(login_data)


@router.get(
    "/me",
    response_model=ResponseModel[UserResponse],
    summary="获取当前用户",
    description="获取当前登录用户的信息"
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前登录用户信息
    
    需要在请求头中携带有效的 Bearer Token
    """
    return ResponseModel.success(data=UserResponse.model_validate(current_user))


@router.post(
    "/refresh",
    response_model=LoginResponse,
    summary="刷新令牌",
    description="使用当前令牌获取新的访问令牌"
)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    刷新访问令牌
    
    使用当前有效的令牌获取新的令牌
    """
    from datetime import timedelta
    from app.core.config import settings
    from app.core.security import create_access_token
    
    expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=expires_delta
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(current_user)
    )

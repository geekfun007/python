"""
Auth Service
认证服务
"""

from typing import Optional
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token, decode_access_token
from app.dal.user_dal import UserDAL
from app.models.user import User
from app.schemas.user import LoginRequest, LoginResponse, UserResponse


# OAuth2 密码承载方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class AuthService:
    """
    认证服务类
    
    提供:
    - 用户登录
    - 令牌验证
    - 获取当前用户
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_dal = UserDAL(db)
    
    async def login(self, login_data: LoginRequest) -> LoginResponse:
        """
        用户登录
        
        Args:
            login_data: 登录请求数据
        
        Returns:
            登录响应（包含令牌和用户信息）
        
        Raises:
            HTTPException: 认证失败时抛出 401 错误
        """
        user = await self.user_dal.authenticate(
            email=login_data.email,
            password=login_data.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 创建访问令牌
        expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=expires_delta
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user)
        )
    
    async def get_user_by_token(self, token: str) -> Optional[User]:
        """
        根据令牌获取用户
        
        Args:
            token: JWT 令牌
        
        Returns:
            用户实例或 None
        """
        payload = decode_access_token(token)
        
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        try:
            user_id = int(user_id)
        except ValueError:
            return None
        
        user = await self.user_dal.get(user_id)
        
        if not user or not user.is_active:
            return None
        
        return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    依赖注入：获取当前登录用户
    
    用法:
        @router.get("/me")
        async def get_me(user: User = Depends(get_current_user)):
            return user
    
    Raises:
        HTTPException: 未认证或用户不存在时抛出 401 错误
    """
    auth_service = AuthService(db)
    user = await auth_service.get_user_by_token(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_user_optional(
    token: Optional[str] = Depends(
        OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)
    ),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    依赖注入：获取当前用户（可选）
    未登录时返回 None，不会抛出异常
    """
    if not token:
        return None
    
    auth_service = AuthService(db)
    return await auth_service.get_user_by_token(token)


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    依赖注入：获取当前管理员用户
    
    Raises:
        HTTPException: 非管理员时抛出 403 错误
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user

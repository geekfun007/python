"""
认证服务
处理用户认证相关的业务逻辑
"""
from datetime import timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import Token, UserCreate, UserResponse


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def register(self, user_data: UserCreate) -> UserResponse:
        """
        用户注册
        
        Args:
            user_data: 用户注册数据
        
        Returns:
            创建的用户信息
        
        Raises:
            BadRequestException: 邮箱或用户名已存在
        """
        # 检查邮箱是否已存在
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise BadRequestException("该邮箱已被注册")
        
        # 检查用户名是否已存在
        existing_user = await self.user_repo.get_by_username(user_data.username)
        if existing_user:
            raise BadRequestException("该用户名已被使用")
        
        # 创建用户
        hashed_password = get_password_hash(user_data.password)
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_superuser": False,
        }
        
        user = await self.user_repo.create(user_dict)
        return UserResponse.model_validate(user)
    
    async def login(self, email: str, password: str) -> Token:
        """
        用户登录
        
        Args:
            email: 用户邮箱
            password: 密码
        
        Returns:
            访问令牌和刷新令牌
        
        Raises:
            UnauthorizedException: 邮箱或密码错误
        """
        user = await self.user_repo.authenticate(email, password)
        if not user:
            raise UnauthorizedException("邮箱或密码错误")
        
        if not user.is_active:
            raise UnauthorizedException("用户已被禁用")
        
        # 创建令牌
        access_token = create_access_token(
            subject=user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            extra_data={"username": user.username},
        )
        refresh_token = create_refresh_token(subject=user.id)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    
    async def refresh_token(self, refresh_token: str) -> Token:
        """
        刷新访问令牌
        
        Args:
            refresh_token: 刷新令牌
        
        Returns:
            新的访问令牌和刷新令牌
        
        Raises:
            UnauthorizedException: 刷新令牌无效
        """
        payload = decode_token(refresh_token)
        if not payload:
            raise UnauthorizedException("无效的刷新令牌")
        
        # 检查令牌类型
        if payload.get("type") != "refresh":
            raise UnauthorizedException("无效的令牌类型")
        
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("令牌中缺少用户信息")
        
        # 获取用户
        user = await self.user_repo.get(int(user_id))
        if not user:
            raise UnauthorizedException("用户不存在")
        
        if not user.is_active:
            raise UnauthorizedException("用户已被禁用")
        
        # 创建新令牌
        access_token = create_access_token(
            subject=user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            extra_data={"username": user.username},
        )
        new_refresh_token = create_refresh_token(subject=user.id)
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    
    async def change_password(
        self,
        user: User,
        old_password: str,
        new_password: str,
    ) -> bool:
        """
        修改密码
        
        Args:
            user: 当前用户
            old_password: 旧密码
            new_password: 新密码
        
        Returns:
            是否修改成功
        
        Raises:
            BadRequestException: 旧密码错误
        """
        if not verify_password(old_password, user.hashed_password):
            raise BadRequestException("旧密码错误")
        
        hashed_password = get_password_hash(new_password)
        return await self.user_repo.set_password(user.id, hashed_password)

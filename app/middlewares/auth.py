"""
认证中间件和依赖
处理JWT令牌验证
"""
from typing import Optional

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedException
from app.core.security import decode_token
from app.db import get_db
from app.models.user import User
from app.repositories.user import UserRepository

# HTTP Bearer 认证方案
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    获取当前认证用户
    
    从请求头中获取JWT令牌，验证并返回用户对象
    
    Args:
        request: 请求对象
        credentials: HTTP Bearer 认证凭据
        db: 数据库会话
    
    Returns:
        当前认证的用户对象
    
    Raises:
        UnauthorizedException: 未提供令牌或令牌无效
    """
    if not credentials:
        raise UnauthorizedException("未提供认证令牌")
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise UnauthorizedException("无效的认证令牌")
    
    # 检查令牌类型
    token_type = payload.get("type")
    if token_type != "access":
        raise UnauthorizedException("无效的令牌类型")
    
    # 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("令牌中缺少用户信息")
    
    # 查询用户
    user_repo = UserRepository(db)
    user = await user_repo.get(int(user_id))
    
    if not user:
        raise UnauthorizedException("用户不存在")
    
    if not user.is_active:
        raise UnauthorizedException("用户已被禁用")
    
    # 将用户信息存储在 request.state 中
    request.state.user = user
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前激活的用户
    
    Args:
        current_user: 当前认证用户
    
    Returns:
        当前激活的用户对象
    
    Raises:
        UnauthorizedException: 用户未激活
    """
    if not current_user.is_active:
        raise UnauthorizedException("用户已被禁用")
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前超级管理员用户
    
    Args:
        current_user: 当前认证用户
    
    Returns:
        当前超级管理员用户对象
    
    Raises:
        UnauthorizedException: 用户非超级管理员
    """
    if not current_user.is_superuser:
        raise UnauthorizedException("需要管理员权限")
    return current_user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    获取可选的当前用户
    
    如果提供了有效的令牌则返回用户，否则返回None
    
    Args:
        credentials: HTTP Bearer 认证凭据
        db: 数据库会话
    
    Returns:
        当前认证的用户对象或None
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    user_repo = UserRepository(db)
    user = await user_repo.get(int(user_id))
    
    if user and user.is_active:
        return user
    
    return None

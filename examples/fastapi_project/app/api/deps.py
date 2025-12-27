"""API 依赖项"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session
from typing import Annotated, Optional

from ..database import get_db
from ..models.user import User
from ..crud.user import user_crud
from ..core.security import decode_token
from ..core.exceptions import UnauthorizedException, ForbiddenException


# OAuth2 密码流
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login",
    scopes={
        "read": "读取权限",
        "write": "写入权限",
        "admin": "管理员权限"
    }
)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """获取当前认证用户
    
    Args:
        security_scopes: 需要的权限范围
        token: JWT token
        db: 数据库会话
        
    Returns:
        当前用户对象
        
    Raises:
        UnauthorizedException: 认证失败
        ForbiddenException: 权限不足
    """
    # 构建认证信息
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    
    # 解码 token
    token_data = decode_token(token)
    if token_data is None or token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭据",
            headers={"WWW-Authenticate": authenticate_value}
        )
    
    # 获取用户
    user = user_crud.get(db, user_id=token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": authenticate_value}
        )
    
    # 检查权限范围
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足",
                headers={"WWW-Authenticate": authenticate_value}
            )
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """获取当前活跃用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        当前活跃用户
        
    Raises:
        ForbiddenException: 用户已禁用
    """
    if not user_crud.is_active(current_user):
        raise ForbiddenException(detail="用户已被禁用")
    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """获取当前超级管理员
    
    Args:
        current_user: 当前活跃用户
        
    Returns:
        当前超级管理员
        
    Raises:
        ForbiddenException: 不是管理员
    """
    if not user_crud.is_superuser(current_user):
        raise ForbiddenException(detail="需要管理员权限")
    return current_user


# 可选认证（不强制要求登录）
async def get_current_user_optional(
    token: Annotated[Optional[str], Depends(OAuth2PasswordBearer(
        tokenUrl="api/v1/auth/login",
        auto_error=False
    ))] = None,
    db: Annotated[Session, Depends(get_db)] = None
) -> Optional[User]:
    """获取当前用户（可选）
    
    如果提供了有效 token 则返回用户，否则返回 None
    """
    if token is None:
        return None
    
    token_data = decode_token(token)
    if token_data is None or token_data.user_id is None:
        return None
    
    return user_crud.get(db, user_id=token_data.user_id)

"""认证路由"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from ...database import get_db
from ...schemas.token import Token
from ...schemas.user import UserCreate, UserResponse
from ...crud.user import user_crud
from ...core.security import create_access_token, create_refresh_token, decode_token
from ...core.exceptions import BadRequestException, UnauthorizedException

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: Annotated[Session, Depends(get_db)]
):
    """
    用户注册
    
    - **email**: 邮箱地址（必须唯一）
    - **username**: 用户名（必须唯一，3-50 字符）
    - **password**: 密码（至少 6 字符，包含大小写字母和数字）
    - **full_name**: 全名（可选）
    """
    # 检查邮箱是否已存在
    if user_crud.get_by_email(db, email=user_in.email):
        raise BadRequestException(detail="该邮箱已被注册")
    
    # 检查用户名是否已存在
    if user_crud.get_by_username(db, username=user_in.username):
        raise BadRequestException(detail="该用户名已被使用")
    
    # 创建用户
    user = user_crud.create(db, obj_in=user_in)
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    """
    用户登录
    
    使用 OAuth2 密码流进行认证，返回访问令牌和刷新令牌
    
    - **username**: 用户名
    - **password**: 密码
    """
    # 验证用户
    user = user_crud.authenticate(
        db,
        username=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    # 确定权限范围
    scopes = ["read", "write"]
    if user.is_superuser:
        scopes.append("admin")
    
    # 创建令牌
    token_data = {
        "sub": str(user.id),  # JWT sub claim must be a string
        "username": user.username,
        "scopes": scopes
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    刷新访问令牌
    
    使用刷新令牌获取新的访问令牌
    
    - **refresh_token**: 刷新令牌
    """
    # 解码刷新令牌
    token_data = decode_token(refresh_token)
    
    if not token_data or not token_data.user_id:
        raise UnauthorizedException(detail="无效的刷新令牌")
    
    # 获取用户
    user = user_crud.get(db, user_id=token_data.user_id)
    if not user:
        raise UnauthorizedException(detail="用户不存在")
    
    if not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    # 确定权限范围
    scopes = ["read", "write"]
    if user.is_superuser:
        scopes.append("admin")
    
    # 创建新令牌
    new_token_data = {
        "sub": str(user.id),  # JWT sub claim must be a string
        "username": user.username,
        "scopes": scopes
    }
    
    new_access_token = create_access_token(new_token_data)
    new_refresh_token = create_refresh_token(new_token_data)
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )

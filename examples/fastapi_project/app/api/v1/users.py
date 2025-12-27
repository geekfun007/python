"""用户路由"""
from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional

from ...database import get_db
from ...models.user import User
from ...schemas.user import UserResponse, UserUpdate
from ...crud.user import user_crud
from ..deps import get_current_active_user, get_current_superuser
from ...core.exceptions import NotFoundException, ForbiddenException, BadRequestException

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    获取当前用户信息
    
    需要认证
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    更新当前用户信息
    
    可更新字段：
    - **email**: 新邮箱
    - **username**: 新用户名
    - **full_name**: 全名
    - **password**: 新密码
    """
    # 检查邮箱是否被占用
    if user_in.email and user_in.email != current_user.email:
        if user_crud.get_by_email(db, email=user_in.email):
            raise BadRequestException(detail="该邮箱已被注册")
    
    # 检查用户名是否被占用
    if user_in.username and user_in.username != current_user.username:
        if user_crud.get_by_username(db, username=user_in.username):
            raise BadRequestException(detail="该用户名已被使用")
    
    # 更新用户
    user = user_crud.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("", response_model=List[UserResponse])
async def list_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])],
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
    is_active: Optional[bool] = Query(None, description="过滤激活状态")
):
    """
    获取用户列表
    
    需要管理员权限
    
    - **skip**: 分页偏移量
    - **limit**: 返回数量（最多 100）
    - **is_active**: 过滤激活状态
    """
    users = user_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        is_active=is_active
    )
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])]
):
    """
    获取指定用户信息
    
    需要管理员权限
    
    - **user_id**: 用户 ID
    """
    user = user_crud.get(db, user_id=user_id)
    if not user:
        raise NotFoundException(detail="用户不存在")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])]
):
    """
    更新指定用户信息
    
    需要管理员权限
    
    - **user_id**: 用户 ID
    """
    user = user_crud.get(db, user_id=user_id)
    if not user:
        raise NotFoundException(detail="用户不存在")
    
    # 检查邮箱是否被占用
    if user_in.email and user_in.email != user.email:
        if user_crud.get_by_email(db, email=user_in.email):
            raise BadRequestException(detail="该邮箱已被注册")
    
    # 检查用户名是否被占用
    if user_in.username and user_in.username != user.username:
        if user_crud.get_by_username(db, username=user_in.username):
            raise BadRequestException(detail="该用户名已被使用")
    
    user = user_crud.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_superuser)]
):
    """
    删除用户
    
    需要超级管理员权限
    
    - **user_id**: 用户 ID
    """
    # 不能删除自己
    if user_id == current_user.id:
        raise ForbiddenException(detail="不能删除自己的账户")
    
    user = user_crud.delete(db, user_id=user_id)
    if not user:
        raise NotFoundException(detail="用户不存在")
    
    return {"message": "用户已删除"}

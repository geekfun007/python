"""
User API Endpoints
用户相关的API端点

FastAPI路由原理：
1. APIRouter: 创建模块化的路由
2. Depends: 依赖注入系统
3. Path/Query: 路径参数和查询参数验证
4. status: HTTP状态码
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.dal.user_dal import UserDAL
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserList
from app.schemas.common import ResponseModel

# 创建路由器
router = APIRouter()


@router.post(
    "/",
    response_model=ResponseModel[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建用户",
    description="创建一个新用户"
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    创建用户
    
    FastAPI原理：
    1. user_in: UserCreate - 请求体自动验证
    2. db: Session = Depends(get_db) - 依赖注入数据库会话
    3. response_model - 响应数据自动序列化
    
    Args:
        user_in: 用户创建数据
        db: 数据库会话
        
    Returns:
        创建的用户信息
    """
    user_dal = UserDAL(db)
    
    # 检查用户名是否已存在
    existing_user = user_dal.get_by_username(user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    existing_email = user_dal.get_by_email(user_in.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )
    
    # 创建用户（实际应用中应该对密码进行哈希）
    user_data = user_in.model_dump(exclude={"password"})
    user_data["hashed_password"] = f"hashed_{user_in.password}"  # 示例，实际应使用bcrypt
    
    user = user_dal.create(user_data)
    
    return ResponseModel(
        code=201,
        message="用户创建成功",
        data=UserResponse.model_validate(user)
    )


@router.get(
    "/",
    response_model=ResponseModel[UserList],
    summary="获取用户列表",
    description="获取用户列表（分页）"
)
def get_users(
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=100, ge=1, le=100, description="返回的最大记录数"),
    active_only: bool = Query(default=False, description="只返回激活用户"),
    db: Session = Depends(get_db)
):
    """
    获取用户列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的最大记录数
        active_only: 是否只返回激活用户
        db: 数据库会话
        
    Returns:
        用户列表
    """
    user_dal = UserDAL(db)
    
    if active_only:
        users = user_dal.get_active_users(skip=skip, limit=limit)
        total = user_dal.count(filters={"is_active": True})
    else:
        users = user_dal.get_multi(skip=skip, limit=limit)
        total = user_dal.count()
    
    return ResponseModel(
        data=UserList(
            total=total,
            items=[UserResponse.model_validate(user) for user in users]
        )
    )


@router.get(
    "/{user_id}",
    response_model=ResponseModel[UserResponse],
    summary="获取用户详情",
    description="根据ID获取用户详情"
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    获取用户详情
    
    Args:
        user_id: 用户ID（路径参数）
        db: 数据库会话
        
    Returns:
        用户详情
    """
    user_dal = UserDAL(db)
    user = user_dal.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 ID {user_id} 不存在"
        )
    
    return ResponseModel(
        data=UserResponse.model_validate(user)
    )


@router.put(
    "/{user_id}",
    response_model=ResponseModel[UserResponse],
    summary="更新用户",
    description="更新用户信息"
)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    更新用户
    
    Args:
        user_id: 用户ID
        user_in: 更新数据
        db: 数据库会话
        
    Returns:
        更新后的用户信息
    """
    user_dal = UserDAL(db)
    
    # 检查用户是否存在
    if not user_dal.exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 ID {user_id} 不存在"
        )
    
    # 准备更新数据（只更新非None的字段）
    update_data = user_in.model_dump(exclude_unset=True)
    
    # 如果更新密码，需要哈希处理
    if "password" in update_data:
        update_data["hashed_password"] = f"hashed_{update_data.pop('password')}"
    
    user = user_dal.update(user_id, update_data)
    
    return ResponseModel(
        message="用户更新成功",
        data=UserResponse.model_validate(user)
    )


@router.delete(
    "/{user_id}",
    response_model=ResponseModel[None],
    summary="删除用户",
    description="删除指定用户"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    删除用户
    
    Args:
        user_id: 用户ID
        db: 数据库会话
        
    Returns:
        删除结果
    """
    user_dal = UserDAL(db)
    
    if not user_dal.exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 ID {user_id} 不存在"
        )
    
    success = user_dal.delete(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除用户失败"
        )
    
    return ResponseModel(
        message="用户删除成功"
    )


@router.get(
    "/search/by-name",
    response_model=ResponseModel[UserList],
    summary="搜索用户",
    description="根据姓名搜索用户"
)
def search_users(
    search_term: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=100, ge=1, le=100, description="返回的最大记录数"),
    db: Session = Depends(get_db)
):
    """
    搜索用户
    
    Args:
        search_term: 搜索关键词
        skip: 跳过的记录数
        limit: 返回的最大记录数
        db: 数据库会话
        
    Returns:
        搜索结果
    """
    user_dal = UserDAL(db)
    users = user_dal.search_by_name(search_term, skip=skip, limit=limit)
    
    return ResponseModel(
        data=UserList(
            total=len(users),
            items=[UserResponse.model_validate(user) for user in users]
        )
    )

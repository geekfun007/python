"""
用户服务
处理用户相关的业务逻辑
"""
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, NotFoundException
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.base import PaginatedResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate


class UserService:
    """用户服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def get_user(self, user_id: int) -> UserResponse:
        """
        获取用户详情
        
        Args:
            user_id: 用户ID
        
        Returns:
            用户信息
        
        Raises:
            NotFoundException: 用户不存在
        """
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundException("用户不存在")
        return UserResponse.model_validate(user)
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """
        根据邮箱获取用户
        
        Args:
            email: 用户邮箱
        
        Returns:
            用户信息或None
        """
        user = await self.user_repo.get_by_email(email)
        if user:
            return UserResponse.model_validate(user)
        return None
    
    async def get_users(
        self,
        page: int = 1,
        page_size: int = 20,
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[UserResponse]:
        """
        获取用户列表（分页）
        
        Args:
            page: 页码
            page_size: 每页数量
            is_active: 是否激活过滤
        
        Returns:
            分页的用户列表
        """
        skip = (page - 1) * page_size
        filters = {}
        if is_active is not None:
            filters["is_active"] = is_active
        
        users = await self.user_repo.get_multi(
            skip=skip,
            limit=page_size,
            filters=filters,
            order_by="created_at",
            order_desc=True,
        )
        total = await self.user_repo.count(filters)
        
        user_responses = [UserResponse.model_validate(user) for user in users]
        
        return PaginatedResponse.create(
            items=user_responses,
            total=total,
            page=page,
            page_size=page_size,
        )
    
    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
        current_user: User,
    ) -> UserResponse:
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            user_data: 更新数据
            current_user: 当前操作用户
        
        Returns:
            更新后的用户信息
        
        Raises:
            NotFoundException: 用户不存在
            BadRequestException: 邮箱或用户名已被使用
        """
        # 检查用户是否存在
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundException("用户不存在")
        
        # 只有管理员或用户本人可以修改
        if not current_user.is_superuser and current_user.id != user_id:
            raise BadRequestException("无权修改此用户")
        
        update_dict = user_data.model_dump(exclude_unset=True)
        
        # 检查邮箱是否已被使用
        if "email" in update_dict and update_dict["email"] != user.email:
            existing = await self.user_repo.get_by_email(update_dict["email"])
            if existing:
                raise BadRequestException("该邮箱已被使用")
        
        # 检查用户名是否已被使用
        if "username" in update_dict and update_dict["username"] != user.username:
            existing = await self.user_repo.get_by_username(update_dict["username"])
            if existing:
                raise BadRequestException("该用户名已被使用")
        
        # 处理密码
        if "password" in update_dict:
            update_dict["hashed_password"] = get_password_hash(update_dict.pop("password"))
        
        # 非管理员不能修改 is_active 和 is_superuser
        if not current_user.is_superuser:
            update_dict.pop("is_active", None)
            update_dict.pop("is_superuser", None)
        
        updated_user = await self.user_repo.update(user_id, update_dict)
        return UserResponse.model_validate(updated_user)
    
    async def delete_user(self, user_id: int, current_user: User) -> bool:
        """
        删除用户
        
        Args:
            user_id: 用户ID
            current_user: 当前操作用户
        
        Returns:
            是否删除成功
        
        Raises:
            NotFoundException: 用户不存在
            BadRequestException: 无权删除
        """
        # 检查用户是否存在
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundException("用户不存在")
        
        # 只有管理员可以删除用户
        if not current_user.is_superuser:
            raise BadRequestException("无权删除用户")
        
        # 不能删除自己
        if current_user.id == user_id:
            raise BadRequestException("不能删除自己")
        
        return await self.user_repo.delete(user_id)
    
    async def activate_user(self, user_id: int) -> UserResponse:
        """
        激活用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            更新后的用户信息
        """
        user = await self.user_repo.update(user_id, {"is_active": True})
        if not user:
            raise NotFoundException("用户不存在")
        return UserResponse.model_validate(user)
    
    async def deactivate_user(self, user_id: int) -> UserResponse:
        """
        禁用用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            更新后的用户信息
        """
        user = await self.user_repo.update(user_id, {"is_active": False})
        if not user:
            raise NotFoundException("用户不存在")
        return UserResponse.model_validate(user)

"""
User Service
用户服务层
"""

from typing import Tuple, List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dal.user_dal import UserDAL
from app.models.user import User, UserStatus, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse


class UserService:
    """
    用户服务类
    
    提供用户相关的业务逻辑:
    - 用户注册
    - 用户信息管理
    - 用户查询
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_dal = UserDAL(db)
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        创建新用户（注册）
        
        Args:
            user_data: 用户创建数据
        
        Returns:
            创建的用户实例
        
        Raises:
            HTTPException: 邮箱或用户名已存在时抛出 400 错误
        """
        # 检查邮箱是否已存在
        if await self.user_dal.check_email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被注册"
            )
        
        # 检查用户名是否已存在
        if await self.user_dal.check_username_exists(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该用户名已被使用"
            )
        
        # 创建用户
        user = await self.user_dal.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            phone=user_data.phone,
            avatar=user_data.avatar,
        )
        
        return user
    
    async def get_user(self, user_id: int) -> User:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            用户实例
        
        Raises:
            HTTPException: 用户不存在时抛出 404 错误
        """
        user = await self.user_dal.get(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return user
    
    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
        current_user: User
    ) -> User:
        """
        更新用户信息
        
        Args:
            user_id: 要更新的用户ID
            user_data: 更新数据
            current_user: 当前登录用户
        
        Returns:
            更新后的用户实例
        
        Raises:
            HTTPException: 权限不足或数据冲突时抛出错误
        """
        # 检查权限：只能更新自己的信息，除非是管理员
        if user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改其他用户信息"
            )
        
        # 检查用户是否存在
        user = await self.user_dal.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 检查邮箱唯一性
        if user_data.email and user_data.email != user.email:
            if await self.user_dal.check_email_exists(user_data.email, user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该邮箱已被使用"
                )
        
        # 检查用户名唯一性
        if user_data.username and user_data.username != user.username:
            if await self.user_dal.check_username_exists(user_data.username, user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该用户名已被使用"
                )
        
        # 非管理员不能修改状态和角色
        update_dict = user_data.model_dump(exclude_unset=True)
        if not current_user.is_admin:
            update_dict.pop("status", None)
            update_dict.pop("role", None)
        
        # 更新用户
        updated_user = await self.user_dal.update(user_id, update_dict)
        
        return updated_user
    
    async def delete_user(self, user_id: int, current_user: User) -> bool:
        """
        删除用户（软删除）
        
        Args:
            user_id: 用户ID
            current_user: 当前登录用户
        
        Returns:
            是否删除成功
        
        Raises:
            HTTPException: 权限不足或用户不存在时抛出错误
        """
        # 只有管理员可以删除用户
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员权限"
            )
        
        # 不能删除自己
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能删除自己的账户"
            )
        
        user = await self.user_dal.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 软删除
        await self.user_dal.update(user_id, {"status": UserStatus.DELETED})
        return True
    
    async def get_users(
        self,
        page: int = 1,
        page_size: int = 20,
        status: UserStatus = None,
        role: UserRole = None,
        keyword: str = None,
    ) -> UserListResponse:
        """
        获取用户列表
        
        Args:
            page: 页码
            page_size: 每页数量
            status: 状态过滤
            role: 角色过滤
            keyword: 搜索关键词
        
        Returns:
            用户列表响应
        """
        skip = (page - 1) * page_size
        
        users, total = await self.user_dal.get_users(
            skip=skip,
            limit=page_size,
            status=status,
            role=role,
            keyword=keyword,
        )
        
        return UserListResponse(
            users=[UserResponse.model_validate(u) for u in users],
            total=total,
            page=page,
            page_size=page_size,
        )
    
    async def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> bool:
        """
        修改密码
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
        
        Returns:
            是否修改成功
        
        Raises:
            HTTPException: 旧密码错误时抛出 400 错误
        """
        from app.core.security import verify_password
        
        user = await self.user_dal.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 验证旧密码
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="旧密码错误"
            )
        
        # 更新密码
        await self.user_dal.update_password(user_id, new_password)
        return True

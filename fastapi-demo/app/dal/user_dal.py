"""
User DAL
用户数据访问层
"""

from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base_dal import BaseDAL
from app.models.user import User, UserStatus, UserRole
from app.core.security import get_password_hash, verify_password


class UserDAL(BaseDAL[User]):
    """
    用户数据访问层
    
    提供用户相关的数据库操作:
    - 用户创建、查询、更新、删除
    - 用户认证
    - 用户状态管理
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        phone: Optional[str] = None,
        avatar: Optional[str] = None,
        status: UserStatus = UserStatus.ACTIVE,
        role: UserRole = UserRole.USER,
    ) -> User:
        """
        创建新用户
        
        Args:
            username: 用户名
            email: 邮箱
            password: 明文密码（会自动哈希）
            phone: 手机号
            avatar: 头像URL
            status: 用户状态
            role: 用户角色
        
        Returns:
            创建的用户实例
        """
        user_data = {
            "username": username,
            "email": email,
            "password_hash": get_password_hash(password),
            "phone": phone,
            "avatar": avatar,
            "status": status,
            "role": role,
        }
        return await self.create(user_data)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            email: 用户邮箱
        
        Returns:
            用户实例或 None
        """
        return await self.get_by_field("email", email)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
        
        Returns:
            用户实例或 None
        """
        return await self.get_by_field("username", username)
    
    async def authenticate(
        self,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        用户认证
        
        Args:
            email: 用户邮箱
            password: 明文密码
        
        Returns:
            认证成功返回用户实例，失败返回 None
        """
        user = await self.get_by_email(email)
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        if user.status != UserStatus.ACTIVE:
            return None
        
        # 更新最后登录时间
        await self.update_last_login(user.id)
        
        return user
    
    async def update_last_login(self, user_id: int) -> None:
        """
        更新用户最后登录时间
        
        Args:
            user_id: 用户ID
        """
        await self.update(user_id, {"last_login_at": datetime.utcnow()})
    
    async def update_password(
        self,
        user_id: int,
        new_password: str
    ) -> bool:
        """
        更新用户密码
        
        Args:
            user_id: 用户ID
            new_password: 新密码（明文）
        
        Returns:
            是否更新成功
        """
        result = await self.update(
            user_id,
            {"password_hash": get_password_hash(new_password)}
        )
        return result is not None
    
    async def check_email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """
        检查邮箱是否已存在
        
        Args:
            email: 邮箱
            exclude_id: 排除的用户ID（用于更新时检查）
        
        Returns:
            是否存在
        """
        stmt = select(func.count()).select_from(User).where(User.email == email)
        
        if exclude_id:
            stmt = stmt.where(User.id != exclude_id)
        
        result = await self.db.execute(stmt)
        return (result.scalar() or 0) > 0
    
    async def check_username_exists(self, username: str, exclude_id: Optional[int] = None) -> bool:
        """
        检查用户名是否已存在
        
        Args:
            username: 用户名
            exclude_id: 排除的用户ID
        
        Returns:
            是否存在
        """
        stmt = select(func.count()).select_from(User).where(User.username == username)
        
        if exclude_id:
            stmt = stmt.where(User.id != exclude_id)
        
        result = await self.db.execute(stmt)
        return (result.scalar() or 0) > 0
    
    async def get_users(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        status: Optional[UserStatus] = None,
        role: Optional[UserRole] = None,
        keyword: Optional[str] = None,
    ) -> Tuple[List[User], int]:
        """
        获取用户列表（支持过滤和搜索）
        
        Args:
            skip: 跳过记录数
            limit: 返回记录数
            status: 过滤状态
            role: 过滤角色
            keyword: 搜索关键词（用户名或邮箱）
        
        Returns:
            (用户列表, 总数)
        """
        filters = []
        
        if status is not None:
            filters.append(User.status == status)
        
        if role is not None:
            filters.append(User.role == role)
        
        if keyword:
            filters.append(
                or_(
                    User.username.contains(keyword),
                    User.email.contains(keyword)
                )
            )
        
        # 获取总数
        total = await self.count(filters)
        
        # 获取列表
        users = await self.get_multi(
            skip=skip,
            limit=limit,
            filters=filters,
            order_by=User.created_at.desc()
        )
        
        return users, total
    
    async def ban_user(self, user_id: int) -> Optional[User]:
        """
        封禁用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            更新后的用户实例
        """
        return await self.update(user_id, {"status": UserStatus.BANNED})
    
    async def activate_user(self, user_id: int) -> Optional[User]:
        """
        激活用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            更新后的用户实例
        """
        return await self.update(user_id, {"status": UserStatus.ACTIVE})

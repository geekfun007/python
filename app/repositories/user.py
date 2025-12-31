"""
用户 Repository
用户数据访问层
"""
from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户仓库类"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            email: 用户邮箱
        
        Returns:
            用户实例或None
        """
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
        
        Returns:
            用户实例或None
        """
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email_or_username(
        self, email: str, username: str
    ) -> Optional[User]:
        """
        根据邮箱或用户名获取用户
        
        Args:
            email: 用户邮箱
            username: 用户名
        
        Returns:
            用户实例或None
        """
        query = select(User).where(
            or_(User.email == email, User.username == username)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def authenticate(
        self, email: str, password: str
    ) -> Optional[User]:
        """
        验证用户凭据
        
        Args:
            email: 用户邮箱
            password: 密码
        
        Returns:
            验证通过返回用户，否则返回None
        """
        from app.core.security import verify_password
        
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def is_active(self, user: User) -> bool:
        """检查用户是否激活"""
        return user.is_active
    
    async def is_superuser(self, user: User) -> bool:
        """检查用户是否为超级管理员"""
        return user.is_superuser
    
    async def set_password(self, user_id: int, hashed_password: str) -> bool:
        """
        设置用户密码
        
        Args:
            user_id: 用户ID
            hashed_password: 密码哈希
        
        Returns:
            是否设置成功
        """
        result = await self.update(user_id, {"hashed_password": hashed_password})
        return result is not None

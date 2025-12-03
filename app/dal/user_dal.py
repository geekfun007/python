"""
User Data Access Layer
用户数据访问层 - 封装用户相关的数据库操作
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.dal.base import BaseDAL
from app.models.user import User


class UserDAL(BaseDAL[User]):
    """
    用户DAL
    
    继承BaseDAL，获得基础CRUD功能
    添加用户特定的查询方法
    """
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
            
        Returns:
            用户实例或None
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            email: 邮箱
            
        Returns:
            用户实例或None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        获取所有激活用户
        
        Args:
            skip: 跳过记录数
            limit: 返回最大记录数
            
        Returns:
            用户列表
        """
        return (
            self.db.query(User)
            .filter(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_by_name(self, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        根据姓名搜索用户（模糊搜索）
        
        Args:
            search_term: 搜索词
            skip: 跳过记录数
            limit: 返回最大记录数
            
        Returns:
            用户列表
            
        原理：
        - like() 实现模糊查询
        - % 是SQL通配符
        """
        return (
            self.db.query(User)
            .filter(User.full_name.like(f"%{search_term}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        用户认证（示例）
        
        注意：实际应用中应该使用密码哈希验证
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            认证成功返回用户实例，否则返回None
        """
        user = self.get_by_username(username)
        if not user:
            return None
        # 这里应该使用 bcrypt 或 passlib 验证密码
        # if not verify_password(password, user.hashed_password):
        #     return None
        return user
    
    def update_last_login(self, user_id: int) -> Optional[User]:
        """
        更新用户最后登录时间（示例）
        
        Args:
            user_id: 用户ID
            
        Returns:
            更新后的用户实例
        """
        from datetime import datetime
        return self.update(user_id, {"updated_at": datetime.now()})

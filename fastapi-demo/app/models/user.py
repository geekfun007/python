"""
User Model
用户数据模型
"""

import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, SmallInteger
from sqlalchemy.orm import relationship

from .base import BaseModel


class UserStatus(enum.IntEnum):
    """用户状态枚举"""
    INACTIVE = 0    # 未激活
    ACTIVE = 1      # 已激活
    BANNED = 2      # 已封禁
    DELETED = 3     # 已删除


class UserRole(enum.IntEnum):
    """用户角色枚举"""
    USER = 0        # 普通用户
    ADMIN = 1       # 管理员
    SUPER_ADMIN = 2 # 超级管理员


class User(BaseModel):
    """
    用户模型
    
    Attributes:
        id: 用户ID
        username: 用户名（唯一）
        email: 邮箱（唯一）
        password_hash: 密码哈希
        phone: 手机号
        avatar: 头像URL
        status: 用户状态
        role: 用户角色
        last_login_at: 最后登录时间
    """
    
    __tablename__ = "users"
    
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="用户名"
    )
    
    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="邮箱"
    )
    
    password_hash = Column(
        String(255),
        nullable=False,
        comment="密码哈希"
    )
    
    phone = Column(
        String(20),
        nullable=True,
        comment="手机号"
    )
    
    avatar = Column(
        String(500),
        nullable=True,
        comment="头像URL"
    )
    
    status = Column(
        SmallInteger,
        nullable=False,
        default=UserStatus.INACTIVE,
        index=True,
        comment="状态: 0-未激活, 1-已激活, 2-已封禁, 3-已删除"
    )
    
    role = Column(
        SmallInteger,
        nullable=False,
        default=UserRole.USER,
        index=True,
        comment="角色: 0-普通用户, 1-管理员, 2-超级管理员"
    )
    
    last_login_at = Column(
        DateTime,
        nullable=True,
        comment="最后登录时间"
    )
    
    # 关系定义
    articles = relationship(
        "Article",
        back_populates="author",
        lazy="dynamic"
    )
    
    comments = relationship(
        "Comment",
        back_populates="user",
        lazy="dynamic"
    )
    
    likes = relationship(
        "UserLike",
        back_populates="user",
        lazy="dynamic"
    )
    
    favorites = relationship(
        "UserFavorite",
        back_populates="user",
        lazy="dynamic"
    )
    
    @property
    def is_active(self) -> bool:
        """用户是否激活"""
        return self.status == UserStatus.ACTIVE
    
    @property
    def is_admin(self) -> bool:
        """用户是否是管理员"""
        return self.role >= UserRole.ADMIN
    
    @property
    def is_super_admin(self) -> bool:
        """用户是否是超级管理员"""
        return self.role == UserRole.SUPER_ADMIN
    
    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

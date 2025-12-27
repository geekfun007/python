"""用户模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class User(Base):
    """用户数据库模型
    
    Attributes:
        id: 用户ID（主键）
        email: 邮箱（唯一）
        username: 用户名（唯一）
        hashed_password: 哈希后的密码
        full_name: 全名
        is_active: 是否激活
        is_superuser: 是否是超级管理员
        created_at: 创建时间
        updated_at: 更新时间
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系：一个用户可以有多个 items
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

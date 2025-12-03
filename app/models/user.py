"""
User Model - 用户模型
演示 SQLAlchemy ORM 的基本用法
"""
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class User(BaseModel):
    """
    用户模型
    
    ORM原理：
    - 每个类对应数据库中的一张表
    - 每个类属性对应表中的一列
    - Column定义列的类型、约束等
    """
    __tablename__ = "users"
    
    # 基本字段
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
    hashed_password = Column(String(255), nullable=False, comment="加密密码")
    full_name = Column(String(100), nullable=True, comment="全名")
    age = Column(Integer, nullable=True, comment="年龄")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_superuser = Column(Boolean, default=False, comment="是否超级用户")
    
    # 关系映射（一对多）
    # 一个用户可以有多个产品
    # products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "age": self.age,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

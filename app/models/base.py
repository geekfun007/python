"""
Base Model with Common Fields
所有模型的基类，包含通用字段
"""
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class BaseModel(Base):
    """
    抽象基类，包含所有表的通用字段
    
    字段说明：
    - id: 主键，自增
    - created_at: 创建时间，自动设置
    - updated_at: 更新时间，自动更新
    """
    __abstract__ = True  # 标记为抽象类，不会创建对应的表
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

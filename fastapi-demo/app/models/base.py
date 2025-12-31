"""
Base Model
ORM 模型基类
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, BigInteger
from sqlalchemy.orm import declared_attr

from app.core.database import Base


class TimestampMixin:
    """
    时间戳混入类
    自动添加 created_at 和 updated_at 字段
    """
    
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow,
            comment="创建时间"
        )
    
    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            comment="更新时间"
        )


class BaseModel(Base, TimestampMixin):
    """
    模型基类
    所有模型继承此类获得：
    - id 主键
    - created_at 创建时间
    - updated_at 更新时间
    """
    
    __abstract__ = True
    
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )
    
    def to_dict(self) -> dict:
        """将模型转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"

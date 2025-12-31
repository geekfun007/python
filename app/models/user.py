"""
用户 ORM 模型
定义用户表结构
"""
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.item import Item


class User(Base, TimestampMixin):
    """
    用户模型
    
    Attributes:
        id: 主键ID
        email: 邮箱（唯一）
        username: 用户名（唯一）
        full_name: 全名
        hashed_password: 密码哈希
        is_active: 是否激活
        is_superuser: 是否为超级管理员
        items: 用户拥有的物品列表
    """
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # 关系
    items: Mapped[List["Item"]] = relationship(
        "Item",
        back_populates="owner",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

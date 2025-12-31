"""
物品 ORM 模型
定义物品表结构
"""
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, SoftDeleteMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Item(Base, TimestampMixin, SoftDeleteMixin):
    """
    物品模型
    
    Attributes:
        id: 主键ID
        title: 标题
        description: 描述
        price: 价格
        category: 分类
        status: 状态
        stock: 库存数量
        owner_id: 所有者ID
        owner: 所有者用户对象
    """
    
    __tablename__ = "items"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False
    )
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, default="other", index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="draft", index=True
    )
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # 外键
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # 关系
    owner: Mapped["User"] = relationship("User", back_populates="items")
    
    def __repr__(self) -> str:
        return f"<Item(id={self.id}, title={self.title}, price={self.price})>"

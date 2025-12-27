"""商品模型"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


# 多对多关系的关联表
item_tags = Table(
    "item_tags",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


class Tag(Base):
    """标签模型"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    # 多对多关系
    items = relationship("Item", secondary=item_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"


class Item(Base):
    """商品数据库模型
    
    Attributes:
        id: 商品ID（主键）
        name: 商品名称
        description: 商品描述
        price: 价格
        stock: 库存数量
        is_active: 是否上架
        owner_id: 所属用户ID（外键）
        created_at: 创建时间
        updated_at: 更新时间
    """
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    owner = relationship("User", back_populates="items")
    tags = relationship("Tag", secondary=item_tags, back_populates="items")
    
    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name})>"

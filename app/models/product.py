"""
Product Model - 产品模型
演示 SQLAlchemy 关系映射和外键
"""
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Product(BaseModel):
    """
    产品模型
    
    演示：
    - 外键关系 (ForeignKey)
    - 多对一关系 (Many-to-One)
    - relationship 的使用
    """
    __tablename__ = "products"
    
    # 基本字段
    name = Column(String(100), nullable=False, index=True, comment="产品名称")
    description = Column(Text, nullable=True, comment="产品描述")
    price = Column(Float, nullable=False, comment="价格")
    stock = Column(Integer, default=0, comment="库存数量")
    category = Column(String(50), nullable=True, index=True, comment="分类")
    
    # 外键 - 关联到用户表
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, comment="所有者ID")
    
    # 关系映射（多对一）
    # 多个产品属于一个用户
    # owner = relationship("User", back_populates="products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

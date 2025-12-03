"""
Product Data Access Layer
产品数据访问层 - 封装产品相关的数据库操作
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.dal.base import BaseDAL
from app.models.product import Product


class ProductDAL(BaseDAL[Product]):
    """
    产品DAL
    
    继承BaseDAL，获得基础CRUD功能
    添加产品特定的查询方法
    """
    
    def __init__(self, db: Session):
        super().__init__(Product, db)
    
    def get_by_name(self, name: str) -> Optional[Product]:
        """
        根据产品名称获取产品
        
        Args:
            name: 产品名称
            
        Returns:
            产品实例或None
        """
        return self.db.query(Product).filter(Product.name == name).first()
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        根据分类获取产品
        
        Args:
            category: 分类名称
            skip: 跳过记录数
            limit: 返回最大记录数
            
        Returns:
            产品列表
        """
        return (
            self.db.query(Product)
            .filter(Product.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        根据所有者ID获取产品
        
        Args:
            owner_id: 所有者ID
            skip: 跳过记录数
            limit: 返回最大记录数
            
        Returns:
            产品列表
        """
        return (
            self.db.query(Product)
            .filter(Product.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_by_name(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        根据名称搜索产品（模糊搜索）
        
        Args:
            search_term: 搜索词
            skip: 跳过记录数
            limit: 返回最大记录数
            
        Returns:
            产品列表
        """
        return (
            self.db.query(Product)
            .filter(Product.name.like(f"%{search_term}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_price_range(
        self, 
        min_price: float, 
        max_price: float, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        """
        根据价格范围获取产品
        
        Args:
            min_price: 最低价格
            max_price: 最高价格
            skip: 跳过记录数
            limit: 返回最大记录数
            
        Returns:
            产品列表
            
        原理：
        - and_() 实现多个条件的AND逻辑
        - between() 也可以用来实现范围查询
        """
        return (
            self.db.query(Product)
            .filter(and_(Product.price >= min_price, Product.price <= max_price))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_in_stock(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        获取有库存的产品
        
        Args:
            skip: 跳过记录数
            limit: 返回最大记录数
            
        Returns:
            产品列表
        """
        return (
            self.db.query(Product)
            .filter(Product.stock > 0)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        """
        更新产品库存
        
        Args:
            product_id: 产品ID
            quantity: 库存变化量（正数增加，负数减少）
            
        Returns:
            更新后的产品实例或None
        """
        product = self.get_by_id(product_id)
        if not product:
            return None
        
        new_stock = product.stock + quantity
        if new_stock < 0:
            new_stock = 0
        
        return self.update(product_id, {"stock": new_stock})
    
    def get_statistics_by_category(self) -> List[dict]:
        """
        按分类统计产品数量
        
        Returns:
            统计结果列表
            
        原理：
        - func.count() 聚合函数
        - group_by() 分组查询
        """
        from sqlalchemy import func
        
        result = (
            self.db.query(
                Product.category,
                func.count(Product.id).label("count"),
                func.avg(Product.price).label("avg_price"),
                func.sum(Product.stock).label("total_stock")
            )
            .group_by(Product.category)
            .all()
        )
        
        return [
            {
                "category": row.category,
                "count": row.count,
                "avg_price": float(row.avg_price) if row.avg_price else 0,
                "total_stock": row.total_stock or 0
            }
            for row in result
        ]

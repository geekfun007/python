"""
物品 Repository
物品数据访问层
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.repositories.base import BaseRepository
from app.schemas.item import ItemStatus


class ItemRepository(BaseRepository[Item]):
    """物品仓库类"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Item, db)
    
    async def get_by_owner(
        self,
        owner_id: int,
        *,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[Item]:
        """
        获取用户的物品列表
        
        Args:
            owner_id: 所有者ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            include_deleted: 是否包含已删除的物品
        
        Returns:
            物品列表
        """
        query = select(Item).where(Item.owner_id == owner_id)
        
        if not include_deleted:
            query = query.where(Item.deleted_at.is_(None))
        
        query = query.offset(skip).limit(limit).order_by(Item.created_at.desc())
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def search(
        self,
        *,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Item], int]:
        """
        搜索物品
        
        Args:
            keyword: 搜索关键词（标题或描述）
            category: 分类
            status: 状态
            min_price: 最低价格
            max_price: 最高价格
            owner_id: 所有者ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
        
        Returns:
            (物品列表, 总数)
        """
        conditions = [Item.deleted_at.is_(None)]
        
        if keyword:
            conditions.append(
                or_(
                    Item.title.ilike(f"%{keyword}%"),
                    Item.description.ilike(f"%{keyword}%"),
                )
            )
        
        if category:
            conditions.append(Item.category == category)
        
        if status:
            conditions.append(Item.status == status)
        
        if min_price is not None:
            conditions.append(Item.price >= min_price)
        
        if max_price is not None:
            conditions.append(Item.price <= max_price)
        
        if owner_id is not None:
            conditions.append(Item.owner_id == owner_id)
        
        # 查询数据
        query = (
            select(Item)
            .where(and_(*conditions))
            .offset(skip)
            .limit(limit)
            .order_by(Item.created_at.desc())
        )
        result = await self.db.execute(query)
        items = list(result.scalars().all())
        
        # 查询总数
        count_query = select(func.count(Item.id)).where(and_(*conditions))
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        
        return items, total
    
    async def soft_delete(self, item_id: int) -> bool:
        """
        软删除物品
        
        Args:
            item_id: 物品ID
        
        Returns:
            是否删除成功
        """
        result = await self.update(item_id, {"deleted_at": datetime.utcnow()})
        return result is not None
    
    async def restore(self, item_id: int) -> Optional[Item]:
        """
        恢复软删除的物品
        
        Args:
            item_id: 物品ID
        
        Returns:
            恢复的物品或None
        """
        return await self.update(item_id, {"deleted_at": None})
    
    async def update_status(
        self, item_id: int, status: ItemStatus
    ) -> Optional[Item]:
        """
        更新物品状态
        
        Args:
            item_id: 物品ID
            status: 新状态
        
        Returns:
            更新后的物品或None
        """
        return await self.update(item_id, {"status": status.value})
    
    async def update_stock(
        self, item_id: int, quantity: int
    ) -> Optional[Item]:
        """
        更新库存（增加或减少）
        
        Args:
            item_id: 物品ID
            quantity: 变化量（正数增加，负数减少）
        
        Returns:
            更新后的物品或None
        """
        item = await self.get(item_id)
        if not item:
            return None
        
        new_stock = max(0, item.stock + quantity)
        return await self.update(item_id, {"stock": new_stock})
    
    async def count_by_owner(self, owner_id: int) -> int:
        """
        统计用户的物品数量
        
        Args:
            owner_id: 所有者ID
        
        Returns:
            物品数量
        """
        query = select(func.count(Item.id)).where(
            and_(Item.owner_id == owner_id, Item.deleted_at.is_(None))
        )
        result = await self.db.execute(query)
        return result.scalar() or 0
    
    async def get_active_items(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Item]:
        """
        获取所有上架的物品
        
        Args:
            skip: 跳过的记录数
            limit: 返回的最大记录数
        
        Returns:
            物品列表
        """
        query = (
            select(Item)
            .where(
                and_(
                    Item.status == ItemStatus.ACTIVE.value,
                    Item.deleted_at.is_(None),
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(Item.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

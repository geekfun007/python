"""
物品服务
处理物品相关的业务逻辑
"""
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from app.models.user import User
from app.repositories.item import ItemRepository
from app.schemas.base import PaginatedResponse
from app.schemas.item import (
    ItemCreate,
    ItemResponse,
    ItemStatus,
    ItemUpdate,
    ItemWithOwner,
)


class ItemService:
    """物品服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.item_repo = ItemRepository(db)
    
    async def create_item(
        self,
        item_data: ItemCreate,
        owner: User,
    ) -> ItemResponse:
        """
        创建物品
        
        Args:
            item_data: 物品数据
            owner: 所有者
        
        Returns:
            创建的物品信息
        """
        item_dict = item_data.model_dump()
        item_dict["owner_id"] = owner.id
        item_dict["status"] = ItemStatus.DRAFT.value
        item_dict["category"] = item_dict["category"].value
        
        item = await self.item_repo.create(item_dict)
        return ItemResponse.model_validate(item)
    
    async def get_item(self, item_id: int) -> ItemResponse:
        """
        获取物品详情
        
        Args:
            item_id: 物品ID
        
        Returns:
            物品信息
        
        Raises:
            NotFoundException: 物品不存在
        """
        item = await self.item_repo.get(item_id)
        if not item or item.deleted_at:
            raise NotFoundException("物品不存在")
        return ItemResponse.model_validate(item)
    
    async def get_item_with_owner(self, item_id: int) -> ItemWithOwner:
        """
        获取物品详情（包含所有者信息）
        
        Args:
            item_id: 物品ID
        
        Returns:
            物品信息（含所有者）
        """
        item = await self.item_repo.get(item_id)
        if not item or item.deleted_at:
            raise NotFoundException("物品不存在")
        
        item_dict = ItemResponse.model_validate(item).model_dump()
        item_dict["owner_username"] = item.owner.username if item.owner else None
        return ItemWithOwner(**item_dict)
    
    async def get_items(
        self,
        page: int = 1,
        page_size: int = 20,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        owner_id: Optional[int] = None,
    ) -> PaginatedResponse[ItemResponse]:
        """
        获取物品列表（分页、搜索）
        
        Args:
            page: 页码
            page_size: 每页数量
            keyword: 搜索关键词
            category: 分类过滤
            status: 状态过滤
            min_price: 最低价格
            max_price: 最高价格
            owner_id: 所有者ID
        
        Returns:
            分页的物品列表
        """
        skip = (page - 1) * page_size
        
        items, total = await self.item_repo.search(
            keyword=keyword,
            category=category,
            status=status,
            min_price=min_price,
            max_price=max_price,
            owner_id=owner_id,
            skip=skip,
            limit=page_size,
        )
        
        item_responses = [ItemResponse.model_validate(item) for item in items]
        
        return PaginatedResponse.create(
            items=item_responses,
            total=total,
            page=page,
            page_size=page_size,
        )
    
    async def get_my_items(
        self,
        owner: User,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedResponse[ItemResponse]:
        """
        获取我的物品列表
        
        Args:
            owner: 所有者
            page: 页码
            page_size: 每页数量
        
        Returns:
            分页的物品列表
        """
        skip = (page - 1) * page_size
        
        items = await self.item_repo.get_by_owner(
            owner_id=owner.id,
            skip=skip,
            limit=page_size,
        )
        total = await self.item_repo.count_by_owner(owner.id)
        
        item_responses = [ItemResponse.model_validate(item) for item in items]
        
        return PaginatedResponse.create(
            items=item_responses,
            total=total,
            page=page,
            page_size=page_size,
        )
    
    async def update_item(
        self,
        item_id: int,
        item_data: ItemUpdate,
        current_user: User,
    ) -> ItemResponse:
        """
        更新物品
        
        Args:
            item_id: 物品ID
            item_data: 更新数据
            current_user: 当前用户
        
        Returns:
            更新后的物品信息
        
        Raises:
            NotFoundException: 物品不存在
            ForbiddenException: 无权修改
        """
        item = await self.item_repo.get(item_id)
        if not item or item.deleted_at:
            raise NotFoundException("物品不存在")
        
        # 检查权限
        if item.owner_id != current_user.id and not current_user.is_superuser:
            raise ForbiddenException("无权修改此物品")
        
        update_dict = item_data.model_dump(exclude_unset=True)
        
        # 处理枚举值
        if "category" in update_dict and update_dict["category"]:
            update_dict["category"] = update_dict["category"].value
        if "status" in update_dict and update_dict["status"]:
            update_dict["status"] = update_dict["status"].value
        
        updated_item = await self.item_repo.update(item_id, update_dict)
        return ItemResponse.model_validate(updated_item)
    
    async def delete_item(
        self,
        item_id: int,
        current_user: User,
        hard_delete: bool = False,
    ) -> bool:
        """
        删除物品
        
        Args:
            item_id: 物品ID
            current_user: 当前用户
            hard_delete: 是否硬删除
        
        Returns:
            是否删除成功
        
        Raises:
            NotFoundException: 物品不存在
            ForbiddenException: 无权删除
        """
        item = await self.item_repo.get(item_id)
        if not item:
            raise NotFoundException("物品不存在")
        
        # 检查权限
        if item.owner_id != current_user.id and not current_user.is_superuser:
            raise ForbiddenException("无权删除此物品")
        
        if hard_delete:
            return await self.item_repo.delete(item_id)
        else:
            return await self.item_repo.soft_delete(item_id)
    
    async def publish_item(
        self,
        item_id: int,
        current_user: User,
    ) -> ItemResponse:
        """
        上架物品
        
        Args:
            item_id: 物品ID
            current_user: 当前用户
        
        Returns:
            更新后的物品信息
        """
        item = await self.item_repo.get(item_id)
        if not item or item.deleted_at:
            raise NotFoundException("物品不存在")
        
        if item.owner_id != current_user.id and not current_user.is_superuser:
            raise ForbiddenException("无权操作此物品")
        
        if item.stock <= 0:
            raise BadRequestException("库存不足，无法上架")
        
        updated_item = await self.item_repo.update_status(item_id, ItemStatus.ACTIVE)
        return ItemResponse.model_validate(updated_item)
    
    async def unpublish_item(
        self,
        item_id: int,
        current_user: User,
    ) -> ItemResponse:
        """
        下架物品
        
        Args:
            item_id: 物品ID
            current_user: 当前用户
        
        Returns:
            更新后的物品信息
        """
        item = await self.item_repo.get(item_id)
        if not item or item.deleted_at:
            raise NotFoundException("物品不存在")
        
        if item.owner_id != current_user.id and not current_user.is_superuser:
            raise ForbiddenException("无权操作此物品")
        
        updated_item = await self.item_repo.update_status(item_id, ItemStatus.INACTIVE)
        return ItemResponse.model_validate(updated_item)
    
    async def update_stock(
        self,
        item_id: int,
        quantity: int,
        current_user: User,
    ) -> ItemResponse:
        """
        更新库存
        
        Args:
            item_id: 物品ID
            quantity: 变化量
            current_user: 当前用户
        
        Returns:
            更新后的物品信息
        """
        item = await self.item_repo.get(item_id)
        if not item or item.deleted_at:
            raise NotFoundException("物品不存在")
        
        if item.owner_id != current_user.id and not current_user.is_superuser:
            raise ForbiddenException("无权操作此物品")
        
        updated_item = await self.item_repo.update_stock(item_id, quantity)
        return ItemResponse.model_validate(updated_item)

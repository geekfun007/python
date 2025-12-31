"""
物品 API
处理物品的 CRUD 操作
"""
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.middlewares.auth import get_current_user, get_optional_user
from app.models.user import User
from app.schemas.base import BaseResponse, PaginatedResponse
from app.schemas.item import (
    ItemCategory,
    ItemCreate,
    ItemResponse,
    ItemStatus,
    ItemUpdate,
    ItemWithOwner,
)
from app.services.item import ItemService

router = APIRouter()


@router.post(
    "",
    response_model=BaseResponse[ItemResponse],
    summary="创建物品",
    description="创建新物品",
)
async def create_item(
    item_data: ItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    创建物品接口
    
    - **title**: 标题（1-200字符）
    - **description**: 描述（可选，最多2000字符）
    - **price**: 价格（>=0）
    - **category**: 分类
    - **stock**: 库存数量（>=0）
    """
    item_service = ItemService(db)
    item = await item_service.create_item(item_data, current_user)
    return BaseResponse.success(data=item, message="创建成功")


@router.get(
    "",
    response_model=BaseResponse[PaginatedResponse[ItemResponse]],
    summary="获取物品列表",
    description="获取物品列表（支持搜索和过滤）",
)
async def get_items(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(default=None, max_length=100, description="搜索关键词"),
    category: Optional[ItemCategory] = Query(default=None, description="分类"),
    status: Optional[ItemStatus] = Query(default=None, description="状态"),
    min_price: Optional[Decimal] = Query(default=None, ge=0, description="最低价格"),
    max_price: Optional[Decimal] = Query(default=None, ge=0, description="最高价格"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取物品列表接口
    
    支持分页、搜索和过滤
    
    - **page**: 页码
    - **page_size**: 每页数量
    - **keyword**: 搜索关键词（标题或描述）
    - **category**: 分类过滤
    - **status**: 状态过滤
    - **min_price**: 最低价格
    - **max_price**: 最高价格
    """
    item_service = ItemService(db)
    result = await item_service.get_items(
        page=page,
        page_size=page_size,
        keyword=keyword,
        category=category.value if category else None,
        status=status.value if status else None,
        min_price=min_price,
        max_price=max_price,
    )
    return BaseResponse.success(data=result, message="获取成功")


@router.get(
    "/me",
    response_model=BaseResponse[PaginatedResponse[ItemResponse]],
    summary="获取我的物品",
    description="获取当前用户的物品列表",
)
async def get_my_items(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    获取我的物品列表接口
    
    - **page**: 页码
    - **page_size**: 每页数量
    """
    item_service = ItemService(db)
    result = await item_service.get_my_items(
        owner=current_user,
        page=page,
        page_size=page_size,
    )
    return BaseResponse.success(data=result, message="获取成功")


@router.get(
    "/{item_id}",
    response_model=BaseResponse[ItemWithOwner],
    summary="获取物品详情",
    description="根据ID获取物品详情",
)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取物品详情接口
    
    - **item_id**: 物品ID
    """
    item_service = ItemService(db)
    item = await item_service.get_item_with_owner(item_id)
    return BaseResponse.success(data=item, message="获取成功")


@router.put(
    "/{item_id}",
    response_model=BaseResponse[ItemResponse],
    summary="更新物品",
    description="更新物品信息",
)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    更新物品信息接口
    
    只有物品所有者或管理员可以修改
    
    - **item_id**: 物品ID
    """
    item_service = ItemService(db)
    item = await item_service.update_item(item_id, item_data, current_user)
    return BaseResponse.success(data=item, message="更新成功")


@router.delete(
    "/{item_id}",
    response_model=BaseResponse,
    summary="删除物品",
    description="删除物品（软删除）",
)
async def delete_item(
    item_id: int,
    hard_delete: bool = Query(default=False, description="是否硬删除"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    删除物品接口
    
    只有物品所有者或管理员可以删除
    
    - **item_id**: 物品ID
    - **hard_delete**: 是否硬删除（默认软删除）
    """
    item_service = ItemService(db)
    await item_service.delete_item(item_id, current_user, hard_delete)
    return BaseResponse.success(message="删除成功")


@router.post(
    "/{item_id}/publish",
    response_model=BaseResponse[ItemResponse],
    summary="上架物品",
    description="将物品上架",
)
async def publish_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    上架物品接口
    
    - **item_id**: 物品ID
    """
    item_service = ItemService(db)
    item = await item_service.publish_item(item_id, current_user)
    return BaseResponse.success(data=item, message="上架成功")


@router.post(
    "/{item_id}/unpublish",
    response_model=BaseResponse[ItemResponse],
    summary="下架物品",
    description="将物品下架",
)
async def unpublish_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    下架物品接口
    
    - **item_id**: 物品ID
    """
    item_service = ItemService(db)
    item = await item_service.unpublish_item(item_id, current_user)
    return BaseResponse.success(data=item, message="下架成功")


@router.post(
    "/{item_id}/stock",
    response_model=BaseResponse[ItemResponse],
    summary="更新库存",
    description="更新物品库存",
)
async def update_stock(
    item_id: int,
    quantity: int = Query(..., description="库存变化量（正数增加，负数减少）"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    更新库存接口
    
    - **item_id**: 物品ID
    - **quantity**: 库存变化量
    """
    item_service = ItemService(db)
    item = await item_service.update_stock(item_id, quantity, current_user)
    return BaseResponse.success(data=item, message="库存更新成功")

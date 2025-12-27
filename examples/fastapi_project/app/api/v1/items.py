"""商品路由"""
from fastapi import APIRouter, Depends, Security, Query, status
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional

from ...database import get_db
from ...models.user import User
from ...schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    TagCreate,
    TagResponse
)
from ...crud.item import item_crud, tag_crud
from ..deps import get_current_active_user
from ...core.exceptions import NotFoundException, ForbiddenException

router = APIRouter()


# ==================== 标签相关 ====================

@router.get("/tags", response_model=List[TagResponse])
async def list_tags(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    获取所有标签
    
    不需要认证
    """
    return tag_crud.get_multi(db, skip=skip, limit=limit)


@router.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: TagCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Security(get_current_active_user, scopes=["write"])]
):
    """
    创建标签
    
    需要写入权限
    """
    # 检查标签是否已存在
    if tag_crud.get_by_name(db, name=tag_in.name):
        from ...core.exceptions import BadRequestException
        raise BadRequestException(detail="标签已存在")
    
    return tag_crud.create(db, obj_in=tag_in)


# ==================== 商品相关 ====================

@router.get("", response_model=List[ItemResponse])
async def list_items(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
    is_active: Optional[bool] = Query(True, description="过滤上架状态"),
    keyword: Optional[str] = Query(None, description="搜索关键词")
):
    """
    获取商品列表
    
    不需要认证（公开接口）
    
    - **skip**: 分页偏移量
    - **limit**: 返回数量
    - **is_active**: 过滤上架状态（默认只显示上架商品）
    - **keyword**: 搜索关键词
    """
    if keyword:
        return item_crud.search(db, keyword=keyword, skip=skip, limit=limit)
    
    return item_crud.get_multi(db, skip=skip, limit=limit, is_active=is_active)


@router.get("/my", response_model=List[ItemResponse])
async def list_my_items(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    获取我的商品列表
    
    需要认证
    """
    return item_crud.get_by_owner(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    """
    获取商品详情
    
    不需要认证
    """
    item = item_crud.get(db, item_id=item_id)
    if not item:
        raise NotFoundException(detail="商品不存在")
    return item


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Security(get_current_active_user, scopes=["write"])]
):
    """
    创建商品
    
    需要写入权限
    
    - **name**: 商品名称
    - **description**: 商品描述
    - **price**: 价格
    - **stock**: 库存
    - **tag_ids**: 标签 ID 列表
    """
    item = item_crud.create(db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Security(get_current_active_user, scopes=["write"])]
):
    """
    更新商品
    
    需要写入权限，只能更新自己的商品（管理员可以更新任何商品）
    """
    item = item_crud.get(db, item_id=item_id)
    if not item:
        raise NotFoundException(detail="商品不存在")
    
    # 检查权限
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise ForbiddenException(detail="无权修改此商品")
    
    item = item_crud.update(db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Security(get_current_active_user, scopes=["write"])]
):
    """
    删除商品
    
    需要写入权限，只能删除自己的商品（管理员可以删除任何商品）
    """
    item = item_crud.get(db, item_id=item_id)
    if not item:
        raise NotFoundException(detail="商品不存在")
    
    # 检查权限
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise ForbiddenException(detail="无权删除此商品")
    
    item_crud.delete(db, item_id=item_id)
    return {"message": "商品已删除"}


@router.post("/{item_id}/stock", response_model=ItemResponse)
async def update_stock(
    item_id: int,
    quantity: int = Query(..., description="变化量（正数增加，负数减少）"),
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["write"])] = None
):
    """
    更新库存
    
    需要写入权限
    
    - **quantity**: 变化量（正数增加，负数减少）
    """
    item = item_crud.get(db, item_id=item_id)
    if not item:
        raise NotFoundException(detail="商品不存在")
    
    # 检查权限
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise ForbiddenException(detail="无权修改此商品库存")
    
    try:
        item = item_crud.update_stock(db, item_id=item_id, quantity=quantity)
        return item
    except ValueError as e:
        from ...core.exceptions import BadRequestException
        raise BadRequestException(detail=str(e))

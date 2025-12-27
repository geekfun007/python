"""商品 CRUD 操作"""
from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.item import Item, Tag
from ..schemas.item import ItemCreate, ItemUpdate, TagCreate


class TagCRUD:
    """标签 CRUD 操作类"""
    
    def get(self, db: Session, tag_id: int) -> Optional[Tag]:
        """根据 ID 获取标签"""
        return db.query(Tag).filter(Tag.id == tag_id).first()
    
    def get_by_name(self, db: Session, name: str) -> Optional[Tag]:
        """根据名称获取标签"""
        return db.query(Tag).filter(Tag.name == name).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Tag]:
        """获取多个标签"""
        return db.query(Tag).offset(skip).limit(limit).all()
    
    def get_by_ids(self, db: Session, tag_ids: List[int]) -> List[Tag]:
        """根据 ID 列表获取多个标签"""
        return db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    
    def create(self, db: Session, *, obj_in: TagCreate) -> Tag:
        """创建标签"""
        db_obj = Tag(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, tag_id: int) -> Optional[Tag]:
        """删除标签"""
        obj = db.query(Tag).get(tag_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


class ItemCRUD:
    """商品 CRUD 操作类"""
    
    def get(self, db: Session, item_id: int) -> Optional[Item]:
        """根据 ID 获取商品"""
        return db.query(Item).filter(Item.id == item_id).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> List[Item]:
        """获取多个商品"""
        query = db.query(Item)
        
        if owner_id is not None:
            query = query.filter(Item.owner_id == owner_id)
        if is_active is not None:
            query = query.filter(Item.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_owner(
        self,
        db: Session,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        """获取指定用户的商品"""
        return (
            db.query(Item)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search(
        self,
        db: Session,
        *,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        """搜索商品"""
        return (
            db.query(Item)
            .filter(
                Item.is_active == True,
                Item.name.ilike(f"%{keyword}%")
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(
        self,
        db: Session,
        *,
        obj_in: ItemCreate,
        owner_id: int
    ) -> Item:
        """创建商品"""
        # 获取标签
        tags = []
        if obj_in.tag_ids:
            tags = tag_crud.get_by_ids(db, obj_in.tag_ids)
        
        # 创建商品
        db_obj = Item(
            name=obj_in.name,
            description=obj_in.description,
            price=obj_in.price,
            stock=obj_in.stock,
            owner_id=owner_id,
            tags=tags
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: Item,
        obj_in: ItemUpdate
    ) -> Item:
        """更新商品"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # 处理标签
        if "tag_ids" in update_data:
            tag_ids = update_data.pop("tag_ids")
            if tag_ids is not None:
                db_obj.tags = tag_crud.get_by_ids(db, tag_ids)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, item_id: int) -> Optional[Item]:
        """删除商品"""
        obj = db.query(Item).get(item_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def update_stock(
        self,
        db: Session,
        *,
        item_id: int,
        quantity: int
    ) -> Optional[Item]:
        """更新库存
        
        Args:
            item_id: 商品 ID
            quantity: 变化量（正数增加，负数减少）
        """
        item = self.get(db, item_id)
        if not item:
            return None
        
        new_stock = item.stock + quantity
        if new_stock < 0:
            raise ValueError("库存不足")
        
        item.stock = new_stock
        db.add(item)
        db.commit()
        db.refresh(item)
        return item


# 创建单例
tag_crud = TagCRUD()
item_crud = ItemCRUD()

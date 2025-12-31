"""
商品/物品相关 Schema (IDL)
定义物品的请求和响应数据模型
"""
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import ConfigDict, Field, field_validator

from app.schemas.base import BaseSchema, TimestampMixin


class ItemStatus(str, Enum):
    """物品状态枚举"""
    
    DRAFT = "draft"          # 草稿
    ACTIVE = "active"        # 上架
    INACTIVE = "inactive"    # 下架
    DELETED = "deleted"      # 已删除


class ItemCategory(str, Enum):
    """物品分类枚举"""
    
    ELECTRONICS = "electronics"  # 电子产品
    CLOTHING = "clothing"        # 服装
    FOOD = "food"                # 食品
    BOOKS = "books"              # 图书
    OTHER = "other"              # 其他


# ============== 物品基础 Schema ==============

class ItemBase(BaseSchema):
    """物品基础模型"""
    
    title: str = Field(..., min_length=1, max_length=200, description="标题")
    description: Optional[str] = Field(None, max_length=2000, description="描述")
    price: Decimal = Field(..., ge=0, decimal_places=2, description="价格")
    category: ItemCategory = Field(default=ItemCategory.OTHER, description="分类")


# ============== 创建物品 ==============

class ItemCreate(ItemBase):
    """创建物品请求模型"""
    
    stock: int = Field(default=0, ge=0, description="库存数量")
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, v: Decimal) -> Decimal:
        """价格验证"""
        if v < 0:
            raise ValueError("价格不能为负数")
        return round(v, 2)
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """标题验证"""
        return v.strip()


# ============== 更新物品 ==============

class ItemUpdate(BaseSchema):
    """更新物品请求模型"""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="标题")
    description: Optional[str] = Field(None, max_length=2000, description="描述")
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="价格")
    category: Optional[ItemCategory] = Field(None, description="分类")
    status: Optional[ItemStatus] = Field(None, description="状态")
    stock: Optional[int] = Field(None, ge=0, description="库存数量")


# ============== 物品响应 ==============

class ItemResponse(ItemBase, TimestampMixin):
    """物品响应模型"""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="物品ID")
    status: ItemStatus = Field(..., description="状态")
    stock: int = Field(..., description="库存数量")
    owner_id: int = Field(..., description="所有者ID")


class ItemWithOwner(ItemResponse):
    """包含所有者信息的物品响应"""
    
    owner_username: Optional[str] = Field(None, description="所有者用户名")


# ============== 物品查询参数 ==============

class ItemQuery(BaseSchema):
    """物品查询参数"""
    
    category: Optional[ItemCategory] = Field(None, description="分类过滤")
    status: Optional[ItemStatus] = Field(None, description="状态过滤")
    min_price: Optional[Decimal] = Field(None, ge=0, description="最低价格")
    max_price: Optional[Decimal] = Field(None, ge=0, description="最高价格")
    search: Optional[str] = Field(None, max_length=100, description="搜索关键词")

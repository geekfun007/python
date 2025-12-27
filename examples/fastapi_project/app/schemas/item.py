"""商品相关的 Pydantic 模式"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TagBase(BaseModel):
    """标签基础模式"""
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    """创建标签的模式"""
    pass


class TagResponse(TagBase):
    """标签响应模式"""
    id: int
    
    model_config = {"from_attributes": True}


class ItemBase(BaseModel):
    """商品基础模式"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0, description="价格必须大于0")
    stock: int = Field(0, ge=0, description="库存不能为负数")


class ItemCreate(ItemBase):
    """创建商品的模式"""
    tag_ids: Optional[List[int]] = Field(default_factory=list)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "iPhone 15",
                    "description": "Apple 最新款智能手机",
                    "price": 7999.00,
                    "stock": 100,
                    "tag_ids": [1, 2]
                }
            ]
        }
    }


class ItemUpdate(BaseModel):
    """更新商品的模式（所有字段可选）"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    tag_ids: Optional[List[int]] = None


class ItemResponse(ItemBase):
    """商品响应模式"""
    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[TagResponse] = []
    
    model_config = {"from_attributes": True}


class ItemWithOwner(ItemResponse):
    """包含所有者信息的商品响应"""
    owner: Optional["UserResponse"] = None


# 用于解决循环导入问题
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import UserResponse

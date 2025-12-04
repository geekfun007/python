"""
Product Schemas
产品相关的Pydantic模型
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseSchema


class ProductBase(BaseModel):
    """产品基础模型"""
    name: Optional[str] = Field(None, max_length=100, description="产品名称")
    description: Optional[str] = Field(None, description="产品描述")
    price: Optional[float] = Field(None, gt=0, description="价格")
    stock: Optional[int] = Field(None, ge=0, description="库存数量")
    category: Optional[str] = Field(None, max_length=50, description="分类")
    owner_id: Optional[int] = Field(None, description="所有者ID")


class ProductCreate(ProductBase):
    """
    创建产品的请求模型
    
    特点：
    - 名称和价格为必填
    - price gt=0 表示必须大于0
    - stock ge=0 表示必须大于等于0
    """
    name: str = Field(..., max_length=100, description="产品名称")
    price: float = Field(..., gt=0, description="价格")
    description: Optional[str] = Field(None, description="产品描述")
    stock: int = Field(default=0, ge=0, description="库存数量")
    category: Optional[str] = Field(None, max_length=50, description="分类")
    owner_id: Optional[int] = Field(None, description="所有者ID")
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v: float) -> float:
        """验证价格精度"""
        if v > 0:
            # 保留两位小数
            return round(v, 2)
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "iPhone 15 Pro",
                "description": "最新款苹果手机",
                "price": 7999.00,
                "stock": 100,
                "category": "电子产品",
                "owner_id": 1
            }
        }


class ProductUpdate(ProductBase):
    """
    更新产品的请求模型
    所有字段都是可选的
    """
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        """验证价格精度"""
        if v is not None and v > 0:
            return round(v, 2)
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "price": 7499.00,
                "stock": 80
            }
        }


class ProductResponse(BaseSchema):
    """
    产品响应模型
    
    继承BaseSchema获得id和时间戳
    """
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: Optional[str] = None
    owner_id: Optional[int] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "iPhone 15 Pro",
                "description": "最新款苹果手机",
                "price": 7999.00,
                "stock": 100,
                "category": "电子产品",
                "owner_id": 1,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }


class ProductList(BaseModel):
    """
    产品列表响应模型
    包含分页信息
    """
    total: int = Field(..., description="总记录数")
    items: List[ProductResponse] = Field(..., description="产品列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 50,
                "items": [
                    {
                        "id": 1,
                        "name": "iPhone 15 Pro",
                        "description": "最新款苹果手机",
                        "price": 7999.00,
                        "stock": 100,
                        "category": "电子产品",
                        "owner_id": 1,
                        "created_at": "2024-01-01T00:00:00",
                        "updated_at": "2024-01-01T00:00:00"
                    }
                ]
            }
        }


class ProductStockUpdate(BaseModel):
    """
    库存更新模型
    """
    quantity: int = Field(..., description="库存变化量（正数增加，负数减少）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "quantity": -10
            }
        }

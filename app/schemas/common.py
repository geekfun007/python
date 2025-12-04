"""
Common Schemas
通用的Pydantic模型
"""
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List
from datetime import datetime

# 泛型类型变量
T = TypeVar('T')


class PaginationParams(BaseModel):
    """
    分页参数
    
    Pydantic原理：
    - Field() 提供字段验证和描述
    - ge=1 表示 greater than or equal to 1
    - le=100 表示 less than or equal to 100
    """
    skip: int = Field(default=0, ge=0, description="跳过的记录数")
    limit: int = Field(default=100, ge=1, le=100, description="返回的最大记录数")


class ResponseModel(BaseModel, Generic[T]):
    """
    统一响应模型
    
    使用泛型 Generic[T] 使得这个模型可以包装任何类型的数据
    """
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    
    class Config:
        """Pydantic配置"""
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": None
            }
        }


class BaseSchema(BaseModel):
    """
    基础Schema，包含通用字段
    """
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """
        Pydantic配置
        
        from_attributes=True: 允许从ORM模型创建Pydantic模型
        这是Pydantic v2的新特性，替代了v1的orm_mode
        """
        from_attributes = True

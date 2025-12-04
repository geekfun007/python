"""
User Schemas
用户相关的Pydantic模型

Pydantic原理：
1. 数据验证：自动验证输入数据类型和约束
2. 数据序列化：将复杂对象转换为JSON
3. 数据文档：自动生成API文档
4. 类型提示：提供完整的类型提示支持
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from app.schemas.common import BaseSchema


class UserBase(BaseModel):
    """
    用户基础模型 - 包含所有可选字段
    用于继承
    """
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    full_name: Optional[str] = Field(None, max_length=100, description="全名")
    age: Optional[int] = Field(None, ge=0, le=150, description="年龄")
    is_active: Optional[bool] = Field(True, description="是否激活")


class UserCreate(UserBase):
    """
    创建用户的请求模型
    
    特点：
    - 必填字段使用非Optional类型
    - 包含密码字段（创建时需要）
    - Field() 提供验证规则
    """
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, max_length=50, description="密码")
    full_name: Optional[str] = Field(None, max_length=100, description="全名")
    age: Optional[int] = Field(None, ge=0, le=150, description="年龄")
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """
        自定义验证器：验证用户名只包含字母数字和下划线
        
        原理：
        - @field_validator 装饰器标记验证函数
        - 验证失败时抛出 ValueError
        """
        if not v.replace('_', '').isalnum():
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "secret123",
                "full_name": "John Doe",
                "age": 30
            }
        }


class UserUpdate(UserBase):
    """
    更新用户的请求模型
    
    特点：
    - 所有字段都是可选的
    - 只更新提供的字段
    """
    password: Optional[str] = Field(None, min_length=6, max_length=50, description="密码")
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe Updated",
                "age": 31
            }
        }


class UserResponse(BaseSchema):
    """
    用户响应模型
    
    特点：
    - 继承BaseSchema获得id和时间戳字段
    - 不包含密码等敏感字段
    - from_attributes=True 允许从ORM模型转换
    """
    username: str
    email: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    is_active: bool
    is_superuser: bool = False
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "age": 30,
                "is_active": True,
                "is_superuser": False,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }


class UserList(BaseModel):
    """
    用户列表响应模型
    包含分页信息
    """
    total: int = Field(..., description="总记录数")
    items: List[UserResponse] = Field(..., description="用户列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 100,
                "items": [
                    {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "full_name": "John Doe",
                        "age": 30,
                        "is_active": True,
                        "is_superuser": False,
                        "created_at": "2024-01-01T00:00:00",
                        "updated_at": "2024-01-01T00:00:00"
                    }
                ]
            }
        }

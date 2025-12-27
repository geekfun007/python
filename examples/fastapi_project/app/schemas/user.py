"""用户相关的 Pydantic 模式"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
import re


class UserBase(BaseModel):
    """用户基础模式"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """验证用户名只包含字母、数字和下划线"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v.lower()


class UserCreate(UserBase):
    """创建用户的模式"""
    password: str = Field(..., min_length=6, max_length=100)
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """验证密码强度"""
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        return v


class UserUpdate(BaseModel):
    """更新用户的模式（所有字段可选）"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """用户响应模式（不包含密码）"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class UserInDB(UserResponse):
    """数据库中的用户模式（包含哈希密码）"""
    hashed_password: str


class UserWithItems(UserResponse):
    """包含商品列表的用户响应"""
    items: List["ItemResponse"] = []


# 用于解决循环导入问题
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .item import ItemResponse

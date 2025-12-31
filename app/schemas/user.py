"""
用户相关 Schema (IDL)
定义用户的请求和响应数据模型
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.base import BaseSchema, TimestampMixin


# ============== 用户基础 Schema ==============

class UserBase(BaseSchema):
    """用户基础模型"""
    
    email: EmailStr = Field(..., description="用户邮箱")
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    full_name: Optional[str] = Field(None, max_length=100, description="全名")
    is_active: bool = Field(default=True, description="是否激活")


# ============== 创建用户 ==============

class UserCreate(BaseSchema):
    """创建用户请求模型"""
    
    email: EmailStr = Field(..., description="用户邮箱")
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=8, max_length=100, description="密码")
    full_name: Optional[str] = Field(None, max_length=100, description="全名")
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """密码强度验证"""
        if not any(c.isupper() for c in v):
            raise ValueError("密码必须包含至少一个大写字母")
        if not any(c.islower() for c in v):
            raise ValueError("密码必须包含至少一个小写字母")
        if not any(c.isdigit() for c in v):
            raise ValueError("密码必须包含至少一个数字")
        return v
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """用户名验证"""
        if not v.isalnum():
            raise ValueError("用户名只能包含字母和数字")
        return v.lower()


# ============== 更新用户 ==============

class UserUpdate(BaseSchema):
    """更新用户请求模型"""
    
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    full_name: Optional[str] = Field(None, max_length=100, description="全名")
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="新密码")
    is_active: Optional[bool] = Field(None, description="是否激活")


# ============== 用户响应 ==============

class UserResponse(UserBase, TimestampMixin):
    """用户响应模型"""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="用户ID")
    is_superuser: bool = Field(default=False, description="是否为超级管理员")


class UserInDB(UserResponse):
    """数据库中的用户模型（包含密码哈希）"""
    
    hashed_password: str


# ============== 认证相关 ==============

class UserLogin(BaseSchema):
    """用户登录请求"""
    
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., description="密码")


class Token(BaseModel):
    """令牌响应"""
    
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")


class TokenPayload(BaseModel):
    """令牌载荷"""
    
    sub: str = Field(..., description="主题(用户ID)")
    exp: datetime = Field(..., description="过期时间")
    type: str = Field(..., description="令牌类型")


class PasswordChange(BaseSchema):
    """修改密码请求"""
    
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=8, description="新密码")
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """密码强度验证"""
        if not any(c.isupper() for c in v):
            raise ValueError("密码必须包含至少一个大写字母")
        if not any(c.islower() for c in v):
            raise ValueError("密码必须包含至少一个小写字母")
        if not any(c.isdigit() for c in v):
            raise ValueError("密码必须包含至少一个数字")
        return v

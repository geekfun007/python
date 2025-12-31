"""
User Schemas
用户相关请求/响应模型
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from app.models.user import UserStatus, UserRole


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    avatar: Optional[str] = Field(None, max_length=500, description="头像URL")


class UserCreate(UserBase):
    """
    用户创建请求
    
    Example:
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "securepassword123",
            "phone": "13800138000"
        }
    """
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class UserUpdate(BaseModel):
    """
    用户更新请求
    所有字段可选
    """
    username: Optional[str] = Field(None, min_length=2, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    avatar: Optional[str] = Field(None, max_length=500, description="头像URL")
    status: Optional[UserStatus] = Field(None, description="用户状态")
    role: Optional[UserRole] = Field(None, description="用户角色")


class UserResponse(BaseModel):
    """
    用户响应模型
    
    Example:
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "status": 1,
            "role": 0,
            "created_at": "2024-01-01T00:00:00"
        }
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    phone: Optional[str] = Field(None, description="手机号")
    avatar: Optional[str] = Field(None, description="头像URL")
    status: int = Field(..., description="用户状态")
    role: int = Field(..., description="用户角色")
    last_login_at: Optional[datetime] = Field(None, description="最后登录时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class UserListResponse(BaseModel):
    """用户列表响应"""
    users: List[UserResponse] = Field(..., description="用户列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    page_size: int = Field(..., description="每页数量")


class LoginRequest(BaseModel):
    """
    登录请求
    
    Example:
        {
            "email": "john@example.com",
            "password": "securepassword123"
        }
    """
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=1, description="密码")


class LoginResponse(BaseModel):
    """
    登录响应
    
    Example:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIs...",
            "token_type": "bearer",
            "expires_in": 1800,
            "user": {...}
        }
    """
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间（秒）")
    user: UserResponse = Field(..., description="用户信息")


class TokenPayload(BaseModel):
    """JWT Token 载荷"""
    sub: int = Field(..., description="用户ID")
    exp: Optional[datetime] = Field(None, description="过期时间")


class PasswordChange(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., min_length=1, description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=100, description="新密码")

"""
Interaction Schemas
用户互动相关请求/响应模型
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class CommentBase(BaseModel):
    """评论基础模型"""
    content: str = Field(..., min_length=1, max_length=1000, description="评论内容")


class CommentCreate(CommentBase):
    """
    评论创建请求
    
    Example:
        {
            "article_id": 1,
            "content": "写得很好！",
            "parent_id": null
        }
    """
    article_id: int = Field(..., description="文章ID")
    parent_id: Optional[int] = Field(None, description="父评论ID（回复时使用）")


class CommentResponse(BaseModel):
    """
    评论响应模型
    
    Example:
        {
            "id": 1,
            "article_id": 1,
            "user_id": 2,
            "user_name": "john_doe",
            "content": "写得很好！",
            "like_count": 5,
            "created_at": "2024-01-01T00:00:00"
        }
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="评论ID")
    article_id: int = Field(..., description="文章ID")
    user_id: int = Field(..., description="用户ID")
    user_name: Optional[str] = Field(None, description="用户名")
    user_avatar: Optional[str] = Field(None, description="用户头像")
    content: str = Field(..., description="评论内容")
    parent_id: Optional[int] = Field(None, description="父评论ID")
    like_count: int = Field(default=0, description="点赞数")
    status: int = Field(..., description="评论状态")
    replies: List["CommentResponse"] = Field(default=[], description="回复列表")
    created_at: datetime = Field(..., description="创建时间")


class CommentListResponse(BaseModel):
    """评论列表响应"""
    comments: List[CommentResponse] = Field(..., description="评论列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    page_size: int = Field(..., description="每页数量")


class LikeRequest(BaseModel):
    """
    点赞请求
    
    Example:
        {
            "target_type": 1,
            "target_id": 1
        }
    """
    target_type: int = Field(..., ge=1, le=2, description="目标类型: 1-文章, 2-评论")
    target_id: int = Field(..., description="目标ID")


class LikeResponse(BaseModel):
    """点赞响应"""
    liked: bool = Field(..., description="是否已点赞")
    like_count: int = Field(..., description="当前点赞数")


class FavoriteRequest(BaseModel):
    """收藏请求"""
    article_id: int = Field(..., description="文章ID")


class FavoriteResponse(BaseModel):
    """收藏响应"""
    favorited: bool = Field(..., description="是否已收藏")

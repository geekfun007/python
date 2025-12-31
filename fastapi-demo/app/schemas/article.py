"""
Article Schemas
文章相关请求/响应模型
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from app.models.article import ArticleStatus


class CategoryBase(BaseModel):
    """分类基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    description: Optional[str] = Field(None, max_length=255, description="分类描述")
    parent_id: Optional[int] = Field(None, description="父分类ID")


class CategoryCreate(CategoryBase):
    """分类创建请求"""
    sort_order: int = Field(default=0, description="排序权重")


class CategoryResponse(BaseModel):
    """分类响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="分类ID")
    name: str = Field(..., description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    parent_id: Optional[int] = Field(None, description="父分类ID")
    sort_order: int = Field(..., description="排序权重")
    created_at: datetime = Field(..., description="创建时间")


class TagBase(BaseModel):
    """标签基础模型"""
    name: str = Field(..., min_length=1, max_length=30, description="标签名称")
    color: Optional[str] = Field(default="#666666", max_length=10, description="标签颜色")


class TagCreate(TagBase):
    """标签创建请求"""
    pass


class TagResponse(BaseModel):
    """标签响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="标签ID")
    name: str = Field(..., description="标签名称")
    color: Optional[str] = Field(None, description="标签颜色")


class ArticleBase(BaseModel):
    """文章基础模型"""
    title: str = Field(..., min_length=1, max_length=200, description="文章标题")
    content: str = Field(..., min_length=1, description="文章内容")
    summary: Optional[str] = Field(None, max_length=500, description="文章摘要")
    cover_image: Optional[str] = Field(None, max_length=500, description="封面图片URL")


class ArticleCreate(ArticleBase):
    """
    文章创建请求
    
    Example:
        {
            "title": "FastAPI 入门教程",
            "content": "# FastAPI 入门...",
            "summary": "FastAPI 入门教程概述",
            "category_id": 1,
            "tag_ids": [1, 2, 3],
            "status": 0
        }
    """
    category_id: Optional[int] = Field(None, description="分类ID")
    tag_ids: Optional[List[int]] = Field(default=[], description="标签ID列表")
    status: ArticleStatus = Field(default=ArticleStatus.DRAFT, description="文章状态")


class ArticleUpdate(BaseModel):
    """
    文章更新请求
    所有字段可选
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="文章标题")
    content: Optional[str] = Field(None, min_length=1, description="文章内容")
    summary: Optional[str] = Field(None, max_length=500, description="文章摘要")
    cover_image: Optional[str] = Field(None, max_length=500, description="封面图片URL")
    category_id: Optional[int] = Field(None, description="分类ID")
    tag_ids: Optional[List[int]] = Field(None, description="标签ID列表")
    status: Optional[ArticleStatus] = Field(None, description="文章状态")


class ArticleResponse(BaseModel):
    """
    文章响应模型
    
    Example:
        {
            "id": 1,
            "title": "FastAPI 入门教程",
            "content": "# FastAPI 入门...",
            "author_id": 1,
            "author_name": "admin",
            "status": 1,
            "view_count": 100,
            "like_count": 10,
            "created_at": "2024-01-01T00:00:00"
        }
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="文章ID")
    title: str = Field(..., description="文章标题")
    content: str = Field(..., description="文章内容")
    summary: Optional[str] = Field(None, description="文章摘要")
    cover_image: Optional[str] = Field(None, description="封面图片URL")
    author_id: int = Field(..., description="作者ID")
    author_name: Optional[str] = Field(None, description="作者名称")
    category: Optional[CategoryResponse] = Field(None, description="分类信息")
    tags: List[TagResponse] = Field(default=[], description="标签列表")
    status: int = Field(..., description="文章状态")
    view_count: int = Field(..., description="浏览量")
    like_count: int = Field(..., description="点赞数")
    comment_count: int = Field(..., description="评论数")
    published_at: Optional[datetime] = Field(None, description="发布时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class ArticleListResponse(BaseModel):
    """文章列表响应"""
    articles: List[ArticleResponse] = Field(..., description="文章列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    page_size: int = Field(..., description="每页数量")


class ArticleFilter(BaseModel):
    """
    文章查询过滤器
    
    Example:
        {
            "keyword": "FastAPI",
            "author_id": 1,
            "category_id": 2,
            "status": 1
        }
    """
    keyword: Optional[str] = Field(None, description="搜索关键词")
    author_id: Optional[int] = Field(None, description="作者ID")
    category_id: Optional[int] = Field(None, description="分类ID")
    tag_ids: Optional[List[int]] = Field(None, description="标签ID列表")
    status: Optional[ArticleStatus] = Field(None, description="文章状态")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")

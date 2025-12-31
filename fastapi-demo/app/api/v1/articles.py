"""
Articles Router
文章相关 API 路由
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.article import (
    ArticleCreate, ArticleUpdate, ArticleResponse, 
    ArticleListResponse, ArticleFilter
)
from app.schemas.interaction import (
    CommentCreate, CommentResponse, CommentListResponse,
    LikeResponse, FavoriteResponse
)
from app.schemas.common import ResponseModel
from app.services.article_service import ArticleService
from app.services.auth_service import get_current_user, get_current_user_optional
from app.models.user import User
from app.models.article import ArticleStatus

router = APIRouter()


# ==================== 文章 CRUD ====================

@router.get(
    "",
    response_model=ResponseModel[ArticleListResponse],
    summary="获取文章列表",
    description="获取已发布的文章列表，支持分页和过滤"
)
async def get_articles(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    tag_ids: Optional[str] = Query(None, description="标签ID列表（逗号分隔）"),
    author_id: Optional[int] = Query(None, description="作者ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取文章列表
    
    - 默认只返回已发布的文章
    - 支持关键词搜索（标题、摘要）
    - 支持按分类、标签、作者过滤
    """
    # 解析标签ID
    tag_id_list = None
    if tag_ids:
        tag_id_list = [int(id.strip()) for id in tag_ids.split(",") if id.strip()]
    
    filters = ArticleFilter(
        keyword=keyword,
        category_id=category_id,
        tag_ids=tag_id_list,
        author_id=author_id,
    )
    
    article_service = ArticleService(db)
    result = await article_service.get_articles(
        page=page,
        page_size=page_size,
        filters=filters,
        published_only=True,
    )
    return ResponseModel.success(data=result)


@router.post(
    "",
    response_model=ResponseModel[ArticleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建文章",
    description="创建新文章"
)
async def create_article(
    article_data: ArticleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建新文章
    
    - **title**: 文章标题
    - **content**: 文章内容（支持 Markdown）
    - **summary**: 文章摘要（可选）
    - **cover_image**: 封面图片URL（可选）
    - **category_id**: 分类ID（可选）
    - **tag_ids**: 标签ID列表（可选）
    - **status**: 文章状态（默认为草稿）
    """
    article_service = ArticleService(db)
    result = await article_service.create_article(article_data, current_user)
    return ResponseModel.success(data=result, message="文章创建成功")


@router.get(
    "/my",
    response_model=ResponseModel[ArticleListResponse],
    summary="获取我的文章",
    description="获取当前用户的所有文章（包括草稿）"
)
async def get_my_articles(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[ArticleStatus] = Query(None, description="文章状态"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的文章列表
    
    - 包括所有状态的文章（草稿、已发布、已归档）
    - 支持按状态过滤
    """
    filters = ArticleFilter(author_id=current_user.id, status=status)
    
    article_service = ArticleService(db)
    result = await article_service.get_articles(
        page=page,
        page_size=page_size,
        filters=filters,
        published_only=False,
    )
    return ResponseModel.success(data=result)


@router.get(
    "/{article_id}",
    response_model=ResponseModel[ArticleResponse],
    summary="获取文章详情",
    description="根据ID获取文章详细信息"
)
async def get_article(
    article_id: int = Path(..., description="文章ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取文章详情
    
    - 自动增加浏览量
    """
    article_service = ArticleService(db)
    result = await article_service.get_article(article_id, increment_view=True)
    return ResponseModel.success(data=result)


@router.put(
    "/{article_id}",
    response_model=ResponseModel[ArticleResponse],
    summary="更新文章",
    description="更新文章信息"
)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新文章
    
    - 只能更新自己的文章（管理员除外）
    - 所有字段可选，只更新提供的字段
    """
    article_service = ArticleService(db)
    result = await article_service.update_article(article_id, article_data, current_user)
    return ResponseModel.success(data=result, message="文章更新成功")


@router.delete(
    "/{article_id}",
    response_model=ResponseModel,
    summary="删除文章",
    description="删除文章（软删除）"
)
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除文章
    
    - 只能删除自己的文章（管理员除外）
    - 执行软删除
    """
    article_service = ArticleService(db)
    await article_service.delete_article(article_id, current_user)
    return ResponseModel.success(message="文章删除成功")


@router.post(
    "/{article_id}/publish",
    response_model=ResponseModel[ArticleResponse],
    summary="发布文章",
    description="将文章状态改为已发布"
)
async def publish_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发布文章
    
    - 将文章状态改为 PUBLISHED
    - 记录发布时间
    """
    article_service = ArticleService(db)
    result = await article_service.publish_article(article_id, current_user)
    return ResponseModel.success(data=result, message="文章发布成功")


# ==================== 评论 ====================

@router.get(
    "/{article_id}/comments",
    response_model=ResponseModel[CommentListResponse],
    summary="获取文章评论",
    description="获取指定文章的评论列表"
)
async def get_article_comments(
    article_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取文章评论
    
    - 返回嵌套的评论结构（包含回复）
    """
    article_service = ArticleService(db)
    result = await article_service.get_article_comments(article_id, page, page_size)
    return ResponseModel.success(data=result)


@router.post(
    "/{article_id}/comments",
    response_model=ResponseModel[CommentResponse],
    status_code=status.HTTP_201_CREATED,
    summary="添加评论",
    description="为文章添加评论"
)
async def add_comment(
    article_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    添加评论
    
    - **content**: 评论内容
    - **parent_id**: 父评论ID（回复时使用，可选）
    """
    # 确保 article_id 一致
    comment_data.article_id = article_id
    
    article_service = ArticleService(db)
    result = await article_service.create_comment(comment_data, current_user)
    return ResponseModel.success(data=result, message="评论成功")


@router.delete(
    "/comments/{comment_id}",
    response_model=ResponseModel,
    summary="删除评论",
    description="删除评论"
)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除评论
    
    - 只能删除自己的评论（管理员除外）
    """
    article_service = ArticleService(db)
    await article_service.delete_comment(comment_id, current_user)
    return ResponseModel.success(message="评论删除成功")


# ==================== 点赞和收藏 ====================

@router.post(
    "/{article_id}/like",
    response_model=ResponseModel[LikeResponse],
    summary="点赞/取消点赞",
    description="切换文章点赞状态"
)
async def toggle_like(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    点赞/取消点赞
    
    - 已点赞时取消点赞
    - 未点赞时添加点赞
    """
    article_service = ArticleService(db)
    result = await article_service.toggle_article_like(article_id, current_user)
    return ResponseModel.success(
        data=LikeResponse(**result),
        message="点赞成功" if result["liked"] else "已取消点赞"
    )


@router.post(
    "/{article_id}/favorite",
    response_model=ResponseModel[FavoriteResponse],
    summary="收藏/取消收藏",
    description="切换文章收藏状态"
)
async def toggle_favorite(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    收藏/取消收藏
    
    - 已收藏时取消收藏
    - 未收藏时添加收藏
    """
    article_service = ArticleService(db)
    result = await article_service.toggle_article_favorite(article_id, current_user)
    return ResponseModel.success(
        data=FavoriteResponse(**result),
        message="收藏成功" if result["favorited"] else "已取消收藏"
    )

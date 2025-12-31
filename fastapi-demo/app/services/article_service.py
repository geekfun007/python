"""
Article Service
文章服务层
"""

from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dal.article_dal import ArticleDAL, CategoryDAL, TagDAL
from app.dal.interaction_dal import CommentDAL, LikeDAL, FavoriteDAL
from app.models.article import Article, ArticleStatus
from app.models.interaction import LikeTargetType
from app.models.user import User
from app.schemas.article import (
    ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse,
    ArticleFilter, CategoryCreate, CategoryResponse, TagCreate, TagResponse
)
from app.schemas.interaction import CommentCreate, CommentResponse, CommentListResponse


class ArticleService:
    """
    文章服务类
    
    提供文章相关的业务逻辑:
    - 文章 CRUD
    - 文章发布
    - 评论管理
    - 点赞和收藏
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.article_dal = ArticleDAL(db)
        self.category_dal = CategoryDAL(db)
        self.tag_dal = TagDAL(db)
        self.comment_dal = CommentDAL(db)
        self.like_dal = LikeDAL(db)
        self.favorite_dal = FavoriteDAL(db)
    
    # ==================== 文章操作 ====================
    
    async def create_article(
        self,
        article_data: ArticleCreate,
        author: User
    ) -> ArticleResponse:
        """
        创建文章
        
        Args:
            article_data: 文章创建数据
            author: 作者
        
        Returns:
            文章响应
        """
        article = await self.article_dal.create_article(
            title=article_data.title,
            content=article_data.content,
            author_id=author.id,
            summary=article_data.summary,
            cover_image=article_data.cover_image,
            category_id=article_data.category_id,
            tag_ids=article_data.tag_ids,
            status=article_data.status,
        )
        
        return self._to_article_response(article)
    
    async def get_article(
        self,
        article_id: int,
        increment_view: bool = False
    ) -> ArticleResponse:
        """
        获取文章详情
        
        Args:
            article_id: 文章ID
            increment_view: 是否增加浏览量
        
        Returns:
            文章响应
        
        Raises:
            HTTPException: 文章不存在时抛出 404 错误
        """
        article = await self.article_dal.get_with_relations(article_id)
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        if increment_view:
            await self.article_dal.increment_view_count(article_id)
            article.view_count += 1
        
        return self._to_article_response(article)
    
    async def get_articles(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[ArticleFilter] = None,
        published_only: bool = True,
    ) -> ArticleListResponse:
        """
        获取文章列表
        
        Args:
            page: 页码
            page_size: 每页数量
            filters: 过滤条件
            published_only: 是否只返回已发布的文章
        
        Returns:
            文章列表响应
        """
        skip = (page - 1) * page_size
        
        filter_status = ArticleStatus.PUBLISHED if published_only else None
        if filters and filters.status is not None:
            filter_status = filters.status
        
        articles, total = await self.article_dal.get_articles(
            skip=skip,
            limit=page_size,
            author_id=filters.author_id if filters else None,
            category_id=filters.category_id if filters else None,
            tag_ids=filters.tag_ids if filters else None,
            status=filter_status,
            keyword=filters.keyword if filters else None,
            start_date=filters.start_date if filters else None,
            end_date=filters.end_date if filters else None,
        )
        
        return ArticleListResponse(
            articles=[self._to_article_response(a) for a in articles],
            total=total,
            page=page,
            page_size=page_size,
        )
    
    async def update_article(
        self,
        article_id: int,
        article_data: ArticleUpdate,
        current_user: User
    ) -> ArticleResponse:
        """
        更新文章
        
        Args:
            article_id: 文章ID
            article_data: 更新数据
            current_user: 当前用户
        
        Returns:
            更新后的文章响应
        
        Raises:
            HTTPException: 文章不存在或无权限时抛出错误
        """
        article = await self.article_dal.get(article_id)
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        # 检查权限：只能更新自己的文章，除非是管理员
        if article.author_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此文章"
            )
        
        update_dict = article_data.model_dump(exclude_unset=True)
        
        updated_article = await self.article_dal.update_article(
            article_id,
            **update_dict
        )
        
        return self._to_article_response(updated_article)
    
    async def delete_article(
        self,
        article_id: int,
        current_user: User
    ) -> bool:
        """
        删除文章（软删除）
        
        Args:
            article_id: 文章ID
            current_user: 当前用户
        
        Returns:
            是否删除成功
        """
        article = await self.article_dal.get(article_id)
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        # 检查权限
        if article.author_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此文章"
            )
        
        await self.article_dal.update(article_id, {"status": ArticleStatus.DELETED})
        return True
    
    async def publish_article(
        self,
        article_id: int,
        current_user: User
    ) -> ArticleResponse:
        """
        发布文章
        
        Args:
            article_id: 文章ID
            current_user: 当前用户
        
        Returns:
            发布后的文章响应
        """
        article = await self.article_dal.get(article_id)
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        if article.author_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权发布此文章"
            )
        
        published_article = await self.article_dal.publish_article(article_id)
        return self._to_article_response(published_article)
    
    # ==================== 评论操作 ====================
    
    async def create_comment(
        self,
        comment_data: CommentCreate,
        user: User
    ) -> CommentResponse:
        """创建评论"""
        # 检查文章是否存在
        article = await self.article_dal.get(comment_data.article_id)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        # 检查父评论是否存在
        if comment_data.parent_id:
            parent = await self.comment_dal.get(comment_data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="回复的评论不存在"
                )
        
        comment = await self.comment_dal.create_comment(
            article_id=comment_data.article_id,
            user_id=user.id,
            content=comment_data.content,
            parent_id=comment_data.parent_id,
        )
        
        # 更新文章评论数
        await self.article_dal.increment_comment_count(comment_data.article_id)
        
        return CommentResponse(
            id=comment.id,
            article_id=comment.article_id,
            user_id=comment.user_id,
            user_name=user.username,
            user_avatar=user.avatar,
            content=comment.content,
            parent_id=comment.parent_id,
            like_count=comment.like_count,
            status=comment.status,
            created_at=comment.created_at,
        )
    
    async def get_article_comments(
        self,
        article_id: int,
        page: int = 1,
        page_size: int = 50,
    ) -> CommentListResponse:
        """获取文章评论"""
        skip = (page - 1) * page_size
        
        comments, total = await self.comment_dal.get_article_comments(
            article_id,
            skip=skip,
            limit=page_size,
        )
        
        return CommentListResponse(
            comments=[self._to_comment_response(c) for c in comments],
            total=total,
            page=page,
            page_size=page_size,
        )
    
    async def delete_comment(
        self,
        comment_id: int,
        current_user: User
    ) -> bool:
        """删除评论"""
        comment = await self.comment_dal.get(comment_id)
        
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="评论不存在"
            )
        
        # 只有评论作者或管理员可以删除
        if comment.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此评论"
            )
        
        await self.comment_dal.soft_delete(comment_id)
        await self.article_dal.increment_comment_count(comment.article_id, -1)
        return True
    
    # ==================== 点赞和收藏 ====================
    
    async def toggle_article_like(
        self,
        article_id: int,
        user: User
    ) -> dict:
        """切换文章点赞状态"""
        article = await self.article_dal.get(article_id)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        liked = await self.like_dal.toggle_like(
            user_id=user.id,
            target_type=LikeTargetType.ARTICLE,
            target_id=article_id,
        )
        
        # 更新文章点赞数
        delta = 1 if liked else -1
        await self.article_dal.increment_like_count(article_id, delta)
        
        return {
            "liked": liked,
            "like_count": article.like_count + delta
        }
    
    async def toggle_article_favorite(
        self,
        article_id: int,
        user: User
    ) -> dict:
        """切换文章收藏状态"""
        article = await self.article_dal.get(article_id)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        favorited = await self.favorite_dal.toggle_favorite(
            user_id=user.id,
            article_id=article_id,
        )
        
        return {"favorited": favorited}
    
    # ==================== 分类和标签 ====================
    
    async def get_categories(self) -> List[CategoryResponse]:
        """获取所有分类"""
        categories = await self.category_dal.get_all_with_children()
        return [CategoryResponse.model_validate(c) for c in categories]
    
    async def create_category(
        self,
        category_data: CategoryCreate
    ) -> CategoryResponse:
        """创建分类"""
        # 检查名称是否重复
        existing = await self.category_dal.get_by_name(category_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分类名称已存在"
            )
        
        category = await self.category_dal.create(category_data.model_dump())
        return CategoryResponse.model_validate(category)
    
    async def get_tags(self) -> List[TagResponse]:
        """获取所有标签"""
        tags = await self.tag_dal.get_popular_tags(limit=100)
        return [TagResponse.model_validate(t) for t in tags]
    
    async def create_tag(self, tag_data: TagCreate) -> TagResponse:
        """创建标签"""
        existing = await self.tag_dal.get_by_name(tag_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="标签名称已存在"
            )
        
        tag = await self.tag_dal.create(tag_data.model_dump())
        return TagResponse.model_validate(tag)
    
    # ==================== 辅助方法 ====================
    
    def _to_article_response(self, article: Article) -> ArticleResponse:
        """将文章模型转换为响应模型"""
        return ArticleResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            summary=article.summary,
            cover_image=article.cover_image,
            author_id=article.author_id,
            author_name=article.author.username if article.author else None,
            category=CategoryResponse.model_validate(article.category) if article.category else None,
            tags=[TagResponse.model_validate(t) for t in article.tags] if article.tags else [],
            status=article.status,
            view_count=article.view_count,
            like_count=article.like_count,
            comment_count=article.comment_count,
            published_at=article.published_at,
            created_at=article.created_at,
            updated_at=article.updated_at,
        )
    
    def _to_comment_response(self, comment) -> CommentResponse:
        """将评论模型转换为响应模型"""
        replies = []
        if hasattr(comment, 'replies') and comment.replies:
            replies = [self._to_comment_response(r) for r in comment.replies]
        
        return CommentResponse(
            id=comment.id,
            article_id=comment.article_id,
            user_id=comment.user_id,
            user_name=comment.user.username if comment.user else None,
            user_avatar=comment.user.avatar if comment.user else None,
            content=comment.content,
            parent_id=comment.parent_id,
            like_count=comment.like_count,
            status=comment.status,
            replies=replies,
            created_at=comment.created_at,
        )

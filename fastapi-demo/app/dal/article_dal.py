"""
Article DAL
文章数据访问层
"""

from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from .base_dal import BaseDAL
from app.models.article import Article, ArticleStatus, Category, Tag, ArticleTag
from app.models.user import User


class CategoryDAL(BaseDAL[Category]):
    """分类数据访问层"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Category, db)
    
    async def get_by_name(self, name: str) -> Optional[Category]:
        """根据名称获取分类"""
        return await self.get_by_field("name", name)
    
    async def get_all_with_children(self) -> List[Category]:
        """获取所有分类（包含子分类关系）"""
        stmt = (
            select(Category)
            .options(selectinload(Category.children))
            .where(Category.parent_id.is_(None))
            .order_by(Category.sort_order)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class TagDAL(BaseDAL[Tag]):
    """标签数据访问层"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Tag, db)
    
    async def get_by_name(self, name: str) -> Optional[Tag]:
        """根据名称获取标签"""
        return await self.get_by_field("name", name)
    
    async def get_by_ids(self, ids: List[int]) -> List[Tag]:
        """根据ID列表获取标签"""
        if not ids:
            return []
        
        stmt = select(Tag).where(Tag.id.in_(ids))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_popular_tags(self, limit: int = 20) -> List[Tag]:
        """获取热门标签（按使用次数排序）"""
        stmt = (
            select(Tag, func.count(ArticleTag.article_id).label("count"))
            .outerjoin(ArticleTag, Tag.id == ArticleTag.tag_id)
            .group_by(Tag.id)
            .order_by(func.count(ArticleTag.article_id).desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return [row[0] for row in result.all()]


class ArticleDAL(BaseDAL[Article]):
    """
    文章数据访问层
    
    提供文章相关的数据库操作:
    - 文章 CRUD
    - 文章搜索和过滤
    - 标签关联管理
    - 计数器操作
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(Article, db)
    
    async def create_article(
        self,
        title: str,
        content: str,
        author_id: int,
        summary: Optional[str] = None,
        cover_image: Optional[str] = None,
        category_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
        status: ArticleStatus = ArticleStatus.DRAFT,
    ) -> Article:
        """
        创建新文章
        
        Args:
            title: 文章标题
            content: 文章内容
            author_id: 作者ID
            summary: 文章摘要
            cover_image: 封面图片
            category_id: 分类ID
            tag_ids: 标签ID列表
            status: 文章状态
        
        Returns:
            创建的文章实例
        """
        article_data = {
            "title": title,
            "content": content,
            "author_id": author_id,
            "summary": summary,
            "cover_image": cover_image,
            "category_id": category_id,
            "status": status,
        }
        
        article = await self.create(article_data)
        
        # 关联标签
        if tag_ids:
            await self._set_article_tags(article.id, tag_ids)
        
        # 重新加载以获取关联数据
        return await self.get_with_relations(article.id)
    
    async def get_with_relations(self, article_id: int) -> Optional[Article]:
        """
        获取文章（包含关联数据）
        
        Args:
            article_id: 文章ID
        
        Returns:
            文章实例（包含作者、分类、标签信息）
        """
        stmt = (
            select(Article)
            .options(
                joinedload(Article.author),
                joinedload(Article.category),
                selectinload(Article.tags),
            )
            .where(Article.id == article_id)
        )
        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()
    
    async def get_articles(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
        status: Optional[ArticleStatus] = None,
        keyword: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Tuple[List[Article], int]:
        """
        获取文章列表（支持过滤和搜索）
        
        Args:
            skip: 跳过记录数
            limit: 返回记录数
            author_id: 作者ID过滤
            category_id: 分类ID过滤
            tag_ids: 标签ID过滤
            status: 状态过滤
            keyword: 关键词搜索
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            (文章列表, 总数)
        """
        # 构建基础查询
        base_stmt = select(Article).options(
            joinedload(Article.author),
            joinedload(Article.category),
            selectinload(Article.tags),
        )
        
        count_stmt = select(func.count()).select_from(Article)
        
        # 应用过滤条件
        if author_id is not None:
            base_stmt = base_stmt.where(Article.author_id == author_id)
            count_stmt = count_stmt.where(Article.author_id == author_id)
        
        if category_id is not None:
            base_stmt = base_stmt.where(Article.category_id == category_id)
            count_stmt = count_stmt.where(Article.category_id == category_id)
        
        if status is not None:
            base_stmt = base_stmt.where(Article.status == status)
            count_stmt = count_stmt.where(Article.status == status)
        
        if keyword:
            search_filter = or_(
                Article.title.contains(keyword),
                Article.summary.contains(keyword)
            )
            base_stmt = base_stmt.where(search_filter)
            count_stmt = count_stmt.where(search_filter)
        
        if start_date:
            base_stmt = base_stmt.where(Article.created_at >= start_date)
            count_stmt = count_stmt.where(Article.created_at >= start_date)
        
        if end_date:
            base_stmt = base_stmt.where(Article.created_at <= end_date)
            count_stmt = count_stmt.where(Article.created_at <= end_date)
        
        # 标签过滤（需要 JOIN）
        if tag_ids:
            base_stmt = (
                base_stmt
                .join(ArticleTag, Article.id == ArticleTag.article_id)
                .where(ArticleTag.tag_id.in_(tag_ids))
                .distinct()
            )
            count_stmt = (
                count_stmt
                .join(ArticleTag, Article.id == ArticleTag.article_id)
                .where(ArticleTag.tag_id.in_(tag_ids))
            )
        
        # 获取总数
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar() or 0
        
        # 获取列表
        list_stmt = (
            base_stmt
            .order_by(Article.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        
        result = await self.db.execute(list_stmt)
        articles = list(result.unique().scalars().all())
        
        return articles, total
    
    async def update_article(
        self,
        article_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        summary: Optional[str] = None,
        cover_image: Optional[str] = None,
        category_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
        status: Optional[ArticleStatus] = None,
    ) -> Optional[Article]:
        """
        更新文章
        
        Args:
            article_id: 文章ID
            其他参数: 要更新的字段
        
        Returns:
            更新后的文章实例
        """
        update_data = {}
        
        if title is not None:
            update_data["title"] = title
        if content is not None:
            update_data["content"] = content
        if summary is not None:
            update_data["summary"] = summary
        if cover_image is not None:
            update_data["cover_image"] = cover_image
        if category_id is not None:
            update_data["category_id"] = category_id
        if status is not None:
            update_data["status"] = status
        
        if update_data:
            await self.update(article_id, update_data)
        
        # 更新标签关联
        if tag_ids is not None:
            await self._set_article_tags(article_id, tag_ids)
        
        return await self.get_with_relations(article_id)
    
    async def publish_article(self, article_id: int) -> Optional[Article]:
        """
        发布文章
        
        Args:
            article_id: 文章ID
        
        Returns:
            更新后的文章实例
        """
        await self.update(article_id, {
            "status": ArticleStatus.PUBLISHED,
            "published_at": datetime.utcnow()
        })
        return await self.get_with_relations(article_id)
    
    async def increment_view_count(self, article_id: int) -> None:
        """增加浏览量"""
        article = await self.get(article_id)
        if article:
            await self.update(article_id, {"view_count": article.view_count + 1})
    
    async def increment_like_count(self, article_id: int, delta: int = 1) -> None:
        """增加/减少点赞数"""
        article = await self.get(article_id)
        if article:
            new_count = max(0, article.like_count + delta)
            await self.update(article_id, {"like_count": new_count})
    
    async def increment_comment_count(self, article_id: int, delta: int = 1) -> None:
        """增加/减少评论数"""
        article = await self.get(article_id)
        if article:
            new_count = max(0, article.comment_count + delta)
            await self.update(article_id, {"comment_count": new_count})
    
    async def _set_article_tags(self, article_id: int, tag_ids: List[int]) -> None:
        """
        设置文章标签（替换现有标签）
        
        Args:
            article_id: 文章ID
            tag_ids: 标签ID列表
        """
        # 删除现有关联
        from sqlalchemy import delete
        delete_stmt = delete(ArticleTag).where(ArticleTag.article_id == article_id)
        await self.db.execute(delete_stmt)
        
        # 添加新关联
        for tag_id in tag_ids:
            article_tag = ArticleTag(article_id=article_id, tag_id=tag_id)
            self.db.add(article_tag)
        
        await self.db.flush()
    
    async def get_user_articles(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Article], int]:
        """获取用户的文章列表"""
        return await self.get_articles(skip=skip, limit=limit, author_id=user_id)
    
    async def get_published_articles(
        self,
        skip: int = 0,
        limit: int = 20,
        keyword: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> Tuple[List[Article], int]:
        """获取已发布的文章列表"""
        return await self.get_articles(
            skip=skip,
            limit=limit,
            status=ArticleStatus.PUBLISHED,
            keyword=keyword,
            category_id=category_id,
        )

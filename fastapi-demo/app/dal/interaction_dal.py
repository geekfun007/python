"""
Interaction DAL
用户互动数据访问层（评论、点赞、收藏）
"""

from typing import Optional, List, Tuple
from sqlalchemy import select, func, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from .base_dal import BaseDAL
from app.models.interaction import Comment, CommentStatus, UserLike, UserFavorite, LikeTargetType
from app.models.user import User


class CommentDAL(BaseDAL[Comment]):
    """
    评论数据访问层
    
    提供评论相关的数据库操作:
    - 评论 CRUD
    - 获取文章评论（支持嵌套回复）
    - 评论审核
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(Comment, db)
    
    async def create_comment(
        self,
        article_id: int,
        user_id: int,
        content: str,
        parent_id: Optional[int] = None,
    ) -> Comment:
        """
        创建评论
        
        Args:
            article_id: 文章ID
            user_id: 用户ID
            content: 评论内容
            parent_id: 父评论ID（回复时使用）
        
        Returns:
            创建的评论实例
        """
        comment_data = {
            "article_id": article_id,
            "user_id": user_id,
            "content": content,
            "parent_id": parent_id,
            "status": CommentStatus.APPROVED,
        }
        return await self.create(comment_data)
    
    async def get_with_user(self, comment_id: int) -> Optional[Comment]:
        """
        获取评论（包含用户信息）
        
        Args:
            comment_id: 评论ID
        
        Returns:
            评论实例
        """
        stmt = (
            select(Comment)
            .options(joinedload(Comment.user))
            .where(Comment.id == comment_id)
        )
        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()
    
    async def get_article_comments(
        self,
        article_id: int,
        skip: int = 0,
        limit: int = 50,
        include_replies: bool = True,
    ) -> Tuple[List[Comment], int]:
        """
        获取文章评论
        
        Args:
            article_id: 文章ID
            skip: 跳过记录数
            limit: 返回记录数
            include_replies: 是否包含回复
        
        Returns:
            (评论列表, 总数)
        """
        # 基础查询 - 只获取顶级评论
        base_filter = [
            Comment.article_id == article_id,
            Comment.status == CommentStatus.APPROVED,
        ]
        
        if not include_replies:
            base_filter.append(Comment.parent_id.is_(None))
        
        # 获取总数
        count_stmt = (
            select(func.count())
            .select_from(Comment)
            .where(*base_filter)
        )
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar() or 0
        
        # 获取评论列表
        if include_replies:
            # 只获取顶级评论，回复通过关系加载
            stmt = (
                select(Comment)
                .options(
                    joinedload(Comment.user),
                    joinedload(Comment.replies).joinedload(Comment.user),
                )
                .where(
                    Comment.article_id == article_id,
                    Comment.status == CommentStatus.APPROVED,
                    Comment.parent_id.is_(None),
                )
                .order_by(Comment.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
        else:
            stmt = (
                select(Comment)
                .options(joinedload(Comment.user))
                .where(*base_filter)
                .order_by(Comment.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
        
        result = await self.db.execute(stmt)
        comments = list(result.unique().scalars().all())
        
        return comments, total
    
    async def get_user_comments(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Comment], int]:
        """获取用户的评论列表"""
        filters = [Comment.user_id == user_id, Comment.status == CommentStatus.APPROVED]
        
        total = await self.count(filters)
        comments = await self.get_multi(
            skip=skip,
            limit=limit,
            filters=filters,
            order_by=Comment.created_at.desc()
        )
        
        return comments, total
    
    async def soft_delete(self, comment_id: int) -> bool:
        """
        软删除评论
        
        Args:
            comment_id: 评论ID
        
        Returns:
            是否成功
        """
        result = await self.update(comment_id, {"status": CommentStatus.DELETED})
        return result is not None


class LikeDAL(BaseDAL[UserLike]):
    """
    点赞数据访问层
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(UserLike, db)
    
    async def get_like(
        self,
        user_id: int,
        target_type: LikeTargetType,
        target_id: int
    ) -> Optional[UserLike]:
        """
        获取用户的点赞记录
        
        Args:
            user_id: 用户ID
            target_type: 目标类型
            target_id: 目标ID
        
        Returns:
            点赞记录或 None
        """
        stmt = select(UserLike).where(
            UserLike.user_id == user_id,
            UserLike.target_type == target_type,
            UserLike.target_id == target_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def toggle_like(
        self,
        user_id: int,
        target_type: LikeTargetType,
        target_id: int
    ) -> bool:
        """
        切换点赞状态
        
        Args:
            user_id: 用户ID
            target_type: 目标类型
            target_id: 目标ID
        
        Returns:
            True=点赞, False=取消点赞
        """
        existing = await self.get_like(user_id, target_type, target_id)
        
        if existing:
            # 取消点赞
            await self.delete(existing.id)
            return False
        else:
            # 添加点赞
            await self.create({
                "user_id": user_id,
                "target_type": target_type,
                "target_id": target_id,
            })
            return True
    
    async def is_liked(
        self,
        user_id: int,
        target_type: LikeTargetType,
        target_id: int
    ) -> bool:
        """检查用户是否已点赞"""
        like = await self.get_like(user_id, target_type, target_id)
        return like is not None
    
    async def get_like_count(
        self,
        target_type: LikeTargetType,
        target_id: int
    ) -> int:
        """获取点赞数"""
        stmt = (
            select(func.count())
            .select_from(UserLike)
            .where(
                UserLike.target_type == target_type,
                UserLike.target_id == target_id,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0


class FavoriteDAL(BaseDAL[UserFavorite]):
    """
    收藏数据访问层
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(UserFavorite, db)
    
    async def get_favorite(
        self,
        user_id: int,
        article_id: int
    ) -> Optional[UserFavorite]:
        """
        获取收藏记录
        
        Args:
            user_id: 用户ID
            article_id: 文章ID
        
        Returns:
            收藏记录或 None
        """
        stmt = select(UserFavorite).where(
            UserFavorite.user_id == user_id,
            UserFavorite.article_id == article_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def toggle_favorite(
        self,
        user_id: int,
        article_id: int
    ) -> bool:
        """
        切换收藏状态
        
        Args:
            user_id: 用户ID
            article_id: 文章ID
        
        Returns:
            True=收藏, False=取消收藏
        """
        existing = await self.get_favorite(user_id, article_id)
        
        if existing:
            await self.delete(existing.id)
            return False
        else:
            await self.create({
                "user_id": user_id,
                "article_id": article_id,
            })
            return True
    
    async def is_favorited(self, user_id: int, article_id: int) -> bool:
        """检查用户是否已收藏"""
        favorite = await self.get_favorite(user_id, article_id)
        return favorite is not None
    
    async def get_user_favorites(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[UserFavorite], int]:
        """
        获取用户收藏列表
        
        Args:
            user_id: 用户ID
            skip: 跳过记录数
            limit: 返回记录数
        
        Returns:
            (收藏列表, 总数)
        """
        filters = [UserFavorite.user_id == user_id]
        
        total = await self.count(filters)
        
        stmt = (
            select(UserFavorite)
            .options(joinedload(UserFavorite.article))
            .where(*filters)
            .order_by(UserFavorite.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        favorites = list(result.unique().scalars().all())
        
        return favorites, total

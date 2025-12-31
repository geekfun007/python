"""
Interaction Models
用户互动相关数据模型（评论、点赞、收藏）
"""

import enum
from sqlalchemy import Column, String, Text, SmallInteger, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class CommentStatus(enum.IntEnum):
    """评论状态枚举"""
    PENDING = 0     # 待审核
    APPROVED = 1    # 已通过
    DELETED = 2     # 已删除


class LikeTargetType(enum.IntEnum):
    """点赞目标类型枚举"""
    ARTICLE = 1     # 文章
    COMMENT = 2     # 评论


class Comment(BaseModel):
    """
    评论模型
    
    Attributes:
        id: 评论ID
        article_id: 文章ID
        user_id: 用户ID
        content: 评论内容
        parent_id: 父评论ID（用于回复）
        like_count: 点赞数
        status: 评论状态
    """
    
    __tablename__ = "comments"
    
    article_id = Column(
        BigInteger,
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="文章ID"
    )
    
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    
    content = Column(
        Text,
        nullable=False,
        comment="评论内容"
    )
    
    parent_id = Column(
        BigInteger,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="父评论ID"
    )
    
    like_count = Column(
        Integer,
        nullable=False,
        default=0,
        comment="点赞数"
    )
    
    status = Column(
        SmallInteger,
        nullable=False,
        default=CommentStatus.APPROVED,
        index=True,
        comment="状态: 0-待审核, 1-已通过, 2-已删除"
    )
    
    # 关系定义
    article = relationship(
        "Article",
        back_populates="comments"
    )
    
    user = relationship(
        "User",
        back_populates="comments"
    )
    
    # 自关联关系（回复）
    parent = relationship(
        "Comment",
        remote_side="Comment.id",
        backref="replies"
    )
    
    @property
    def is_reply(self) -> bool:
        """是否是回复"""
        return self.parent_id is not None
    
    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, article_id={self.article_id}, user_id={self.user_id})>"


class UserLike(BaseModel):
    """
    用户点赞模型
    
    Attributes:
        id: ID
        user_id: 用户ID
        target_type: 目标类型（文章/评论）
        target_id: 目标ID
    """
    
    __tablename__ = "user_likes"
    
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    
    target_type = Column(
        SmallInteger,
        nullable=False,
        comment="目标类型: 1-文章, 2-评论"
    )
    
    target_id = Column(
        BigInteger,
        nullable=False,
        index=True,
        comment="目标ID"
    )
    
    # 关系定义
    user = relationship(
        "User",
        back_populates="likes"
    )
    
    def __repr__(self) -> str:
        return f"<UserLike(user_id={self.user_id}, target_type={self.target_type}, target_id={self.target_id})>"


class UserFavorite(BaseModel):
    """
    用户收藏模型
    
    Attributes:
        id: ID
        user_id: 用户ID
        article_id: 文章ID
    """
    
    __tablename__ = "user_favorites"
    
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    
    article_id = Column(
        BigInteger,
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="文章ID"
    )
    
    # 关系定义
    user = relationship(
        "User",
        back_populates="favorites"
    )
    
    article = relationship("Article")
    
    def __repr__(self) -> str:
        return f"<UserFavorite(user_id={self.user_id}, article_id={self.article_id})>"

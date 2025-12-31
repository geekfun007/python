"""
Article Model
文章相关数据模型
"""

import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, SmallInteger, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel, Base, TimestampMixin


class ArticleStatus(enum.IntEnum):
    """文章状态枚举"""
    DRAFT = 0       # 草稿
    PUBLISHED = 1   # 已发布
    ARCHIVED = 2    # 已归档
    DELETED = 3     # 已删除


class Category(BaseModel):
    """
    文章分类模型
    
    Attributes:
        id: 分类ID
        name: 分类名称
        description: 分类描述
        parent_id: 父分类ID
        sort_order: 排序权重
    """
    
    __tablename__ = "categories"
    
    name = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="分类名称"
    )
    
    description = Column(
        String(255),
        nullable=True,
        comment="分类描述"
    )
    
    parent_id = Column(
        BigInteger,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="父分类ID"
    )
    
    sort_order = Column(
        Integer,
        nullable=False,
        default=0,
        comment="排序权重"
    )
    
    # 自关联关系
    parent = relationship(
        "Category",
        remote_side="Category.id",
        backref="children"
    )
    
    # 文章关系
    articles = relationship(
        "Article",
        back_populates="category",
        lazy="dynamic"
    )
    
    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"


class Tag(Base, TimestampMixin):
    """
    标签模型
    
    Attributes:
        id: 标签ID
        name: 标签名称
        color: 标签颜色
    """
    
    __tablename__ = "tags"
    
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )
    
    name = Column(
        String(30),
        unique=True,
        nullable=False,
        comment="标签名称"
    )
    
    color = Column(
        String(10),
        nullable=True,
        default="#666666",
        comment="标签颜色"
    )
    
    # 通过中间表关联文章
    articles = relationship(
        "Article",
        secondary="article_tags",
        back_populates="tags"
    )
    
    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name='{self.name}')>"


class Article(BaseModel):
    """
    文章模型
    
    Attributes:
        id: 文章ID
        title: 文章标题
        content: 文章内容
        summary: 文章摘要
        cover_image: 封面图片
        author_id: 作者ID
        category_id: 分类ID
        status: 文章状态
        view_count: 浏览量
        like_count: 点赞数
        comment_count: 评论数
        published_at: 发布时间
    """
    
    __tablename__ = "articles"
    
    title = Column(
        String(200),
        nullable=False,
        comment="文章标题"
    )
    
    content = Column(
        Text,
        nullable=False,
        comment="文章内容"
    )
    
    summary = Column(
        String(500),
        nullable=True,
        comment="文章摘要"
    )
    
    cover_image = Column(
        String(500),
        nullable=True,
        comment="封面图片URL"
    )
    
    author_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="作者ID"
    )
    
    category_id = Column(
        BigInteger,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="分类ID"
    )
    
    status = Column(
        SmallInteger,
        nullable=False,
        default=ArticleStatus.DRAFT,
        index=True,
        comment="状态: 0-草稿, 1-已发布, 2-已归档, 3-已删除"
    )
    
    view_count = Column(
        Integer,
        nullable=False,
        default=0,
        comment="浏览量"
    )
    
    like_count = Column(
        Integer,
        nullable=False,
        default=0,
        comment="点赞数"
    )
    
    comment_count = Column(
        Integer,
        nullable=False,
        default=0,
        comment="评论数"
    )
    
    published_at = Column(
        DateTime,
        nullable=True,
        index=True,
        comment="发布时间"
    )
    
    # 关系定义
    author = relationship(
        "User",
        back_populates="articles"
    )
    
    category = relationship(
        "Category",
        back_populates="articles"
    )
    
    tags = relationship(
        "Tag",
        secondary="article_tags",
        back_populates="articles"
    )
    
    comments = relationship(
        "Comment",
        back_populates="article",
        lazy="dynamic"
    )
    
    @property
    def is_published(self) -> bool:
        """文章是否已发布"""
        return self.status == ArticleStatus.PUBLISHED
    
    def publish(self):
        """发布文章"""
        self.status = ArticleStatus.PUBLISHED
        self.published_at = datetime.utcnow()
    
    def archive(self):
        """归档文章"""
        self.status = ArticleStatus.ARCHIVED
    
    def increment_view_count(self):
        """增加浏览量"""
        self.view_count += 1
    
    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title='{self.title[:20]}...')>"


class ArticleTag(Base):
    """
    文章标签关联表
    多对多关系中间表
    """
    
    __tablename__ = "article_tags"
    
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )
    
    article_id = Column(
        BigInteger,
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="文章ID"
    )
    
    tag_id = Column(
        BigInteger,
        ForeignKey("tags.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="标签ID"
    )
    
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="创建时间"
    )

"""
Data Access Layer (DAL)
数据访问层 - 封装所有数据库操作
"""

from .user_dal import UserDAL
from .article_dal import ArticleDAL, CategoryDAL, TagDAL
from .interaction_dal import CommentDAL, LikeDAL, FavoriteDAL

__all__ = [
    "UserDAL",
    "ArticleDAL",
    "CategoryDAL",
    "TagDAL",
    "CommentDAL",
    "LikeDAL",
    "FavoriteDAL",
]

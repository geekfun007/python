"""
Repository (DAL) 模块
数据访问层，封装数据库操作
"""
from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository
from app.repositories.item import ItemRepository

__all__ = ["BaseRepository", "UserRepository", "ItemRepository"]

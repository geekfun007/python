"""
Data Access Layer Package
数据访问层 - 封装所有数据库操作
"""
from app.dal.base import BaseDAL
from app.dal.user_dal import UserDAL
from app.dal.product_dal import ProductDAL

__all__ = ["BaseDAL", "UserDAL", "ProductDAL"]

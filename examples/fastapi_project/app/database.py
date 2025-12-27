"""数据库配置和会话管理"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from .config import settings


# 创建数据库引擎
# SQLite 需要 check_same_thread=False 参数
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        echo=settings.debug
    )
else:
    engine = create_engine(
        settings.database_url,
        echo=settings.debug
    )

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建模型基类
Base = declarative_base()


def get_db() -> Generator:
    """获取数据库会话
    
    作为 FastAPI 依赖使用，确保会话在请求结束后关闭
    
    Yields:
        Session: 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """创建所有数据库表"""
    Base.metadata.create_all(bind=engine)

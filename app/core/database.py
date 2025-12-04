"""
数据库连接和会话管理
Database Connection and Session Management

原理说明：
1. SQLAlchemy Engine: 数据库连接池管理器
2. SessionLocal: 会话工厂，用于创建数据库会话
3. Base: 声明式基类，所有ORM模型继承此类
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from config import settings

# 创建数据库引擎
# echo=True 会打印所有SQL语句，便于调试
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # 连接池预检查，确保连接有效
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 最大溢出连接数
)

# 创建会话工厂
# autocommit=False: 手动控制事务提交
# autoflush=False: 手动控制刷新到数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建声明式基类
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话的依赖注入函数
    
    使用方式:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    
    原理：
    - FastAPI的依赖注入系统会自动调用此函数
    - yield确保请求结束后关闭会话
    - finally块保证即使发生异常也会关闭会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库，创建所有表
    
    注意：生产环境建议使用Alembic进行数据库迁移
    """
    Base.metadata.create_all(bind=engine)

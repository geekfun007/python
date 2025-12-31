"""
Base DAL
数据访问层基类，提供通用 CRUD 操作
"""

from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseDAL(Generic[ModelType]):
    """
    数据访问层基类
    
    提供通用的 CRUD 操作:
    - create: 创建记录
    - get: 根据 ID 获取单条记录
    - get_multi: 获取多条记录（支持分页）
    - update: 更新记录
    - delete: 删除记录
    - count: 统计记录数
    
    Example:
        class UserDAL(BaseDAL[User]):
            def __init__(self, db: AsyncSession):
                super().__init__(User, db)
    """
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        初始化 DAL
        
        Args:
            model: SQLAlchemy 模型类
            db: 异步数据库会话
        """
        self.model = model
        self.db = db
    
    async def create(self, obj_in: dict[str, Any]) -> ModelType:
        """
        创建新记录
        
        Args:
            obj_in: 创建数据字典
        
        Returns:
            创建的模型实例
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def get(self, id: int) -> Optional[ModelType]:
        """
        根据 ID 获取记录
        
        Args:
            id: 记录 ID
        
        Returns:
            模型实例或 None
        """
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_field(
        self,
        field: str,
        value: Any
    ) -> Optional[ModelType]:
        """
        根据字段值获取记录
        
        Args:
            field: 字段名
            value: 字段值
        
        Returns:
            模型实例或 None
        """
        column = getattr(self.model, field, None)
        if column is None:
            raise ValueError(f"Model {self.model.__name__} has no field '{field}'")
        
        stmt = select(self.model).where(column == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[Any] = None,
        filters: Optional[List[Any]] = None,
    ) -> List[ModelType]:
        """
        获取多条记录
        
        Args:
            skip: 跳过记录数
            limit: 返回记录数
            order_by: 排序字段
            filters: 过滤条件列表
        
        Returns:
            模型实例列表
        """
        stmt = select(self.model)
        
        if filters:
            for filter_condition in filters:
                stmt = stmt.where(filter_condition)
        
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        else:
            # 默认按 ID 降序
            stmt = stmt.order_by(self.model.id.desc())
        
        stmt = stmt.offset(skip).limit(limit)
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def update(
        self,
        id: int,
        obj_in: dict[str, Any]
    ) -> Optional[ModelType]:
        """
        更新记录
        
        Args:
            id: 记录 ID
            obj_in: 更新数据字典（仅包含要更新的字段）
        
        Returns:
            更新后的模型实例或 None
        """
        # 过滤掉 None 值
        update_data = {k: v for k, v in obj_in.items() if v is not None}
        
        if not update_data:
            return await self.get(id)
        
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        await self.db.execute(stmt)
        await self.db.flush()
        
        return await self.get(id)
    
    async def delete(self, id: int) -> bool:
        """
        删除记录
        
        Args:
            id: 记录 ID
        
        Returns:
            是否删除成功
        """
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount > 0
    
    async def count(
        self,
        filters: Optional[List[Any]] = None
    ) -> int:
        """
        统计记录数
        
        Args:
            filters: 过滤条件列表
        
        Returns:
            记录数量
        """
        stmt = select(func.count()).select_from(self.model)
        
        if filters:
            for filter_condition in filters:
                stmt = stmt.where(filter_condition)
        
        result = await self.db.execute(stmt)
        return result.scalar() or 0
    
    async def exists(self, id: int) -> bool:
        """
        检查记录是否存在
        
        Args:
            id: 记录 ID
        
        Returns:
            是否存在
        """
        stmt = select(func.count()).select_from(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return (result.scalar() or 0) > 0

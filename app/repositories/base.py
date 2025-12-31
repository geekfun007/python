"""
基础 Repository
实现通用的CRUD操作
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    基础仓库类
    提供通用的CRUD操作
    
    使用方式:
        class UserRepository(BaseRepository[User]):
            def __init__(self, db: AsyncSession):
                super().__init__(User, db)
    """
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        初始化仓库
        
        Args:
            model: ORM模型类
            db: 异步数据库会话
        """
        self.model = model
        self.db = db
    
    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """
        创建记录
        
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
        根据ID获取单条记录
        
        Args:
            id: 记录ID
        
        Returns:
            模型实例或None
        """
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_field(
        self, field: str, value: Any
    ) -> Optional[ModelType]:
        """
        根据字段值获取单条记录
        
        Args:
            field: 字段名
            value: 字段值
        
        Returns:
            模型实例或None
        """
        query = select(self.model).where(getattr(self.model, field) == value)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False,
    ) -> List[ModelType]:
        """
        获取多条记录
        
        Args:
            skip: 跳过的记录数
            limit: 返回的最大记录数
            filters: 过滤条件字典
            order_by: 排序字段
            order_desc: 是否降序
        
        Returns:
            模型实例列表
        """
        query = select(self.model)
        
        # 应用过滤条件
        if filters:
            for field, value in filters.items():
                if value is not None and hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        # 应用排序
        if order_by and hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            if order_desc:
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column)
        
        # 应用分页
        query = query.offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        统计记录数
        
        Args:
            filters: 过滤条件字典
        
        Returns:
            记录数量
        """
        query = select(func.count(self.model.id))
        
        if filters:
            for field, value in filters.items():
                if value is not None and hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        result = await self.db.execute(query)
        return result.scalar() or 0
    
    async def update(
        self, id: int, obj_in: Dict[str, Any]
    ) -> Optional[ModelType]:
        """
        更新记录
        
        Args:
            id: 记录ID
            obj_in: 更新数据字典
        
        Returns:
            更新后的模型实例或None
        """
        # 过滤掉None值
        update_data = {k: v for k, v in obj_in.items() if v is not None}
        
        if not update_data:
            return await self.get(id)
        
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await self.db.execute(query)
        await self.db.flush()
        return result.scalar_one_or_none()
    
    async def delete(self, id: int) -> bool:
        """
        删除记录
        
        Args:
            id: 记录ID
        
        Returns:
            是否删除成功
        """
        query = delete(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        await self.db.flush()
        return result.rowcount > 0
    
    async def exists(self, id: int) -> bool:
        """
        检查记录是否存在
        
        Args:
            id: 记录ID
        
        Returns:
            是否存在
        """
        query = select(func.count(self.model.id)).where(self.model.id == id)
        result = await self.db.execute(query)
        return (result.scalar() or 0) > 0

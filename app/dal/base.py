"""
Base Data Access Layer
基础数据访问层 - 提供通用CRUD操作

DAL模式原理：
1. 分离关注点：业务逻辑与数据库操作分离
2. 可测试性：可以轻松mock DAL进行单元测试
3. 可维护性：数据库操作集中管理
4. 可复用性：通用操作可以在基类中实现
"""
from typing import Generic, TypeVar, Type, List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.base import BaseModel

# 泛型类型变量
ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseDAL(Generic[ModelType]):
    """
    基础DAL类，提供通用的CRUD操作
    
    使用泛型 Generic[ModelType] 使得这个类可以适用于任何模型
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        初始化DAL
        
        Args:
            model: ORM模型类
            db: 数据库会话
        """
        self.model = model
        self.db = db
    
    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """
        创建新记录
        
        Args:
            obj_in: 包含模型字段的字典
            
        Returns:
            创建的模型实例
            
        原理：
        1. 使用字典解包创建模型实例
        2. add() 将对象添加到会话
        3. commit() 提交事务到数据库
        4. refresh() 从数据库刷新对象，获取自动生成的字段（如id）
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        根据ID获取单条记录
        
        Args:
            id: 主键ID
            
        Returns:
            模型实例或None
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        获取多条记录（分页）
        
        Args:
            skip: 跳过的记录数（偏移量）
            limit: 返回的最大记录数
            filters: 过滤条件字典
            
        Returns:
            模型实例列表
            
        原理：
        - offset() 实现分页的偏移
        - limit() 限制返回数量
        - all() 执行查询并返回所有结果
        """
        query = self.db.query(self.model)
        
        # 应用过滤条件
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """
        更新记录
        
        Args:
            id: 主键ID
            obj_in: 要更新的字段字典
            
        Returns:
            更新后的模型实例或None
            
        原理：
        1. 先查询对象
        2. 遍历更新字典，设置对象属性
        3. commit() 提交更改
        4. refresh() 刷新对象
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        
        for key, value in obj_in.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """
        删除记录
        
        Args:
            id: 主键ID
            
        Returns:
            是否删除成功
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        统计记录数
        
        Args:
            filters: 过滤条件字典
            
        Returns:
            记录数量
        """
        query = self.db.query(self.model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        
        return query.count()
    
    def exists(self, id: int) -> bool:
        """
        检查记录是否存在
        
        Args:
            id: 主键ID
            
        Returns:
            是否存在
        """
        return self.db.query(self.model).filter(self.model.id == id).first() is not None

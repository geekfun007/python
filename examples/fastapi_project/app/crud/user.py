"""用户 CRUD 操作"""
from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash, verify_password


class UserCRUD:
    """用户 CRUD 操作类"""
    
    def get(self, db: Session, user_id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """获取多个用户"""
        query = db.query(User)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """创建用户"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: UserUpdate
    ) -> User:
        """更新用户"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # 如果更新密码，需要哈希处理
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, user_id: int) -> Optional[User]:
        """删除用户"""
        obj = db.query(User).get(user_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def authenticate(
        self,
        db: Session,
        *,
        username: str,
        password: str
    ) -> Optional[User]:
        """验证用户"""
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """检查用户是否激活"""
        return user.is_active
    
    def is_superuser(self, user: User) -> bool:
        """检查是否是超级管理员"""
        return user.is_superuser


# 创建单例
user_crud = UserCRUD()

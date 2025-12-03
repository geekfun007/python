# MySQL 数据库使用指南

## 目录

1. [数据库安装和配置](#数据库安装和配置)
2. [数据库设计](#数据库设计)
3. [SQLAlchemy ORM 详解](#sqlalchemy-orm-详解)
4. [数据库迁移](#数据库迁移)
5. [查询优化](#查询优化)
6. [事务管理](#事务管理)
7. [常见问题](#常见问题)

## 数据库安装和配置

### MySQL 安装

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### macOS

```bash
brew install mysql
brew services start mysql
```

#### Windows

下载 MySQL 安装程序: https://dev.mysql.com/downloads/installer/

### 创建数据库和用户

```sql
-- 登录 MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE fastapi_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'fastapi_user'@'localhost' IDENTIFIED BY 'your_password';

-- 授权
GRANT ALL PRIVILEGES ON fastapi_demo.* TO 'fastapi_user'@'localhost';
FLUSH PRIVILEGES;

-- 验证
SHOW DATABASES;
USE fastapi_demo;
```

### 配置连接

在 `.env` 文件中配置:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=fastapi_user
DB_PASSWORD=your_password
DB_NAME=fastapi_demo
```

## 数据库设计

### 表设计原则

#### 1. 命名规范

- **表名**: 小写，复数形式 (`users`, `products`)
- **字段名**: 小写，蛇形命名 (`created_at`, `user_id`)
- **主键**: 统一使用 `id`
- **外键**: 使用 `表名_id` (`user_id`, `product_id`)

#### 2. 数据类型选择

```sql
-- 整数
INT           -- -2147483648 到 2147483647
BIGINT        -- 更大范围
TINYINT       -- 布尔值 (0/1)

-- 字符串
VARCHAR(n)    -- 可变长度，最大 65535
CHAR(n)       -- 固定长度
TEXT          -- 长文本，最大 65535
MEDIUMTEXT    -- 更长文本
LONGTEXT      -- 非常长的文本

-- 数值
DECIMAL(p,s)  -- 精确小数 (price: DECIMAL(10,2))
FLOAT         -- 浮点数
DOUBLE        -- 双精度浮点数

-- 日期时间
DATE          -- 日期 (YYYY-MM-DD)
DATETIME      -- 日期时间 (YYYY-MM-DD HH:MM:SS)
TIMESTAMP     -- 时间戳 (自动更新)

-- 其他
JSON          -- JSON 数据
ENUM          -- 枚举值
```

#### 3. 索引设计

```sql
-- 主键索引（自动创建）
PRIMARY KEY (id)

-- 唯一索引
UNIQUE KEY idx_username (username)
UNIQUE KEY idx_email (email)

-- 普通索引
INDEX idx_category (category)
INDEX idx_created_at (created_at)

-- 复合索引
INDEX idx_user_category (user_id, category)

-- 全文索引
FULLTEXT INDEX idx_description (description)
```

### 表结构示例

#### users 表

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
    hashed_password VARCHAR(255) NOT NULL COMMENT '加密密码',
    full_name VARCHAR(100) COMMENT '全名',
    age INT COMMENT '年龄',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_superuser BOOLEAN DEFAULT FALSE COMMENT '是否超级用户',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
```

#### products 表

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    name VARCHAR(100) NOT NULL COMMENT '产品名称',
    description TEXT COMMENT '产品描述',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    stock INT DEFAULT 0 COMMENT '库存数量',
    category VARCHAR(50) COMMENT '分类',
    owner_id INT COMMENT '所有者ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_owner_id (owner_id),
    INDEX idx_created_at (created_at),
    
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='产品表';
```

## SQLAlchemy ORM 详解

### ORM 基础概念

ORM (Object-Relational Mapping) 将数据库表映射为 Python 类。

**映射关系:**
```
数据库            Python
--------         --------
表(Table)    →   类(Class)
行(Row)      →   对象(Object)
列(Column)   →   属性(Attribute)
```

### 定义模型

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    # 列定义
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关系
    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
```

### 列类型和约束

```python
# 主键
id = Column(Integer, primary_key=True, autoincrement=True)

# 唯一约束
username = Column(String(50), unique=True)

# 非空约束
email = Column(String(100), nullable=False)

# 默认值
is_active = Column(Boolean, default=True)

# 服务器端默认值
created_at = Column(DateTime, server_default=func.now())

# 自动更新
updated_at = Column(DateTime, onupdate=func.now())

# 索引
username = Column(String(50), index=True)

# 注释
age = Column(Integer, comment="用户年龄")
```

### 关系映射

#### 一对多关系 (One-to-Many)

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    
    # 一对多：一个用户有多个产品
    products = relationship("Product", back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # 多对一：多个产品属于一个用户
    owner = relationship("User", back_populates="products")
```

#### 多对多关系 (Many-to-Many)

```python
# 关联表
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    
    # 多对多
    roles = relationship("Role", secondary=user_roles, back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    # 多对多
    users = relationship("User", secondary=user_roles, back_populates="roles")
```

#### 一对一关系 (One-to-One)

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    
    # 一对一
    profile = relationship("UserProfile", uselist=False, back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    bio = Column(Text)
    
    # 一对一
    user = relationship("User", back_populates="profile")
```

### CRUD 操作

#### Create (创建)

```python
# 创建单个对象
user = User(username="john", email="john@example.com")
db.add(user)
db.commit()
db.refresh(user)  # 刷新以获取自动生成的字段

# 批量创建
users = [
    User(username="user1", email="user1@example.com"),
    User(username="user2", email="user2@example.com"),
]
db.add_all(users)
db.commit()
```

#### Read (查询)

```python
# 查询所有
users = db.query(User).all()

# 根据主键查询
user = db.query(User).get(1)

# 条件查询
user = db.query(User).filter(User.username == "john").first()

# 多条件查询
users = db.query(User).filter(
    User.age > 18,
    User.is_active == True
).all()

# 使用 and_/or_
from sqlalchemy import and_, or_
users = db.query(User).filter(
    and_(
        User.age > 18,
        or_(User.is_active == True, User.is_superuser == True)
    )
).all()

# 排序
users = db.query(User).order_by(User.created_at.desc()).all()

# 分页
users = db.query(User).offset(10).limit(20).all()

# 计数
count = db.query(User).filter(User.is_active == True).count()

# 模糊查询
users = db.query(User).filter(User.username.like("%john%")).all()

# 范围查询
users = db.query(User).filter(User.age.between(18, 30)).all()

# IN 查询
users = db.query(User).filter(User.id.in_([1, 2, 3])).all()

# 聚合查询
from sqlalchemy import func
result = db.query(
    User.age,
    func.count(User.id).label("count")
).group_by(User.age).all()
```

#### Update (更新)

```python
# 更新单个对象
user = db.query(User).get(1)
user.age = 31
db.commit()

# 批量更新
db.query(User).filter(User.age < 18).update({"is_active": False})
db.commit()

# 使用字典更新
user = db.query(User).get(1)
update_data = {"age": 31, "full_name": "John Doe"}
for key, value in update_data.items():
    setattr(user, key, value)
db.commit()
```

#### Delete (删除)

```python
# 删除单个对象
user = db.query(User).get(1)
db.delete(user)
db.commit()

# 批量删除
db.query(User).filter(User.is_active == False).delete()
db.commit()
```

### 高级查询

#### Join 查询

```python
# Inner Join
results = db.query(User, Product).join(Product).all()

# Left Join
results = db.query(User).outerjoin(Product).all()

# 指定连接条件
results = db.query(User).join(
    Product,
    User.id == Product.owner_id
).all()
```

#### 子查询

```python
# 标量子查询
subquery = db.query(func.avg(User.age)).scalar_subquery()
users = db.query(User).filter(User.age > subquery).all()

# 表子查询
subquery = db.query(
    Product.owner_id,
    func.count(Product.id).label("product_count")
).group_by(Product.owner_id).subquery()

users = db.query(User, subquery.c.product_count).join(
    subquery,
    User.id == subquery.c.owner_id
).all()
```

#### 加载策略

```python
from sqlalchemy.orm import joinedload, selectinload, subqueryload

# Joined Load (一次查询，使用 JOIN)
users = db.query(User).options(joinedload(User.products)).all()

# Select In Load (两次查询，使用 IN)
users = db.query(User).options(selectinload(User.products)).all()

# Subquery Load (两次查询，使用子查询)
users = db.query(User).options(subqueryload(User.products)).all()

# 防止懒加载
users = db.query(User).options(noload(User.products)).all()
```

## 数据库迁移

### 使用 Alembic

#### 安装和初始化

```bash
pip install alembic
alembic init alembic
```

#### 配置 alembic.ini

```ini
# alembic.ini
sqlalchemy.url = mysql+pymysql://user:password@localhost/dbname
```

#### 配置 env.py

```python
# alembic/env.py
from app.core.database import Base
from app.models import User, Product  # 导入所有模型

target_metadata = Base.metadata
```

#### 创建迁移

```bash
# 自动生成迁移脚本
alembic revision --autogenerate -m "Initial migration"

# 手动创建迁移脚本
alembic revision -m "Add column"
```

#### 执行迁移

```bash
# 升级到最新版本
alembic upgrade head

# 升级到指定版本
alembic upgrade +1

# 查看当前版本
alembic current

# 查看历史
alembic history

# 回滚
alembic downgrade -1
```

#### 迁移脚本示例

```python
"""Add email column to users

Revision ID: abc123
Create Date: 2024-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """升级"""
    op.add_column('users', sa.Column('email', sa.String(100), nullable=True))
    op.create_index('idx_email', 'users', ['email'])

def downgrade():
    """降级"""
    op.drop_index('idx_email', table_name='users')
    op.drop_column('users', 'email')
```

## 查询优化

### 1. 使用索引

```python
# 在常查询的字段上创建索引
username = Column(String(50), index=True)

# 复合索引
Index('idx_user_category', 'user_id', 'category')
```

### 2. 避免 N+1 查询

```python
# 不好：N+1 查询
users = db.query(User).all()
for user in users:
    print(user.products)  # 每次循环执行一次查询

# 好：使用 joinedload
users = db.query(User).options(joinedload(User.products)).all()
for user in users:
    print(user.products)  # 不会执行额外查询
```

### 3. 只查询需要的列

```python
# 不好：查询所有列
users = db.query(User).all()

# 好：只查询需要的列
users = db.query(User.id, User.username).all()
```

### 4. 使用分页

```python
# 始终使用分页
users = db.query(User).offset(skip).limit(limit).all()
```

### 5. 批量操作

```python
# 批量插入
db.bulk_insert_mappings(User, [
    {"username": "user1"},
    {"username": "user2"},
])

# 批量更新
db.bulk_update_mappings(User, [
    {"id": 1, "age": 20},
    {"id": 2, "age": 25},
])
```

## 事务管理

### 基本事务

```python
db = SessionLocal()
try:
    # 执行数据库操作
    user = User(username="john")
    db.add(user)
    db.commit()  # 提交事务
except Exception:
    db.rollback()  # 回滚事务
    raise
finally:
    db.close()  # 关闭会话
```

### 使用上下文管理器

```python
from contextlib import contextmanager

@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# 使用
with get_db_context() as db:
    user = User(username="john")
    db.add(user)
```

### 嵌套事务

```python
db = SessionLocal()
try:
    # 外层事务
    user = User(username="john")
    db.add(user)
    
    # 嵌套事务
    savepoint = db.begin_nested()
    try:
        product = Product(name="iPhone")
        db.add(product)
        db.commit()  # 提交嵌套事务
    except Exception:
        savepoint.rollback()  # 回滚嵌套事务
    
    db.commit()  # 提交外层事务
except Exception:
    db.rollback()
finally:
    db.close()
```

## 常见问题

### 1. 连接超时

**问题**: `Lost connection to MySQL server`

**解决**:
```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 连接前检查
    pool_recycle=3600    # 1小时回收连接
)
```

### 2. 字符编码问题

**问题**: 中文乱码

**解决**:
```python
engine = create_engine(
    DATABASE_URL + "?charset=utf8mb4",
    encoding='utf-8'
)
```

### 3. 时区问题

**问题**: 时间不正确

**解决**:
```python
# 使用 UTC 时间
from datetime import datetime, timezone

created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
```

### 4. 连接池耗尽

**问题**: `QueuePool limit overflow`

**解决**:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,        # 增加连接池大小
    max_overflow=40      # 增加溢出连接数
)
```

### 5. 死锁

**问题**: `Deadlock found when trying to get lock`

**解决**:
- 保持事务简短
- 按相同顺序访问资源
- 使用适当的隔离级别
- 添加重试逻辑

```python
from sqlalchemy.exc import OperationalError
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        # 数据库操作
        db.commit()
        break
    except OperationalError as e:
        if "Deadlock" in str(e) and attempt < max_retries - 1:
            db.rollback()
            time.sleep(0.1 * (attempt + 1))
        else:
            raise
```

## 总结

本指南涵盖了:
- MySQL 安装和配置
- 数据库设计最佳实践
- SQLAlchemy ORM 使用
- 数据库迁移
- 查询优化技巧
- 事务管理
- 常见问题解决

遵循这些最佳实践可以:
- 提高应用性能
- 保证数据一致性
- 简化维护工作
- 避免常见错误

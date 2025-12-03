"""
数据库初始化脚本
Database Initialization Script

功能：
1. 创建所有表
2. 插入示例数据
3. 验证数据库连接
"""
import sys
from sqlalchemy.exc import OperationalError
from app.core.database import engine, SessionLocal, Base
from app.models import User, Product
from config import settings


def create_tables():
    """创建所有表"""
    print("🔧 创建数据库表...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功")
        return True
    except OperationalError as e:
        print(f"❌ 数据库连接失败: {e}")
        print(f"\n请检查:")
        print(f"  1. MySQL 服务是否运行")
        print(f"  2. 数据库 '{settings.DB_NAME}' 是否存在")
        print(f"  3. 用户 '{settings.DB_USER}' 是否有权限")
        print(f"  4. .env 文件配置是否正确")
        return False
    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        return False


def insert_sample_data():
    """插入示例数据"""
    print("\n📝 插入示例数据...")
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        if db.query(User).count() > 0:
            print("ℹ️  数据库已有数据，跳过插入")
            return True
        
        # 创建示例用户
        users = [
            User(
                username="admin",
                email="admin@example.com",
                hashed_password="hashed_admin123",
                full_name="管理员",
                age=30,
                is_active=True,
                is_superuser=True
            ),
            User(
                username="john_doe",
                email="john@example.com",
                hashed_password="hashed_secret123",
                full_name="John Doe",
                age=25,
                is_active=True,
                is_superuser=False
            ),
            User(
                username="jane_smith",
                email="jane@example.com",
                hashed_password="hashed_secret456",
                full_name="Jane Smith",
                age=28,
                is_active=True,
                is_superuser=False
            ),
        ]
        
        db.add_all(users)
        db.commit()
        
        # 刷新以获取 ID
        for user in users:
            db.refresh(user)
        
        print(f"✅ 创建了 {len(users)} 个示例用户")
        
        # 创建示例产品
        products = [
            Product(
                name="iPhone 15 Pro",
                description="最新款苹果手机，搭载A17 Pro芯片",
                price=7999.00,
                stock=100,
                category="电子产品",
                owner_id=users[0].id
            ),
            Product(
                name="MacBook Pro 16",
                description="强大的专业笔记本电脑",
                price=19999.00,
                stock=50,
                category="电子产品",
                owner_id=users[0].id
            ),
            Product(
                name="AirPods Pro",
                description="主动降噪无线耳机",
                price=1999.00,
                stock=200,
                category="配件",
                owner_id=users[1].id
            ),
            Product(
                name="iPad Air",
                description="轻薄强大的平板电脑",
                price=4799.00,
                stock=150,
                category="电子产品",
                owner_id=users[1].id
            ),
            Product(
                name="Apple Watch Series 9",
                description="健康和健身的终极设备",
                price=3199.00,
                stock=120,
                category="可穿戴设备",
                owner_id=users[2].id
            ),
        ]
        
        db.add_all(products)
        db.commit()
        
        print(f"✅ 创建了 {len(products)} 个示例产品")
        
        return True
        
    except Exception as e:
        print(f"❌ 插入示例数据失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def verify_data():
    """验证数据"""
    print("\n🔍 验证数据...")
    db = SessionLocal()
    
    try:
        user_count = db.query(User).count()
        product_count = db.query(Product).count()
        
        print(f"✅ 用户总数: {user_count}")
        print(f"✅ 产品总数: {product_count}")
        
        # 显示示例数据
        print("\n📊 示例用户:")
        users = db.query(User).limit(3).all()
        for user in users:
            print(f"  - {user.username} ({user.email}) - {user.full_name}")
        
        print("\n📊 示例产品:")
        products = db.query(Product).limit(5).all()
        for product in products:
            print(f"  - {product.name} - ¥{product.price} (库存: {product.stock})")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证数据失败: {e}")
        return False
    finally:
        db.close()


def main():
    """主函数"""
    print("=" * 60)
    print("FastAPI 数据库初始化")
    print("=" * 60)
    
    print(f"\n📋 配置信息:")
    print(f"  数据库: {settings.DB_NAME}")
    print(f"  主机: {settings.DB_HOST}:{settings.DB_PORT}")
    print(f"  用户: {settings.DB_USER}")
    
    # 1. 创建表
    if not create_tables():
        sys.exit(1)
    
    # 2. 插入示例数据
    if not insert_sample_data():
        sys.exit(1)
    
    # 3. 验证数据
    if not verify_data():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ 数据库初始化完成！")
    print("=" * 60)
    print("\n🚀 现在可以运行应用:")
    print("   python main.py")
    print("\n📚 或访问 API 文档:")
    print("   http://localhost:8000/docs")
    print("=" * 60)


if __name__ == "__main__":
    main()

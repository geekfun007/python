"""
项目完整性验证脚本
Project Verification Script

验证项目所有组件是否正确配置
"""
import os
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} 不存在")
        return False


def check_directory_exists(dirpath, description):
    """检查目录是否存在"""
    if os.path.isdir(dirpath):
        file_count = len([f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))])
        print(f"✅ {description}: {dirpath} ({file_count} 个文件)")
        return True
    else:
        print(f"❌ {description}: {dirpath} 不存在")
        return False


def verify_project():
    """验证项目结构"""
    print("=" * 60)
    print("FastAPI 项目完整性验证")
    print("=" * 60)
    
    all_checks_passed = True
    
    # 1. 核心文件
    print("\n📁 核心文件:")
    core_files = [
        ("main.py", "应用入口"),
        ("config.py", "配置文件"),
        ("init_db.py", "数据库初始化"),
        ("test_api.py", "API测试脚本"),
        ("requirements.txt", "生产依赖"),
        ("requirements-dev.txt", "开发依赖"),
    ]
    for filename, desc in core_files:
        if not check_file_exists(filename, desc):
            all_checks_passed = False
    
    # 2. 配置文件
    print("\n⚙️  配置文件:")
    config_files = [
        (".env.example", "环境变量示例"),
        (".gitignore", "Git忽略文件"),
        ("Dockerfile", "Docker配置"),
        ("docker-compose.yml", "Docker Compose配置"),
        ("Makefile", "项目管理命令"),
    ]
    for filename, desc in config_files:
        if not check_file_exists(filename, desc):
            all_checks_passed = False
    
    # 3. 文档文件
    print("\n📚 文档文件:")
    doc_files = [
        ("README.md", "主文档"),
        ("QUICKSTART.md", "快速开始"),
        ("ARCHITECTURE.md", "架构设计"),
        ("FASTAPI_PRINCIPLES.md", "FastAPI原理"),
        ("DATABASE_GUIDE.md", "数据库指南"),
        ("PROJECT_SUMMARY.md", "项目总结"),
    ]
    for filename, desc in doc_files:
        if not check_file_exists(filename, desc):
            all_checks_passed = False
    
    # 4. 应用目录
    print("\n📦 应用目录结构:")
    app_dirs = [
        ("app", "应用包"),
        ("app/api", "API层"),
        ("app/api/v1", "API v1"),
        ("app/core", "核心模块"),
        ("app/dal", "数据访问层"),
        ("app/models", "ORM模型"),
        ("app/schemas", "Pydantic模型"),
        ("app/middleware", "中间件"),
    ]
    for dirname, desc in app_dirs:
        if not check_directory_exists(dirname, desc):
            all_checks_passed = False
    
    # 5. 关键模块文件
    print("\n🔧 关键模块文件:")
    module_files = [
        ("app/__init__.py", "应用包初始化"),
        ("app/core/database.py", "数据库配置"),
        ("app/models/user.py", "用户模型"),
        ("app/models/product.py", "产品模型"),
        ("app/dal/base.py", "基础DAL"),
        ("app/dal/user_dal.py", "用户DAL"),
        ("app/dal/product_dal.py", "产品DAL"),
        ("app/schemas/user.py", "用户Schema"),
        ("app/schemas/product.py", "产品Schema"),
        ("app/api/v1/users.py", "用户API"),
        ("app/api/v1/products.py", "产品API"),
        ("app/middleware/logging.py", "日志中间件"),
    ]
    for filename, desc in module_files:
        if not check_file_exists(filename, desc):
            all_checks_passed = False
    
    # 6. 统计信息
    print("\n📊 项目统计:")
    
    # Python 文件数量
    py_files = list(Path('.').rglob('*.py'))
    py_files = [f for f in py_files if '__pycache__' not in str(f)]
    print(f"  Python 文件: {len(py_files)} 个")
    
    # Markdown 文件数量
    md_files = list(Path('.').rglob('*.md'))
    print(f"  文档文件: {len(md_files)} 个")
    
    # 代码行数统计（估算）
    total_lines = 0
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                total_lines += len(f.readlines())
        except:
            pass
    print(f"  代码总行数: {total_lines} 行")
    
    # 7. 验证导入
    print("\n🔍 验证 Python 导入:")
    try:
        import config
        print("✅ config 模块导入成功")
    except ImportError as e:
        print(f"❌ config 模块导入失败: {e}")
        all_checks_passed = False
    
    try:
        from app.core.database import Base, engine, SessionLocal
        print("✅ database 模块导入成功")
    except ImportError as e:
        print(f"❌ database 模块导入失败: {e}")
        all_checks_passed = False
    
    try:
        from app.models import User, Product
        print("✅ models 模块导入成功")
    except ImportError as e:
        print(f"❌ models 模块导入失败: {e}")
        all_checks_passed = False
    
    try:
        from app.dal import UserDAL, ProductDAL
        print("✅ dal 模块导入成功")
    except ImportError as e:
        print(f"❌ dal 模块导入失败: {e}")
        all_checks_passed = False
    
    try:
        from app.schemas import UserCreate, ProductCreate
        print("✅ schemas 模块导入成功")
    except ImportError as e:
        print(f"❌ schemas 模块导入失败: {e}")
        all_checks_passed = False
    
    # 8. 最终结果
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✅ 项目验证通过！所有组件都已正确配置。")
        print("\n🚀 下一步:")
        print("  1. 配置 .env 文件")
        print("  2. 创建 MySQL 数据库")
        print("  3. 运行 python init_db.py")
        print("  4. 启动应用 python main.py")
        print("  5. 访问 http://localhost:8000/docs")
    else:
        print("❌ 项目验证失败！请检查缺失的组件。")
    print("=" * 60)
    
    return all_checks_passed


if __name__ == "__main__":
    success = verify_project()
    sys.exit(0 if success else 1)

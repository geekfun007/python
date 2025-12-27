"""
Python 模块与模块化详解
包含：模块基础、导入方式、包结构、__init__.py、模块搜索路径、最佳实践等
"""

import sys
import os
import importlib
import importlib.util
from pathlib import Path
from types import ModuleType


# ============================================
# 1. 模块基础概念
# ============================================

def module_basics():
    """模块基础概念"""
    print("\n=== 模块基础概念 ===")
    
    print("""
    什么是模块？
    ─────────────────────────────────────
    • 模块(Module)是一个包含 Python 代码的 .py 文件
    • 模块可以包含函数、类、变量和可执行代码
    • 模块是代码重用和组织的基本单位
    
    模块的类型：
    ─────────────────────────────────────
    1. 内置模块 (Built-in)：随 Python 安装的模块
       例如：sys, os, math, json
    
    2. 标准库模块 (Standard Library)：Python 自带的模块
       例如：datetime, collections, pathlib
    
    3. 第三方模块 (Third-party)：通过 pip 安装
       例如：requests, numpy, pandas
    
    4. 自定义模块 (Custom)：自己编写的 .py 文件
    """)
    
    # 查看已加载的模块
    print("已加载的部分模块:")
    loaded = [name for name in sys.modules.keys() if not name.startswith('_')][:10]
    for name in loaded:
        print(f"  • {name}")


# ============================================
# 2. 导入模块的方式
# ============================================

def import_methods():
    """各种导入方式详解"""
    print("\n=== 导入模块的方式 ===")
    
    # 方式1: import module
    print("1. import module")
    import math
    print(f"   math.pi = {math.pi}")
    print(f"   math.sqrt(16) = {math.sqrt(16)}")
    
    # 方式2: import module as alias
    print("\n2. import module as alias")
    import datetime as dt
    print(f"   dt.date.today() = {dt.date.today()}")
    
    # 方式3: from module import name
    print("\n3. from module import name")
    from os.path import join, exists
    print(f"   join('a', 'b', 'c') = {join('a', 'b', 'c')}")
    print(f"   exists('/tmp') = {exists('/tmp')}")
    
    # 方式4: from module import name as alias
    print("\n4. from module import name as alias")
    from collections import Counter as Cnt
    print(f"   Cnt('hello') = {Cnt('hello')}")
    
    # 方式5: from module import * (不推荐)
    print("\n5. from module import * (不推荐)")
    print("   这会导入模块的所有公开名称")
    print("   可能会覆盖当前命名空间中的名称")
    print("   建议：只在交互式环境中使用")
    
    # 方式6: 延迟导入 (Lazy Import)
    print("\n6. 延迟导入 (Lazy Import)")
    def get_json():
        import json  # 仅在需要时导入
        return json
    print("   在函数内部导入，仅在调用时加载")


def import_internals():
    """导入机制内部原理"""
    print("\n=== 导入机制内部原理 ===")
    
    print("""
    导入模块时，Python 执行以下步骤：
    ─────────────────────────────────────
    1. 检查 sys.modules 缓存是否已存在该模块
    2. 如果不存在，按顺序搜索模块：
       a. 内置模块
       b. sys.path 中的路径
    3. 找到后创建模块对象
    4. 执行模块代码（仅首次导入）
    5. 将模块对象添加到 sys.modules
    6. 将名称绑定到当前命名空间
    """)
    
    # 查看 sys.path
    print("模块搜索路径 (sys.path):")
    for i, path in enumerate(sys.path[:5]):
        print(f"  {i}. {path}")
    if len(sys.path) > 5:
        print(f"  ... 还有 {len(sys.path) - 5} 个路径")
    
    # 检查模块是否已缓存
    print("\n检查模块是否在缓存中:")
    print(f"  'os' in sys.modules: {'os' in sys.modules}")
    print(f"  'nonexistent' in sys.modules: {'nonexistent' in sys.modules}")


# ============================================
# 3. 模块属性
# ============================================

def module_attributes():
    """模块特殊属性"""
    print("\n=== 模块特殊属性 ===")
    
    import json
    
    # __name__
    print("1. __name__ - 模块名称")
    print(f"   json.__name__ = '{json.__name__}'")
    print(f"   当前模块 __name__ = '{__name__}'")
    
    # __file__
    print("\n2. __file__ - 模块文件路径")
    print(f"   json.__file__ = '{json.__file__}'")
    
    # __doc__
    print("\n3. __doc__ - 模块文档字符串")
    print(f"   json.__doc__[:50] = '{json.__doc__[:50]}...'")
    
    # __package__
    print("\n4. __package__ - 模块所属包")
    print(f"   json.__package__ = '{json.__package__}'")
    
    # __spec__
    print("\n5. __spec__ - 模块规格信息")
    print(f"   json.__spec__.name = '{json.__spec__.name}'")
    print(f"   json.__spec__.loader = {type(json.__spec__.loader).__name__}")
    
    # __all__
    print("\n6. __all__ - 公开的名称列表")
    print("   定义 from module import * 时导出的名称")
    if hasattr(json, '__all__'):
        print(f"   json.__all__ = {json.__all__[:5]}...")
    
    # dir() 查看模块内容
    print("\n7. dir(module) - 查看模块内容")
    json_attrs = [a for a in dir(json) if not a.startswith('_')]
    print(f"   json 公开属性: {json_attrs}")


# ============================================
# 4. __name__ 和 __main__
# ============================================

def name_main_demo():
    """__name__ 和 __main__ 详解"""
    print("\n=== __name__ 和 __main__ ===")
    
    print("""
    __name__ 的值取决于模块的使用方式：
    ─────────────────────────────────────
    1. 直接运行脚本: __name__ == "__main__"
    2. 被导入时: __name__ == 模块名
    
    常见用法：
    ─────────────────────────────────────
    if __name__ == "__main__":
        # 只在直接运行时执行
        main()
    
    这样做的好处：
    • 区分 "作为脚本运行" 和 "被导入"
    • 允许模块既是库又是可执行脚本
    • 便于测试和调试
    """)
    
    # 示例
    print("当前 __name__ 值:")
    print(f"  __name__ = '{__name__}'")
    
    if __name__ == "__main__":
        print("  ✓ 这是直接运行的脚本")
    else:
        print("  ✓ 这是被导入的模块")


# ============================================
# 5. 创建自定义模块
# ============================================

def create_custom_module():
    """创建和使用自定义模块"""
    print("\n=== 创建自定义模块 ===")
    
    # 创建示例模块目录
    demo_dir = Path("/tmp/module_demo")
    demo_dir.mkdir(exist_ok=True)
    
    # 创建一个简单模块
    mymodule_content = '''"""
这是一个示例模块
演示模块的基本结构
"""

# 模块级变量
VERSION = "1.0.0"
AUTHOR = "Demo"

# 私有变量 (约定)
_internal_config = {"debug": False}

# 公开的名称列表
__all__ = ['greet', 'Calculator', 'VERSION']

def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

def _private_helper():
    """私有辅助函数"""
    pass

class Calculator:
    """计算器类"""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b

# 模块初始化代码 (导入时执行)
print(f"[mymodule] 模块已加载, 版本: {VERSION}")
'''
    
    mymodule_path = demo_dir / "mymodule.py"
    mymodule_path.write_text(mymodule_content)
    
    print(f"已创建模块: {mymodule_path}")
    print("\n模块内容结构:")
    print("""
    mymodule.py
    ├── VERSION (变量)
    ├── AUTHOR (变量)
    ├── _internal_config (私有变量)
    ├── __all__ (公开名称列表)
    ├── greet() (函数)
    ├── _private_helper() (私有函数)
    └── Calculator (类)
    """)
    
    # 动态导入模块
    print("动态导入模块:")
    sys.path.insert(0, str(demo_dir))
    
    try:
        # 如果已缓存，先移除
        if 'mymodule' in sys.modules:
            del sys.modules['mymodule']
        
        import mymodule
        
        print(f"\n使用模块:")
        print(f"  mymodule.VERSION = {mymodule.VERSION}")
        print(f"  mymodule.greet('Python') = {mymodule.greet('Python')}")
        
        calc = mymodule.Calculator()
        print(f"  calc.add(10, 5) = {calc.add(10, 5)}")
        
    finally:
        sys.path.remove(str(demo_dir))


# ============================================
# 6. 包 (Package) 结构
# ============================================

def package_structure():
    """Python 包结构详解"""
    print("\n=== Python 包结构 ===")
    
    print("""
    什么是包？
    ─────────────────────────────────────
    • 包是包含 __init__.py 的目录
    • 包用于组织相关的模块
    • 包可以嵌套形成层级结构
    
    典型的包结构：
    ─────────────────────────────────────
    mypackage/
    ├── __init__.py          # 包初始化文件
    ├── module1.py           # 模块
    ├── module2.py           # 模块
    └── subpackage/          # 子包
        ├── __init__.py
        └── module3.py
    
    __init__.py 的作用：
    ─────────────────────────────────────
    1. 标识目录是一个包
    2. 包初始化代码
    3. 定义 __all__ 控制 import *
    4. 提供便捷的导入接口
    """)


def create_demo_package():
    """创建演示包"""
    print("\n=== 创建演示包 ===")
    
    # 创建包目录结构
    pkg_root = Path("/tmp/demo_pkg")
    
    # 清理旧文件
    import shutil
    if pkg_root.exists():
        shutil.rmtree(pkg_root)
    
    # 创建目录
    pkg_root.mkdir(parents=True)
    (pkg_root / "utils").mkdir()
    (pkg_root / "models").mkdir()
    
    # 1. 主包 __init__.py
    init_content = '''"""
Demo Package - 演示包
一个用于演示 Python 包结构的示例包
"""

__version__ = "1.0.0"
__author__ = "Demo"

# 导入常用功能，方便用户使用
from .utils.helpers import format_name, validate_email
from .models.user import User

# 定义公开接口
__all__ = ['User', 'format_name', 'validate_email', 'utils', 'models']

print(f"[demo_pkg] 包已初始化, 版本: {__version__}")
'''
    (pkg_root / "__init__.py").write_text(init_content)
    
    # 2. utils/__init__.py
    utils_init = '''"""
工具模块
"""
from .helpers import format_name, validate_email
from .validators import is_valid_phone

__all__ = ['format_name', 'validate_email', 'is_valid_phone']
'''
    (pkg_root / "utils" / "__init__.py").write_text(utils_init)
    
    # 3. utils/helpers.py
    helpers_content = '''"""
辅助函数模块
"""

def format_name(first_name, last_name):
    """格式化姓名"""
    return f"{first_name.title()} {last_name.title()}"

def validate_email(email):
    """验证邮箱格式"""
    import re
    pattern = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
    return bool(re.match(pattern, email))

def _internal_helper():
    """内部辅助函数"""
    pass
'''
    (pkg_root / "utils" / "helpers.py").write_text(helpers_content)
    
    # 4. utils/validators.py
    validators_content = '''"""
验证器模块
"""

def is_valid_phone(phone):
    """验证电话号码"""
    import re
    pattern = r'^\\d{11}$'
    return bool(re.match(pattern, phone))

def is_valid_id(id_number):
    """验证身份证号"""
    return len(str(id_number)) == 18
'''
    (pkg_root / "utils" / "validators.py").write_text(validators_content)
    
    # 5. models/__init__.py
    models_init = '''"""
数据模型模块
"""
from .user import User
from .product import Product

__all__ = ['User', 'Product']
'''
    (pkg_root / "models" / "__init__.py").write_text(models_init)
    
    # 6. models/user.py
    user_content = '''"""
用户模型
"""

class User:
    """用户类"""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def __repr__(self):
        return f"User(name='{self.name}', email='{self.email}')"
    
    def greet(self):
        return f"Hello, I'm {self.name}"
'''
    (pkg_root / "models" / "user.py").write_text(user_content)
    
    # 7. models/product.py
    product_content = '''"""
产品模型
"""

class Product:
    """产品类"""
    
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price})"
'''
    (pkg_root / "models" / "product.py").write_text(product_content)
    
    print("创建的包结构:")
    print("""
    demo_pkg/
    ├── __init__.py          # 包主入口
    ├── utils/
    │   ├── __init__.py      # utils 子包
    │   ├── helpers.py       # 辅助函数
    │   └── validators.py    # 验证器
    └── models/
        ├── __init__.py      # models 子包
        ├── user.py          # 用户模型
        └── product.py       # 产品模型
    """)
    
    return pkg_root


def use_demo_package():
    """使用演示包"""
    print("\n=== 使用演示包 ===")
    
    pkg_root = Path("/tmp/demo_pkg")
    parent_dir = pkg_root.parent
    
    # 添加到路径
    sys.path.insert(0, str(parent_dir))
    
    try:
        # 清除缓存
        modules_to_remove = [k for k in sys.modules.keys() 
                           if k.startswith('demo_pkg')]
        for m in modules_to_remove:
            del sys.modules[m]
        
        print("1. 导入整个包:")
        import demo_pkg
        print(f"   demo_pkg.__version__ = {demo_pkg.__version__}")
        
        print("\n2. 使用顶层导出的功能:")
        user = demo_pkg.User("alice", "alice@example.com")
        print(f"   demo_pkg.User(...) = {user}")
        print(f"   demo_pkg.format_name('john', 'doe') = {demo_pkg.format_name('john', 'doe')}")
        
        print("\n3. 从子包导入:")
        from demo_pkg.utils import validate_email, is_valid_phone
        print(f"   validate_email('test@test.com') = {validate_email('test@test.com')}")
        print(f"   is_valid_phone('13800138000') = {is_valid_phone('13800138000')}")
        
        print("\n4. 从具体模块导入:")
        from demo_pkg.models.product import Product
        product = Product("Laptop", 999.99)
        print(f"   Product(...) = {product}")
        
        print("\n5. 查看包结构:")
        print(f"   dir(demo_pkg) = {[a for a in dir(demo_pkg) if not a.startswith('_')]}")
        
    finally:
        sys.path.remove(str(parent_dir))


# ============================================
# 7. 相对导入与绝对导入
# ============================================

def relative_vs_absolute_imports():
    """相对导入与绝对导入"""
    print("\n=== 相对导入与绝对导入 ===")
    
    print("""
    绝对导入 (Absolute Import)
    ─────────────────────────────────────
    从项目根目录开始的完整路径
    
    from mypackage.utils.helpers import format_name
    from mypackage.models import User
    import mypackage.utils
    
    优点：
    • 清晰明确
    • IDE 支持好
    • 推荐使用
    
    相对导入 (Relative Import)
    ─────────────────────────────────────
    相对于当前模块的位置
    
    from . import module          # 当前包
    from .. import module         # 父包
    from .module import func      # 当前包的模块
    from ..sibling import func    # 父包的兄弟模块
    
    示例 (在 demo_pkg/utils/helpers.py 中):
    ─────────────────────────────────────
    # 导入同级模块
    from .validators import is_valid_phone
    
    # 导入父包内容
    from .. import __version__
    
    # 导入兄弟包
    from ..models import User
    
    注意事项：
    ─────────────────────────────────────
    • 相对导入只能在包内使用
    • 不能在直接运行的脚本中使用相对导入
    • 推荐在包内部使用相对导入
    """)


# ============================================
# 8. 动态导入
# ============================================

def dynamic_import():
    """动态导入模块"""
    print("\n=== 动态导入 ===")
    
    # 方法1: importlib.import_module
    print("1. importlib.import_module()")
    module_name = "json"
    json_module = importlib.import_module(module_name)
    print(f"   导入 '{module_name}': {type(json_module)}")
    print(f"   json_module.dumps([1,2,3]) = {json_module.dumps([1,2,3])}")
    
    # 方法2: 从字符串导入
    print("\n2. 导入子模块")
    os_path = importlib.import_module("os.path")
    print(f"   os.path.sep = '{os_path.sep}'")
    
    # 方法3: __import__ (底层函数)
    print("\n3. __import__() 函数")
    math_module = __import__("math")
    print(f"   math.pi = {math_module.pi}")
    
    # 方法4: 从文件路径导入
    print("\n4. 从文件路径导入模块")
    print("""
    spec = importlib.util.spec_from_file_location("name", "/path/to/module.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    """)
    
    # 方法5: 插件系统示例
    print("5. 插件系统示例:")
    
    def load_plugin(plugin_name):
        """动态加载插件"""
        try:
            plugin = importlib.import_module(f"plugins.{plugin_name}")
            return plugin
        except ImportError:
            return None
    
    print("   load_plugin('my_plugin') - 动态加载插件模块")


# ============================================
# 9. 重新加载模块
# ============================================

def reload_module():
    """重新加载模块"""
    print("\n=== 重新加载模块 ===")
    
    print("""
    模块只会被导入一次（缓存在 sys.modules 中）
    如需重新加载修改后的模块，使用 importlib.reload()
    """)
    
    import json
    
    print("重新加载 json 模块:")
    print(f"  Before: id(json) = {id(json)}")
    
    importlib.reload(json)
    
    print(f"  After:  id(json) = {id(json)}")
    
    print("""
    注意事项：
    ─────────────────────────────────────
    • reload() 会重新执行模块代码
    • 已经导入的对象不会自动更新
    • 主要用于开发和调试
    • 生产环境中应避免使用
    
    示例：
    ─────────────────────────────────────
    from importlib import reload
    import mymodule
    
    # 修改 mymodule.py 后
    reload(mymodule)  # 重新加载
    """)


# ============================================
# 10. 模块搜索路径
# ============================================

def module_search_path():
    """模块搜索路径详解"""
    print("\n=== 模块搜索路径 ===")
    
    print("""
    Python 按以下顺序搜索模块：
    ─────────────────────────────────────
    1. 内置模块
    2. sys.path 中的路径:
       a. 当前脚本所在目录
       b. PYTHONPATH 环境变量
       c. 标准库目录
       d. site-packages (第三方包)
    """)
    
    print("当前 sys.path:")
    for i, path in enumerate(sys.path):
        print(f"  {i}. {path}")
    
    print("\n修改搜索路径的方法:")
    print("""
    # 方法1: 直接修改 sys.path
    sys.path.insert(0, '/my/custom/path')
    
    # 方法2: 使用 PYTHONPATH 环境变量
    export PYTHONPATH="/my/custom/path:$PYTHONPATH"
    
    # 方法3: 使用 .pth 文件 (放在 site-packages)
    # 创建 mypath.pth 文件，写入路径
    
    # 方法4: 使用 site 模块
    import site
    site.addsitedir('/my/custom/path')
    """)
    
    # 查找模块位置
    print("\n查找模块文件位置:")
    
    def find_module(name):
        """查找模块位置"""
        spec = importlib.util.find_spec(name)
        if spec and spec.origin:
            return spec.origin
        return "内置模块或未找到"
    
    modules = ['os', 'json', 'sys', 'collections']
    for mod in modules:
        print(f"  {mod}: {find_module(mod)}")


# ============================================
# 11. 命名空间包
# ============================================

def namespace_packages():
    """命名空间包 (PEP 420)"""
    print("\n=== 命名空间包 ===")
    
    print("""
    命名空间包 (Python 3.3+)
    ─────────────────────────────────────
    • 不需要 __init__.py 的包
    • 可以跨多个目录分布
    • 用于大型项目和插件系统
    
    传统包 vs 命名空间包:
    ─────────────────────────────────────
    传统包 (Regular Package):
    mypackage/
    └── __init__.py  # 必需
    
    命名空间包 (Namespace Package):
    mypackage/       # 无 __init__.py
    
    命名空间包用例:
    ─────────────────────────────────────
    # 目录A
    company/
    └── package_a/
        └── module_a.py
    
    # 目录B
    company/
    └── package_b/
        └── module_b.py
    
    # 可以这样导入:
    from company.package_a import module_a
    from company.package_b import module_b
    
    建议:
    ─────────────────────────────────────
    • 简单项目使用传统包
    • 复杂插件系统考虑命名空间包
    """)


# ============================================
# 12. 循环导入
# ============================================

def circular_import():
    """循环导入问题"""
    print("\n=== 循环导入问题 ===")
    
    print("""
    什么是循环导入？
    ─────────────────────────────────────
    模块A导入模块B，同时模块B也导入模块A
    
    # module_a.py
    from module_b import func_b
    
    def func_a():
        return "A"
    
    # module_b.py
    from module_a import func_a  # 循环！
    
    def func_b():
        return "B"
    
    解决方案:
    ─────────────────────────────────────
    1. 重构代码，提取公共部分
       # common.py - 放置共享代码
    
    2. 延迟导入（在函数内导入）
       def func():
           from module_b import func_b
           return func_b()
    
    3. 导入模块而非特定名称
       import module_b
       def func():
           return module_b.func_b()
    
    4. 使用 TYPE_CHECKING
       from typing import TYPE_CHECKING
       if TYPE_CHECKING:
           from module_b import ClassB  # 仅类型检查时导入
    
    最佳实践:
    ─────────────────────────────────────
    • 保持模块职责单一
    • 使用依赖注入
    • 合理组织代码结构
    """)


# ============================================
# 13. __all__ 详解
# ============================================

def all_attribute():
    """__all__ 属性详解"""
    print("\n=== __all__ 属性 ===")
    
    print("""
    __all__ 的作用:
    ─────────────────────────────────────
    1. 定义 from module import * 导出的名称
    2. 作为模块的公开 API 文档
    3. 帮助 IDE 进行代码补全
    
    示例:
    ─────────────────────────────────────
    # mymodule.py
    __all__ = ['public_func', 'PublicClass', 'PUBLIC_CONST']
    
    def public_func():
        pass
    
    def _private_func():  # 不在 __all__ 中
        pass
    
    class PublicClass:
        pass
    
    class _PrivateClass:  # 不在 __all__ 中
        pass
    
    PUBLIC_CONST = 42
    _PRIVATE_CONST = 0
    
    使用效果:
    ─────────────────────────────────────
    from mymodule import *
    # 只导入: public_func, PublicClass, PUBLIC_CONST
    
    # 但仍然可以显式导入私有成员
    from mymodule import _private_func  # 可以，但不推荐
    """)
    
    # 演示
    import json
    print("\njson 模块的 __all__:")
    if hasattr(json, '__all__'):
        print(f"  {json.__all__}")
    
    import os
    print("\nos 模块的部分 __all__:")
    if hasattr(os, '__all__'):
        print(f"  {os.__all__[:10]}... (共 {len(os.__all__)} 个)")


# ============================================
# 14. 模块设计最佳实践
# ============================================

def best_practices():
    """模块设计最佳实践"""
    print("\n=== 模块设计最佳实践 ===")
    
    print("""
    1. 模块命名
    ─────────────────────────────────────
    • 使用小写字母和下划线
    • 名称简短且有意义
    • 避免与标准库冲突
    
    ✓ user_manager.py
    ✓ http_client.py
    ✗ UserManager.py
    ✗ my-module.py
    
    2. 模块结构
    ─────────────────────────────────────
    '''
    模块文档字符串
    描述模块的功能和用法
    '''
    
    # 1. 标准库导入
    import os
    import sys
    
    # 2. 第三方库导入
    import requests
    import numpy as np
    
    # 3. 本地导入
    from .utils import helper
    
    # 4. 常量定义
    MAX_SIZE = 1024
    DEFAULT_TIMEOUT = 30
    
    # 5. 异常定义
    class CustomError(Exception):
        pass
    
    # 6. 类定义
    class MyClass:
        pass
    
    # 7. 函数定义
    def my_function():
        pass
    
    # 8. __all__ 定义
    __all__ = ['MyClass', 'my_function']
    
    # 9. 主程序入口
    if __name__ == "__main__":
        main()
    
    3. 导入规范
    ─────────────────────────────────────
    • 每个导入单独一行
    • 导入顺序: 标准库 > 第三方 > 本地
    • 避免 from x import *
    • 使用绝对导入（包内可用相对导入）
    
    4. 封装原则
    ─────────────────────────────────────
    • 使用 _前缀 标记私有成员
    • 使用 __all__ 定义公开接口
    • 提供清晰的文档字符串
    
    5. 包设计
    ─────────────────────────────────────
    • 在 __init__.py 中导出常用接口
    • 保持包结构扁平
    • 避免过深的嵌套
    """)


# ============================================
# 15. 实战项目结构
# ============================================

def practical_project_structure():
    """实战项目结构"""
    print("\n=== 实战项目结构 ===")
    
    print("""
    小型项目结构:
    ─────────────────────────────────────
    myproject/
    ├── myproject/
    │   ├── __init__.py
    │   ├── core.py
    │   └── utils.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_core.py
    ├── setup.py
    ├── requirements.txt
    └── README.md
    
    中型项目结构:
    ─────────────────────────────────────
    myproject/
    ├── src/
    │   └── myproject/
    │       ├── __init__.py
    │       ├── core/
    │       │   ├── __init__.py
    │       │   └── engine.py
    │       ├── utils/
    │       │   ├── __init__.py
    │       │   └── helpers.py
    │       └── api/
    │           ├── __init__.py
    │           └── routes.py
    ├── tests/
    ├── docs/
    ├── pyproject.toml
    └── README.md
    
    大型项目结构:
    ─────────────────────────────────────
    company_project/
    ├── src/
    │   ├── company/
    │   │   ├── __init__.py
    │   │   ├── auth/
    │   │   │   ├── __init__.py
    │   │   │   ├── models.py
    │   │   │   ├── services.py
    │   │   │   └── api.py
    │   │   ├── orders/
    │   │   │   ├── __init__.py
    │   │   │   ├── models.py
    │   │   │   ├── services.py
    │   │   │   └── api.py
    │   │   └── common/
    │   │       ├── __init__.py
    │   │       ├── database.py
    │   │       └── utils.py
    ├── tests/
    │   ├── unit/
    │   ├── integration/
    │   └── e2e/
    ├── scripts/
    ├── configs/
    ├── docs/
    └── pyproject.toml
    """)


# ============================================
# 16. 实战：创建可发布的包
# ============================================

def create_publishable_package():
    """创建可发布的包"""
    print("\n=== 创建可发布的包 ===")
    
    pkg_root = Path("/tmp/myawesomelib")
    
    import shutil
    if pkg_root.exists():
        shutil.rmtree(pkg_root)
    
    # 创建目录结构
    (pkg_root / "src" / "myawesomelib").mkdir(parents=True)
    (pkg_root / "tests").mkdir()
    
    # 1. pyproject.toml
    pyproject = '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "myawesomelib"
version = "0.1.0"
description = "An awesome library for demonstration"
readme = "README.md"
authors = [
    {name = "Your Name", email = "your@email.com"}
]
requires-python = ">=3.8"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "black", "mypy"]

[project.urls]
Homepage = "https://github.com/yourname/myawesomelib"
Documentation = "https://myawesomelib.readthedocs.io"

[project.scripts]
myawesomelib = "myawesomelib.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
'''
    (pkg_root / "pyproject.toml").write_text(pyproject)
    
    # 2. src/myawesomelib/__init__.py
    init_content = '''"""
MyAwesomeLib - An awesome library
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .core import awesome_function, AwesomeClass
from .utils import format_data

__all__ = ['awesome_function', 'AwesomeClass', 'format_data']
'''
    (pkg_root / "src" / "myawesomelib" / "__init__.py").write_text(init_content)
    
    # 3. src/myawesomelib/core.py
    core_content = '''"""
核心功能模块
"""

def awesome_function(data):
    """一个很棒的函数"""
    return f"Awesome: {data}"

class AwesomeClass:
    """一个很棒的类"""
    
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello from {self.name}!"
'''
    (pkg_root / "src" / "myawesomelib" / "core.py").write_text(core_content)
    
    # 4. src/myawesomelib/utils.py
    utils_content = '''"""
工具函数模块
"""

def format_data(data, style="default"):
    """格式化数据"""
    if style == "upper":
        return str(data).upper()
    elif style == "lower":
        return str(data).lower()
    return str(data)
'''
    (pkg_root / "src" / "myawesomelib" / "utils.py").write_text(utils_content)
    
    # 5. src/myawesomelib/cli.py
    cli_content = '''"""
命令行接口
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description="MyAwesomeLib CLI")
    parser.add_argument("command", choices=["greet", "format"])
    parser.add_argument("--name", default="World")
    
    args = parser.parse_args()
    
    if args.command == "greet":
        print(f"Hello, {args.name}!")
    elif args.command == "format":
        print(f"Formatted: {args.name}")

if __name__ == "__main__":
    main()
'''
    (pkg_root / "src" / "myawesomelib" / "cli.py").write_text(cli_content)
    
    # 6. tests/test_core.py
    test_content = '''"""
核心模块测试
"""

import pytest
from myawesomelib import awesome_function, AwesomeClass

def test_awesome_function():
    result = awesome_function("test")
    assert result == "Awesome: test"

def test_awesome_class():
    obj = AwesomeClass("MyLib")
    assert obj.greet() == "Hello from MyLib!"
'''
    (pkg_root / "tests" / "test_core.py").write_text(test_content)
    (pkg_root / "tests" / "__init__.py").write_text("")
    
    # 7. README.md
    readme_content = '''# MyAwesomeLib

An awesome library for demonstration.

## Installation

```bash
pip install myawesomelib
```

## Usage

```python
from myawesomelib import awesome_function, AwesomeClass

# 使用函数
result = awesome_function("hello")
print(result)  # Awesome: hello

# 使用类
obj = AwesomeClass("Demo")
print(obj.greet())  # Hello from Demo!
```

## CLI

```bash
myawesomelib greet --name Python
```

## License

MIT
'''
    (pkg_root / "README.md").write_text(readme_content)
    
    print(f"创建的包位置: {pkg_root}")
    print("\n包结构:")
    print("""
    myawesomelib/
    ├── pyproject.toml       # 现代包配置文件
    ├── README.md            # 说明文档
    ├── src/
    │   └── myawesomelib/
    │       ├── __init__.py  # 包入口，导出公开API
    │       ├── core.py      # 核心功能
    │       ├── utils.py     # 工具函数
    │       └── cli.py       # 命令行接口
    └── tests/
        ├── __init__.py
        └── test_core.py     # 测试文件
    """)
    
    print("发布包的步骤:")
    print("""
    1. 安装构建工具:
       pip install build twine
    
    2. 构建包:
       python -m build
    
    3. 上传到 PyPI:
       twine upload dist/*
    
    4. 安装开发模式:
       pip install -e .
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 模块与模块化详解")
    print("=" * 60)
    
    # 基础概念
    module_basics()
    import_methods()
    import_internals()
    
    # 模块属性
    module_attributes()
    name_main_demo()
    
    # 自定义模块
    create_custom_module()
    
    # 包结构
    package_structure()
    create_demo_package()
    use_demo_package()
    
    # 导入机制
    relative_vs_absolute_imports()
    dynamic_import()
    reload_module()
    module_search_path()
    
    # 高级主题
    namespace_packages()
    circular_import()
    all_attribute()
    
    # 最佳实践
    best_practices()
    practical_project_structure()
    
    # 实战
    create_publishable_package()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Python 高级教程 - 元类详解

元类是"类的类"，控制类的创建过程。
本模块涵盖:
1. 元类基础
2. type 与元类
3. __new__ 和 __init__ 的使用
4. 实战应用: 单例、ORM、插件系统
"""

from typing import Any, Dict, Tuple
import abc

# ============================================================================
# 1. 元类基础 - 理解类的创建
# ============================================================================

print("=" * 60)
print("1. 理解元类基础")
print("=" * 60)

# 类也是对象，可以动态创建
def create_class_dynamically():
    """使用 type() 动态创建类"""
    
    # type(name, bases, dict) 创建类
    MyClass = type('MyClass', (), {
        'x': 10,
        'get_x': lambda self: self.x
    })
    
    obj = MyClass()
    print(f"动态创建的类: {MyClass}")
    print(f"类的类型: {type(MyClass)}")
    print(f"对象的类型: {type(obj)}")
    print(f"obj.get_x() = {obj.get_x()}")
    print()


# ============================================================================
# 2. 自定义元类 - 控制类的创建
# ============================================================================

class Meta(type):
    """自定义元类示例"""
    
    def __new__(mcs, name: str, bases: Tuple, attrs: Dict):
        """
        __new__ 在类创建时调用
        mcs: 元类本身
        name: 类名
        bases: 基类元组
        attrs: 类属性字典
        """
        print(f"\n创建类: {name}")
        print(f"基类: {bases}")
        print(f"属性: {list(attrs.keys())}")
        
        # 可以修改类属性
        attrs['created_by'] = 'Meta'
        attrs['class_id'] = id(attrs)
        
        # 调用父类创建类对象
        return super().__new__(mcs, name, bases, attrs)
    
    def __init__(cls, name: str, bases: Tuple, attrs: Dict):
        """
        __init__ 在类创建后调用
        cls: 新创建的类
        """
        print(f"初始化类: {name}")
        super().__init__(name, bases, attrs)


class MyClass(metaclass=Meta):
    """使用自定义元类的类"""
    
    def __init__(self, value):
        self.value = value
    
    def display(self):
        print(f"Value: {self.value}")


# ============================================================================
# 3. 单例元类
# ============================================================================

class SingletonMeta(type):
    """单例模式元类 - 确保类只有一个实例"""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """
        拦截类的实例化过程
        当调用 MyClass() 时会调用此方法
        """
        if cls not in cls._instances:
            # 创建新实例
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """数据库连接类 - 单例模式"""
    
    def __init__(self, host: str = "localhost", port: int = 5432):
        self.host = host
        self.port = port
        print(f"初始化数据库连接: {host}:{port}")
    
    def connect(self):
        return f"连接到 {self.host}:{self.port}"


# ============================================================================
# 4. 属性验证元类
# ============================================================================

class ValidatedMeta(type):
    """属性验证元类"""
    
    def __new__(mcs, name, bases, attrs):
        # 收集所有需要验证的属性
        validators = {}
        for key, value in attrs.items():
            if key.startswith('validate_'):
                field_name = key.replace('validate_', '')
                validators[field_name] = value
        
        # 存储验证器
        attrs['_validators'] = validators
        
        return super().__new__(mcs, name, bases, attrs)


class Person(metaclass=ValidatedMeta):
    """使用验证元类的 Person 类"""
    
    @staticmethod
    def validate_age(value):
        if not isinstance(value, int):
            raise TypeError("年龄必须是整数")
        if value < 0 or value > 150:
            raise ValueError("年龄必须在 0-150 之间")
        return value
    
    @staticmethod
    def validate_name(value):
        if not isinstance(value, str):
            raise TypeError("姓名必须是字符串")
        if len(value) < 2:
            raise ValueError("姓名至少2个字符")
        return value
    
    def __init__(self, name: str, age: int):
        # 使用验证器
        if 'name' in self._validators:
            name = self._validators['name'](name)
        if 'age' in self._validators:
            age = self._validators['age'](age)
        
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


# ============================================================================
# 5. ORM 元类 - 简化的数据库模型
# ============================================================================

class Field:
    """数据库字段基类"""
    
    def __init__(self, field_type, default=None):
        self.field_type = field_type
        self.default = default
    
    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.field_type.__name__}>"


class IntegerField(Field):
    """整数字段"""
    def __init__(self, default=0):
        super().__init__(int, default)


class StringField(Field):
    """字符串字段"""
    def __init__(self, max_length=255, default=""):
        super().__init__(str, default)
        self.max_length = max_length


class ModelMeta(type):
    """ORM 模型元类"""
    
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return super().__new__(mcs, name, bases, attrs)
        
        # 收集字段
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                attrs.pop(key)  # 从类属性中移除
        
        # 存储字段信息
        attrs['_fields'] = fields
        attrs['_table_name'] = name.lower()
        
        return super().__new__(mcs, name, bases, attrs)


class Model(metaclass=ModelMeta):
    """ORM 基类"""
    
    def __init__(self, **kwargs):
        # 初始化字段
        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, field.default)
            setattr(self, field_name, value)
    
    def save(self):
        """保存到数据库 (模拟)"""
        fields = []
        values = []
        for field_name in self._fields:
            fields.append(field_name)
            values.append(repr(getattr(self, field_name)))
        
        sql = f"INSERT INTO {self._table_name} ({', '.join(fields)}) " \
              f"VALUES ({', '.join(values)})"
        return sql
    
    def __repr__(self):
        attrs = ', '.join(
            f"{k}={repr(getattr(self, k))}"
            for k in self._fields
        )
        return f"{self.__class__.__name__}({attrs})"


class User(Model):
    """用户模型"""
    id = IntegerField()
    username = StringField(max_length=50)
    email = StringField(max_length=100)
    age = IntegerField()


# ============================================================================
# 6. 插件注册元类
# ============================================================================

class PluginMeta(type):
    """插件注册元类"""
    
    plugins = {}
    
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        
        # 注册插件 (跳过基类)
        if name != 'Plugin' and 'plugin_name' in attrs:
            plugin_name = attrs['plugin_name']
            mcs.plugins[plugin_name] = cls
            print(f"注册插件: {plugin_name} -> {name}")
        
        return cls


class Plugin(metaclass=PluginMeta):
    """插件基类"""
    
    @classmethod
    def get_plugin(cls, name: str):
        """获取插件类"""
        return PluginMeta.plugins.get(name)
    
    @classmethod
    def list_plugins(cls):
        """列出所有插件"""
        return list(PluginMeta.plugins.keys())
    
    def execute(self):
        raise NotImplementedError


class JSONPlugin(Plugin):
    """JSON 处理插件"""
    plugin_name = 'json'
    
    def execute(self):
        return "处理 JSON 数据"


class XMLPlugin(Plugin):
    """XML 处理插件"""
    plugin_name = 'xml'
    
    def execute(self):
        return "处理 XML 数据"


class CSVPlugin(Plugin):
    """CSV 处理插件"""
    plugin_name = 'csv'
    
    def execute(self):
        return "处理 CSV 数据"


# ============================================================================
# 7. 抽象基类元类 (ABC)
# ============================================================================

class AbstractAnimal(abc.ABC):
    """抽象动物类"""
    
    @abc.abstractmethod
    def make_sound(self) -> str:
        """发出声音 - 必须实现"""
        pass
    
    @abc.abstractmethod
    def move(self) -> str:
        """移动方式 - 必须实现"""
        pass
    
    def describe(self):
        """描述动物 - 可选实现"""
        return f"{self.__class__.__name__}: {self.make_sound()}, {self.move()}"


class Dog(AbstractAnimal):
    """狗类"""
    
    def make_sound(self) -> str:
        return "汪汪叫"
    
    def move(self) -> str:
        return "四条腿跑"


class Bird(AbstractAnimal):
    """鸟类"""
    
    def make_sound(self) -> str:
        return "叽叽喳喳"
    
    def move(self) -> str:
        return "飞翔"


# ============================================================================
# 8. 属性自动添加元类
# ============================================================================

class AutoPropertyMeta(type):
    """自动为私有属性添加 property 的元类"""
    
    def __new__(mcs, name, bases, attrs):
        # 为以 _ 开头的属性创建 property
        for attr_name in list(attrs.keys()):
            if attr_name.startswith('_') and not attr_name.startswith('__'):
                prop_name = attr_name[1:]  # 去掉下划线
                
                # 创建 getter 和 setter
                def make_getter(attr):
                    return lambda self: getattr(self, attr)
                
                def make_setter(attr):
                    return lambda self, value: setattr(self, attr, value)
                
                if prop_name not in attrs:
                    attrs[prop_name] = property(
                        make_getter(attr_name),
                        make_setter(attr_name)
                    )
        
        return super().__new__(mcs, name, bases, attrs)


class Circle(metaclass=AutoPropertyMeta):
    """圆形类 - 自动生成属性"""
    
    def __init__(self, radius: float):
        self._radius = radius
    
    def area(self):
        import math
        return math.pi * self._radius ** 2


# ============================================================================
# 演示函数
# ============================================================================

def demo_dynamic_class():
    """演示动态创建类"""
    print("\n" + "=" * 60)
    print("2. 动态创建类")
    print("=" * 60)
    create_class_dynamically()


def demo_custom_metaclass():
    """演示自定义元类"""
    print("=" * 60)
    print("3. 自定义元类")
    print("=" * 60)
    obj = MyClass(42)
    obj.display()
    print(f"created_by: {MyClass.created_by}")
    print(f"class_id: {MyClass.class_id}")
    print()


def demo_singleton():
    """演示单例元类"""
    print("=" * 60)
    print("4. 单例元类")
    print("=" * 60)
    db1 = Database("localhost", 5432)
    db2 = Database("remote", 3306)  # 返回同一实例
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1 连接: {db1.connect()}")
    print(f"db2 连接: {db2.connect()}")
    print()


def demo_validation():
    """演示属性验证"""
    print("=" * 60)
    print("5. 属性验证元类")
    print("=" * 60)
    
    try:
        person1 = Person("张三", 25)
        print(f"创建成功: {person1}")
        
        person2 = Person("李", 200)  # 验证失败
    except (TypeError, ValueError) as e:
        print(f"验证失败: {e}")
    print()


def demo_orm():
    """演示 ORM 元类"""
    print("=" * 60)
    print("6. ORM 元类")
    print("=" * 60)
    
    user = User(id=1, username="admin", email="admin@example.com", age=30)
    print(f"用户对象: {user}")
    print(f"表名: {User._table_name}")
    print(f"字段: {User._fields}")
    print(f"SQL: {user.save()}")
    print()


def demo_plugin_system():
    """演示插件注册"""
    print("=" * 60)
    print("7. 插件注册元类")
    print("=" * 60)
    
    print(f"可用插件: {Plugin.list_plugins()}")
    
    # 动态获取并使用插件
    for plugin_name in Plugin.list_plugins():
        PluginClass = Plugin.get_plugin(plugin_name)
        plugin = PluginClass()
        print(f"{plugin_name}: {plugin.execute()}")
    print()


def demo_abstract_class():
    """演示抽象基类"""
    print("=" * 60)
    print("8. 抽象基类 (ABC)")
    print("=" * 60)
    
    dog = Dog()
    bird = Bird()
    
    print(dog.describe())
    print(bird.describe())
    
    # 尝试实例化抽象类会失败
    try:
        animal = AbstractAnimal()
    except TypeError as e:
        print(f"\n不能实例化抽象类: {e}")
    print()


def demo_auto_property():
    """演示自动属性生成"""
    print("=" * 60)
    print("9. 自动属性元类")
    print("=" * 60)
    
    circle = Circle(5.0)
    print(f"半径 (通过属性): {circle.radius}")
    print(f"面积: {circle.area():.2f}")
    
    circle.radius = 10.0
    print(f"新半径: {circle.radius}")
    print(f"新面积: {circle.area():.2f}")
    print()


# ============================================================================
# 重要注意事项
# ============================================================================

"""
元类最佳实践和注意事项:

1. 何时使用元类
   ✓ 需要控制类的创建过程
   ✓ 实现框架级别的功能 (如 ORM)
   ✓ 自动注册、验证、修改类属性
   ✗ 简单的功能可用装饰器或继承实现
   
2. 元类方法
   - __new__: 创建类对象，返回类实例
   - __init__: 初始化类对象
   - __call__: 控制类的实例化过程
   - __prepare__: 准备类的命名空间 (很少用)

3. 执行顺序
   - 元类的 __new__ 和 __init__ 在类定义时执行
   - 元类的 __call__ 在创建类实例时执行
   - 顺序: MetaClass.__new__ -> MetaClass.__init__ -> 
           Class 定义完成 -> MetaClass.__call__ -> 
           Class.__new__ -> Class.__init__

4. 常见陷阱
   - 过度使用元类导致代码难以理解
   - 元类继承问题 (多重元类冲突)
   - 调试困难
   - 性能开销

5. 替代方案
   - 装饰器: 适用于修改单个类
   - __init_subclass__: Python 3.6+ 的简化方案
   - 描述符: 适用于属性级别的控制
   
6. 元类继承
   - 子类会继承父类的元类
   - 多个元类冲突需要创建组合元类
   - 使用 type() 检查元类

7. 调试技巧
   - 添加 print 语句跟踪执行流程
   - 使用 __mro__ 查看方法解析顺序
   - inspect 模块检查类结构

8. 实际应用场景
   - Django ORM: 数据库模型定义
   - SQLAlchemy: 数据库映射
   - abc.ABCMeta: 抽象基类
   - Enum: 枚举类型
   - 插件系统: 自动注册

9. Python 3.6+ 简化方案
   使用 __init_subclass__ 替代简单的元类:
   
   class Base:
       def __init_subclass__(cls, **kwargs):
           super().__init_subclass__(**kwargs)
           # 在这里处理子类
           
10. 性能考虑
    - 元类操作在类定义时执行一次
    - 不影响实例创建性能 (除非重写 __call__)
    - 复杂的元类逻辑会增加导入时间
"""


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Python 高级教程 - 元类详解")
    print("=" * 60)
    
    demo_dynamic_class()
    demo_custom_metaclass()
    demo_singleton()
    demo_validation()
    demo_orm()
    demo_plugin_system()
    demo_abstract_class()
    demo_auto_property()
    
    print("=" * 60)
    print("元类教程完成!")
    print("=" * 60)

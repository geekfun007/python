"""
Python 高级教程 - 描述符详解

描述符是 Python 中实现属性访问自定义逻辑的强大机制。
本模块涵盖:
1. 描述符协议
2. 数据描述符 vs 非数据描述符
3. property、classmethod、staticmethod 的实现
4. 实战应用: 类型检查、延迟计算、属性验证
"""

from typing import Any, Optional
import weakref
from functools import wraps

# ============================================================================
# 1. 描述符协议基础
# ============================================================================

class Descriptor:
    """基础描述符示例"""
    
    def __init__(self, name: str = None):
        self.name = name
    
    def __set_name__(self, owner, name):
        """Python 3.6+ 自动设置描述符名称"""
        self.name = name
    
    def __get__(self, instance, owner):
        """
        获取属性值
        instance: 实例对象 (类属性访问时为 None)
        owner: 所属类
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        """设置属性值"""
        print(f"设置 {self.name} = {value}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        """删除属性"""
        print(f"删除 {self.name}")
        del instance.__dict__[self.name]


class MyClass:
    """使用描述符的类"""
    x = Descriptor()
    
    def __init__(self, x):
        self.x = x


# ============================================================================
# 2. 类型检查描述符
# ============================================================================

class TypedProperty:
    """类型检查描述符"""
    
    def __init__(self, name: str, expected_type: type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} 必须是 {self.expected_type.__name__} 类型, "
                f"实际是 {type(value).__name__}"
            )
        instance.__dict__[self.name] = value


class Person:
    """使用类型检查描述符的类"""
    
    name = TypedProperty('name', str)
    age = TypedProperty('age', int)
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


# ============================================================================
# 3. 范围验证描述符
# ============================================================================

class RangeValidator:
    """范围验证描述符"""
    
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(
                f"{self.name} 不能小于 {self.min_value}, 实际值: {value}"
            )
        if self.max_value is not None and value > self.max_value:
            raise ValueError(
                f"{self.name} 不能大于 {self.max_value}, 实际值: {value}"
            )
        instance.__dict__[self.name] = value


class Product:
    """产品类"""
    
    price = RangeValidator(min_value=0, max_value=10000)
    quantity = RangeValidator(min_value=0)
    
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def total_value(self):
        return self.price * self.quantity
    
    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


# ============================================================================
# 4. 延迟计算描述符
# ============================================================================

class LazyProperty:
    """延迟计算属性描述符"""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # 检查是否已计算
        value = instance.__dict__.get(self.name)
        if value is None:
            print(f"计算 {self.name}...")
            value = self.func(instance)
            instance.__dict__[self.name] = value
        else:
            print(f"从缓存读取 {self.name}...")
        return value


class DataProcessor:
    """数据处理类"""
    
    def __init__(self, data: list):
        self.data = data
    
    @LazyProperty
    def sum(self):
        """延迟计算总和"""
        import time
        time.sleep(0.1)  # 模拟耗时操作
        return sum(self.data)
    
    @LazyProperty
    def average(self):
        """延迟计算平均值"""
        import time
        time.sleep(0.1)  # 模拟耗时操作
        return sum(self.data) / len(self.data) if self.data else 0


# ============================================================================
# 5. 自定义 property 实现
# ============================================================================

class MyProperty:
    """自定义 property 实现"""
    
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("属性不可读")
        return self.fget(instance)
    
    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("属性不可写")
        self.fset(instance, value)
    
    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("属性不可删除")
        self.fdel(instance)
    
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class Temperature:
    """温度类 - 使用自定义 property"""
    
    def __init__(self, celsius: float):
        self._celsius = celsius
    
    @MyProperty
    def celsius(self):
        """摄氏温度"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value
    
    @MyProperty
    def fahrenheit(self):
        """华氏温度"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9


# ============================================================================
# 6. 弱引用描述符 (避免内存泄漏)
# ============================================================================

class WeakDescriptor:
    """使用弱引用的描述符 - 避免循环引用"""
    
    def __init__(self):
        self.data = weakref.WeakKeyDictionary()
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.data.get(instance)
    
    def __set__(self, instance, value):
        self.data[instance] = value


class Node:
    """节点类 - 使用弱引用描述符"""
    
    parent = WeakDescriptor()
    
    def __init__(self, name: str):
        self.name = name
        self.parent = None
    
    def __repr__(self):
        parent_name = self.parent.name if self.parent else None
        return f"Node(name='{self.name}', parent='{parent_name}')"


# ============================================================================
# 7. 访问日志描述符
# ============================================================================

class LoggedAccess:
    """记录访问日志的描述符"""
    
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = getattr(instance, self.private_name)
        print(f"读取 {self.public_name} = {value}")
        return value
    
    def __set__(self, instance, value):
        print(f"写入 {self.public_name} = {value}")
        setattr(instance, self.private_name, value)


class Account:
    """账户类 - 带访问日志"""
    
    balance = LoggedAccess()
    
    def __init__(self, balance: float):
        self.balance = balance
    
    def deposit(self, amount: float):
        self.balance += amount
    
    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("余额不足")
        self.balance -= amount


# ============================================================================
# 8. 单位转换描述符
# ============================================================================

class Unit:
    """单位转换描述符基类"""
    
    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = '_' + name
    
    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Meter(Unit):
    """米单位描述符"""
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name, 0)


class Kilometer:
    """千米描述符"""
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.meter / 1000
    
    def __set__(self, instance, value):
        instance.meter = value * 1000


class Distance:
    """距离类 - 支持多种单位"""
    
    meter = Meter()
    kilometer = Kilometer()
    
    def __init__(self, meter: float = 0):
        self.meter = meter
    
    def __repr__(self):
        return f"Distance({self.meter}m / {self.kilometer}km)"


# ============================================================================
# 9. 方法描述符 (staticmethod 和 classmethod 的实现)
# ============================================================================

class StaticMethod:
    """自定义 staticmethod 实现"""
    
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        return self.func


class ClassMethod:
    """自定义 classmethod 实现"""
    
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            return self.func(owner, *args, **kwargs)
        return wrapper


class MyClass2:
    """演示自定义方法描述符"""
    
    @StaticMethod
    def static_func(x, y):
        return x + y
    
    @ClassMethod
    def class_func(cls, x):
        return f"{cls.__name__}: {x}"


# ============================================================================
# 10. 数据描述符 vs 非数据描述符
# ============================================================================

class DataDescriptor:
    """数据描述符 - 同时定义 __get__ 和 __set__"""
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(f"DataDescriptor.__get__ for {self.name}")
        return instance.__dict__.get('_' + self.name)
    
    def __set__(self, instance, value):
        print(f"DataDescriptor.__set__ for {self.name}")
        instance.__dict__['_' + self.name] = value


class NonDataDescriptor:
    """非数据描述符 - 只定义 __get__"""
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(f"NonDataDescriptor.__get__ for {self.name}")
        return instance.__dict__.get('_' + self.name, "默认值")


class Demo:
    """演示描述符优先级"""
    
    data = DataDescriptor()
    non_data = NonDataDescriptor()
    
    def __init__(self):
        self.data = "初始数据"
        self.non_data = "初始非数据"


# ============================================================================
# 演示函数
# ============================================================================

def demo_basic_descriptor():
    """演示基础描述符"""
    print("=" * 60)
    print("1. 基础描述符")
    print("=" * 60)
    obj = MyClass(10)
    print(f"obj.x = {obj.x}")
    obj.x = 20
    print(f"obj.x = {obj.x}")
    del obj.x
    print()


def demo_type_checking():
    """演示类型检查"""
    print("=" * 60)
    print("2. 类型检查描述符")
    print("=" * 60)
    person = Person("张三", 25)
    print(person)
    
    try:
        person.age = "三十"  # 类型错误
    except TypeError as e:
        print(f"错误: {e}")
    print()


def demo_range_validation():
    """演示范围验证"""
    print("=" * 60)
    print("3. 范围验证描述符")
    print("=" * 60)
    product = Product("笔记本", 5000, 10)
    print(product)
    print(f"总价值: {product.total_value()}")
    
    try:
        product.price = -100  # 范围错误
    except ValueError as e:
        print(f"错误: {e}")
    print()


def demo_lazy_property():
    """演示延迟计算"""
    print("=" * 60)
    print("4. 延迟计算描述符")
    print("=" * 60)
    processor = DataProcessor([1, 2, 3, 4, 5])
    print(f"第一次访问 sum: {processor.sum}")
    print(f"第二次访问 sum: {processor.sum}")
    print(f"第一次访问 average: {processor.average}")
    print()


def demo_custom_property():
    """演示自定义 property"""
    print("=" * 60)
    print("5. 自定义 Property")
    print("=" * 60)
    temp = Temperature(25)
    print(f"摄氏温度: {temp.celsius}°C")
    print(f"华氏温度: {temp.fahrenheit}°F")
    
    temp.fahrenheit = 100
    print(f"新摄氏温度: {temp.celsius}°C")
    print()


def demo_weak_descriptor():
    """演示弱引用描述符"""
    print("=" * 60)
    print("6. 弱引用描述符")
    print("=" * 60)
    parent = Node("父节点")
    child = Node("子节点")
    child.parent = parent
    print(child)
    print()


def demo_logged_access():
    """演示访问日志"""
    print("=" * 60)
    print("7. 访问日志描述符")
    print("=" * 60)
    account = Account(1000)
    account.deposit(500)
    account.withdraw(200)
    print()


def demo_unit_conversion():
    """演示单位转换"""
    print("=" * 60)
    print("8. 单位转换描述符")
    print("=" * 60)
    distance = Distance(5000)
    print(distance)
    
    distance.kilometer = 10
    print(distance)
    print()


def demo_method_descriptors():
    """演示方法描述符"""
    print("=" * 60)
    print("9. 方法描述符")
    print("=" * 60)
    print(f"静态方法: {MyClass2.static_func(1, 2)}")
    print(f"类方法: {MyClass2.class_func(42)}")
    print()


def demo_descriptor_priority():
    """演示描述符优先级"""
    print("=" * 60)
    print("10. 描述符优先级")
    print("=" * 60)
    obj = Demo()
    
    print("数据描述符:")
    print(f"访问 obj.data: {obj.data}")
    obj.__dict__['data'] = "实例字典值"  # 数据描述符优先级高
    print(f"再次访问 obj.data: {obj.data}")
    
    print("\n非数据描述符:")
    print(f"访问 obj.non_data: {obj.non_data}")
    obj.__dict__['non_data'] = "实例字典值"  # 实例字典优先级高
    print(f"再次访问 obj.non_data: {obj.non_data}")
    print()


# ============================================================================
# 重要注意事项
# ============================================================================

"""
描述符最佳实践和注意事项:

1. 描述符协议
   - __get__(self, instance, owner): 获取属性
   - __set__(self, instance, value): 设置属性
   - __delete__(self, instance): 删除属性
   - __set_name__(self, owner, name): Python 3.6+ 自动设置名称

2. 数据描述符 vs 非数据描述符
   数据描述符: 定义了 __get__ 和 __set__
   非数据描述符: 只定义了 __get__
   
   属性查找优先级:
   1. 数据描述符 (类属性)
   2. 实例字典
   3. 非数据描述符 (类属性)
   4. 类字典
   5. __getattr__

3. 常见应用场景
   - 属性验证 (类型、范围、格式)
   - 延迟计算和缓存
   - 单位转换
   - 访问控制和日志
   - ORM 字段定义

4. property 实现
   property 是数据描述符的标准实现
   支持 getter、setter、deleter
   
5. 方法也是描述符
   - staticmethod: 返回原始函数
   - classmethod: 返回绑定类的函数
   - 普通方法: 返回绑定实例的函数

6. 内存管理
   - 描述符实例在类级别创建 (所有实例共享)
   - 使用实例字典存储实例特定数据
   - 考虑使用弱引用避免内存泄漏

7. 性能考虑
   - 描述符调用有性能开销
   - 频繁访问的属性考虑使用 __slots__
   - 缓存计算结果

8. 调试技巧
   - 添加日志追踪描述符调用
   - 使用 __set_name__ 获取属性名
   - inspect.getmembers_static 避免触发描述符

9. 常见陷阱
   - 忘记处理 instance is None 的情况
   - 不使用 __set_name__ 导致名称不匹配
   - 循环引用导致内存泄漏
   - 数据描述符与实例属性冲突

10. 替代方案
    - 简单场景使用 @property
    - Python 3.6+ 使用 __set_name__
    - 考虑使用 __getattr__ 和 __setattr__
"""


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Python 高级教程 - 描述符详解")
    print("=" * 60 + "\n")
    
    demo_basic_descriptor()
    demo_type_checking()
    demo_range_validation()
    demo_lazy_property()
    demo_custom_property()
    demo_weak_descriptor()
    demo_logged_access()
    demo_unit_conversion()
    demo_method_descriptors()
    demo_descriptor_priority()
    
    print("=" * 60)
    print("描述符教程完成!")
    print("=" * 60)

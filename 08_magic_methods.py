"""
Python 高级教程 - 魔法方法详解

魔法方法 (Magic Methods) 也称特殊方法，用双下划线包围。
本模块涵盖:
1. 对象创建和初始化
2. 字符串表示
3. 运算符重载
4. 容器协议
5. 上下文管理器
6. 属性访问
"""

from typing import Any, Iterator, Optional
import copy

# ============================================================================
# 1. 对象创建和初始化
# ============================================================================

class Person:
    """演示对象创建过程"""
    
    def __new__(cls, name: str, age: int):
        """
        创建对象实例 - 在 __init__ 之前调用
        必须返回实例对象
        """
        print(f"__new__: 创建 {cls.__name__} 实例")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, name: str, age: int):
        """初始化对象属性"""
        print(f"__init__: 初始化实例")
        self.name = name
        self.age = age
    
    def __del__(self):
        """对象销毁时调用 (不推荐使用)"""
        print(f"__del__: 销毁 {self.name}")


# ============================================================================
# 2. 字符串表示
# ============================================================================

class Book:
    """书籍类 - 演示字符串表示"""
    
    def __init__(self, title: str, author: str, price: float):
        self.title = title
        self.author = author
        self.price = price
    
    def __str__(self) -> str:
        """用户友好的字符串表示 - str() 和 print()"""
        return f"《{self.title}》 by {self.author}"
    
    def __repr__(self) -> str:
        """开发者友好的字符串表示 - repr()"""
        return f"Book(title='{self.title}', author='{self.author}', price={self.price})"
    
    def __format__(self, format_spec: str) -> str:
        """自定义格式化 - format() 和 f-string"""
        if format_spec == 'short':
            return self.title
        elif format_spec == 'long':
            return f"{self.title} by {self.author} (${self.price})"
        return str(self)


# ============================================================================
# 3. 比较运算符
# ============================================================================

class Version:
    """版本号类 - 支持比较"""
    
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch
    
    def __eq__(self, other: Any) -> bool:
        """等于 =="""
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == \
               (other.major, other.minor, other.patch)
    
    def __lt__(self, other: Any) -> bool:
        """小于 <"""
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < \
               (other.major, other.minor, other.patch)
    
    def __le__(self, other: Any) -> bool:
        """小于等于 <="""
        return self == other or self < other
    
    def __gt__(self, other: Any) -> bool:
        """大于 >"""
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) > \
               (other.major, other.minor, other.patch)
    
    def __ge__(self, other: Any) -> bool:
        """大于等于 >="""
        return self == other or self > other
    
    def __ne__(self, other: Any) -> bool:
        """不等于 !="""
        return not self == other
    
    def __repr__(self) -> str:
        return f"Version({self.major}.{self.minor}.{self.patch})"


# ============================================================================
# 4. 数学运算符
# ============================================================================

class Vector:
    """向量类 - 支持数学运算"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Vector') -> 'Vector':
        """加法 +"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        """减法 -"""
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector':
        """乘法 * (标量乘法)"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: float) -> 'Vector':
        """右乘法 - 支持 scalar * vector"""
        return self * scalar
    
    def __truediv__(self, scalar: float) -> 'Vector':
        """除法 /"""
        return Vector(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> 'Vector':
        """取负 -"""
        return Vector(-self.x, -self.y)
    
    def __abs__(self) -> float:
        """绝对值 (模长)"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __eq__(self, other: Any) -> bool:
        """等于"""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"


# ============================================================================
# 5. 容器协议
# ============================================================================

class CustomList:
    """自定义列表 - 实现容器协议"""
    
    def __init__(self, *items):
        self._items = list(items)
    
    def __len__(self) -> int:
        """长度 - len()"""
        return len(self._items)
    
    def __getitem__(self, index: int) -> Any:
        """获取元素 - obj[index]"""
        return self._items[index]
    
    def __setitem__(self, index: int, value: Any) -> None:
        """设置元素 - obj[index] = value"""
        self._items[index] = value
    
    def __delitem__(self, index: int) -> None:
        """删除元素 - del obj[index]"""
        del self._items[index]
    
    def __contains__(self, item: Any) -> bool:
        """包含检查 - item in obj"""
        return item in self._items
    
    def __iter__(self) -> Iterator:
        """迭代 - for item in obj"""
        return iter(self._items)
    
    def __reversed__(self) -> Iterator:
        """反向迭代 - reversed(obj)"""
        return reversed(self._items)
    
    def __repr__(self) -> str:
        return f"CustomList({', '.join(repr(item) for item in self._items)})"


# ============================================================================
# 6. 可调用对象
# ============================================================================

class Multiplier:
    """可调用类 - 实现 __call__"""
    
    def __init__(self, factor: int):
        self.factor = factor
    
    def __call__(self, x: int) -> int:
        """使对象可调用 - obj(x)"""
        return x * self.factor


class Counter:
    """计数器 - 有状态的可调用对象"""
    
    def __init__(self):
        self.count = 0
    
    def __call__(self) -> int:
        """每次调用递增计数"""
        self.count += 1
        return self.count


# ============================================================================
# 7. 属性访问
# ============================================================================

class DynamicAttributes:
    """动态属性类"""
    
    def __init__(self):
        self._data = {}
    
    def __getattr__(self, name: str) -> Any:
        """获取不存在的属性时调用"""
        print(f"__getattr__: {name}")
        return self._data.get(name, f"未找到属性 {name}")
    
    def __setattr__(self, name: str, value: Any) -> None:
        """设置属性时调用"""
        if name == '_data':
            # 避免无限递归
            super().__setattr__(name, value)
        else:
            print(f"__setattr__: {name} = {value}")
            self._data[name] = value
    
    def __delattr__(self, name: str) -> None:
        """删除属性时调用"""
        print(f"__delattr__: {name}")
        if name in self._data:
            del self._data[name]
    
    def __getattribute__(self, name: str) -> Any:
        """获取任何属性时都会调用 (慎用)"""
        # 注意: 这会拦截所有属性访问
        return super().__getattribute__(name)


class ValidatedAttributes:
    """属性验证类"""
    
    def __init__(self):
        self._age = 0
    
    def __setattr__(self, name: str, value: Any) -> None:
        """属性设置验证"""
        if name == '_age':
            super().__setattr__(name, value)
        elif name == 'age':
            if not isinstance(value, int):
                raise TypeError("年龄必须是整数")
            if value < 0 or value > 150:
                raise ValueError("年龄必须在 0-150 之间")
            super().__setattr__('_age', value)
        else:
            super().__setattr__(name, value)
    
    def __getattr__(self, name: str) -> Any:
        if name == 'age':
            return self._age
        raise AttributeError(f"没有属性 {name}")


# ============================================================================
# 8. 上下文管理器
# ============================================================================

class ManagedResource:
    """资源管理器"""
    
    def __init__(self, name: str):
        self.name = name
    
    def __enter__(self):
        """进入上下文"""
        print(f"获取资源: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        print(f"释放资源: {self.name}")
        return False  # 不抑制异常


# ============================================================================
# 9. 描述符协议
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
            raise TypeError(f"{self.name} 必须是 {self.expected_type.__name__}")
        instance.__dict__[self.name] = value


# ============================================================================
# 10. 拷贝协议
# ============================================================================

class Node:
    """节点类 - 支持拷贝"""
    
    def __init__(self, value: int, next_node: Optional['Node'] = None):
        self.value = value
        self.next = next_node
    
    def __copy__(self) -> 'Node':
        """浅拷贝"""
        print(f"浅拷贝节点 {self.value}")
        return Node(self.value, self.next)
    
    def __deepcopy__(self, memo) -> 'Node':
        """深拷贝"""
        print(f"深拷贝节点 {self.value}")
        if self.next:
            next_copy = copy.deepcopy(self.next, memo)
        else:
            next_copy = None
        return Node(self.value, next_copy)
    
    def __repr__(self) -> str:
        if self.next:
            return f"Node({self.value}) -> {self.next}"
        return f"Node({self.value})"


# ============================================================================
# 11. 哈希和相等
# ============================================================================

class Point:
    """点类 - 可哈希"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __eq__(self, other: Any) -> bool:
        """相等比较"""
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        """哈希值 - 用于 set 和 dict 键"""
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


# ============================================================================
# 12. 布尔值转换
# ============================================================================

class Empty:
    """空对象 - 始终为 False"""
    
    def __bool__(self) -> bool:
        return False


class NonEmpty:
    """非空对象 - 根据内容判断"""
    
    def __init__(self, items: list):
        self.items = items
    
    def __bool__(self) -> bool:
        """有内容时为 True"""
        return len(self.items) > 0
    
    def __len__(self) -> int:
        return len(self.items)


# ============================================================================
# 演示函数
# ============================================================================

def demo_object_creation():
    """演示对象创建"""
    print("=" * 60)
    print("1. 对象创建和初始化")
    print("=" * 60)
    person = Person("张三", 25)
    print()


def demo_string_representation():
    """演示字符串表示"""
    print("=" * 60)
    print("2. 字符串表示")
    print("=" * 60)
    book = Book("Python 编程", "作者", 59.9)
    print(f"str(): {str(book)}")
    print(f"repr(): {repr(book)}")
    print(f"format(short): {format(book, 'short')}")
    print(f"format(long): {format(book, 'long')}")
    print()


def demo_comparison():
    """演示比较运算"""
    print("=" * 60)
    print("3. 比较运算符")
    print("=" * 60)
    v1 = Version(1, 2, 3)
    v2 = Version(1, 2, 5)
    v3 = Version(2, 0, 0)
    
    print(f"{v1} == {v2}: {v1 == v2}")
    print(f"{v1} < {v2}: {v1 < v2}")
    print(f"{v1} < {v3}: {v1 < v3}")
    print(f"{v3} > {v1}: {v3 > v1}")
    print()


def demo_math_operators():
    """演示数学运算"""
    print("=" * 60)
    print("4. 数学运算符")
    print("=" * 60)
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    
    print(f"{v1} + {v2} = {v1 + v2}")
    print(f"{v1} - {v2} = {v1 - v2}")
    print(f"{v1} * 2 = {v1 * 2}")
    print(f"3 * {v1} = {3 * v1}")
    print(f"{v1} / 2 = {v1 / 2}")
    print(f"-{v1} = {-v1}")
    print(f"|{v1}| = {abs(v1)}")
    print()


def demo_container_protocol():
    """演示容器协议"""
    print("=" * 60)
    print("5. 容器协议")
    print("=" * 60)
    lst = CustomList(1, 2, 3, 4, 5)
    
    print(f"列表: {lst}")
    print(f"长度: {len(lst)}")
    print(f"第一个元素: {lst[0]}")
    print(f"3 in lst: {3 in lst}")
    
    lst[0] = 10
    print(f"修改后: {lst}")
    
    print("遍历:")
    for item in lst:
        print(f"  {item}")
    print()


def demo_callable():
    """演示可调用对象"""
    print("=" * 60)
    print("6. 可调用对象")
    print("=" * 60)
    
    multiply_by_5 = Multiplier(5)
    print(f"multiply_by_5(10) = {multiply_by_5(10)}")
    
    counter = Counter()
    print(f"计数: {counter()}, {counter()}, {counter()}")
    print()


def demo_dynamic_attributes():
    """演示动态属性"""
    print("=" * 60)
    print("7. 动态属性访问")
    print("=" * 60)
    
    obj = DynamicAttributes()
    obj.name = "张三"
    obj.age = 25
    print(f"name: {obj.name}")
    print(f"age: {obj.age}")
    del obj.name
    print()


def demo_validated_attributes():
    """演示属性验证"""
    print("=" * 60)
    print("8. 属性验证")
    print("=" * 60)
    
    obj = ValidatedAttributes()
    obj.age = 25
    print(f"age: {obj.age}")
    
    try:
        obj.age = "三十"  # 类型错误
    except TypeError as e:
        print(f"错误: {e}")
    print()


def demo_copy():
    """演示拷贝"""
    print("=" * 60)
    print("9. 拷贝协议")
    print("=" * 60)
    
    node1 = Node(1, Node(2, Node(3)))
    print(f"原始: {node1}")
    
    shallow = copy.copy(node1)
    print(f"浅拷贝: {shallow}")
    
    deep = copy.deepcopy(node1)
    print(f"深拷贝: {deep}")
    print()


def demo_hashable():
    """演示哈希"""
    print("=" * 60)
    print("10. 哈希和集合")
    print("=" * 60)
    
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)
    
    print(f"p1 == p2: {p1 == p2}")
    print(f"hash(p1) == hash(p2): {hash(p1) == hash(p2)}")
    
    points = {p1, p2, p3}
    print(f"集合: {points}")
    print(f"集合长度: {len(points)}")
    print()


def demo_boolean():
    """演示布尔转换"""
    print("=" * 60)
    print("11. 布尔值转换")
    print("=" * 60)
    
    empty = Empty()
    print(f"bool(Empty()): {bool(empty)}")
    
    non_empty_with_items = NonEmpty([1, 2, 3])
    non_empty_without_items = NonEmpty([])
    
    print(f"bool(NonEmpty([1,2,3])): {bool(non_empty_with_items)}")
    print(f"bool(NonEmpty([])): {bool(non_empty_without_items)}")
    print()


# ============================================================================
# 重要注意事项
# ============================================================================

"""
魔法方法最佳实践和注意事项:

1. 常用魔法方法分类

   对象生命周期:
   - __new__: 创建实例
   - __init__: 初始化实例
   - __del__: 销毁实例 (很少使用)

   字符串表示:
   - __str__: 用户友好表示
   - __repr__: 开发者表示 (应该可eval)
   - __format__: 自定义格式化

   比较运算:
   - __eq__, __ne__: 相等/不等
   - __lt__, __le__, __gt__, __ge__: 大小比较

   数学运算:
   - __add__, __sub__, __mul__, __truediv__: 四则运算
   - __radd__, __rsub__: 右运算
   - __iadd__, __isub__: 增量赋值
   - __neg__, __pos__, __abs__: 一元运算

   容器协议:
   - __len__: 长度
   - __getitem__, __setitem__, __delitem__: 索引访问
   - __contains__: in 运算
   - __iter__: 迭代
   - __reversed__: 反向迭代

   属性访问:
   - __getattr__: 获取不存在的属性
   - __setattr__: 设置属性
   - __delattr__: 删除属性
   - __getattribute__: 拦截所有属性访问

   其他:
   - __call__: 可调用对象
   - __hash__: 哈希值
   - __bool__: 布尔值转换
   - __copy__, __deepcopy__: 拷贝

2. 重要原则

   - 实现 __eq__ 时也应该实现 __hash__ (如果要用于 set/dict)
   - __repr__ 应该返回可执行的代码
   - __str__ 优先考虑可读性
   - 实现一个比较运算符时，考虑实现全部
   - 使用 functools.total_ordering 简化比较运算符

3. 性能考虑

   - __getattribute__ 会拦截所有属性访问，性能开销大
   - 频繁调用的魔法方法要优化
   - 使用 __slots__ 减少内存占用

4. 安全性

   - __setattr__ 中避免无限递归
   - __getattribute__ 必须调用 super()
   - __del__ 不保证被调用，不要依赖它

5. 可读性

   - 不要过度使用魔法方法
   - 保持方法行为符合直觉
   - 文档化特殊行为

6. 调试技巧

   - 添加 print 语句追踪调用
   - 使用 __repr__ 便于调试
   - dir(obj) 查看所有魔法方法

7. 常见陷阱

   - 忘记返回 NotImplemented (比较运算)
   - __new__ 忘记返回实例
   - __init__ 有返回值
   - 在 __setattr__ 中直接设置属性导致无限递归
   - __hash__ 和 __eq__ 不一致

8. 实用工具

   functools.total_ordering: 自动生成比较方法
   dataclasses: 自动生成常用魔法方法
   abc: 抽象基类

9. Python 3.6+ 新特性

   - __init_subclass__: 子类化钩子
   - __set_name__: 描述符命名
   - __fspath__: 路径协议
   
10. 文档资源

    Python 数据模型文档:
    https://docs.python.org/3/reference/datamodel.html
"""


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Python 高级教程 - 魔法方法详解")
    print("=" * 60 + "\n")
    
    demo_object_creation()
    demo_string_representation()
    demo_comparison()
    demo_math_operators()
    demo_container_protocol()
    demo_callable()
    demo_dynamic_attributes()
    demo_validated_attributes()
    demo_copy()
    demo_hashable()
    demo_boolean()
    
    print("=" * 60)
    print("魔法方法教程完成!")
    print("=" * 60)

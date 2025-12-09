"""
Python 高级教程 - 类型提示详解

类型提示提高代码可读性和可维护性，支持静态类型检查。
本模块涵盖:
1. 基础类型提示
2. 泛型类型
3. Protocol 协议类型
4. TypeVar 和泛型函数
5. 实战应用
"""

from typing import (
    List, Dict, Tuple, Set, Optional, Union, Any, Callable,
    TypeVar, Generic, Protocol, Literal, Final, ClassVar,
    Sequence, Mapping, Iterable, Iterator, Type, cast,
    overload, runtime_checkable
)
from dataclasses import dataclass
from abc import ABC, abstractmethod

# ============================================================================
# 1. 基础类型提示
# ============================================================================

def greet(name: str) -> str:
    """基础类型提示"""
    return f"你好, {name}!"


def calculate_sum(numbers: List[int]) -> int:
    """列表类型提示"""
    return sum(numbers)


def get_user_info(user_id: int) -> Dict[str, Any]:
    """字典类型提示"""
    return {
        "id": user_id,
        "name": "张三",
        "age": 25
    }


def parse_coordinates(coord_str: str) -> Tuple[float, float]:
    """元组类型提示"""
    x, y = coord_str.split(',')
    return float(x), float(y)


# ============================================================================
# 2. Optional 和 Union 类型
# ============================================================================

def find_user(user_id: int) -> Optional[Dict[str, Any]]:
    """可能返回 None 的函数"""
    if user_id > 0:
        return {"id": user_id, "name": "用户"}
    return None


def process_value(value: Union[int, str, float]) -> str:
    """联合类型 - 接受多种类型"""
    return f"处理值: {value} (类型: {type(value).__name__})"


# Python 3.10+ 可以使用 | 语法
def modern_union(value: int | str | None) -> str:
    """现代联合类型语法"""
    if value is None:
        return "空值"
    return str(value)


# ============================================================================
# 3. 函数类型提示
# ============================================================================

def apply_operation(x: int, y: int, operation: Callable[[int, int], int]) -> int:
    """接受函数作为参数"""
    return operation(x, y)


def create_multiplier(factor: int) -> Callable[[int], int]:
    """返回函数"""
    def multiply(x: int) -> int:
        return x * factor
    return multiply


# ============================================================================
# 4. 泛型类型 (TypeVar)
# ============================================================================

T = TypeVar('T')  # 任意类型
K = TypeVar('K')  # 键类型
V = TypeVar('V')  # 值类型
Number = TypeVar('Number', int, float)  # 受限类型变量


def first_element(items: List[T]) -> T:
    """返回列表第一个元素 - 保持类型"""
    return items[0]


def swap_pair(pair: Tuple[T, K]) -> Tuple[K, T]:
    """交换元组元素"""
    return pair[1], pair[0]


def add_numbers(x: Number, y: Number) -> Number:
    """受限类型变量 - 只能是 int 或 float"""
    return x + y  # type: ignore


# ============================================================================
# 5. 泛型类
# ============================================================================

class Stack(Generic[T]):
    """泛型栈"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """压栈"""
        self._items.append(item)
    
    def pop(self) -> T:
        """出栈"""
        return self._items.pop()
    
    def peek(self) -> Optional[T]:
        """查看栈顶"""
        return self._items[-1] if self._items else None
    
    def is_empty(self) -> bool:
        """是否为空"""
        return len(self._items) == 0


class Pair(Generic[K, V]):
    """泛型键值对"""
    
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
    
    def get_key(self) -> K:
        return self.key
    
    def get_value(self) -> V:
        return self.value


# ============================================================================
# 6. Protocol - 结构化子类型
# ============================================================================

@runtime_checkable
class Drawable(Protocol):
    """可绘制协议"""
    
    def draw(self) -> str:
        ...


@runtime_checkable
class Comparable(Protocol):
    """可比较协议"""
    
    def __lt__(self, other: Any) -> bool:
        ...


class Circle:
    """圆形 - 实现 Drawable 协议"""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def draw(self) -> str:
        return f"绘制半径为 {self.radius} 的圆形"


class Rectangle:
    """矩形 - 实现 Drawable 协议"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"绘制 {self.width}x{self.height} 的矩形"


def render(shape: Drawable) -> None:
    """渲染形状 - 接受任何实现 Drawable 的对象"""
    print(shape.draw())


# ============================================================================
# 7. Literal 类型
# ============================================================================

def get_status(status: Literal['pending', 'approved', 'rejected']) -> str:
    """Literal 类型 - 限制为特定值"""
    return f"状态: {status}"


Mode = Literal['read', 'write', 'append']


def open_file(filename: str, mode: Mode) -> str:
    """使用 Literal 别名"""
    return f"以 {mode} 模式打开 {filename}"


# ============================================================================
# 8. Final 和 ClassVar
# ============================================================================

MAX_SIZE: Final[int] = 100  # 常量


class Configuration:
    """配置类"""
    
    app_name: ClassVar[str] = "MyApp"  # 类变量
    version: Final[str] = "1.0.0"  # 实例常量
    
    def __init__(self, debug: bool) -> None:
        self.debug: bool = debug


# ============================================================================
# 9. 数据类与类型提示
# ============================================================================

@dataclass
class User:
    """用户数据类"""
    id: int
    name: str
    email: str
    age: int
    active: bool = True
    tags: List[str] = None  # type: ignore
    
    def __post_init__(self) -> None:
        if self.tags is None:
            self.tags = []


@dataclass
class Point:
    """坐标点"""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """计算距离"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# ============================================================================
# 10. 函数重载 (overload)
# ============================================================================

@overload
def process(value: int) -> int:
    ...


@overload
def process(value: str) -> str:
    ...


def process(value: Union[int, str]) -> Union[int, str]:
    """函数重载 - 根据参数类型返回不同类型"""
    if isinstance(value, int):
        return value * 2
    else:
        return value.upper()


# ============================================================================
# 11. 类型别名
# ============================================================================

# 简单别名
UserId = int
UserName = str

# 复杂别名
UserDict = Dict[str, Union[str, int, bool]]
Coordinates = Tuple[float, float, float]
Matrix = List[List[float]]


def create_user(user_id: UserId, name: UserName) -> UserDict:
    """使用类型别名"""
    return {
        "id": user_id,
        "name": name,
        "active": True
    }


# ============================================================================
# 12. 泛型协议
# ============================================================================

class Container(Protocol[T]):
    """泛型容器协议"""
    
    def add(self, item: T) -> None:
        ...
    
    def get(self) -> T:
        ...


class IntContainer:
    """整数容器"""
    
    def __init__(self) -> None:
        self._items: List[int] = []
    
    def add(self, item: int) -> None:
        self._items.append(item)
    
    def get(self) -> int:
        return self._items[-1] if self._items else 0


# ============================================================================
# 13. 高级类型提示
# ============================================================================

def get_item(container: Sequence[T], index: int) -> T:
    """使用抽象类型 - Sequence 可以是 list, tuple 等"""
    return container[index]


def count_items(items: Iterable[Any]) -> int:
    """接受任何可迭代对象"""
    return sum(1 for _ in items)


def create_iterator(items: List[T]) -> Iterator[T]:
    """返回迭代器"""
    return iter(items)


# ============================================================================
# 14. 类型转换 (cast)
# ============================================================================

def process_config(config: Dict[str, Any]) -> None:
    """使用 cast 进行类型转换"""
    # 告诉类型检查器这是一个字符串
    name = cast(str, config.get('name'))
    print(f"配置名称: {name.upper()}")


# ============================================================================
# 15. 自定义泛型类
# ============================================================================

class Repository(Generic[T]):
    """通用仓库类"""
    
    def __init__(self, item_type: Type[T]) -> None:
        self._item_type = item_type
        self._items: Dict[int, T] = {}
        self._next_id = 1
    
    def add(self, item: T) -> int:
        """添加项目"""
        item_id = self._next_id
        self._items[item_id] = item
        self._next_id += 1
        return item_id
    
    def get(self, item_id: int) -> Optional[T]:
        """获取项目"""
        return self._items.get(item_id)
    
    def get_all(self) -> List[T]:
        """获取所有项目"""
        return list(self._items.values())
    
    def delete(self, item_id: int) -> bool:
        """删除项目"""
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False


# ============================================================================
# 演示函数
# ============================================================================

def demo_basic_types():
    """演示基础类型"""
    print("=" * 60)
    print("1. 基础类型提示")
    print("=" * 60)
    
    print(greet("张三"))
    print(f"求和: {calculate_sum([1, 2, 3, 4, 5])}")
    print(f"用户信息: {get_user_info(123)}")
    print(f"坐标: {parse_coordinates('10.5,20.3')}")
    print()


def demo_optional_union():
    """演示 Optional 和 Union"""
    print("=" * 60)
    print("2. Optional 和 Union 类型")
    print("=" * 60)
    
    print(f"查找用户 1: {find_user(1)}")
    print(f"查找用户 -1: {find_user(-1)}")
    print(process_value(42))
    print(process_value("Hello"))
    print(process_value(3.14))
    print()


def demo_function_types():
    """演示函数类型"""
    print("=" * 60)
    print("3. 函数类型提示")
    print("=" * 60)
    
    result = apply_operation(10, 5, lambda x, y: x + y)
    print(f"应用加法: {result}")
    
    multiply_by_3 = create_multiplier(3)
    print(f"乘以 3: {multiply_by_3(7)}")
    print()


def demo_generic_functions():
    """演示泛型函数"""
    print("=" * 60)
    print("4. 泛型函数")
    print("=" * 60)
    
    int_list = [1, 2, 3]
    str_list = ["a", "b", "c"]
    
    print(f"第一个整数: {first_element(int_list)}")
    print(f"第一个字符串: {first_element(str_list)}")
    
    print(f"交换 (1, 'a'): {swap_pair((1, 'a'))}")
    print()


def demo_generic_classes():
    """演示泛型类"""
    print("=" * 60)
    print("5. 泛型类")
    print("=" * 60)
    
    # 整数栈
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    int_stack.push(3)
    print(f"栈顶: {int_stack.peek()}")
    print(f"出栈: {int_stack.pop()}")
    
    # 字符串栈
    str_stack: Stack[str] = Stack()
    str_stack.push("Hello")
    str_stack.push("World")
    print(f"栈顶: {str_stack.peek()}")
    
    # 键值对
    pair: Pair[str, int] = Pair("age", 25)
    print(f"键: {pair.get_key()}, 值: {pair.get_value()}")
    print()


def demo_protocol():
    """演示 Protocol"""
    print("=" * 60)
    print("6. Protocol 协议类型")
    print("=" * 60)
    
    circle = Circle(5.0)
    rectangle = Rectangle(10, 20)
    
    render(circle)
    render(rectangle)
    
    # 运行时检查
    print(f"circle 是 Drawable? {isinstance(circle, Drawable)}")
    print()


def demo_literal():
    """演示 Literal"""
    print("=" * 60)
    print("7. Literal 类型")
    print("=" * 60)
    
    print(get_status('pending'))
    print(get_status('approved'))
    print(open_file('data.txt', 'read'))
    print()


def demo_dataclass():
    """演示数据类"""
    print("=" * 60)
    print("8. 数据类与类型提示")
    print("=" * 60)
    
    user = User(
        id=1,
        name="张三",
        email="zhangsan@example.com",
        age=25,
        tags=["Python", "编程"]
    )
    print(f"用户: {user}")
    
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    print(f"距离: {p1.distance_to(p2)}")
    print()


def demo_overload():
    """演示函数重载"""
    print("=" * 60)
    print("9. 函数重载")
    print("=" * 60)
    
    print(f"process(5): {process(5)}")
    print(f"process('hello'): {process('hello')}")
    print()


def demo_repository():
    """演示仓库模式"""
    print("=" * 60)
    print("10. 泛型仓库类")
    print("=" * 60)
    
    user_repo: Repository[User] = Repository(User)
    
    user1 = User(1, "张三", "zhangsan@example.com", 25)
    user2 = User(2, "李四", "lisi@example.com", 30)
    
    id1 = user_repo.add(user1)
    id2 = user_repo.add(user2)
    
    print(f"添加用户 ID: {id1}, {id2}")
    print(f"获取用户 {id1}: {user_repo.get(id1)}")
    print(f"所有用户: {len(user_repo.get_all())} 个")
    print()


# ============================================================================
# 重要注意事项
# ============================================================================

"""
类型提示最佳实践和注意事项:

1. 类型提示的好处
   ✓ 提高代码可读性和文档性
   ✓ IDE 提供更好的自动完成
   ✓ 静态类型检查 (mypy, pyright)
   ✓ 帮助发现潜在的 bug
   ✓ 重构更安全

2. 何时使用类型提示
   ✓ 公共 API 和接口
   ✓ 复杂的函数和类
   ✓ 团队协作项目
   ✓ 长期维护的代码
   ✗ 简单的脚本或原型

3. 基础类型
   - int, float, str, bool, None
   - List[T], Dict[K, V], Tuple[T, ...], Set[T]
   - Optional[T]: T | None
   - Union[T1, T2]: T1 | T2 (Python 3.10+)
   - Any: 任意类型

4. 高级类型
   - Callable: 函数类型
   - TypeVar: 泛型类型变量
   - Generic: 泛型基类
   - Protocol: 结构化子类型
   - Literal: 字面值类型
   - Final: 常量
   - ClassVar: 类变量

5. 类型检查工具
   - mypy: 最流行的静态类型检查器
   - pyright: 微软开发的类型检查器
   - pyre: Facebook 开发的类型检查器
   
   运行: mypy your_file.py

6. 渐进式类型
   - Python 是动态类型语言
   - 类型提示是可选的
   - 可以逐步添加类型提示
   - 使用 Any 作为过渡

7. Protocol vs ABC
   Protocol:
   - 结构化子类型 (鸭子类型)
   - 不需要显式继承
   - 更灵活

   ABC (抽象基类):
   - 名义化子类型
   - 需要显式继承
   - 更严格

8. 常见陷阱
   - 忘记导入类型 (from typing import ...)
   - 循环导入 (使用字符串 'ClassName')
   - 可变默认参数 (使用 None + __post_init__)
   - 过度使用 Any (失去类型检查)

9. 类型提示与运行时
   - 类型提示不影响运行时性能
   - Python 不强制类型检查
   - 使用 runtime_checkable 支持 isinstance
   - typing.get_type_hints() 获取类型提示

10. Python 版本差异
    Python 3.5+: 基础类型提示
    Python 3.6+: 变量注解
    Python 3.7+: dataclass, 延迟注解
    Python 3.8+: Literal, Protocol, TypedDict
    Python 3.9+: 内置集合类型 (list[int])
    Python 3.10+: | 联合语法
    Python 3.11+: Self 类型

11. 配置 mypy
    创建 mypy.ini:
    [mypy]
    python_version = 3.9
    warn_return_any = True
    warn_unused_configs = True
    disallow_untyped_defs = True

12. 实用建议
    - 从函数签名开始
    - 公共接口优先
    - 使用类型别名提高可读性
    - 文档字符串 + 类型提示
    - 定期运行类型检查
"""


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Python 高级教程 - 类型提示详解")
    print("=" * 60 + "\n")
    
    demo_basic_types()
    demo_optional_union()
    demo_function_types()
    demo_generic_functions()
    demo_generic_classes()
    demo_protocol()
    demo_literal()
    demo_dataclass()
    demo_overload()
    demo_repository()
    
    print("=" * 60)
    print("类型提示教程完成!")
    print("=" * 60)

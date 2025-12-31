"""
Python 类与面向对象编程 (with Type Hints)
=========================================

本文件涵盖：
- 类定义与实例化
- 属性与方法
- 继承与多态
- 特殊方法（魔术方法）
- dataclass
- 抽象类与接口
"""

from typing import Any, ClassVar, Self, Protocol, runtime_checkable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict, astuple
from functools import total_ordering
import copy

# ============================================================================
# 1. 基本类定义
# ============================================================================

class Person:
    """基本类示例"""
    
    # 类属性（所有实例共享）
    species: ClassVar[str] = "Homo sapiens"
    population: ClassVar[int] = 0
    
    def __init__(self, name: str, age: int) -> None:
        """构造函数"""
        # 实例属性
        self.name: str = name
        self.age: int = age
        self._id: int = Person.population  # 约定：单下划线表示"受保护"
        Person.population += 1
    
    def greet(self) -> str:
        """实例方法"""
        return f"Hello, I'm {self.name}, {self.age} years old."
    
    @classmethod
    def create_anonymous(cls) -> Self:
        """类方法：操作类本身"""
        return cls("Anonymous", 0)
    
    @staticmethod
    def is_adult(age: int) -> bool:
        """静态方法：不需要访问类或实例"""
        return age >= 18
    
    def __str__(self) -> str:
        """字符串表示（用户友好）"""
        return f"Person(name={self.name!r}, age={self.age})"
    
    def __repr__(self) -> str:
        """开发者表示（可重建对象）"""
        return f"Person({self.name!r}, {self.age})"


class BasicClassDemo:
    @staticmethod
    def demo() -> None:
        """基本类演示"""
        # 创建实例
        alice = Person("Alice", 30)
        bob = Person("Bob", 25)
        
        print(f"alice: {alice}")
        print(f"alice.greet(): {alice.greet()}")
        
        # 类属性
        print(f"Person.species: {Person.species}")
        print(f"Person.population: {Person.population}")
        
        # 类方法
        anon = Person.create_anonymous()
        print(f"Anonymous: {anon}")
        
        # 静态方法
        print(f"Is 20 adult? {Person.is_adult(20)}")


# ============================================================================
# 2. Property 属性
# ============================================================================

class Circle:
    """使用 property 控制属性访问"""
    
    def __init__(self, radius: float) -> None:
        self._radius: float = radius  # 私有属性
    
    @property
    def radius(self) -> float:
        """获取半径"""
        return self._radius
    
    @radius.setter
    def radius(self, value: float) -> None:
        """设置半径（带验证）"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @radius.deleter
    def radius(self) -> None:
        """删除半径"""
        del self._radius
    
    @property
    def diameter(self) -> float:
        """计算属性（只读）"""
        return self._radius * 2
    
    @property
    def area(self) -> float:
        """计算属性（只读）"""
        import math
        return math.pi * self._radius ** 2


class PropertyDemo:
    @staticmethod
    def demo() -> None:
        """Property 演示"""
        circle = Circle(5.0)
        
        print(f"radius: {circle.radius}")
        print(f"diameter: {circle.diameter}")
        print(f"area: {circle.area:.2f}")
        
        # 使用 setter
        circle.radius = 10.0
        print(f"New radius: {circle.radius}")
        
        # 验证
        try:
            circle.radius = -5.0
        except ValueError as e:
            print(f"Error: {e}")


# ============================================================================
# 3. 继承
# ============================================================================

class Animal:
    """基类"""
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def speak(self) -> str:
        """基类方法"""
        return f"{self.name} makes a sound"
    
    def move(self) -> str:
        return f"{self.name} moves"


class Dog(Animal):
    """继承 Animal"""
    
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)  # 调用父类构造
        self.breed = breed
    
    def speak(self) -> str:
        """覆盖父类方法"""
        return f"{self.name} barks: Woof!"
    
    def fetch(self) -> str:
        """子类特有方法"""
        return f"{self.name} fetches the ball"


class Cat(Animal):
    """另一个子类"""
    
    def speak(self) -> str:
        return f"{self.name} meows: Meow!"
    
    def scratch(self) -> str:
        return f"{self.name} scratches"


# 多重继承
class Flying:
    """混入类"""
    
    def fly(self) -> str:
        return "Flying through the air"


class Swimming:
    """混入类"""
    
    def swim(self) -> str:
        return "Swimming in water"


class Duck(Animal, Flying, Swimming):
    """多重继承"""
    
    def speak(self) -> str:
        return f"{self.name} quacks: Quack!"


class InheritanceDemo:
    @staticmethod
    def demo() -> None:
        """继承演示"""
        dog = Dog("Buddy", "Golden Retriever")
        cat = Cat("Whiskers")
        duck = Duck("Donald")
        
        # 多态
        animals: list[Animal] = [dog, cat, duck]
        for animal in animals:
            print(animal.speak())
        
        # 子类特有方法
        print(dog.fetch())
        print(cat.scratch())
        
        # 多重继承
        print(duck.fly())
        print(duck.swim())
        
        # 类型检查
        print(f"dog is Animal: {isinstance(dog, Animal)}")
        print(f"Dog is subclass of Animal: {issubclass(Dog, Animal)}")
        
        # MRO (Method Resolution Order)
        print(f"Duck MRO: {Duck.__mro__}")


# ============================================================================
# 4. 特殊方法（魔术方法）
# ============================================================================

@total_ordering  # 只需定义 __eq__ 和一个比较方法，自动生成其他
class Money:
    """演示各种特殊方法"""
    
    def __init__(self, amount: float, currency: str = "USD") -> None:
        self.amount = amount
        self.currency = currency
    
    # 字符串表示
    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"
    
    def __repr__(self) -> str:
        return f"Money({self.amount!r}, {self.currency!r})"
    
    # 比较运算
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency
    
    def __lt__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.amount < other.amount
    
    def __hash__(self) -> int:
        return hash((self.amount, self.currency))
    
    # 算术运算
    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)
    
    def __mul__(self, factor: float) -> "Money":
        return Money(self.amount * factor, self.currency)
    
    def __rmul__(self, factor: float) -> "Money":
        """支持 factor * money 形式"""
        return self.__mul__(factor)
    
    def __truediv__(self, factor: float) -> "Money":
        return Money(self.amount / factor, self.currency)
    
    def __neg__(self) -> "Money":
        return Money(-self.amount, self.currency)
    
    def __abs__(self) -> "Money":
        return Money(abs(self.amount), self.currency)
    
    # 布尔值
    def __bool__(self) -> bool:
        return self.amount != 0


class Vector:
    """向量类演示更多特殊方法"""
    
    def __init__(self, *components: float) -> None:
        self._components = list(components)
    
    # 序列协议
    def __len__(self) -> int:
        return len(self._components)
    
    def __getitem__(self, index: int) -> float:
        return self._components[index]
    
    def __setitem__(self, index: int, value: float) -> None:
        self._components[index] = value
    
    def __iter__(self):
        return iter(self._components)
    
    def __contains__(self, item: float) -> bool:
        return item in self._components
    
    # 可调用
    def __call__(self, scalar: float) -> "Vector":
        """使实例可调用，返回缩放后的向量"""
        return Vector(*[c * scalar for c in self._components])
    
    def __repr__(self) -> str:
        return f"Vector{tuple(self._components)}"


class MagicMethodsDemo:
    @staticmethod
    def demo() -> None:
        """特殊方法演示"""
        # Money
        m1 = Money(100, "USD")
        m2 = Money(50, "USD")
        
        print(f"m1: {m1}")
        print(f"m1 + m2: {m1 + m2}")
        print(f"m1 - m2: {m1 - m2}")
        print(f"m1 * 2: {m1 * 2}")
        print(f"2 * m1: {2 * m1}")
        print(f"m1 > m2: {m1 > m2}")
        print(f"bool(m1): {bool(m1)}")
        
        # Vector
        v = Vector(1, 2, 3)
        print(f"\nv: {v}")
        print(f"len(v): {len(v)}")
        print(f"v[0]: {v[0]}")
        print(f"2 in v: {2 in v}")
        print(f"v(2): {v(2)}")  # 调用
        
        # 迭代
        print(f"list(v): {list(v)}")


# ============================================================================
# 5. Context Manager 上下文管理器
# ============================================================================

class FileManager:
    """自定义上下文管理器"""
    
    def __init__(self, filename: str, mode: str = "r") -> None:
        self.filename = filename
        self.mode = mode
        self.file: Any = None
    
    def __enter__(self) -> Any:
        """进入 with 块时调用"""
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type: type | None, exc_val: Exception | None, 
                 exc_tb: Any) -> bool:
        """退出 with 块时调用"""
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        
        # 如果返回 True，异常会被抑制
        # 如果返回 False 或 None，异常会继续传播
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
        return False  # 不抑制异常


# 使用 contextlib 更简单
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    """计时器上下文管理器"""
    import time
    start = time.time()
    print(f"[{name}] Starting...")
    try:
        yield  # 这里执行 with 块内的代码
    finally:
        elapsed = time.time() - start
        print(f"[{name}] Finished in {elapsed:.4f}s")


class ContextManagerDemo:
    @staticmethod
    def demo() -> None:
        """上下文管理器演示"""
        # 使用 timer
        import time
        
        with timer("sleep"):
            time.sleep(0.1)
        
        # 可以获取 yield 的值
        @contextmanager
        def temp_value(initial: int):
            print(f"Setting up with {initial}")
            yield initial * 2
            print("Cleaning up")
        
        with temp_value(5) as value:
            print(f"Value inside context: {value}")


# ============================================================================
# 6. Dataclass
# ============================================================================

@dataclass
class Point2D:
    """基本 dataclass"""
    x: float
    y: float


@dataclass
class Point3D:
    """带默认值和方法的 dataclass"""
    x: float
    y: float
    z: float = 0.0
    
    def distance_from_origin(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5


@dataclass(frozen=True)  # 不可变
class FrozenPoint:
    """不可变 dataclass"""
    x: float
    y: float


@dataclass(order=True)  # 自动生成比较方法
class Student:
    """可排序的 dataclass"""
    # sort_index 用于排序但不参与 __init__
    sort_index: float = field(init=False, repr=False)
    name: str
    grade: float
    age: int = 18
    
    def __post_init__(self) -> None:
        """在 __init__ 之后调用"""
        self.sort_index = self.grade  # 按成绩排序


@dataclass
class Team:
    """包含可变默认值的 dataclass"""
    name: str
    # 可变默认值必须使用 field(default_factory=...)
    members: list[str] = field(default_factory=list)
    scores: dict[str, int] = field(default_factory=dict)


@dataclass
class Config:
    """带元数据的 dataclass"""
    host: str = field(metadata={"help": "Server hostname"})
    port: int = field(default=8080, metadata={"help": "Server port"})
    debug: bool = field(default=False, repr=False)  # 不显示在 repr 中


class DataclassDemo:
    @staticmethod
    def demo() -> None:
        """Dataclass 演示"""
        # 基本使用
        p1 = Point2D(3.0, 4.0)
        p2 = Point2D(3.0, 4.0)
        
        print(f"p1: {p1}")
        print(f"p1 == p2: {p1 == p2}")  # 自动生成 __eq__
        
        # 3D 点
        p3 = Point3D(1.0, 2.0, 2.0)
        print(f"Distance: {p3.distance_from_origin()}")
        
        # 不可变
        fp = FrozenPoint(1.0, 2.0)
        # fp.x = 3.0  # FrozenInstanceError!
        print(f"Frozen point: {fp}")
        
        # 可排序
        students = [
            Student("Alice", 85.0),
            Student("Bob", 92.0),
            Student("Charlie", 78.0),
        ]
        students.sort()
        print(f"Sorted students: {[s.name for s in students]}")
        
        # 转换
        print(f"As dict: {asdict(p1)}")
        print(f"As tuple: {astuple(p1)}")
        
        # 获取字段元数据
        from dataclasses import fields
        for f in fields(Config):
            print(f"Field {f.name}: {f.metadata}")


# ============================================================================
# 7. 抽象基类 (ABC)
# ============================================================================

class Shape(ABC):
    """抽象基类"""
    
    @abstractmethod
    def area(self) -> float:
        """计算面积（必须在子类中实现）"""
        ...
    
    @abstractmethod
    def perimeter(self) -> float:
        """计算周长"""
        ...
    
    def describe(self) -> str:
        """普通方法（可以有实现）"""
        return f"A shape with area {self.area():.2f}"


class Rectangle(Shape):
    """具体实现"""
    
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class CircleShape(Shape):
    """另一个实现"""
    
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius


class ABCDemo:
    @staticmethod
    def demo() -> None:
        """抽象基类演示"""
        # shape = Shape()  # TypeError: Can't instantiate abstract class
        
        rect = Rectangle(4.0, 5.0)
        circle = CircleShape(3.0)
        
        shapes: list[Shape] = [rect, circle]
        for shape in shapes:
            print(f"Area: {shape.area():.2f}, Perimeter: {shape.perimeter():.2f}")
            print(shape.describe())


# ============================================================================
# 8. Protocol（结构化子类型）
# ============================================================================

@runtime_checkable
class Drawable(Protocol):
    """Protocol：基于结构的接口"""
    
    def draw(self) -> None:
        """任何有 draw() 方法的类都符合此协议"""
        ...


class UIButton:
    """没有显式继承 Drawable，但有 draw 方法"""
    
    def __init__(self, label: str) -> None:
        self.label = label
    
    def draw(self) -> None:
        print(f"[Button: {self.label}]")


class UIText:
    def __init__(self, text: str) -> None:
        self.text = text
    
    def draw(self) -> None:
        print(f"Text: {self.text}")


def render_all(items: list[Drawable]) -> None:
    """接受任何符合 Drawable 协议的对象"""
    for item in items:
        item.draw()


class ProtocolDemo:
    @staticmethod
    def demo() -> None:
        """Protocol 演示"""
        items: list[Drawable] = [
            UIButton("Submit"),
            UIText("Hello World"),
        ]
        
        render_all(items)
        
        # 运行时检查（因为有 @runtime_checkable）
        print(f"UIButton is Drawable: {isinstance(UIButton('test'), Drawable)}")


# ============================================================================
# 9. Slots（优化内存）
# ============================================================================

class RegularClass:
    """普通类使用 __dict__ 存储属性"""
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class SlottedClass:
    """使用 __slots__ 限制属性并节省内存"""
    __slots__ = ('x', 'y')
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


@dataclass(slots=True)  # Python 3.10+
class SlottedDataclass:
    """带 slots 的 dataclass"""
    x: int
    y: int


class SlotsDemo:
    @staticmethod
    def demo() -> None:
        """Slots 演示"""
        import sys
        
        regular = RegularClass(1, 2)
        slotted = SlottedClass(1, 2)
        
        # 普通类可以动态添加属性
        regular.z = 3  # OK
        
        # slots 类不能
        try:
            slotted.z = 3  # type: ignore
        except AttributeError as e:
            print(f"Cannot add attribute to slotted class: {e}")
        
        # 内存比较
        print(f"Regular class dict: {regular.__dict__}")
        # print(slotted.__dict__)  # AttributeError: no __dict__
        
        print(f"Slotted class slots: {SlottedClass.__slots__}")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    print("=" * 60)
    print("BASIC CLASS DEMO")
    print("=" * 60)
    BasicClassDemo.demo()
    
    print("\n" + "=" * 60)
    print("PROPERTY DEMO")
    print("=" * 60)
    PropertyDemo.demo()
    
    print("\n" + "=" * 60)
    print("INHERITANCE DEMO")
    print("=" * 60)
    InheritanceDemo.demo()
    
    print("\n" + "=" * 60)
    print("MAGIC METHODS DEMO")
    print("=" * 60)
    MagicMethodsDemo.demo()
    
    print("\n" + "=" * 60)
    print("CONTEXT MANAGER DEMO")
    print("=" * 60)
    ContextManagerDemo.demo()
    
    print("\n" + "=" * 60)
    print("DATACLASS DEMO")
    print("=" * 60)
    DataclassDemo.demo()
    
    print("\n" + "=" * 60)
    print("ABC DEMO")
    print("=" * 60)
    ABCDemo.demo()
    
    print("\n" + "=" * 60)
    print("PROTOCOL DEMO")
    print("=" * 60)
    ProtocolDemo.demo()
    
    print("\n" + "=" * 60)
    print("SLOTS DEMO")
    print("=" * 60)
    SlotsDemo.demo()


if __name__ == "__main__":
    main()

"""
Python 基础语法与类型提示详解
=============================

Type Hints (类型提示) 是 Python 3.5+ 引入的特性，用于声明变量、参数和返回值的类型。
虽然 Python 是动态类型语言，类型提示不会影响运行时行为，但能提供：
1. 更好的代码可读性
2. IDE 智能提示支持
3. 静态类型检查工具支持 (mypy, pyright)
"""

from typing import (
    Any, Union, Optional, Literal, Final, 
    TypeVar, Generic, Callable, Annotated,
    TypeAlias, TypeGuard, Never, Self,
    overload, cast, TYPE_CHECKING
)
from collections.abc import Sequence, Mapping, Iterable, Iterator, Generator

# ============================================================================
# 1. 变量类型注解
# ============================================================================

# 基本类型注解
name: str = "Python"
age: int = 30
price: float = 99.99
is_active: bool = True

# Python 3.10+ 可以使用 | 代替 Union
# value: int | str = 10
value: Union[int, str] = 10

# Optional 等价于 Union[X, None]
maybe_name: Optional[str] = None  # 等价于 Union[str, None]

# Final 表示常量（不应被重新赋值）
MAX_SIZE: Final[int] = 100
API_URL: Final = "https://api.example.com"  # 类型会被推断

# Literal 限制具体的字面值
status: Literal["pending", "active", "done"] = "pending"
http_method: Literal["GET", "POST", "PUT", "DELETE"] = "GET"


# ============================================================================
# 2. 函数类型注解
# ============================================================================

def greet(name: str) -> str:
    """基本函数注解"""
    return f"Hello, {name}!"


def add(a: int, b: int = 0) -> int:
    """带默认参数的函数"""
    return a + b


def process_items(items: list[str], *, uppercase: bool = False) -> list[str]:
    """
    带关键字参数的函数
    * 后面的参数必须以关键字形式传递
    """
    if uppercase:
        return [item.upper() for item in items]
    return items


def get_user_info(user_id: int) -> dict[str, Any]:
    """返回字典类型"""
    return {"id": user_id, "name": "John", "active": True}


def divide(a: float, b: float) -> float | None:
    """可能返回 None 的函数 (Python 3.10+)"""
    if b == 0:
        return None
    return a / b


# 无返回值的函数
def log_message(message: str) -> None:
    """返回 None 的函数"""
    print(f"[LOG] {message}")


# 永不返回的函数（总是抛出异常或无限循环）
def raise_error(message: str) -> Never:
    """Never 表示函数永远不会正常返回"""
    raise RuntimeError(message)


# ============================================================================
# 3. *args 和 **kwargs 类型注解
# ============================================================================

def sum_all(*args: int) -> int:
    """*args 注解为单个元素类型"""
    return sum(args)


def create_user(**kwargs: str | int) -> dict[str, str | int]:
    """**kwargs 注解为值的类型"""
    return dict(kwargs)


def flexible_func(*args: Any, **kwargs: Any) -> None:
    """接受任意参数"""
    print(f"args: {args}, kwargs: {kwargs}")


# ============================================================================
# 4. Callable 类型 - 函数作为参数
# ============================================================================

# Callable[[参数类型列表], 返回类型]
def apply_operation(x: int, y: int, operation: Callable[[int, int], int]) -> int:
    """接受函数作为参数"""
    return operation(x, y)


# 使用示例
def multiply(a: int, b: int) -> int:
    return a * b

result = apply_operation(5, 3, multiply)  # 15


# 带可选参数的 Callable（使用 Protocol 更精确，这里简化）
SimpleCallback = Callable[[], None]
DataCallback = Callable[[str, int], bool]

def register_callback(callback: SimpleCallback) -> None:
    callback()


# ============================================================================
# 5. 泛型 (Generics) 与 TypeVar
# ============================================================================

# 定义类型变量
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

def first_element(items: list[T]) -> T | None:
    """返回列表第一个元素，类型与输入一致"""
    return items[0] if items else None

# 使用时，T 会被推断
num = first_element([1, 2, 3])      # int | None
text = first_element(["a", "b"])    # str | None


# 带约束的 TypeVar
Number = TypeVar('Number', int, float)  # 只能是 int 或 float

def double(value: Number) -> Number:
    return value * 2


# 带上界的 TypeVar
from collections.abc import Sized
SizedT = TypeVar('SizedT', bound=Sized)

def get_length(item: SizedT) -> int:
    return len(item)


# ============================================================================
# 6. 泛型类
# ============================================================================

class Stack(Generic[T]):
    """泛型栈实现"""
    
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()
    
    def peek(self) -> T | None:
        return self._items[-1] if self._items else None
    
    def __len__(self) -> int:
        return len(self._items)


# 使用泛型类
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
value = int_stack.pop()  # 类型推断为 int

str_stack: Stack[str] = Stack()
str_stack.push("hello")


class Pair(Generic[K, V]):
    """多类型参数的泛型类"""
    
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
    
    def swap(self) -> "Pair[V, K]":
        return Pair(self.value, self.key)


# ============================================================================
# 7. 类型别名 (Type Aliases)
# ============================================================================

# 简单别名
UserId = int
Username = str
UserData = dict[str, Any]

# Python 3.10+ 显式类型别名
ConnectionOptions: TypeAlias = dict[str, str | int | bool]

# 复杂类型别名
JsonValue: TypeAlias = (
    str | int | float | bool | None | 
    list["JsonValue"] | dict[str, "JsonValue"]
)

# 使用别名
def get_user(user_id: UserId) -> UserData:
    return {"id": user_id, "name": "John"}


# ============================================================================
# 8. 函数重载 (Overload)
# ============================================================================

@overload
def process(value: int) -> int: ...

@overload
def process(value: str) -> str: ...

@overload
def process(value: list[int]) -> list[int]: ...

def process(value: int | str | list[int]) -> int | str | list[int]:
    """
    实际实现 - @overload 装饰器告诉类型检查器：
    - 传入 int，返回 int
    - 传入 str，返回 str
    - 传入 list[int]，返回 list[int]
    """
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value.upper()
    else:
        return [x * 2 for x in value]


# ============================================================================
# 9. TypeGuard - 类型守卫
# ============================================================================

def is_string_list(items: list[Any]) -> TypeGuard[list[str]]:
    """类型守卫函数：验证列表是否全为字符串"""
    return all(isinstance(item, str) for item in items)


def process_strings(items: list[Any]) -> None:
    if is_string_list(items):
        # 在这个分支里，items 被视为 list[str]
        for item in items:
            print(item.upper())  # IDE 知道 item 是 str


# ============================================================================
# 10. Self 类型 (Python 3.11+)
# ============================================================================

class Builder:
    """使用 Self 类型实现链式调用"""
    
    def __init__(self) -> None:
        self._value: str = ""
    
    def add(self, text: str) -> Self:
        self._value += text
        return self
    
    def add_newline(self) -> Self:
        self._value += "\n"
        return self
    
    def build(self) -> str:
        return self._value


# 链式调用
result = Builder().add("Hello").add(" ").add("World").build()


# ============================================================================
# 11. Annotated - 带元数据的类型注解
# ============================================================================

# Annotated 允许在类型注解中添加元数据
PositiveInt = Annotated[int, "Must be positive"]
Email = Annotated[str, "Valid email address"]
Age = Annotated[int, "Between 0 and 150"]

def create_account(
    username: Annotated[str, "3-20 characters"],
    email: Email,
    age: Age
) -> dict[str, Any]:
    """Annotated 常用于验证框架（如 Pydantic）"""
    return {"username": username, "email": email, "age": age}


# ============================================================================
# 12. Protocol - 结构化子类型（鸭子类型的静态版本）
# ============================================================================

from typing import Protocol, runtime_checkable


class Drawable(Protocol):
    """定义接口：任何有 draw 方法的对象都符合"""
    
    def draw(self) -> None: ...


class Circle:
    """Circle 没有显式继承 Drawable，但有 draw 方法"""
    
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def draw(self) -> None:
        print(f"Drawing circle with radius {self.radius}")


class Square:
    def __init__(self, side: float) -> None:
        self.side = side
    
    def draw(self) -> None:
        print(f"Drawing square with side {self.side}")


def render(shape: Drawable) -> None:
    """接受任何符合 Drawable 协议的对象"""
    shape.draw()


# 都可以传入，因为它们都有 draw() 方法
render(Circle(5.0))
render(Square(3.0))


# 运行时可检查的 Protocol
@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...


class FileHandler:
    def close(self) -> None:
        print("File closed")


# 运行时检查
handler = FileHandler()
print(isinstance(handler, Closeable))  # True


# ============================================================================
# 13. 类型转换 cast()
# ============================================================================

def get_data() -> Any:
    return {"name": "John", "age": 30}


# cast 不做运行时检查，只是告诉类型检查器"相信我"
user_data = cast(dict[str, Any], get_data())
name = user_data["name"]


# ============================================================================
# 14. TYPE_CHECKING - 避免循环导入
# ============================================================================

if TYPE_CHECKING:
    # 这个导入只在类型检查时执行，运行时不执行
    from some_module import SomeHeavyClass


class MyClass:
    # 使用字符串形式的前向引用
    def method(self) -> "SomeHeavyClass":
        from some_module import SomeHeavyClass
        return SomeHeavyClass()


# ============================================================================
# 15. 实战示例：类型安全的配置管理器
# ============================================================================

from dataclasses import dataclass
from pathlib import Path


@dataclass
class DatabaseConfig:
    """数据库配置"""
    host: str
    port: int
    username: str
    password: str
    database: str
    
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class AppConfig:
    """应用配置"""
    debug: bool
    secret_key: str
    database: DatabaseConfig
    allowed_hosts: list[str]
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class ConfigManager(Generic[T]):
    """泛型配置管理器"""
    
    def __init__(self, config_class: type[T]) -> None:
        self._config_class = config_class
        self._config: T | None = None
    
    def load(self, data: dict[str, Any]) -> T:
        """从字典加载配置"""
        # 实际项目中可能使用 Pydantic 或其他库
        self._config = self._config_class(**data)
        return self._config
    
    def get(self) -> T:
        """获取配置"""
        if self._config is None:
            raise RuntimeError("Configuration not loaded")
        return self._config


# 使用示例
def main() -> None:
    # 创建管理器
    db_manager: ConfigManager[DatabaseConfig] = ConfigManager(DatabaseConfig)
    
    # 加载配置
    db_config = db_manager.load({
        "host": "localhost",
        "port": 5432,
        "username": "admin",
        "password": "secret",
        "database": "myapp"
    })
    
    print(f"Connection: {db_config.connection_string}")
    
    # 演示各种类型注解
    print(f"\nGreeting: {greet('Python')}")
    print(f"Sum: {sum_all(1, 2, 3, 4, 5)}")
    print(f"Process int: {process(42)}")
    print(f"Process str: {process('hello')}")


if __name__ == "__main__":
    main()

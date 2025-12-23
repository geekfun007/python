"""
Python 类型系统详解
包含：typing、类型注解、泛型、协议、类型检查等
"""

from typing import (
    List, Dict, Set, Tuple, Optional, Union, Any,
    Callable, TypeVar, Generic, Protocol, Literal,
    Final, ClassVar, TypedDict, NewType, cast,
    overload, get_type_hints, get_args, get_origin
)
from typing_extensions import TypeAlias, Self, Annotated
from dataclasses import dataclass
from abc import ABC, abstractmethod
from collections.abc import Sequence, Iterable, Mapping
import sys


# ============================================
# 1. 基础类型注解
# ============================================

def basic_type_annotations():
    """基础类型注解"""
    print("\n=== 基础类型注解 ===")
    
    # 变量类型注解
    name: str = "Alice"
    age: int = 25
    height: float = 1.75
    is_student: bool = True
    
    print(f"1. 变量注解:")
    print(f"  name: str = {name}")
    print(f"  age: int = {age}")
    print(f"  height: float = {height}")
    
    # 函数类型注解
    def greet(name: str, age: int) -> str:
        """带类型注解的函数"""
        return f"{name} is {age} years old"
    
    result = greet("Bob", 30)
    print(f"\n2. 函数注解:")
    print(f"  {result}")
    
    # 集合类型
    names: list[str] = ["Alice", "Bob", "Charlie"]  # Python 3.9+
    scores: dict[str, int] = {"Alice": 95, "Bob": 87}
    unique_ids: set[int] = {1, 2, 3, 4, 5}
    coordinates: tuple[int, int] = (10, 20)
    
    print(f"\n3. 集合类型注解:")
    print(f"  names: list[str] = {names}")
    print(f"  scores: dict[str, int] = {scores}")
    
    # 旧版本兼容（Python 3.7-3.8）
    old_style_list: List[str] = ["a", "b", "c"]
    old_style_dict: Dict[str, int] = {"x": 1, "y": 2}
    
    print(f"\n4. 旧版本写法 (typing 模块):")
    print(f"  List[str] = {old_style_list}")


# ============================================
# 2. 可选类型与联合类型
# ============================================

def optional_and_union_types():
    """可选类型与联合类型"""
    print("\n=== 可选类型与联合类型 ===")
    
    # Optional - 可能为 None
    def find_user(user_id: int) -> Optional[str]:
        """查找用户，可能返回 None"""
        users = {1: "Alice", 2: "Bob"}
        return users.get(user_id)
    
    print("1. Optional[T] (等价于 Union[T, None]):")
    print(f"  find_user(1) = {find_user(1)}")
    print(f"  find_user(999) = {find_user(999)}")
    
    # Union - 多种类型之一
    def process_id(user_id: Union[int, str]) -> str:
        """处理 int 或 str 类型的 ID"""
        return f"ID: {user_id}"
    
    print("\n2. Union[T1, T2]:")
    print(f"  process_id(123) = {process_id(123)}")
    print(f"  process_id('abc') = {process_id('abc')}")
    
    # Python 3.10+ 新语法
    if sys.version_info >= (3, 10):
        def new_union_syntax(value: int | str) -> int | str:
            """新的联合类型语法"""
            return value
        
        print("\n3. Python 3.10+ 新语法 (int | str):")
        print(f"  支持新语法")
    else:
        print("\n3. Python 3.10+ 新语法:")
        print(f"  需要 Python 3.10+")
    
    # Literal - 字面量类型
    def set_mode(mode: Literal["read", "write", "append"]) -> None:
        """只接受特定的字面量值"""
        print(f"  Mode set to: {mode}")
    
    print("\n4. Literal (字面量类型):")
    set_mode("read")
    set_mode("write")


# ============================================
# 3. 容器类型
# ============================================

def container_types():
    """容器类型注解"""
    print("\n=== 容器类型 ===")
    
    # List, Dict, Set, Tuple
    print("1. 基本容器:")
    numbers: List[int] = [1, 2, 3, 4, 5]
    mapping: Dict[str, int] = {"a": 1, "b": 2}
    unique: Set[str] = {"x", "y", "z"}
    pair: Tuple[int, str] = (1, "one")
    
    print(f"  List[int]: {numbers}")
    print(f"  Dict[str, int]: {mapping}")
    
    # 可变长度元组
    variable_tuple: Tuple[int, ...] = (1, 2, 3, 4, 5)
    print(f"\n2. 可变长度元组:")
    print(f"  Tuple[int, ...]: {variable_tuple}")
    
    # 嵌套类型
    matrix: List[List[int]] = [[1, 2, 3], [4, 5, 6]]
    nested_dict: Dict[str, List[int]] = {"a": [1, 2], "b": [3, 4]}
    
    print(f"\n3. 嵌套类型:")
    print(f"  List[List[int]]: {matrix}")
    print(f"  Dict[str, List[int]]: {nested_dict}")
    
    # Sequence, Iterable, Mapping
    def sum_numbers(numbers: Sequence[int]) -> int:
        """接受任何序列类型"""
        return sum(numbers)
    
    print(f"\n4. 抽象容器类型:")
    print(f"  sum_numbers([1,2,3]): {sum_numbers([1, 2, 3])}")
    print(f"  sum_numbers((4,5,6)): {sum_numbers((4, 5, 6))}")


# ============================================
# 4. 函数类型
# ============================================

def function_types():
    """函数类型注解"""
    print("\n=== 函数类型 ===")
    
    # Callable
    def apply_operation(x: int, y: int, op: Callable[[int, int], int]) -> int:
        """接受一个函数作为参数"""
        return op(x, y)
    
    def add(a: int, b: int) -> int:
        return a + b
    
    def multiply(a: int, b: int) -> int:
        return a * b
    
    print("1. Callable[[参数类型], 返回类型]:")
    print(f"  apply_operation(5, 3, add) = {apply_operation(5, 3, add)}")
    print(f"  apply_operation(5, 3, multiply) = {apply_operation(5, 3, multiply)}")
    
    # Lambda 类型
    transform: Callable[[int], int] = lambda x: x * 2
    print(f"\n2. Lambda 函数:")
    print(f"  transform(5) = {transform(5)}")
    
    # 无参数或返回值
    callback: Callable[[], None] = lambda: print("  Callback executed")
    print(f"\n3. 无参数函数:")
    callback()


# ============================================
# 5. 泛型 (Generic)
# ============================================

def generic_types():
    """泛型类型"""
    print("\n=== 泛型 ===")
    
    # TypeVar - 类型变量
    T = TypeVar('T')
    
    def first_element(items: List[T]) -> Optional[T]:
        """返回列表第一个元素"""
        return items[0] if items else None
    
    print("1. TypeVar:")
    print(f"  first_element([1,2,3]) = {first_element([1, 2, 3])}")
    print(f"  first_element(['a','b']) = {first_element(['a', 'b'])}")
    
    # 泛型类
    K = TypeVar('K')
    V = TypeVar('V')
    
    class Cache(Generic[K, V]):
        """泛型缓存类"""
        def __init__(self):
            self._data: Dict[K, V] = {}
        
        def set(self, key: K, value: V) -> None:
            self._data[key] = value
        
        def get(self, key: K) -> Optional[V]:
            return self._data.get(key)
    
    print("\n2. 泛型类:")
    int_cache: Cache[str, int] = Cache()
    int_cache.set("age", 25)
    print(f"  Cache[str, int]: {int_cache.get('age')}")
    
    # 受限类型变量
    NumberT = TypeVar('NumberT', int, float)
    
    def add_numbers(a: NumberT, b: NumberT) -> NumberT:
        """只接受 int 或 float"""
        return a + b  # type: ignore
    
    print("\n3. 受限 TypeVar:")
    print(f"  add_numbers(5, 3) = {add_numbers(5, 3)}")
    print(f"  add_numbers(5.5, 3.2) = {add_numbers(5.5, 3.2)}")


# ============================================
# 6. Protocol (协议)
# ============================================

def protocol_types():
    """Protocol 协议类型"""
    print("\n=== Protocol (协议) ===")
    
    # 定义协议
    class Drawable(Protocol):
        """可绘制对象协议"""
        def draw(self) -> str:
            ...
    
    # 实现协议（结构子类型）
    class Circle:
        def draw(self) -> str:
            return "Drawing circle"
    
    class Square:
        def draw(self) -> str:
            return "Drawing square"
    
    def render(obj: Drawable) -> None:
        """渲染任何可绘制对象"""
        print(f"  {obj.draw()}")
    
    print("1. Protocol (结构子类型):")
    render(Circle())
    render(Square())
    
    # 可调用协议
    class Validator(Protocol):
        """验证器协议"""
        def __call__(self, value: str) -> bool:
            ...
    
    def email_validator(value: str) -> bool:
        return "@" in value
    
    def validate_input(value: str, validator: Validator) -> bool:
        return validator(value)
    
    print("\n2. 可调用协议:")
    print(f"  validate('test@example.com'): {validate_input('test@example.com', email_validator)}")


# ============================================
# 7. TypedDict
# ============================================

def typed_dict_demo():
    """TypedDict 示例"""
    print("\n=== TypedDict ===")
    
    # 定义 TypedDict
    class User(TypedDict):
        """用户字典类型"""
        name: str
        age: int
        email: str
    
    # 使用
    user: User = {
        "name": "Alice",
        "age": 25,
        "email": "alice@example.com"
    }
    
    print("1. TypedDict:")
    print(f"  user: {user}")
    
    # 可选字段
    class OptionalUser(TypedDict, total=False):
        """带可选字段的用户"""
        name: str
        age: int
        email: str  # 可选
    
    partial_user: OptionalUser = {"name": "Bob", "age": 30}
    print(f"\n2. 可选字段 (total=False):")
    print(f"  partial_user: {partial_user}")
    
    # 函数使用
    def create_user(user: User) -> str:
        return f"Created user: {user['name']}"
    
    print(f"\n3. 函数中使用:")
    print(f"  {create_user(user)}")


# ============================================
# 8. NewType
# ============================================

def newtype_demo():
    """NewType 示例"""
    print("\n=== NewType ===")
    
    # 创建新类型
    UserId = NewType('UserId', int)
    Username = NewType('Username', str)
    
    def get_user(user_id: UserId) -> Username:
        """根据 UserId 获取用户名"""
        users = {UserId(1): Username("Alice"), UserId(2): Username("Bob")}
        return users.get(user_id, Username("Unknown"))
    
    print("1. NewType (类型别名):")
    user_id = UserId(1)
    username = get_user(user_id)
    print(f"  get_user({user_id}) = {username}")
    
    # 类型安全
    print("\n2. 类型安全:")
    print(f"  UserId(1) 是 int 的子类型")
    print(f"  但提供额外的类型检查")


# ============================================
# 9. Type Aliases
# ============================================

def type_aliases():
    """类型别名"""
    print("\n=== 类型别名 ===")
    
    # 简单别名
    Vector = List[float]
    
    def scale_vector(vector: Vector, scalar: float) -> Vector:
        return [x * scalar for x in vector]
    
    print("1. 简单类型别名:")
    v: Vector = [1.0, 2.0, 3.0]
    print(f"  scale_vector({v}, 2) = {scale_vector(v, 2)}")
    
    # 复杂别名
    JSONValue = Union[None, bool, int, float, str, List['JSONValue'], Dict[str, 'JSONValue']]
    
    def process_json(data: JSONValue) -> str:
        return f"Processing: {type(data).__name__}"
    
    print("\n2. 复杂类型别名:")
    print(f"  {process_json({'key': 'value'})}")
    print(f"  {process_json([1, 2, 3])}")
    
    # TypeAlias (Python 3.10+)
    if sys.version_info >= (3, 10):
        ConnectionOptions: TypeAlias = Dict[str, Union[str, int, bool]]
        print("\n3. TypeAlias (Python 3.10+):")
        print(f"  支持 TypeAlias")


# ============================================
# 10. @overload 重载
# ============================================

def overload_demo():
    """函数重载"""
    print("\n=== @overload 函数重载 ===")
    
    @overload
    def process(value: int) -> int:
        ...
    
    @overload
    def process(value: str) -> str:
        ...
    
    def process(value: Union[int, str]) -> Union[int, str]:
        """处理不同类型的值"""
        if isinstance(value, int):
            return value * 2
        else:
            return value.upper()
    
    print("1. 重载函数:")
    print(f"  process(5) = {process(5)}")
    print(f"  process('hello') = {process('hello')}")


# ============================================
# 11. Final 与 ClassVar
# ============================================

def final_and_classvar():
    """Final 和 ClassVar"""
    print("\n=== Final 与 ClassVar ===")
    
    # Final - 不可修改
    MAX_SIZE: Final = 100
    
    print("1. Final (常量):")
    print(f"  MAX_SIZE: Final = {MAX_SIZE}")
    # MAX_SIZE = 200  # 类型检查器会报错
    
    # ClassVar - 类变量
    class Config:
        instance_count: ClassVar[int] = 0
        name: str
        
        def __init__(self, name: str):
            self.name = name
            Config.instance_count += 1
    
    print("\n2. ClassVar (类变量):")
    c1 = Config("config1")
    c2 = Config("config2")
    print(f"  创建了 {Config.instance_count} 个实例")


# ============================================
# 12. 类型检查工具
# ============================================

def type_checking_tools():
    """类型检查工具"""
    print("\n=== 类型检查工具 ===")
    
    print("""
    常用类型检查工具:
    
    1. mypy
       - 最流行的类型检查器
       - 安装: pip install mypy
       - 使用: mypy your_script.py
    
    2. pyright
       - 微软开发
       - 速度快
       - VS Code 集成
    
    3. pyre
       - Facebook 开发
       - 专注性能
    
    4. pytype
       - Google 开发
       - 类型推断
    
    使用示例:
    
    # 检查单个文件
    mypy script.py
    
    # 检查整个项目
    mypy src/
    
    # 配置文件 mypy.ini
    [mypy]
    python_version = 3.9
    warn_return_any = True
    warn_unused_configs = True
    disallow_untyped_defs = True
    """)


# ============================================
# 13. 高级特性
# ============================================

def advanced_features():
    """高级类型特性"""
    print("\n=== 高级类型特性 ===")
    
    # 1. cast - 类型转换
    from typing import cast
    
    def get_value() -> Any:
        return "hello"
    
    value = cast(str, get_value())
    print(f"1. cast:")
    print(f"  cast(str, value) = {value}")
    
    # 2. TYPE_CHECKING - 仅在类型检查时导入
    from typing import TYPE_CHECKING
    
    if TYPE_CHECKING:
        # 这里的导入只在类型检查时生效
        pass
    
    print(f"\n2. TYPE_CHECKING:")
    print(f"  用于避免循环导入")
    
    # 3. Annotated - 带元数据的注解
    from typing import Annotated
    
    Age = Annotated[int, "必须 >= 0"]
    
    def set_age(age: Age) -> None:
        print(f"  Age set to: {age}")
    
    print(f"\n3. Annotated (带元数据):")
    set_age(25)
    
    # 4. get_type_hints - 获取类型提示
    def example_func(x: int, y: str) -> bool:
        return True
    
    hints = get_type_hints(example_func)
    print(f"\n4. get_type_hints:")
    print(f"  函数类型提示: {hints}")


# ============================================
# 14. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. API 响应类型
    print("1. API 响应类型:")
    
    class APIResponse(TypedDict):
        status: int
        data: Dict[str, Any]
        message: str
    
    def fetch_data(url: str) -> APIResponse:
        """模拟 API 请求"""
        return {
            "status": 200,
            "data": {"users": [{"name": "Alice", "age": 25}]},
            "message": "Success"
        }
    
    response = fetch_data("https://api.example.com/users")
    print(f"  Status: {response['status']}")
    print(f"  Message: {response['message']}")
    
    # 2. 配置类
    print("\n2. 配置类:")
    
    @dataclass
    class DatabaseConfig:
        host: str
        port: int
        database: str
        username: str
        password: str
        pool_size: int = 10
        
        def get_connection_string(self) -> str:
            return f"postgresql://{self.username}@{self.host}:{self.port}/{self.database}"
    
    db_config = DatabaseConfig(
        host="localhost",
        port=5432,
        database="mydb",
        username="admin",
        password="secret"
    )
    print(f"  Connection: {db_config.get_connection_string()}")
    
    # 3. 泛型容器
    print("\n3. 泛型容器:")
    
    T = TypeVar('T')
    
    class Stack(Generic[T]):
        """泛型栈"""
        def __init__(self):
            self._items: List[T] = []
        
        def push(self, item: T) -> None:
            self._items.append(item)
        
        def pop(self) -> Optional[T]:
            return self._items.pop() if self._items else None
        
        def peek(self) -> Optional[T]:
            return self._items[-1] if self._items else None
    
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(f"  Stack peek: {int_stack.peek()}")
    print(f"  Stack pop: {int_stack.pop()}")


# ============================================
# 15. 最佳实践
# ============================================

def best_practices():
    """类型注解最佳实践"""
    print("\n=== 最佳实践 ===")
    
    print("""
    类型注解最佳实践:
    
    1. 何时使用类型注解
       ✓ 公共 API 函数
       ✓ 复杂的数据结构
       ✓ 容易出错的地方
       ✗ 非常简单的函数
       ✗ 临时脚本
    
    2. 注解风格
       ✓ def func(x: int) -> int:
       ✗ def func(x): # type: (int) -> int
    
    3. 使用现代语法
       ✓ list[int]  # Python 3.9+
       ✗ List[int]  # 旧版本
    
    4. Optional vs Union[T, None]
       ✓ Optional[str]  # 更清晰
       ✗ Union[str, None]  # 冗长
    
    5. 避免 Any
       ✗ def func(x: Any) -> Any:
       ✓ def func(x: Union[int, str]) -> int:
    
    6. 使用 Protocol 而非 ABC
       ✓ Protocol (鸭子类型)
       ✗ ABC (继承)
    
    7. 渐进式类型
       - 从关键函数开始
       - 逐步增加覆盖
       - 不强制 100% 覆盖
    
    8. 配置类型检查器
       - 使用 mypy.ini
       - 设置合理的严格级别
       - CI/CD 集成
    
    9. 文档字符串
       - 类型注解 + docstring
       - 解释业务逻辑
       - 不重复类型信息
    
    10. 性能影响
        - 类型注解不影响运行时性能
        - 只在开发时检查
        - 可以用 TYPE_CHECKING 优化导入
    
    工具链:
    - mypy: 类型检查
    - black: 代码格式化
    - pylint: 代码质量
    - pydantic: 运行时验证
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 类型系统详解")
    print("=" * 60)
    
    basic_type_annotations()
    optional_and_union_types()
    container_types()
    function_types()
    generic_types()
    protocol_types()
    typed_dict_demo()
    newtype_demo()
    type_aliases()
    overload_demo()
    final_and_classvar()
    type_checking_tools()
    advanced_features()
    practical_examples()
    best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

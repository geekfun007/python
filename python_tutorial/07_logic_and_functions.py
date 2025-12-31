"""
Python 逻辑控制与函数 (with Type Hints)
=======================================

本文件涵盖：
- 条件语句 (if/elif/else)
- 循环 (for/while)
- 函数定义与调用
- 装饰器
- 闭包
- 函数式编程
"""

from typing import (
    Any, Callable, TypeVar, ParamSpec, Concatenate,
    overload, Literal
)
from functools import wraps, partial, reduce, lru_cache, cache
from operator import add, mul, itemgetter, attrgetter
from collections.abc import Callable as ABCCallable
import time

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')

# ============================================================================
# 1. 条件语句
# ============================================================================

class ConditionalDemo:
    """条件语句演示"""
    
    @staticmethod
    def if_elif_else() -> None:
        """基本条件语句"""
        score = 85
        
        # 基本 if/elif/else
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        print(f"Score {score} -> Grade {grade}")
        
        # 三元表达式
        status = "pass" if score >= 60 else "fail"
        print(f"Status: {status}")
        
        # 嵌套三元表达式（不推荐，可读性差）
        category = "excellent" if score >= 90 else "good" if score >= 80 else "average"
        print(f"Category: {category}")
    
    @staticmethod
    def truthiness_conditions() -> None:
        """真值条件"""
        # Python 中任何对象都可以用于条件判断
        items: list[int] = []
        
        # 不好的写法
        # if len(items) == 0:
        
        # 更 Pythonic
        if not items:
            print("List is empty")
        
        # 检查 None
        value: str | None = None
        
        # 显式检查
        if value is None:
            print("Value is None")
        
        # 注意: 这会把空字符串也当作 False
        if not value:
            print("Value is falsy (None or empty)")
        
        # and/or 返回操作数，不是 bool
        name: str | None = None
        display = name or "Anonymous"  # 短路求值
        print(f"Display name: {display}")
        
        # 条件表达式
        result = name if name is not None else "Default"
        print(f"Result: {result}")
    
    @staticmethod
    def match_statement() -> None:
        """match 语句 (Python 3.10+)"""
        def http_status(status: int) -> str:
            match status:
                case 200:
                    return "OK"
                case 201:
                    return "Created"
                case 400:
                    return "Bad Request"
                case 404:
                    return "Not Found"
                case 500:
                    return "Internal Server Error"
                case _:
                    return f"Unknown status: {status}"
        
        print(f"Status 200: {http_status(200)}")
        print(f"Status 404: {http_status(404)}")
        print(f"Status 999: {http_status(999)}")
        
        # 模式匹配
        def process_command(command: tuple[str, ...]) -> str:
            match command:
                case ("quit",):
                    return "Quitting"
                case ("hello", name):
                    return f"Hello, {name}!"
                case ("add", x, y):
                    return f"Sum: {int(x) + int(y)}"
                case ("list", *items):
                    return f"Items: {items}"
                case _:
                    return "Unknown command"
        
        print(process_command(("hello", "Python")))
        print(process_command(("add", "5", "3")))
        print(process_command(("list", "a", "b", "c")))
        
        # 结构匹配
        def describe_point(point: dict[str, Any]) -> str:
            match point:
                case {"x": 0, "y": 0}:
                    return "Origin"
                case {"x": x, "y": 0}:
                    return f"On X-axis at {x}"
                case {"x": 0, "y": y}:
                    return f"On Y-axis at {y}"
                case {"x": x, "y": y}:
                    return f"Point at ({x}, {y})"
                case _:
                    return "Invalid point"
        
        print(describe_point({"x": 0, "y": 0}))
        print(describe_point({"x": 5, "y": 0}))
        print(describe_point({"x": 3, "y": 4}))


# ============================================================================
# 2. 循环
# ============================================================================

class LoopDemo:
    """循环演示"""
    
    @staticmethod
    def for_loop() -> None:
        """for 循环"""
        # 遍历列表
        fruits = ["apple", "banana", "cherry"]
        for fruit in fruits:
            print(f"Fruit: {fruit}")
        
        # 带索引遍历
        for i, fruit in enumerate(fruits):
            print(f"{i}: {fruit}")
        
        # enumerate 起始索引
        for i, fruit in enumerate(fruits, start=1):
            print(f"{i}. {fruit}")
        
        # 遍历字典
        person = {"name": "Alice", "age": 30, "city": "NYC"}
        for key in person:
            print(f"Key: {key}")
        
        for key, value in person.items():
            print(f"{key}: {value}")
        
        # 遍历多个序列
        names = ["Alice", "Bob", "Charlie"]
        ages = [25, 30, 35]
        
        for name, age in zip(names, ages):
            print(f"{name} is {age}")
        
        # zip_longest 处理不等长序列
        from itertools import zip_longest
        scores = [85, 90]
        for name, score in zip_longest(names, scores, fillvalue=0):
            print(f"{name}: {score}")
        
        # range
        for i in range(5):
            print(i, end=" ")
        print()
        
        for i in range(2, 10, 2):
            print(i, end=" ")
        print()
    
    @staticmethod
    def while_loop() -> None:
        """while 循环"""
        # 基本 while
        count = 0
        while count < 5:
            print(f"Count: {count}")
            count += 1
        
        # 条件变量
        found = False
        items = [1, 3, 5, 7, 9]
        target = 5
        i = 0
        
        while i < len(items) and not found:
            if items[i] == target:
                found = True
            i += 1
        
        print(f"Found {target}: {found}")
        
        # 无限循环（通常配合 break）
        # while True:
        #     user_input = input("Enter command: ")
        #     if user_input == "quit":
        #         break
    
    @staticmethod
    def loop_control() -> None:
        """循环控制"""
        # break - 跳出循环
        for i in range(10):
            if i == 5:
                break
            print(i, end=" ")
        print("(break at 5)")
        
        # continue - 跳过当前迭代
        for i in range(10):
            if i % 2 == 0:
                continue
            print(i, end=" ")
        print("(skip even)")
        
        # else - 循环正常结束时执行（没有 break）
        for i in range(5):
            if i == 10:  # 不会触发
                break
        else:
            print("Loop completed without break")
        
        # 查找元素示例
        numbers = [2, 4, 6, 8]
        for n in numbers:
            if n % 2 != 0:
                print(f"Found odd number: {n}")
                break
        else:
            print("No odd numbers found")
    
    @staticmethod
    def comprehensions() -> None:
        """推导式"""
        # 列表推导
        squares = [x**2 for x in range(10)]
        print(f"Squares: {squares}")
        
        # 带条件
        even_squares = [x**2 for x in range(10) if x % 2 == 0]
        print(f"Even squares: {even_squares}")
        
        # 嵌套
        matrix = [[i*3+j for j in range(3)] for i in range(3)]
        print(f"Matrix: {matrix}")
        
        # 扁平化
        flat = [x for row in matrix for x in row]
        print(f"Flat: {flat}")
        
        # 字典推导
        square_dict = {x: x**2 for x in range(5)}
        print(f"Square dict: {square_dict}")
        
        # 集合推导
        unique_lengths = {len(word) for word in ["hello", "world", "hi", "python"]}
        print(f"Unique lengths: {unique_lengths}")
        
        # 生成器表达式（惰性求值）
        gen = (x**2 for x in range(1000000))
        print(f"Generator: {type(gen)}")
        print(f"First 5: {[next(gen) for _ in range(5)]}")


# ============================================================================
# 3. 函数定义
# ============================================================================

class FunctionDemo:
    """函数演示"""
    
    @staticmethod
    def basic_functions() -> None:
        """基本函数"""
        # 无参数无返回
        def say_hello() -> None:
            print("Hello!")
        
        # 带参数和返回值
        def add(a: int, b: int) -> int:
            return a + b
        
        # 默认参数
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"
        
        # 注意：默认参数的陷阱
        # 不要使用可变对象作为默认值！
        def bad_append(item: int, lst: list[int] = []) -> list[int]:
            lst.append(item)
            return lst
        
        # 正确做法
        def good_append(item: int, lst: list[int] | None = None) -> list[int]:
            if lst is None:
                lst = []
            lst.append(item)
            return lst
        
        say_hello()
        print(f"add(2, 3) = {add(2, 3)}")
        print(f"greet('Python') = {greet('Python')}")
        print(f"greet('Python', 'Hi') = {greet('Python', 'Hi')}")
    
    @staticmethod
    def args_kwargs() -> None:
        """*args 和 **kwargs"""
        # *args: 接受任意数量的位置参数
        def sum_all(*args: int) -> int:
            """参数会被收集为元组"""
            return sum(args)
        
        print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
        print(f"sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
        
        # **kwargs: 接受任意数量的关键字参数
        def print_info(**kwargs: Any) -> None:
            """参数会被收集为字典"""
            for key, value in kwargs.items():
                print(f"  {key}: {value}")
        
        print("print_info:")
        print_info(name="Alice", age=30, city="NYC")
        
        # 组合使用
        def flexible(*args: Any, **kwargs: Any) -> None:
            print(f"  args: {args}")
            print(f"  kwargs: {kwargs}")
        
        print("flexible:")
        flexible(1, 2, 3, x=10, y=20)
        
        # 解包传参
        numbers = [1, 2, 3]
        print(f"sum_all(*numbers) = {sum_all(*numbers)}")
        
        info = {"name": "Bob", "age": 25}
        print("print_info(**info):")
        print_info(**info)
    
    @staticmethod
    def keyword_only_positional_only() -> None:
        """仅限关键字和仅限位置参数"""
        # * 之后的参数必须以关键字形式传递
        def keyword_only(a: int, *, b: int, c: int = 0) -> int:
            return a + b + c
        
        # keyword_only(1, 2)  # TypeError!
        print(f"keyword_only(1, b=2) = {keyword_only(1, b=2)}")
        print(f"keyword_only(1, b=2, c=3) = {keyword_only(1, b=2, c=3)}")
        
        # / 之前的参数必须以位置形式传递 (Python 3.8+)
        def positional_only(a: int, b: int, /) -> int:
            return a + b
        
        print(f"positional_only(1, 2) = {positional_only(1, 2)}")
        # positional_only(a=1, b=2)  # TypeError!
        
        # 组合
        def mixed(pos_only: int, /, standard: int, *, kw_only: int) -> int:
            return pos_only + standard + kw_only
        
        print(f"mixed(1, 2, kw_only=3) = {mixed(1, 2, kw_only=3)}")
        print(f"mixed(1, standard=2, kw_only=3) = {mixed(1, standard=2, kw_only=3)}")


# ============================================================================
# 4. 闭包 (Closure)
# ============================================================================

def make_multiplier(factor: int) -> Callable[[int], int]:
    """创建乘法器闭包"""
    def multiplier(x: int) -> int:
        return x * factor
    return multiplier


def make_counter(start: int = 0) -> Callable[[], int]:
    """创建计数器闭包"""
    count = start
    
    def counter() -> int:
        nonlocal count  # 声明使用外部变量
        count += 1
        return count
    
    return counter


def make_accumulator() -> tuple[
    Callable[[float], None],  # add
    Callable[[], float],      # get_total
    Callable[[], None],       # reset
]:
    """创建累加器闭包"""
    total = 0.0
    
    def add(value: float) -> None:
        nonlocal total
        total += value
    
    def get_total() -> float:
        return total
    
    def reset() -> None:
        nonlocal total
        total = 0.0
    
    return add, get_total, reset


class ClosureDemo:
    """闭包演示"""
    
    @staticmethod
    def demo() -> None:
        """闭包演示"""
        # 乘法器
        double = make_multiplier(2)
        triple = make_multiplier(3)
        
        print(f"double(5) = {double(5)}")
        print(f"triple(5) = {triple(5)}")
        
        # 计数器
        counter1 = make_counter()
        counter2 = make_counter(100)
        
        print(f"counter1: {counter1()}, {counter1()}, {counter1()}")
        print(f"counter2: {counter2()}, {counter2()}")
        
        # 累加器
        add, get_total, reset = make_accumulator()
        add(10)
        add(20)
        add(30)
        print(f"Total: {get_total()}")
        reset()
        print(f"After reset: {get_total()}")
        
        # 闭包陷阱：循环中的闭包
        funcs: list[Callable[[], int]] = []
        for i in range(3):
            funcs.append(lambda: i)  # 所有函数都会返回 2！
        
        print(f"Bad closures: {[f() for f in funcs]}")  # [2, 2, 2]
        
        # 解决方案：使用默认参数
        funcs = []
        for i in range(3):
            funcs.append(lambda x=i: x)  # 捕获当前值
        
        print(f"Good closures: {[f() for f in funcs]}")  # [0, 1, 2]


# ============================================================================
# 5. 装饰器 (Decorator)
# ============================================================================

# 基本装饰器
def simple_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """简单装饰器"""
    @wraps(func)  # 保留原函数元信息
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper


# 带参数的装饰器
def repeat(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """重复执行装饰器"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result: R
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


# 计时装饰器
def timer(func: Callable[P, R]) -> Callable[P, R]:
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


# 缓存装饰器（记忆化）
def memoize(func: Callable[..., R]) -> Callable[..., R]:
    """简单缓存装饰器"""
    cache: dict[tuple[Any, ...], R] = {}
    
    @wraps(func)
    def wrapper(*args: Any) -> R:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


# 类装饰器
def singleton(cls: type[T]) -> type[T]:
    """单例装饰器"""
    instances: dict[type[T], T] = {}
    
    @wraps(cls, updated=[])
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance  # type: ignore


# 带参数验证的装饰器
def validate_types(*types: type) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """类型验证装饰器"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for arg, expected_type in zip(args, types):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Expected {expected_type.__name__}, got {type(arg).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator


class DecoratorDemo:
    """装饰器演示"""
    
    @staticmethod
    def demo() -> None:
        """装饰器演示"""
        # 简单装饰器
        @simple_decorator
        def say_hello(name: str) -> str:
            return f"Hello, {name}!"
        
        print(say_hello("Python"))
        print()
        
        # 带参数的装饰器
        @repeat(3)
        def greet() -> None:
            print("Hi!")
        
        greet()
        print()
        
        # 计时装饰器
        @timer
        def slow_function() -> None:
            time.sleep(0.1)
        
        slow_function()
        print()
        
        # 缓存装饰器
        @memoize
        def fibonacci(n: int) -> int:
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)
        
        print(f"fibonacci(30) = {fibonacci(30)}")  # 快速
        
        # 使用内置 lru_cache
        @lru_cache(maxsize=128)
        def fib_cached(n: int) -> int:
            if n < 2:
                return n
            return fib_cached(n - 1) + fib_cached(n - 2)
        
        print(f"fib_cached(30) = {fib_cached(30)}")
        print(f"Cache info: {fib_cached.cache_info()}")
        
        # 单例装饰器
        @singleton
        class Database:
            def __init__(self) -> None:
                print("Creating Database instance")
        
        db1 = Database()
        db2 = Database()
        print(f"db1 is db2: {db1 is db2}")
    
    @staticmethod
    def decorator_stacking() -> None:
        """装饰器堆叠"""
        @timer
        @simple_decorator
        def complex_function(x: int) -> int:
            return x * 2
        
        # 等价于:
        # complex_function = timer(simple_decorator(complex_function))
        
        print(complex_function(5))


# ============================================================================
# 6. 函数式编程
# ============================================================================

class FunctionalDemo:
    """函数式编程演示"""
    
    @staticmethod
    def lambda_functions() -> None:
        """Lambda 函数"""
        # 基本 lambda
        square = lambda x: x ** 2
        print(f"square(5) = {square(5)}")
        
        # 多参数
        add = lambda x, y: x + y
        print(f"add(3, 4) = {add(3, 4)}")
        
        # 作为参数传递
        numbers = [3, 1, 4, 1, 5, 9, 2, 6]
        sorted_numbers = sorted(numbers, key=lambda x: -x)  # 降序
        print(f"Sorted descending: {sorted_numbers}")
        
        # 排序复杂对象
        people = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
        ]
        sorted_by_age = sorted(people, key=lambda p: p["age"])
        print(f"Sorted by age: {[p['name'] for p in sorted_by_age]}")
    
    @staticmethod
    def map_filter_reduce() -> None:
        """map, filter, reduce"""
        numbers = [1, 2, 3, 4, 5]
        
        # map: 对每个元素应用函数
        squared = list(map(lambda x: x ** 2, numbers))
        print(f"map (square): {squared}")
        
        # 多个序列
        a = [1, 2, 3]
        b = [4, 5, 6]
        sums = list(map(lambda x, y: x + y, a, b))
        print(f"map (add two lists): {sums}")
        
        # filter: 过滤元素
        evens = list(filter(lambda x: x % 2 == 0, numbers))
        print(f"filter (even): {evens}")
        
        # reduce: 累积操作
        product = reduce(mul, numbers)
        print(f"reduce (multiply): {product}")
        
        # reduce with initial value
        sum_with_initial = reduce(add, numbers, 100)
        print(f"reduce (sum with initial 100): {sum_with_initial}")
        
        # 链式操作
        result = reduce(
            add,
            map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, range(10)))
        )
        print(f"Sum of squares of even numbers 0-9: {result}")
        
        # 更可读的方式（推导式）
        result2 = sum(x ** 2 for x in range(10) if x % 2 == 0)
        print(f"Same with comprehension: {result2}")
    
    @staticmethod
    def partial_functions() -> None:
        """部分应用"""
        # functools.partial
        def power(base: int, exponent: int) -> int:
            return base ** exponent
        
        square = partial(power, exponent=2)
        cube = partial(power, exponent=3)
        
        print(f"square(5) = {square(5)}")
        print(f"cube(5) = {cube(5)}")
        
        # 实用示例
        base64_encode = partial(int.to_bytes, length=8, byteorder='big')
        
        # 格式化函数
        def format_number(num: float, prefix: str = "", suffix: str = "", decimals: int = 2) -> str:
            return f"{prefix}{num:.{decimals}f}{suffix}"
        
        format_currency = partial(format_number, prefix="$", decimals=2)
        format_percent = partial(format_number, suffix="%", decimals=1)
        
        print(f"Currency: {format_currency(1234.567)}")
        print(f"Percent: {format_percent(0.756 * 100)}")
    
    @staticmethod
    def operator_module() -> None:
        """operator 模块"""
        from operator import add, mul, itemgetter, attrgetter, methodcaller
        
        # 基本运算符函数
        print(f"add(5, 3) = {add(5, 3)}")
        print(f"mul(5, 3) = {mul(5, 3)}")
        
        # itemgetter: 获取项目
        data = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
        
        # 按分数排序
        sorted_by_score = sorted(data, key=itemgetter(1))
        print(f"Sorted by score: {sorted_by_score}")
        
        # 获取多个项目
        get_name_and_score = itemgetter(0, 1)
        print(f"itemgetter(0, 1): {get_name_and_score(data[0])}")
        
        # attrgetter: 获取属性
        from dataclasses import dataclass
        
        @dataclass
        class Student:
            name: str
            grade: float
            age: int
        
        students = [
            Student("Alice", 85.0, 20),
            Student("Bob", 92.0, 22),
            Student("Charlie", 78.0, 19),
        ]
        
        sorted_by_grade = sorted(students, key=attrgetter('grade'), reverse=True)
        print(f"Top student: {sorted_by_grade[0].name}")
        
        # methodcaller: 调用方法
        names = ["hello", "world", "python"]
        upper_names = list(map(methodcaller('upper'), names))
        print(f"Upper names: {upper_names}")
    
    @staticmethod
    def higher_order_functions() -> None:
        """高阶函数"""
        # 函数组合
        def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
            """组合多个函数 (f ∘ g ∘ h)(x) = f(g(h(x)))"""
            def composed(x: Any) -> Any:
                for f in reversed(funcs):
                    x = f(x)
                return x
            return composed
        
        # 示例
        add_one = lambda x: x + 1
        double = lambda x: x * 2
        square = lambda x: x ** 2
        
        # (square ∘ double ∘ add_one)(3) = square(double(add_one(3))) = square(double(4)) = square(8) = 64
        f = compose(square, double, add_one)
        print(f"compose(square, double, add_one)(3) = {f(3)}")
        
        # 柯里化
        def curry(func: Callable[..., T]) -> Callable[..., T]:
            """简单柯里化"""
            def curried(*args: Any) -> Any:
                if len(args) >= func.__code__.co_argcount:
                    return func(*args)
                return lambda *more: curried(*args, *more)
            return curried  # type: ignore
        
        @curry
        def add_three(a: int, b: int, c: int) -> int:
            return a + b + c
        
        print(f"add_three(1)(2)(3) = {add_three(1)(2)(3)}")
        print(f"add_three(1, 2)(3) = {add_three(1, 2)(3)}")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    print("=" * 60)
    print("CONDITIONAL DEMO")
    print("=" * 60)
    ConditionalDemo.if_elif_else()
    print()
    ConditionalDemo.truthiness_conditions()
    print()
    ConditionalDemo.match_statement()
    
    print("\n" + "=" * 60)
    print("LOOP DEMO")
    print("=" * 60)
    LoopDemo.for_loop()
    print()
    LoopDemo.while_loop()
    print()
    LoopDemo.loop_control()
    print()
    LoopDemo.comprehensions()
    
    print("\n" + "=" * 60)
    print("FUNCTION DEMO")
    print("=" * 60)
    FunctionDemo.basic_functions()
    print()
    FunctionDemo.args_kwargs()
    print()
    FunctionDemo.keyword_only_positional_only()
    
    print("\n" + "=" * 60)
    print("CLOSURE DEMO")
    print("=" * 60)
    ClosureDemo.demo()
    
    print("\n" + "=" * 60)
    print("DECORATOR DEMO")
    print("=" * 60)
    DecoratorDemo.demo()
    print()
    DecoratorDemo.decorator_stacking()
    
    print("\n" + "=" * 60)
    print("FUNCTIONAL DEMO")
    print("=" * 60)
    FunctionalDemo.lambda_functions()
    print()
    FunctionalDemo.map_filter_reduce()
    print()
    FunctionalDemo.partial_functions()
    print()
    FunctionalDemo.operator_module()
    print()
    FunctionalDemo.higher_order_functions()


if __name__ == "__main__":
    main()

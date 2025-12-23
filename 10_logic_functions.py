"""
Python 逻辑控制与函数详解
包含：if/else、循环、函数定义、参数、装饰器、lambda等
"""

from functools import wraps, lru_cache, partial, reduce
from typing import Callable, Any, List, Optional
import time


# ============================================
# 1. 条件语句
# ============================================

def conditional_statements():
    """条件语句"""
    print("\n=== 条件语句 ===")
    
    # 基本 if-elif-else
    print("1. if-elif-else:")
    score = 85
    
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    print(f"  分数 {score}: {grade}")
    
    # 三元运算符
    print("\n2. 三元运算符:")
    x = 10
    result = "偶数" if x % 2 == 0 else "奇数"
    print(f"  {x} 是 {result}")
    
    # 链式比较
    print("\n3. 链式比较:")
    age = 25
    print(f"  18 <= {age} <= 60: {18 <= age <= 60}")
    
    # 逻辑运算符
    print("\n4. 逻辑运算符:")
    a, b = True, False
    print(f"  {a} and {b} = {a and b}")
    print(f"  {a} or {b} = {a or b}")
    print(f"  not {a} = {not a}")
    
    # 真值测试
    print("\n5. 真值测试:")
    empty_list = []
    non_empty_list = [1, 2, 3]
    
    if empty_list:
        print("  空列表为真")
    else:
        print("  空列表为假")
    
    if non_empty_list:
        print("  非空列表为真")
    
    # match-case (Python 3.10+)
    print("\n6. match-case (Python 3.10+):")
    try:
        status = 200
        exec("""
match status:
    case 200:
        print("  OK")
    case 404:
        print("  Not Found")
    case 500:
        print("  Server Error")
    case _:
        print("  Unknown")
""")
    except SyntaxError:
        print("  (需要 Python 3.10+)")


# ============================================
# 2. 循环语句
# ============================================

def loop_statements():
    """循环语句"""
    print("\n=== 循环语句 ===")
    
    # for 循环
    print("1. for 循环:")
    for i in range(5):
        print(f"  {i}", end=" ")
    print()
    
    # 遍历列表
    print("\n2. 遍历列表:")
    fruits = ["apple", "banana", "cherry"]
    for fruit in fruits:
        print(f"  {fruit}")
    
    # enumerate - 带索引遍历
    print("\n3. enumerate:")
    for index, fruit in enumerate(fruits, start=1):
        print(f"  {index}. {fruit}")
    
    # zip - 并行遍历
    print("\n4. zip:")
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    for name, age in zip(names, ages):
        print(f"  {name}: {age}岁")
    
    # while 循环
    print("\n5. while 循环:")
    count = 0
    while count < 5:
        print(f"  {count}", end=" ")
        count += 1
    print()
    
    # break 和 continue
    print("\n6. break 和 continue:")
    for i in range(10):
        if i == 3:
            continue  # 跳过3
        if i == 7:
            break  # 在7处停止
        print(f"  {i}", end=" ")
    print()
    
    # else 子句
    print("\n7. for-else:")
    for i in range(5):
        print(f"  {i}", end=" ")
    else:
        print("\n  循环正常结束")
    
    # 嵌套循环
    print("\n8. 嵌套循环:")
    for i in range(3):
        for j in range(3):
            print(f"  ({i},{j})", end=" ")
        print()


# ============================================
# 3. 函数基础
# ============================================

def function_basics():
    """函数基础"""
    print("\n=== 函数基础 ===")
    
    # 基本函数定义
    def greet(name):
        """问候函数"""
        return f"Hello, {name}!"
    
    print("1. 基本函数:")
    print(f"  {greet('Alice')}")
    
    # 多个返回值
    def get_stats(numbers):
        """返回统计信息"""
        return min(numbers), max(numbers), sum(numbers) / len(numbers)
    
    print("\n2. 多返回值:")
    data = [1, 2, 3, 4, 5]
    min_val, max_val, avg = get_stats(data)
    print(f"  最小值: {min_val}, 最大值: {max_val}, 平均值: {avg}")
    
    # 默认参数
    def power(base, exponent=2):
        """幂运算，默认平方"""
        return base ** exponent
    
    print("\n3. 默认参数:")
    print(f"  power(5) = {power(5)}")
    print(f"  power(5, 3) = {power(5, 3)}")
    
    # 关键字参数
    def create_profile(name, age, city="Beijing"):
        """创建用户资料"""
        return {"name": name, "age": age, "city": city}
    
    print("\n4. 关键字参数:")
    profile = create_profile(name="Alice", age=25, city="Shanghai")
    print(f"  {profile}")
    
    # 可变位置参数 (*args)
    def sum_all(*args):
        """求和所有参数"""
        return sum(args)
    
    print("\n5. *args:")
    print(f"  sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
    print(f"  sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
    
    # 可变关键字参数 (**kwargs)
    def print_info(**kwargs):
        """打印信息"""
        for key, value in kwargs.items():
            print(f"    {key}: {value}")
    
    print("\n6. **kwargs:")
    print_info(name="Bob", age=30, city="Beijing")
    
    # 混合参数
    def complex_function(a, b, *args, key1="default", **kwargs):
        """复杂参数函数"""
        print(f"    a={a}, b={b}")
        print(f"    args={args}")
        print(f"    key1={key1}")
        print(f"    kwargs={kwargs}")
    
    print("\n7. 混合参数:")
    complex_function(1, 2, 3, 4, 5, key1="value", x=10, y=20)


# ============================================
# 4. 函数高级特性
# ============================================

def advanced_functions():
    """函数高级特性"""
    print("\n=== 函数高级特性 ===")
    
    # 1. 函数作为参数
    print("1. 函数作为参数:")
    def apply_operation(x, y, operation):
        """应用操作"""
        return operation(x, y)
    
    def add(a, b):
        return a + b
    
    def multiply(a, b):
        return a * b
    
    print(f"  apply_operation(5, 3, add) = {apply_operation(5, 3, add)}")
    print(f"  apply_operation(5, 3, multiply) = {apply_operation(5, 3, multiply)}")
    
    # 2. 函数返回函数
    print("\n2. 函数返回函数:")
    def make_multiplier(n):
        """创建乘法函数"""
        def multiplier(x):
            return x * n
        return multiplier
    
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"  double(5) = {double(5)}")
    print(f"  triple(5) = {triple(5)}")
    
    # 3. 闭包
    print("\n3. 闭包:")
    def make_counter():
        """创建计数器"""
        count = 0
        def counter():
            nonlocal count
            count += 1
            return count
        return counter
    
    c1 = make_counter()
    print(f"  第1次调用: {c1()}")
    print(f"  第2次调用: {c1()}")
    print(f"  第3次调用: {c1()}")
    
    # 4. lambda 函数
    print("\n4. lambda 函数:")
    square = lambda x: x ** 2
    print(f"  square(5) = {square(5)}")
    
    pairs = [(1, 'one'), (2, 'two'), (3, 'three')]
    pairs.sort(key=lambda pair: pair[1])
    print(f"  按字符串排序: {pairs}")
    
    # 5. map, filter, reduce
    print("\n5. map, filter, reduce:")
    numbers = [1, 2, 3, 4, 5]
    
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"  map: {squared}")
    
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"  filter: {evens}")
    
    from functools import reduce
    product = reduce(lambda x, y: x * y, numbers)
    print(f"  reduce: {product}")


# ============================================
# 5. 装饰器
# ============================================

def decorators_demo():
    """装饰器"""
    print("\n=== 装饰器 ===")
    
    # 1. 基本装饰器
    print("1. 基本装饰器:")
    def uppercase_decorator(func):
        """大写装饰器"""
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()
        return wrapper
    
    @uppercase_decorator
    def greet(name):
        return f"hello, {name}"
    
    print(f"  {greet('alice')}")
    
    # 2. 带参数的装饰器
    print("\n2. 带参数的装饰器:")
    def repeat(times):
        """重复执行装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                for _ in range(times):
                    result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator
    
    @repeat(times=3)
    def say_hello():
        print("  Hello!")
        return "Done"
    
    say_hello()
    
    # 3. 保留函数元信息
    print("\n3. functools.wraps:")
    def timer(func):
        """计时装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"  {func.__name__} 耗时: {(end-start)*1000:.2f}ms")
            return result
        return wrapper
    
    @timer
    def slow_function():
        """慢函数"""
        time.sleep(0.1)
        return "完成"
    
    result = slow_function()
    print(f"  函数名: {slow_function.__name__}")
    print(f"  文档: {slow_function.__doc__}")
    
    # 4. 类装饰器
    print("\n4. 类装饰器:")
    class CountCalls:
        """计数装饰器"""
        def __init__(self, func):
            self.func = func
            self.count = 0
        
        def __call__(self, *args, **kwargs):
            self.count += 1
            print(f"  第 {self.count} 次调用")
            return self.func(*args, **kwargs)
    
    @CountCalls
    def say_hi():
        return "Hi!"
    
    say_hi()
    say_hi()
    say_hi()
    
    # 5. 多个装饰器
    print("\n5. 多个装饰器:")
    def bold(func):
        def wrapper(*args, **kwargs):
            return "<b>" + func(*args, **kwargs) + "</b>"
        return wrapper
    
    def italic(func):
        def wrapper(*args, **kwargs):
            return "<i>" + func(*args, **kwargs) + "</i>"
        return wrapper
    
    @bold
    @italic
    def greet_html(name):
        return f"Hello, {name}"
    
    print(f"  {greet_html('World')}")


def built_in_decorators():
    """内置装饰器"""
    print("\n=== 内置装饰器 ===")
    
    # 1. @property
    print("1. @property:")
    class Circle:
        def __init__(self, radius):
            self._radius = radius
        
        @property
        def radius(self):
            return self._radius
        
        @radius.setter
        def radius(self, value):
            if value < 0:
                raise ValueError("半径不能为负数")
            self._radius = value
        
        @property
        def area(self):
            import math
            return math.pi * self._radius ** 2
    
    circle = Circle(5)
    print(f"  半径: {circle.radius}")
    print(f"  面积: {circle.area:.2f}")
    circle.radius = 10
    print(f"  新面积: {circle.area:.2f}")
    
    # 2. @staticmethod 和 @classmethod
    print("\n2. @staticmethod 和 @classmethod:")
    class MathUtils:
        pi = 3.14159
        
        @staticmethod
        def add(a, b):
            """静态方法"""
            return a + b
        
        @classmethod
        def get_pi(cls):
            """类方法"""
            return cls.pi
    
    print(f"  add(5, 3) = {MathUtils.add(5, 3)}")
    print(f"  pi = {MathUtils.get_pi()}")
    
    # 3. @lru_cache - 缓存
    print("\n3. @lru_cache:")
    @lru_cache(maxsize=128)
    def fibonacci(n):
        """斐波那契数列（带缓存）"""
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print(f"  fibonacci(10) = {fibonacci(10)}")
    print(f"  缓存信息: {fibonacci.cache_info()}")


# ============================================
# 6. 函数式编程工具
# ============================================

def functional_programming():
    """函数式编程"""
    print("\n=== 函数式编程工具 ===")
    
    # 1. partial - 偏函数
    print("1. partial:")
    def power(base, exponent):
        return base ** exponent
    
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    
    print(f"  square(5) = {square(5)}")
    print(f"  cube(5) = {cube(5)}")
    
    # 2. map
    print("\n2. map:")
    numbers = [1, 2, 3, 4, 5]
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"  平方: {squared}")
    
    # 3. filter
    print("\n3. filter:")
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"  偶数: {evens}")
    
    # 4. reduce
    print("\n4. reduce:")
    from functools import reduce
    total = reduce(lambda x, y: x + y, numbers)
    print(f"  求和: {total}")
    
    product = reduce(lambda x, y: x * y, numbers)
    print(f"  求积: {product}")
    
    # 5. all 和 any
    print("\n5. all 和 any:")
    print(f"  all([True, True, True]) = {all([True, True, True])}")
    print(f"  all([True, False, True]) = {all([True, False, True])}")
    print(f"  any([False, False, False]) = {any([False, False, False])}")
    print(f"  any([False, True, False]) = {any([False, True, False])}")
    
    # 6. sorted
    print("\n6. sorted:")
    words = ["banana", "apple", "cherry", "date"]
    print(f"  按字母: {sorted(words)}")
    print(f"  按长度: {sorted(words, key=len)}")
    print(f"  降序: {sorted(words, reverse=True)}")


# ============================================
# 7. 递归
# ============================================

def recursion_demo():
    """递归"""
    print("\n=== 递归 ===")
    
    # 1. 阶乘
    print("1. 阶乘:")
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)
    
    print(f"  5! = {factorial(5)}")
    
    # 2. 斐波那契数列
    print("\n2. 斐波那契:")
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print(f"  fibonacci(10) = {fibonacci(10)}")
    
    # 3. 带缓存的递归
    print("\n3. 带缓存的递归:")
    @lru_cache(maxsize=None)
    def fibonacci_cached(n):
        if n < 2:
            return n
        return fibonacci_cached(n-1) + fibonacci_cached(n-2)
    
    print(f"  fibonacci_cached(30) = {fibonacci_cached(30)}")
    
    # 4. 列表求和（递归）
    print("\n4. 列表求和:")
    def sum_list(lst):
        if not lst:
            return 0
        return lst[0] + sum_list(lst[1:])
    
    print(f"  sum_list([1,2,3,4,5]) = {sum_list([1,2,3,4,5])}")
    
    # 5. 树遍历
    print("\n5. 树遍历:")
    def print_tree(node, indent=0):
        """递归打印树结构"""
        if isinstance(node, dict):
            for key, value in node.items():
                print("  " * indent + f"- {key}:")
                print_tree(value, indent + 1)
        elif isinstance(node, list):
            for item in node:
                print_tree(item, indent)
        else:
            print("  " * indent + f"{node}")
    
    tree = {
        "root": {
            "child1": ["leaf1", "leaf2"],
            "child2": {
                "grandchild": "leaf3"
            }
        }
    }
    print_tree(tree)


# ============================================
# 8. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 参数验证装饰器
    print("1. 参数验证装饰器:")
    def validate_positive(func):
        """验证参数为正数"""
        @wraps(func)
        def wrapper(x):
            if x <= 0:
                raise ValueError(f"参数必须为正数，得到: {x}")
            return func(x)
        return wrapper
    
    @validate_positive
    def sqrt(x):
        """平方根"""
        return x ** 0.5
    
    try:
        print(f"  sqrt(16) = {sqrt(16)}")
        print(f"  sqrt(-1) = {sqrt(-1)}")
    except ValueError as e:
        print(f"  错误: {e}")
    
    # 2. 重试装饰器
    print("\n2. 重试装饰器:")
    def retry(max_attempts=3):
        """重试装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                attempts = 0
                while attempts < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        if attempts >= max_attempts:
                            print(f"  失败: 已达到最大重试次数")
                            raise
                        print(f"  重试 {attempts}/{max_attempts}")
            return wrapper
        return decorator
    
    @retry(max_attempts=3)
    def unstable_operation():
        import random
        if random.random() < 0.7:
            raise RuntimeError("操作失败")
        return "成功"
    
    try:
        result = unstable_operation()
        print(f"  结果: {result}")
    except:
        pass
    
    # 3. 缓存装饰器
    print("\n3. 简单缓存:")
    def simple_cache(func):
        """简单缓存装饰器"""
        cache = {}
        @wraps(func)
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        return wrapper
    
    @simple_cache
    def expensive_function(n):
        """耗时函数"""
        print(f"  计算 {n}...")
        time.sleep(0.01)
        return n ** 2
    
    print(f"  第1次: {expensive_function(5)}")
    print(f"  第2次: {expensive_function(5)}")  # 使用缓存
    
    # 4. 权限检查
    print("\n4. 权限检查装饰器:")
    current_user = {"name": "Alice", "role": "admin"}
    
    def require_role(role):
        """要求特定角色"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if current_user.get("role") != role:
                    raise PermissionError(f"需要 {role} 权限")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @require_role("admin")
    def delete_user(user_id):
        return f"删除用户 {user_id}"
    
    try:
        result = delete_user(123)
        print(f"  {result}")
    except PermissionError as e:
        print(f"  权限错误: {e}")
    
    # 5. 函数组合
    print("\n5. 函数组合:")
    def compose(*functions):
        """组合多个函数"""
        def inner(arg):
            result = arg
            for func in reversed(functions):
                result = func(result)
            return result
        return inner
    
    def add_one(x):
        return x + 1
    
    def double(x):
        return x * 2
    
    def square(x):
        return x ** 2
    
    # 组合: square(double(add_one(x)))
    combined = compose(square, double, add_one)
    print(f"  combined(5) = {combined(5)}")  # (5+1)*2)^2 = 144


# ============================================
# 9. 最佳实践
# ============================================

def best_practices():
    """最佳实践"""
    print("\n=== 最佳实践 ===")
    
    print("""
    1. 函数应该小而专注
       - 单一职责原则
       - 易于测试和维护
    
    2. 使用有意义的名称
       ✓ calculate_average()
       ✗ calc() 或 func1()
    
    3. 添加文档字符串
       - 说明函数功能
       - 参数和返回值说明
    
    4. 避免修改可变默认参数
       ✗ def func(items=[]):
       ✓ def func(items=None):
              if items is None:
                  items = []
    
    5. 使用类型提示 (Python 3.5+)
       def greet(name: str) -> str:
           return f"Hello, {name}"
    
    6. 优先使用生成器
       - 处理大数据集时
       - 节省内存
    
    7. 合理使用装饰器
       - 日志记录
       - 性能测量
       - 权限检查
    
    8. 避免深层嵌套
       - 提取为独立函数
       - 提前返回
    
    9. 使用异常处理
       - 不要忽略错误
       - 具体的异常类型
    
    10. 编写可测试的代码
        - 避免副作用
        - 依赖注入
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 逻辑控制与函数详解")
    print("=" * 60)
    
    conditional_statements()
    loop_statements()
    
    function_basics()
    advanced_functions()
    
    decorators_demo()
    built_in_decorators()
    
    functional_programming()
    recursion_demo()
    
    practical_examples()
    best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

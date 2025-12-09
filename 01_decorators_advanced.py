"""
Python 高级教程 - 装饰器详解

装饰器是 Python 中最强大的特性之一，本模块涵盖：
1. 基础装饰器
2. 带参数的装饰器
3. 类装饰器
4. 装饰器叠加
5. 实战应用场景
"""

import functools
import time
from typing import Callable, Any, TypeVar, ParamSpec

# ============================================================================
# 1. 基础装饰器
# ============================================================================

def timer(func: Callable) -> Callable:
    """计时装饰器 - 测量函数执行时间"""
    @functools.wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行时间: {end - start:.4f}秒")
        return result
    return wrapper


@timer
def slow_function():
    """一个慢速函数示例"""
    time.sleep(1)
    return "完成"


# ============================================================================
# 2. 带参数的装饰器
# ============================================================================

def repeat(times: int = 1):
    """重复执行装饰器 - 可指定重复次数"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                print(f"第 {i + 1} 次执行:")
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator


@repeat(times=3)
def greet(name: str):
    """问候函数"""
    print(f"你好, {name}!")
    return f"问候 {name}"


# ============================================================================
# 3. 类装饰器
# ============================================================================

class CountCalls:
    """统计函数调用次数的类装饰器"""
    
    def __init__(self, func: Callable):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} 已被调用 {self.count} 次")
        return self.func(*args, **kwargs)
    
    def reset(self):
        """重置计数器"""
        self.count = 0


@CountCalls
def process_data(data: list):
    """处理数据的函数"""
    return sum(data)


# ============================================================================
# 4. 缓存装饰器 (Memoization)
# ============================================================================

def memoize(func: Callable) -> Callable:
    """缓存函数结果的装饰器"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
            print(f"计算并缓存: {args}")
        else:
            print(f"从缓存读取: {args}")
        return cache[args]
    
    wrapper.cache = cache  # 暴露缓存以便调试
    wrapper.clear_cache = lambda: cache.clear()  # 清除缓存方法
    return wrapper


@memoize
def fibonacci(n: int) -> int:
    """斐波那契数列 - 递归实现"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ============================================================================
# 5. 权限验证装饰器
# ============================================================================

class User:
    """用户类"""
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role


# 模拟当前用户
current_user = User("张三", "admin")


def require_role(*allowed_roles: str):
    """权限验证装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role not in allowed_roles:
                raise PermissionError(
                    f"用户 {current_user.name} 权限不足。"
                    f"需要角色: {allowed_roles}，当前角色: {current_user.role}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


@require_role("admin", "manager")
def delete_user(user_id: int):
    """删除用户 - 需要管理员权限"""
    return f"用户 {user_id} 已删除"


@require_role("admin")
def view_logs():
    """查看日志 - 需要管理员权限"""
    return "日志内容..."


# ============================================================================
# 6. 重试装饰器
# ============================================================================

def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器 - 失败时自动重试"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"尝试 {attempt}/{max_attempts}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"失败: {e}")
                    if attempt < max_attempts:
                        print(f"等待 {delay} 秒后重试...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


@retry(max_attempts=3, delay=0.5)
def unstable_api_call(success_rate: float = 0.3):
    """模拟不稳定的 API 调用"""
    import random
    if random.random() < success_rate:
        return "API 调用成功!"
    raise ConnectionError("API 调用失败")


# ============================================================================
# 7. 类型检查装饰器
# ============================================================================

def validate_types(**type_hints):
    """运行时类型检查装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 检查关键字参数类型
            for arg_name, expected_type in type_hints.items():
                if arg_name in kwargs:
                    value = kwargs[arg_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"参数 '{arg_name}' 类型错误: "
                            f"期望 {expected_type.__name__}, "
                            f"实际 {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


@validate_types(name=str, age=int, salary=float)
def create_employee(name, age, salary):
    """创建员工记录"""
    return {
        "name": name,
        "age": age,
        "salary": salary
    }


# ============================================================================
# 8. 单例装饰器
# ============================================================================

def singleton(cls):
    """单例模式装饰器 - 确保类只有一个实例"""
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class DatabaseConnection:
    """数据库连接类 - 单例模式"""
    
    def __init__(self, host: str = "localhost"):
        self.host = host
        print(f"创建数据库连接: {host}")
    
    def query(self, sql: str):
        return f"执行查询: {sql}"


# ============================================================================
# 9. 装饰器叠加
# ============================================================================

@timer
@retry(max_attempts=2, delay=0.1)
@memoize
def complex_calculation(n: int) -> int:
    """复杂计算 - 使用多个装饰器"""
    if n == 0:
        import random
        if random.random() < 0.5:
            raise ValueError("随机失败")
    return n ** 2 + 2 * n + 1


# ============================================================================
# 10. 上下文装饰器 (使用 contextlib)
# ============================================================================

from contextlib import contextmanager

@contextmanager
def temporary_change(obj, attr, value):
    """临时修改对象属性的上下文管理器"""
    original = getattr(obj, attr)
    setattr(obj, attr, value)
    try:
        yield obj
    finally:
        setattr(obj, attr, original)


# ============================================================================
# 实战应用示例
# ============================================================================

def demo_basic_decorator():
    """演示基础装饰器"""
    print("=" * 60)
    print("1. 基础装饰器 - 计时器")
    print("=" * 60)
    result = slow_function()
    print(f"结果: {result}\n")


def demo_parametrized_decorator():
    """演示带参数的装饰器"""
    print("=" * 60)
    print("2. 带参数的装饰器 - 重复执行")
    print("=" * 60)
    results = greet("李四")
    print(f"所有结果: {results}\n")


def demo_class_decorator():
    """演示类装饰器"""
    print("=" * 60)
    print("3. 类装饰器 - 调用计数")
    print("=" * 60)
    process_data([1, 2, 3])
    process_data([4, 5, 6])
    process_data([7, 8, 9])
    print(f"总调用次数: {process_data.count}\n")


def demo_memoization():
    """演示缓存装饰器"""
    print("=" * 60)
    print("4. 缓存装饰器 - 斐波那契")
    print("=" * 60)
    print(f"fibonacci(5) = {fibonacci(5)}")
    print(f"fibonacci(5) = {fibonacci(5)}")  # 从缓存读取
    print(f"缓存内容: {fibonacci.cache}\n")


def demo_authorization():
    """演示权限验证"""
    print("=" * 60)
    print("5. 权限验证装饰器")
    print("=" * 60)
    try:
        result = delete_user(123)
        print(f"成功: {result}")
    except PermissionError as e:
        print(f"权限错误: {e}")
    
    # 切换用户角色
    global current_user
    original_role = current_user.role
    current_user.role = "user"
    try:
        view_logs()
    except PermissionError as e:
        print(f"权限错误: {e}")
    current_user.role = original_role
    print()


def demo_retry():
    """演示重试装饰器"""
    print("=" * 60)
    print("6. 重试装饰器")
    print("=" * 60)
    try:
        result = unstable_api_call(success_rate=0.6)
        print(f"成功: {result}")
    except ConnectionError as e:
        print(f"最终失败: {e}")
    print()


def demo_type_validation():
    """演示类型检查"""
    print("=" * 60)
    print("7. 类型检查装饰器")
    print("=" * 60)
    try:
        emp1 = create_employee(name="王五", age=30, salary=50000.0)
        print(f"创建成功: {emp1}")
        
        # 类型错误示例
        emp2 = create_employee(name="赵六", age="三十", salary=60000.0)
    except TypeError as e:
        print(f"类型错误: {e}")
    print()


def demo_singleton():
    """演示单例模式"""
    print("=" * 60)
    print("8. 单例装饰器")
    print("=" * 60)
    db1 = DatabaseConnection("localhost")
    db2 = DatabaseConnection("remote")  # 实际上返回同一个实例
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1.host: {db1.host}")
    print(f"db2.host: {db2.host}\n")


def demo_stacked_decorators():
    """演示装饰器叠加"""
    print("=" * 60)
    print("9. 装饰器叠加")
    print("=" * 60)
    try:
        result = complex_calculation(5)
        print(f"结果: {result}")
        result = complex_calculation(5)  # 从缓存读取
        print(f"结果: {result}")
    except ValueError as e:
        print(f"计算失败: {e}")
    print()


# ============================================================================
# 重要注意事项
# ============================================================================

"""
装饰器最佳实践和注意事项:

1. 始终使用 @functools.wraps
   - 保留原函数的名称、文档字符串等元信息
   - 便于调试和文档生成

2. 装饰器执行顺序
   - @decorator1
     @decorator2
     def func(): ...
   - 执行顺序: decorator2(decorator1(func))
   - 从下往上应用装饰器

3. 性能考虑
   - 装饰器会增加函数调用开销
   - 对性能敏感的代码谨慎使用
   - 使用 functools.lru_cache 替代自定义缓存装饰器

4. 调试技巧
   - 使用 func.__wrapped__ 访问原始函数
   - 装饰器可以添加额外属性 (如 cache, count)
   - 考虑添加装饰器启用/禁用开关

5. 类方法装饰器
   - 注意 self 参数的处理
   - 装饰器与 @classmethod, @staticmethod 的结合
   - 装饰器顺序: @classmethod 应该在最外层

6. 异步装饰器
   - 装饰异步函数需要定义异步包装器
   - 使用 async def 和 await
   
7. 常见陷阱
   - 忘记使用 @functools.wraps
   - 装饰器返回 None 而非函数
   - 带参数装饰器需要两层嵌套
   - 类装饰器要实现 __call__ 方法
"""


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Python 高级教程 - 装饰器详解")
    print("=" * 60 + "\n")
    
    demo_basic_decorator()
    demo_parametrized_decorator()
    demo_class_decorator()
    demo_memoization()
    demo_authorization()
    demo_retry()
    demo_type_validation()
    demo_singleton()
    demo_stacked_decorators()
    
    print("=" * 60)
    print("装饰器教程完成!")
    print("=" * 60)

"""
Python 错误处理与迭代器 (with Type Hints)
=========================================

本文件涵盖：
- 异常处理 (try/except/finally)
- 自定义异常
- 迭代器 (Iterator)
- 生成器 (Generator)
"""

from typing import Any, Generator, Iterator, Iterable, TypeVar, Callable
from collections.abc import Iterator as ABCIterator
from contextlib import contextmanager
import sys
import traceback

T = TypeVar('T')

# ============================================================================
# 1. 异常处理基础
# ============================================================================

class ExceptionBasicsDemo:
    """异常处理基础"""
    
    @staticmethod
    def basic_try_except() -> None:
        """基本 try/except"""
        # 基本形式
        try:
            result = 10 / 0
        except ZeroDivisionError:
            print("Cannot divide by zero!")
        
        # 捕获异常对象
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            print(f"Error: {e}")
        
        # 多个异常类型
        try:
            value = int("not a number")
        except (ValueError, TypeError) as e:
            print(f"Conversion error: {e}")
        
        # 分别处理不同异常
        def risky_operation(x: Any) -> int:
            try:
                return int(x) / len(x)  # type: ignore
            except ValueError:
                print("Invalid value")
                return 0
            except TypeError:
                print("Invalid type")
                return 0
            except ZeroDivisionError:
                print("Empty input")
                return 0
        
        risky_operation("abc")
        risky_operation(123)
        risky_operation("")
    
    @staticmethod
    def try_except_else_finally() -> None:
        """完整的 try 语句"""
        def process_file(filename: str) -> str | None:
            try:
                # 可能抛出异常的代码
                f = open(filename, 'r')
                content = f.read()
            except FileNotFoundError:
                print(f"File {filename} not found")
                return None
            except PermissionError:
                print(f"No permission to read {filename}")
                return None
            else:
                # 没有异常时执行
                print(f"Successfully read {filename}")
                return content
            finally:
                # 无论如何都会执行（清理代码）
                print("Cleanup: closing file if opened")
                try:
                    f.close()
                except NameError:
                    pass  # f 可能未定义
        
        # 测试
        process_file("nonexistent.txt")
    
    @staticmethod
    def exception_hierarchy() -> None:
        """异常层次结构"""
        # Python 异常层次（部分）
        """
        BaseException
        ├── SystemExit
        ├── KeyboardInterrupt
        ├── GeneratorExit
        └── Exception
            ├── StopIteration
            ├── ArithmeticError
            │   ├── FloatingPointError
            │   ├── OverflowError
            │   └── ZeroDivisionError
            ├── AssertionError
            ├── AttributeError
            ├── BufferError
            ├── EOFError
            ├── ImportError
            │   └── ModuleNotFoundError
            ├── LookupError
            │   ├── IndexError
            │   └── KeyError
            ├── MemoryError
            ├── NameError
            │   └── UnboundLocalError
            ├── OSError
            │   ├── FileExistsError
            │   ├── FileNotFoundError
            │   ├── PermissionError
            │   └── ...
            ├── RuntimeError
            │   └── RecursionError
            ├── TypeError
            └── ValueError
        """
        
        # 捕获基类会捕获所有子类
        try:
            d: dict[str, int] = {}
            print(d['key'])
        except LookupError as e:  # 捕获 KeyError 和 IndexError
            print(f"Lookup error: {type(e).__name__}: {e}")
    
    @staticmethod
    def raise_exceptions() -> None:
        """抛出异常"""
        # 基本抛出
        def check_positive(value: int) -> int:
            if value < 0:
                raise ValueError(f"Value must be positive, got {value}")
            return value
        
        try:
            check_positive(-5)
        except ValueError as e:
            print(f"Caught: {e}")
        
        # 重新抛出
        def wrapper() -> None:
            try:
                check_positive(-1)
            except ValueError:
                print("Logging the error...")
                raise  # 重新抛出当前异常
        
        try:
            wrapper()
        except ValueError:
            print("Re-raised exception caught")
        
        # 异常链
        def load_config(filename: str) -> dict[str, Any]:
            try:
                with open(filename) as f:
                    return {"content": f.read()}
            except FileNotFoundError as e:
                # raise ... from ... 保留原因链
                raise RuntimeError(f"Cannot load config: {filename}") from e
        
        try:
            load_config("config.json")
        except RuntimeError as e:
            print(f"Error: {e}")
            print(f"Caused by: {e.__cause__}")


# ============================================================================
# 2. 自定义异常
# ============================================================================

# 基本自定义异常
class ValidationError(Exception):
    """验证错误"""
    pass


class NetworkError(Exception):
    """网络错误"""
    pass


# 带属性的自定义异常
class HttpError(Exception):
    """HTTP 错误"""
    
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class AuthenticationError(HttpError):
    """认证错误"""
    
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(401, message)


class NotFoundError(HttpError):
    """资源未找到"""
    
    def __init__(self, resource: str) -> None:
        self.resource = resource
        super().__init__(404, f"Resource not found: {resource}")


# 业务异常层次
class BusinessError(Exception):
    """业务错误基类"""
    
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class InsufficientFundsError(BusinessError):
    """余额不足"""
    
    def __init__(self, balance: float, required: float) -> None:
        super().__init__(
            "INSUFFICIENT_FUNDS",
            f"Insufficient funds: have {balance}, need {required}",
            {"balance": balance, "required": required}
        )


class CustomExceptionDemo:
    """自定义异常演示"""
    
    @staticmethod
    def demo() -> None:
        # 使用自定义异常
        def validate_user(data: dict[str, Any]) -> None:
            if not data.get("email"):
                raise ValidationError("Email is required")
            if not data.get("password"):
                raise ValidationError("Password is required")
        
        try:
            validate_user({"email": "test@example.com"})
        except ValidationError as e:
            print(f"Validation failed: {e}")
        
        # HTTP 异常
        def fetch_resource(resource_id: int) -> dict[str, Any]:
            if resource_id == 0:
                raise AuthenticationError()
            if resource_id == 404:
                raise NotFoundError(f"user/{resource_id}")
            return {"id": resource_id, "name": "Test"}
        
        for rid in [0, 404, 1]:
            try:
                result = fetch_resource(rid)
                print(f"Got: {result}")
            except HttpError as e:
                print(f"HTTP Error {e.status_code}: {e.message}")
        
        # 业务异常
        def withdraw(balance: float, amount: float) -> float:
            if amount > balance:
                raise InsufficientFundsError(balance, amount)
            return balance - amount
        
        try:
            withdraw(100.0, 150.0)
        except InsufficientFundsError as e:
            print(f"Business Error: {e.to_dict()}")


# ============================================================================
# 3. 异常处理最佳实践
# ============================================================================

class ExceptionBestPracticesDemo:
    """异常处理最佳实践"""
    
    @staticmethod
    def specific_exceptions() -> None:
        """捕获特定异常"""
        # 不好的做法
        def bad_example() -> None:
            try:
                # 一些代码
                pass
            except Exception:  # 太宽泛
                pass
            
            try:
                pass
            except:  # 更糟糕，捕获所有包括 SystemExit
                pass
        
        # 好的做法
        def good_example(filename: str) -> str | None:
            try:
                with open(filename) as f:
                    return f.read()
            except FileNotFoundError:
                print(f"File not found: {filename}")
                return None
            except PermissionError:
                print(f"Permission denied: {filename}")
                return None
    
    @staticmethod
    def exception_context() -> None:
        """提供有用的错误上下文"""
        class DataProcessor:
            def process(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
                results: list[dict[str, Any]] = []
                for i, item in enumerate(data):
                    try:
                        processed = self._process_item(item)
                        results.append(processed)
                    except Exception as e:
                        # 添加上下文信息
                        raise RuntimeError(
                            f"Error processing item {i}: {item}"
                        ) from e
                return results
            
            def _process_item(self, item: dict[str, Any]) -> dict[str, Any]:
                return {"value": item["value"] * 2}
        
        processor = DataProcessor()
        try:
            processor.process([{"value": 1}, {"invalid": 2}])
        except RuntimeError as e:
            print(f"Error: {e}")
            print(f"Cause: {e.__cause__}")
    
    @staticmethod
    def traceback_handling() -> None:
        """处理异常追溯"""
        def level3() -> None:
            raise ValueError("Something went wrong")
        
        def level2() -> None:
            level3()
        
        def level1() -> None:
            level2()
        
        try:
            level1()
        except ValueError:
            # 获取异常信息
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_value}")
            
            # 格式化追溯
            print("\nFormatted traceback:")
            traceback.print_exc()
            
            # 获取追溯字符串
            tb_str = traceback.format_exc()
            print(f"\nTraceback as string:\n{tb_str}")


# ============================================================================
# 4. 迭代器 (Iterator)
# ============================================================================

class CountDown:
    """自定义迭代器"""
    
    def __init__(self, start: int) -> None:
        self.current = start
    
    def __iter__(self) -> "CountDown":
        """返回迭代器对象（自身）"""
        return self
    
    def __next__(self) -> int:
        """返回下一个值"""
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


class Range:
    """模拟内置 range"""
    
    def __init__(self, start: int, stop: int | None = None, step: int = 1) -> None:
        if stop is None:
            self.start = 0
            self.stop = start
        else:
            self.start = start
            self.stop = stop
        self.step = step
    
    def __iter__(self) -> Iterator[int]:
        """返回迭代器"""
        current = self.start
        while (self.step > 0 and current < self.stop) or \
              (self.step < 0 and current > self.stop):
            yield current
            current += self.step


class InfiniteCounter:
    """无限迭代器"""
    
    def __init__(self, start: int = 0, step: int = 1) -> None:
        self.current = start
        self.step = step
    
    def __iter__(self) -> "InfiniteCounter":
        return self
    
    def __next__(self) -> int:
        result = self.current
        self.current += self.step
        return result


class IteratorDemo:
    """迭代器演示"""
    
    @staticmethod
    def basic_iterator() -> None:
        """基本迭代器使用"""
        # 使用自定义迭代器
        print("Countdown:")
        for n in CountDown(5):
            print(f"  {n}")
        
        # 手动迭代
        print("\nManual iteration:")
        countdown = CountDown(3)
        print(f"  next: {next(countdown)}")
        print(f"  next: {next(countdown)}")
        print(f"  next: {next(countdown)}")
        # next(countdown)  # 会抛出 StopIteration
        
        # 使用自定义 Range
        print("\nCustom Range:")
        for n in Range(0, 10, 2):
            print(f"  {n}", end=" ")
        print()
    
    @staticmethod
    def builtin_iterators() -> None:
        """内置迭代器工具"""
        from itertools import (
            count, cycle, repeat,
            chain, compress, dropwhile, takewhile,
            islice, starmap, accumulate,
            product, permutations, combinations
        )
        
        # count: 无限计数器
        print("count(10, 2):", end=" ")
        for i, n in enumerate(count(10, 2)):
            if i >= 5:
                break
            print(n, end=" ")
        print()
        
        # cycle: 循环迭代
        print("cycle('ABC'):", end=" ")
        for i, c in enumerate(cycle('ABC')):
            if i >= 7:
                break
            print(c, end=" ")
        print()
        
        # repeat: 重复
        print("repeat('X', 5):", list(repeat('X', 5)))
        
        # chain: 连接多个迭代器
        print("chain([1,2], [3,4]):", list(chain([1, 2], [3, 4])))
        
        # islice: 切片
        print("islice(count(), 5, 10):", list(islice(count(), 5, 10)))
        
        # takewhile/dropwhile: 条件过滤
        nums = [1, 3, 5, 2, 4, 6]
        print(f"takewhile(<5, {nums}):", list(takewhile(lambda x: x < 5, nums)))
        print(f"dropwhile(<5, {nums}):", list(dropwhile(lambda x: x < 5, nums)))
        
        # accumulate: 累积
        print("accumulate([1,2,3,4]):", list(accumulate([1, 2, 3, 4])))
        
        # 组合
        print("product('AB', '12'):", list(product('AB', '12')))
        print("permutations('ABC', 2):", list(permutations('ABC', 2)))
        print("combinations('ABC', 2):", list(combinations('ABC', 2)))


# ============================================================================
# 5. 生成器 (Generator)
# ============================================================================

def countdown_generator(n: int) -> Generator[int, None, None]:
    """简单生成器"""
    while n > 0:
        yield n
        n -= 1


def fibonacci(limit: int) -> Generator[int, None, None]:
    """斐波那契数列生成器"""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b


def read_large_file(filename: str, chunk_size: int = 1024) -> Generator[str, None, None]:
    """逐块读取大文件"""
    with open(filename, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def coroutine_example() -> Generator[None, int, str]:
    """协程示例（接收值的生成器）"""
    total = 0
    count = 0
    
    while True:
        value = yield  # 接收发送的值
        if value is None:
            break
        total += value
        count += 1
    
    return f"Average: {total / count if count else 0}"


def delegating_generator() -> Generator[int, None, None]:
    """委托生成器 (yield from)"""
    yield from range(5)
    yield from [10, 20, 30]
    yield from countdown_generator(3)


class GeneratorDemo:
    """生成器演示"""
    
    @staticmethod
    def basic_generator() -> None:
        """基本生成器"""
        print("Countdown generator:")
        for n in countdown_generator(5):
            print(f"  {n}")
        
        print("\nFibonacci:")
        print(f"  {list(fibonacci(100))}")
        
        # 生成器表达式
        squares = (x**2 for x in range(10))
        print(f"\nGenerator expression: {type(squares)}")
        print(f"  First 5: {[next(squares) for _ in range(5)]}")
    
    @staticmethod
    def generator_methods() -> None:
        """生成器方法"""
        def controlled_generator() -> Generator[int, str | None, str]:
            """可控制的生成器"""
            received = None
            for i in range(5):
                received = yield i
                if received == "stop":
                    return "Stopped early"
                print(f"  Received: {received}")
            return "Completed normally"
        
        # send() 发送值
        gen = controlled_generator()
        print(f"Start: {next(gen)}")  # 必须先调用 next()
        print(f"Send 'hello': {gen.send('hello')}")
        print(f"Send 'world': {gen.send('world')}")
        
        # throw() 抛出异常
        def exception_generator() -> Generator[int, None, None]:
            try:
                for i in range(10):
                    yield i
            except ValueError:
                print("  ValueError caught in generator!")
                yield -1
        
        gen2 = exception_generator()
        print(f"\nException generator: {next(gen2)}, {next(gen2)}")
        print(f"  Throw ValueError: {gen2.throw(ValueError)}")
        
        # close() 关闭生成器
        gen3 = countdown_generator(100)
        print(f"\nBefore close: {next(gen3)}")
        gen3.close()
        # next(gen3)  # StopIteration
    
    @staticmethod
    def yield_from_demo() -> None:
        """yield from 演示"""
        print("Delegating generator:")
        for value in delegating_generator():
            print(f"  {value}")
        
        # 递归展平嵌套列表
        def flatten(items: list[Any]) -> Generator[Any, None, None]:
            for item in items:
                if isinstance(item, list):
                    yield from flatten(item)
                else:
                    yield item
        
        nested = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
        print(f"\nFlatten {nested}:")
        print(f"  {list(flatten(nested))}")
    
    @staticmethod
    def generator_pipeline() -> None:
        """生成器管道"""
        def read_numbers() -> Generator[int, None, None]:
            """数据源"""
            for i in range(1, 11):
                yield i
        
        def filter_even(nums: Iterable[int]) -> Generator[int, None, None]:
            """过滤偶数"""
            for n in nums:
                if n % 2 == 0:
                    yield n
        
        def square(nums: Iterable[int]) -> Generator[int, None, None]:
            """平方"""
            for n in nums:
                yield n ** 2
        
        def limit(nums: Iterable[int], max_count: int) -> Generator[int, None, None]:
            """限制数量"""
            for i, n in enumerate(nums):
                if i >= max_count:
                    break
                yield n
        
        # 构建管道
        pipeline = limit(square(filter_even(read_numbers())), 3)
        
        print("Generator pipeline (read -> filter even -> square -> limit 3):")
        print(f"  {list(pipeline)}")
    
    @staticmethod
    def memory_efficiency() -> None:
        """内存效率演示"""
        import sys
        
        # 列表 vs 生成器内存使用
        list_data = [x**2 for x in range(10000)]
        gen_data = (x**2 for x in range(10000))
        
        print(f"List size: {sys.getsizeof(list_data)} bytes")
        print(f"Generator size: {sys.getsizeof(gen_data)} bytes")
        
        # 列表需要一次性存储所有数据
        # 生成器只在需要时计算，几乎不占内存


# ============================================================================
# 6. 上下文管理器与异常
# ============================================================================

@contextmanager
def managed_resource(name: str) -> Generator[str, None, None]:
    """资源管理上下文管理器"""
    print(f"Acquiring {name}")
    try:
        yield f"Resource: {name}"
    except Exception as e:
        print(f"Error in {name}: {e}")
        raise
    finally:
        print(f"Releasing {name}")


@contextmanager
def suppress_exceptions(*exceptions: type[Exception]) -> Generator[None, None, None]:
    """抑制特定异常"""
    try:
        yield
    except exceptions:
        pass


class ContextManagerExceptionDemo:
    @staticmethod
    def demo() -> None:
        """上下文管理器异常处理"""
        # 正常使用
        with managed_resource("database") as db:
            print(f"Using {db}")
        
        # 有异常
        print("\nWith exception:")
        try:
            with managed_resource("file") as f:
                print(f"Using {f}")
                raise ValueError("Something went wrong")
        except ValueError:
            print("Exception propagated")
        
        # 抑制异常
        print("\nSuppressing exception:")
        with suppress_exceptions(ValueError, KeyError):
            raise ValueError("This will be suppressed")
        print("Continued after suppressed exception")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    print("=" * 60)
    print("EXCEPTION BASICS")
    print("=" * 60)
    ExceptionBasicsDemo.basic_try_except()
    print()
    ExceptionBasicsDemo.try_except_else_finally()
    print()
    ExceptionBasicsDemo.exception_hierarchy()
    print()
    ExceptionBasicsDemo.raise_exceptions()
    
    print("\n" + "=" * 60)
    print("CUSTOM EXCEPTIONS")
    print("=" * 60)
    CustomExceptionDemo.demo()
    
    print("\n" + "=" * 60)
    print("EXCEPTION BEST PRACTICES")
    print("=" * 60)
    ExceptionBestPracticesDemo.exception_context()
    print()
    ExceptionBestPracticesDemo.traceback_handling()
    
    print("\n" + "=" * 60)
    print("ITERATOR DEMO")
    print("=" * 60)
    IteratorDemo.basic_iterator()
    print()
    IteratorDemo.builtin_iterators()
    
    print("\n" + "=" * 60)
    print("GENERATOR DEMO")
    print("=" * 60)
    GeneratorDemo.basic_generator()
    print()
    GeneratorDemo.generator_methods()
    print()
    GeneratorDemo.yield_from_demo()
    print()
    GeneratorDemo.generator_pipeline()
    print()
    GeneratorDemo.memory_efficiency()
    
    print("\n" + "=" * 60)
    print("CONTEXT MANAGER EXCEPTION DEMO")
    print("=" * 60)
    ContextManagerExceptionDemo.demo()


if __name__ == "__main__":
    main()

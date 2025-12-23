"""
Python 异常处理详解
包含：try-except、异常类型、自定义异常、上下文管理器等
"""

import sys
import traceback
import logging
from contextlib import contextmanager


# ============================================
# 1. 异常基础
# ============================================

def exception_basics():
    """异常处理基础"""
    print("\n=== 异常处理基础 ===")
    
    # 基本 try-except
    print("1. 基本 try-except:")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("  错误: 除数不能为零")
    
    # 捕获多个异常
    print("\n2. 捕获多个异常:")
    try:
        numbers = [1, 2, 3]
        print(numbers[10])
    except (IndexError, KeyError) as e:
        print(f"  索引或键错误: {e}")
    
    # 捕获所有异常
    print("\n3. 捕获所有异常:")
    try:
        x = int("abc")
    except Exception as e:
        print(f"  发生异常: {type(e).__name__}: {e}")
    
    # else 子句
    print("\n4. else 子句（没有异常时执行）:")
    try:
        result = 10 / 2
    except ZeroDivisionError:
        print("  除数为零")
    else:
        print(f"  计算成功: {result}")
    
    # finally 子句
    print("\n5. finally 子句（总是执行）:")
    try:
        file = open("/tmp/test.txt", "w")
        file.write("Hello")
    except IOError as e:
        print(f"  IO错误: {e}")
    finally:
        print("  清理资源...")
        try:
            file.close()
        except:
            pass


def exception_hierarchy():
    """异常层次结构"""
    print("\n=== 异常层次结构 ===")
    
    print("""
    BaseException
    ├── SystemExit
    ├── KeyboardInterrupt
    ├── GeneratorExit
    └── Exception
        ├── StopIteration
        ├── ArithmeticError
        │   ├── ZeroDivisionError
        │   ├── FloatingPointError
        │   └── OverflowError
        ├── AssertionError
        ├── AttributeError
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
        │   ├── FileNotFoundError
        │   ├── PermissionError
        │   └── TimeoutError
        ├── RuntimeError
        │   ├── NotImplementedError
        │   └── RecursionError
        ├── TypeError
        ├── ValueError
        │   └── UnicodeError
        └── Warning
    """)
    
    # 捕获异常层次
    print("异常捕获示例:")
    
    def test_exception(exception_type):
        try:
            if exception_type == "lookup":
                [1, 2, 3][10]  # IndexError
            elif exception_type == "arithmetic":
                1 / 0  # ZeroDivisionError
            elif exception_type == "type":
                "string" + 123  # TypeError
        except LookupError as e:
            print(f"  LookupError: {e}")
        except ArithmeticError as e:
            print(f"  ArithmeticError: {e}")
        except Exception as e:
            print(f"  其他异常: {type(e).__name__}: {e}")
    
    test_exception("lookup")
    test_exception("arithmetic")
    test_exception("type")


# ============================================
# 2. 常见异常类型
# ============================================

def common_exceptions():
    """常见异常类型示例"""
    print("\n=== 常见异常类型 ===")
    
    # 1. ZeroDivisionError
    print("1. ZeroDivisionError:")
    try:
        print(10 / 0)
    except ZeroDivisionError as e:
        print(f"  {e}")
    
    # 2. IndexError
    print("\n2. IndexError:")
    try:
        lst = [1, 2, 3]
        print(lst[10])
    except IndexError as e:
        print(f"  {e}")
    
    # 3. KeyError
    print("\n3. KeyError:")
    try:
        d = {"a": 1, "b": 2}
        print(d["c"])
    except KeyError as e:
        print(f"  {e}")
    
    # 4. ValueError
    print("\n4. ValueError:")
    try:
        int("abc")
    except ValueError as e:
        print(f"  {e}")
    
    # 5. TypeError
    print("\n5. TypeError:")
    try:
        "string" + 123
    except TypeError as e:
        print(f"  {e}")
    
    # 6. AttributeError
    print("\n6. AttributeError:")
    try:
        lst = [1, 2, 3]
        lst.non_existent_method()
    except AttributeError as e:
        print(f"  {e}")
    
    # 7. FileNotFoundError
    print("\n7. FileNotFoundError:")
    try:
        with open("/nonexistent/file.txt") as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"  {e}")
    
    # 8. ImportError / ModuleNotFoundError
    print("\n8. ModuleNotFoundError:")
    try:
        import nonexistent_module
    except ModuleNotFoundError as e:
        print(f"  {e}")


# ============================================
# 3. 抛出异常
# ============================================

def raising_exceptions():
    """抛出异常"""
    print("\n=== 抛出异常 ===")
    
    # 基本抛出
    print("1. 使用 raise 抛出异常:")
    def divide(a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b
    
    try:
        result = divide(10, 0)
    except ValueError as e:
        print(f"  捕获到: {e}")
    
    # 重新抛出异常
    print("\n2. 重新抛出异常:")
    try:
        try:
            x = 1 / 0
        except ZeroDivisionError:
            print("  捕获到异常，进行处理后重新抛出")
            raise  # 重新抛出相同的异常
    except ZeroDivisionError as e:
        print(f"  外层捕获: {e}")
    
    # 异常链
    print("\n3. 异常链 (from):")
    try:
        try:
            result = int("abc")
        except ValueError as e:
            raise RuntimeError("数据处理失败") from e
    except RuntimeError as e:
        print(f"  RuntimeError: {e}")
        print(f"  原因: {e.__cause__}")
    
    # 抑制异常链
    print("\n4. 抑制异常链 (from None):")
    try:
        try:
            result = int("abc")
        except ValueError:
            raise RuntimeError("处理失败") from None
    except RuntimeError as e:
        print(f"  RuntimeError: {e}")
        print(f"  原因: {e.__cause__}")


# ============================================
# 4. 自定义异常
# ============================================

def custom_exceptions():
    """自定义异常"""
    print("\n=== 自定义异常 ===")
    
    # 简单自定义异常
    class InvalidAgeError(Exception):
        """年龄无效异常"""
        pass
    
    def set_age(age):
        if age < 0 or age > 150:
            raise InvalidAgeError(f"年龄 {age} 无效")
        return age
    
    print("1. 简单自定义异常:")
    try:
        set_age(200)
    except InvalidAgeError as e:
        print(f"  {e}")
    
    # 带额外信息的自定义异常
    class ValidationError(Exception):
        """验证错误"""
        def __init__(self, field, message):
            self.field = field
            self.message = message
            super().__init__(f"{field}: {message}")
    
    def validate_user(username, email):
        if len(username) < 3:
            raise ValidationError("username", "用户名至少3个字符")
        if "@" not in email:
            raise ValidationError("email", "邮箱格式无效")
    
    print("\n2. 带额外信息的异常:")
    try:
        validate_user("ab", "invalid-email")
    except ValidationError as e:
        print(f"  字段: {e.field}")
        print(f"  消息: {e.message}")
    
    # 异常层次结构
    class AppError(Exception):
        """应用程序基础异常"""
        pass
    
    class DatabaseError(AppError):
        """数据库错误"""
        pass
    
    class NetworkError(AppError):
        """网络错误"""
        pass
    
    class ConfigError(AppError):
        """配置错误"""
        pass
    
    print("\n3. 异常层次:")
    try:
        raise DatabaseError("数据库连接失败")
    except AppError as e:
        print(f"  应用错误: {type(e).__name__}: {e}")


# ============================================
# 5. 异常上下文管理
# ============================================

def exception_context():
    """异常上下文管理"""
    print("\n=== 异常上下文管理 ===")
    
    # 使用 with 语句
    print("1. with 语句（自动资源管理）:")
    try:
        with open("/tmp/test.txt", "w") as f:
            f.write("Hello, World!")
            # 即使发生异常，文件也会被正确关闭
            # raise ValueError("测试异常")
        print("  文件已自动关闭")
    except Exception as e:
        print(f"  异常: {e}")
    
    # 自定义上下文管理器
    print("\n2. 自定义上下文管理器:")
    
    class DatabaseConnection:
        def __init__(self, db_name):
            self.db_name = db_name
            self.connected = False
        
        def __enter__(self):
            print(f"  连接到数据库: {self.db_name}")
            self.connected = True
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"  关闭数据库连接: {self.db_name}")
            self.connected = False
            if exc_type is not None:
                print(f"  处理异常: {exc_type.__name__}")
            return False  # 不抑制异常
        
        def execute(self, query):
            if not self.connected:
                raise RuntimeError("未连接到数据库")
            print(f"  执行查询: {query}")
    
    try:
        with DatabaseConnection("mydb") as db:
            db.execute("SELECT * FROM users")
            # raise ValueError("模拟错误")
    except Exception as e:
        print(f"  捕获异常: {e}")
    
    # 使用 contextmanager 装饰器
    print("\n3. contextmanager 装饰器:")
    
    @contextmanager
    def temporary_value(var_name, temp_value):
        """临时修改全局变量"""
        original = globals().get(var_name)
        print(f"  保存原值: {var_name} = {original}")
        globals()[var_name] = temp_value
        print(f"  设置临时值: {var_name} = {temp_value}")
        try:
            yield
        finally:
            if original is None:
                globals().pop(var_name, None)
            else:
                globals()[var_name] = original
            print(f"  恢复原值: {var_name} = {original}")
    
    DEBUG = False
    print(f"  初始值: DEBUG = {DEBUG}")
    
    with temporary_value("DEBUG", True):
        print(f"  上下文中: DEBUG = {DEBUG}")
    
    print(f"  恢复后: DEBUG = {DEBUG}")


# ============================================
# 6. 异常信息
# ============================================

def exception_info():
    """异常信息获取"""
    print("\n=== 异常信息 ===")
    
    try:
        result = 10 / 0
    except Exception as e:
        # 异常对象
        print(f"1. 异常对象:")
        print(f"  类型: {type(e)}")
        print(f"  消息: {e}")
        print(f"  参数: {e.args}")
        
        # sys.exc_info()
        print(f"\n2. sys.exc_info():")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"  类型: {exc_type}")
        print(f"  值: {exc_value}")
        print(f"  traceback: {exc_traceback}")
        
        # traceback 模块
        print(f"\n3. traceback 模块:")
        print("  格式化traceback:")
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for line in tb_lines:
            print(f"    {line.strip()}")
        
        # 获取调用栈
        print(f"\n4. 调用栈:")
        tb_list = traceback.extract_tb(exc_traceback)
        for frame in tb_list:
            print(f"    文件: {frame.filename}")
            print(f"    行号: {frame.lineno}")
            print(f"    函数: {frame.name}")
            print(f"    代码: {frame.line}")


def exception_logging():
    """异常日志记录"""
    print("\n=== 异常日志 ===")
    
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # 记录异常
    print("1. 记录异常:")
    try:
        result = 10 / 0
    except Exception as e:
        logger.error("发生错误", exc_info=True)
    
    # 简化写法
    print("\n2. 使用 exception() 方法:")
    try:
        int("abc")
    except Exception as e:
        logger.exception("转换失败")


# ============================================
# 7. 断言
# ============================================

def assertions_demo():
    """断言"""
    print("\n=== 断言 ===")
    
    # 基本断言
    print("1. 基本断言:")
    x = 10
    assert x > 0, "x 必须为正数"
    print("  断言通过")
    
    # 断言失败
    print("\n2. 断言失败:")
    try:
        y = -5
        assert y > 0, f"y 必须为正数，当前值: {y}"
    except AssertionError as e:
        print(f"  AssertionError: {e}")
    
    # 使用场景
    print("\n3. 断言使用场景:")
    
    def calculate_average(numbers):
        assert len(numbers) > 0, "列表不能为空"
        assert all(isinstance(n, (int, float)) for n in numbers), "所有元素必须是数字"
        return sum(numbers) / len(numbers)
    
    try:
        avg = calculate_average([1, 2, 3, 4, 5])
        print(f"  平均值: {avg}")
        
        avg = calculate_average([])
    except AssertionError as e:
        print(f"  断言失败: {e}")


# ============================================
# 8. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 重试机制
    print("1. 重试机制:")
    import time
    
    def retry(max_attempts=3, delay=1):
        """重试装饰器"""
        def decorator(func):
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
                        print(f"  重试 {attempts}/{max_attempts}: {e}")
                        time.sleep(delay)
            return wrapper
        return decorator
    
    @retry(max_attempts=3, delay=0.1)
    def unstable_function():
        import random
        if random.random() < 0.7:
            raise ConnectionError("连接失败")
        return "成功"
    
    try:
        result = unstable_function()
        print(f"  结果: {result}")
    except Exception as e:
        print(f"  最终失败: {e}")
    
    # 2. 输入验证
    print("\n2. 输入验证:")
    
    class InputValidator:
        @staticmethod
        def validate_email(email):
            if not isinstance(email, str):
                raise TypeError("邮箱必须是字符串")
            if "@" not in email:
                raise ValueError("无效的邮箱格式")
            return email.lower()
        
        @staticmethod
        def validate_age(age):
            if not isinstance(age, int):
                raise TypeError("年龄必须是整数")
            if age < 0 or age > 150:
                raise ValueError(f"年龄超出有效范围: {age}")
            return age
    
    try:
        email = InputValidator.validate_email("user@example.com")
        print(f"  有效邮箱: {email}")
        
        age = InputValidator.validate_age(25)
        print(f"  有效年龄: {age}")
        
        # 无效输入
        InputValidator.validate_age(200)
    except (TypeError, ValueError) as e:
        print(f"  验证失败: {e}")
    
    # 3. 资源清理
    print("\n3. 资源清理:")
    
    class FileProcessor:
        def __init__(self, filename):
            self.filename = filename
            self.file = None
        
        def process(self):
            try:
                self.file = open(self.filename, 'w')
                self.file.write("Processing...")
                # 模拟错误
                # raise IOError("写入失败")
                print(f"  处理文件: {self.filename}")
            except IOError as e:
                print(f"  IO错误: {e}")
                raise
            finally:
                if self.file:
                    self.file.close()
                    print(f"  关闭文件: {self.filename}")
    
    processor = FileProcessor("/tmp/process.txt")
    try:
        processor.process()
    except Exception as e:
        print(f"  处理失败: {e}")
    
    # 4. 错误分类处理
    print("\n4. 错误分类处理:")
    
    def handle_api_request(endpoint):
        """模拟API请求"""
        import random
        error_type = random.choice(["success", "network", "auth", "server"])
        
        try:
            if error_type == "network":
                raise ConnectionError("网络连接失败")
            elif error_type == "auth":
                raise PermissionError("认证失败")
            elif error_type == "server":
                raise RuntimeError("服务器内部错误")
            return {"status": "success", "data": "响应数据"}
        
        except ConnectionError as e:
            print(f"  网络错误: {e} - 请检查网络连接")
            return {"status": "error", "type": "network"}
        except PermissionError as e:
            print(f"  认证错误: {e} - 请检查凭证")
            return {"status": "error", "type": "auth"}
        except Exception as e:
            print(f"  未知错误: {e}")
            return {"status": "error", "type": "unknown"}
    
    result = handle_api_request("/api/data")
    print(f"  结果: {result}")


# ============================================
# 9. 最佳实践
# ============================================

def best_practices():
    """异常处理最佳实践"""
    print("\n=== 异常处理最佳实践 ===")
    
    print("""
    1. 具体捕获异常
       ✓ except ValueError:
       ✗ except Exception:
       ✗ except:
    
    2. 不要忽略异常
       ✗ except Exception: pass
       ✓ except Exception as e: logger.error(e)
    
    3. 使用自定义异常
       - 创建有意义的异常类
       - 异常名称应该清晰表达错误类型
    
    4. 异常中包含有用信息
       ✓ raise ValueError(f"Invalid age: {age}")
       ✗ raise ValueError("Error")
    
    5. 合理使用 finally
       - 确保资源被释放
       - 清理操作
    
    6. 不要使用异常控制流程
       ✗ try: return dict[key]
          except KeyError: return None
       ✓ return dict.get(key)
    
    7. 记录异常
       - 使用 logging 模块
       - 包含 exc_info=True 或使用 exception()
    
    8. 优先使用上下文管理器
       ✓ with open(file) as f:
       ✗ f = open(file); try: ...; finally: f.close()
    
    9. 抛出合适级别的异常
       - 不要将底层异常直接暴露给用户
       - 使用异常链保留原始信息
    
    10. 测试异常情况
        - 为异常路径编写测试
        - 使用 pytest.raises 或 unittest.assertRaises
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 异常处理详解")
    print("=" * 60)
    
    exception_basics()
    exception_hierarchy()
    common_exceptions()
    
    raising_exceptions()
    custom_exceptions()
    
    exception_context()
    exception_info()
    exception_logging()
    
    assertions_demo()
    practical_examples()
    best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

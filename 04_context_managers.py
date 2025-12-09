"""
Python 高级教程 - 上下文管理器详解

上下文管理器用于管理资源的获取和释放，确保资源被正确清理。
本模块涵盖:
1. 上下文管理器协议
2. contextlib 模块
3. 异步上下文管理器
4. 实战应用
"""

import contextlib
import time
from typing import Optional, Any
import threading
import asyncio

# ============================================================================
# 1. 基础上下文管理器
# ============================================================================

class FileManager:
    """文件管理器 - 基础上下文管理器"""
    
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """进入上下文时调用"""
        print(f"打开文件: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文时调用
        exc_type: 异常类型
        exc_val: 异常值
        exc_tb: 异常追踪
        返回 True 表示异常已处理，False 表示继续传播异常
        """
        if self.file:
            print(f"关闭文件: {self.filename}")
            self.file.close()
        
        if exc_type is not None:
            print(f"发生异常: {exc_type.__name__}: {exc_val}")
            # 返回 False 让异常继续传播
            return False


# ============================================================================
# 2. 计时上下文管理器
# ============================================================================

class Timer:
    """计时上下文管理器"""
    
    def __init__(self, name: str = "操作"):
        self.name = name
        self.start_time = None
        self.elapsed = 0
    
    def __enter__(self):
        self.start_time = time.time()
        print(f"开始 {self.name}...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start_time
        print(f"{self.name} 完成，耗时: {self.elapsed:.4f}秒")
        return False


# ============================================================================
# 3. 数据库连接管理器
# ============================================================================

class DatabaseConnection:
    """数据库连接管理器 (模拟)"""
    
    def __init__(self, host: str, database: str):
        self.host = host
        self.database = database
        self.connection = None
        self.in_transaction = False
    
    def __enter__(self):
        print(f"连接数据库: {self.host}/{self.database}")
        self.connection = f"Connection<{self.host}/{self.database}>"
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("提交事务")
        else:
            print(f"回滚事务: {exc_type.__name__}")
        
        print("关闭数据库连接")
        self.connection = None
        return False
    
    def execute(self, query: str):
        """执行查询"""
        if not self.connection:
            raise RuntimeError("未连接数据库")
        print(f"执行查询: {query}")
        return f"结果: {query}"


# ============================================================================
# 4. 临时属性修改器
# ============================================================================

class TemporaryAttribute:
    """临时修改对象属性"""
    
    def __init__(self, obj, **attrs):
        self.obj = obj
        self.new_attrs = attrs
        self.old_attrs = {}
    
    def __enter__(self):
        # 保存原始值
        for key, new_value in self.new_attrs.items():
            self.old_attrs[key] = getattr(self.obj, key, None)
            setattr(self.obj, key, new_value)
        return self.obj
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 恢复原始值
        for key, old_value in self.old_attrs.items():
            setattr(self.obj, key, old_value)
        return False


# ============================================================================
# 5. 使用 @contextmanager 装饰器
# ============================================================================

@contextlib.contextmanager
def simple_timer(name: str):
    """简单计时器 - 使用 contextmanager 装饰器"""
    start = time.time()
    print(f"[{name}] 开始...")
    try:
        yield start  # yield 之前是 __enter__
    finally:
        # yield 之后是 __exit__
        elapsed = time.time() - start
        print(f"[{name}] 完成，耗时: {elapsed:.4f}秒")


@contextlib.contextmanager
def temporary_directory():
    """临时目录管理器"""
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    print(f"创建临时目录: {temp_dir}")
    try:
        yield temp_dir
    finally:
        print(f"删除临时目录: {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)


@contextlib.contextmanager
def suppress_stdout():
    """抑制标准输出"""
    import sys
    import io
    
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = old_stdout


# ============================================================================
# 6. 锁管理器
# ============================================================================

class Lock:
    """自定义锁管理器"""
    
    def __init__(self, name: str = "Lock"):
        self.name = name
        self.locked = False
        self._lock = threading.Lock()
    
    def __enter__(self):
        print(f"获取锁: {self.name}")
        self._lock.acquire()
        self.locked = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"释放锁: {self.name}")
        self._lock.release()
        self.locked = False
        return False


# ============================================================================
# 7. 可重入上下文管理器
# ============================================================================

class ReentrantContextManager:
    """可重入上下文管理器"""
    
    def __init__(self, name: str):
        self.name = name
        self.count = 0
    
    def __enter__(self):
        self.count += 1
        print(f"[{self.name}] 进入 (深度: {self.count})")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[{self.name}] 退出 (深度: {self.count})")
        self.count -= 1
        return False


# ============================================================================
# 8. 异常处理上下文管理器
# ============================================================================

class ExceptionHandler:
    """异常处理上下文管理器"""
    
    def __init__(self, *exception_types, default_value=None):
        self.exception_types = exception_types or (Exception,)
        self.default_value = default_value
        self.exception = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, self.exception_types):
            self.exception = exc_val
            print(f"捕获异常: {exc_type.__name__}: {exc_val}")
            return True  # 抑制异常
        return False


# ============================================================================
# 9. 多个上下文管理器的组合
# ============================================================================

@contextlib.contextmanager
def combined_context(*managers):
    """组合多个上下文管理器"""
    exits = []
    
    try:
        for manager in managers:
            exit_func = manager.__exit__
            enter_result = manager.__enter__()
            exits.append(exit_func)
            yield enter_result
    except Exception:
        # 反向调用 __exit__
        for exit_func in reversed(exits):
            exit_func(None, None, None)
        raise


# ============================================================================
# 10. 异步上下文管理器
# ============================================================================

class AsyncDatabaseConnection:
    """异步数据库连接管理器"""
    
    def __init__(self, host: str):
        self.host = host
        self.connection = None
    
    async def __aenter__(self):
        """异步进入上下文"""
        print(f"异步连接数据库: {self.host}")
        await asyncio.sleep(0.1)  # 模拟异步连接
        self.connection = f"AsyncConnection<{self.host}>"
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文"""
        print(f"异步关闭数据库连接: {self.host}")
        await asyncio.sleep(0.1)  # 模拟异步关闭
        self.connection = None
        return False
    
    async def query(self, sql: str):
        """执行异步查询"""
        await asyncio.sleep(0.05)
        return f"结果: {sql}"


@contextlib.asynccontextmanager
async def async_timer(name: str):
    """异步计时器"""
    start = time.time()
    print(f"[异步 {name}] 开始...")
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"[异步 {name}] 完成，耗时: {elapsed:.4f}秒")


# ============================================================================
# 11. 资源池管理器
# ============================================================================

class ResourcePool:
    """资源池管理器"""
    
    def __init__(self, create_resource, max_size: int = 5):
        self.create_resource = create_resource
        self.max_size = max_size
        self.pool = []
        self.in_use = set()
    
    def acquire(self):
        """获取资源"""
        if self.pool:
            resource = self.pool.pop()
            print(f"从池中获取资源: {resource}")
        elif len(self.in_use) < self.max_size:
            resource = self.create_resource()
            print(f"创建新资源: {resource}")
        else:
            raise RuntimeError("资源池已满")
        
        self.in_use.add(resource)
        return resource
    
    def release(self, resource):
        """释放资源"""
        if resource in self.in_use:
            self.in_use.remove(resource)
            self.pool.append(resource)
            print(f"释放资源到池: {resource}")
    
    @contextlib.contextmanager
    def get_resource(self):
        """上下文管理器方式获取资源"""
        resource = self.acquire()
        try:
            yield resource
        finally:
            self.release(resource)


# ============================================================================
# 演示函数
# ============================================================================

def demo_basic_context_manager():
    """演示基础上下文管理器"""
    print("=" * 60)
    print("1. 基础上下文管理器 - 文件操作")
    print("=" * 60)
    
    # 创建测试文件
    with open('test.txt', 'w') as f:
        f.write("测试内容\n")
    
    # 使用自定义文件管理器
    with FileManager('test.txt', 'r') as f:
        content = f.read()
        print(f"文件内容: {content.strip()}")
    
    # 清理
    import os
    os.remove('test.txt')
    print()


def demo_timer():
    """演示计时器"""
    print("=" * 60)
    print("2. 计时上下文管理器")
    print("=" * 60)
    
    with Timer("慢速操作"):
        time.sleep(0.5)
    
    with simple_timer("使用装饰器的计时器"):
        time.sleep(0.3)
    print()


def demo_database():
    """演示数据库管理器"""
    print("=" * 60)
    print("3. 数据库连接管理器")
    print("=" * 60)
    
    # 正常情况
    with DatabaseConnection("localhost", "test_db") as db:
        db.execute("SELECT * FROM users")
    
    # 异常情况
    try:
        with DatabaseConnection("localhost", "test_db") as db:
            db.execute("SELECT * FROM users")
            raise ValueError("模拟错误")
    except ValueError:
        pass
    print()


def demo_temporary_attribute():
    """演示临时属性修改"""
    print("=" * 60)
    print("4. 临时属性修改器")
    print("=" * 60)
    
    class Config:
        debug = False
        timeout = 30
    
    print(f"原始配置: debug={Config.debug}, timeout={Config.timeout}")
    
    with TemporaryAttribute(Config, debug=True, timeout=60):
        print(f"临时配置: debug={Config.debug}, timeout={Config.timeout}")
    
    print(f"恢复配置: debug={Config.debug}, timeout={Config.timeout}")
    print()


def demo_suppress():
    """演示抑制输出"""
    print("=" * 60)
    print("5. 抑制标准输出")
    print("=" * 60)
    
    print("这行会显示")
    with suppress_stdout():
        print("这行不会显示")
    print("这行会显示")
    print()


def demo_lock():
    """演示锁管理器"""
    print("=" * 60)
    print("6. 锁管理器")
    print("=" * 60)
    
    lock = Lock("共享资源锁")
    
    def worker(name: str):
        with lock:
            print(f"[{name}] 正在访问共享资源...")
            time.sleep(0.1)
            print(f"[{name}] 访问完成")
    
    threads = [
        threading.Thread(target=worker, args=(f"线程{i}",))
        for i in range(3)
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print()


def demo_reentrant():
    """演示可重入上下文管理器"""
    print("=" * 60)
    print("7. 可重入上下文管理器")
    print("=" * 60)
    
    ctx = ReentrantContextManager("可重入上下文")
    
    with ctx:
        print("  外层代码")
        with ctx:
            print("    内层代码")
        print("  外层代码")
    print()


def demo_exception_handler():
    """演示异常处理"""
    print("=" * 60)
    print("8. 异常处理上下文管理器")
    print("=" * 60)
    
    with ExceptionHandler(ValueError, TypeError) as handler:
        print("尝试执行可能出错的代码...")
        raise ValueError("这是一个值错误")
    
    print(f"捕获的异常: {handler.exception}")
    print()


def demo_contextlib_utilities():
    """演示 contextlib 实用工具"""
    print("=" * 60)
    print("9. contextlib 实用工具")
    print("=" * 60)
    
    # suppress - 抑制异常
    with contextlib.suppress(FileNotFoundError):
        open('不存在的文件.txt', 'r')
        print("这行不会执行")
    print("异常被抑制，继续执行")
    
    # closing - 自动调用 close()
    from io import StringIO
    with contextlib.closing(StringIO("数据")) as f:
        print(f"读取数据: {f.read()}")
    
    # redirect_stdout - 重定向标准输出
    from io import StringIO
    output = StringIO()
    with contextlib.redirect_stdout(output):
        print("这会被重定向")
    print(f"捕获的输出: {output.getvalue().strip()}")
    print()


async def demo_async_context_manager():
    """演示异步上下文管理器"""
    print("=" * 60)
    print("10. 异步上下文管理器")
    print("=" * 60)
    
    async with AsyncDatabaseConnection("async-db") as db:
        result = await db.query("SELECT * FROM async_users")
        print(result)
    
    async with async_timer("异步操作"):
        await asyncio.sleep(0.2)
    print()


def demo_resource_pool():
    """演示资源池"""
    print("=" * 60)
    print("11. 资源池管理器")
    print("=" * 60)
    
    # 创建资源池
    counter = [0]
    def create_resource():
        counter[0] += 1
        return f"Resource-{counter[0]}"
    
    pool = ResourcePool(create_resource, max_size=3)
    
    # 使用资源
    with pool.get_resource() as r1:
        print(f"使用资源: {r1}")
        
        with pool.get_resource() as r2:
            print(f"使用资源: {r2}")
        
        with pool.get_resource() as r3:
            print(f"再次使用资源: {r3}")  # 应该复用 r2
    print()


# ============================================================================
# 重要注意事项
# ============================================================================

"""
上下文管理器最佳实践和注意事项:

1. 上下文管理器协议
   - __enter__: 进入上下文，返回资源对象
   - __exit__: 退出上下文，处理异常和清理
   - 返回 True 表示异常已处理，False 继续传播

2. 使用场景
   ✓ 文件操作 (自动关闭)
   ✓ 数据库连接 (自动提交/回滚)
   ✓ 锁管理 (自动释放)
   ✓ 临时状态修改 (自动恢复)
   ✓ 资源池管理 (自动归还)

3. @contextmanager 装饰器
   - 使用生成器简化上下文管理器
   - yield 之前是 __enter__
   - yield 之后是 __exit__ (在 finally 中)
   - 更简洁，推荐用于简单场景

4. 异步上下文管理器
   - 实现 __aenter__ 和 __aexit__
   - 使用 async with 语句
   - @asynccontextmanager 装饰器

5. 异常处理
   - __exit__ 接收异常信息
   - 返回 True 抑制异常
   - 返回 False 或 None 继续传播异常
   - 务必在 finally 中清理资源

6. 可重入性
   - 某些上下文管理器支持嵌套使用
   - threading.RLock 是可重入锁
   - 设计时考虑是否需要可重入

7. 多个上下文管理器
   - 使用多个 with 子句
   - with contextlib.ExitStack() 动态管理
   - 执行顺序: 后进先出 (LIFO)

8. 常见陷阱
   - 忘记在 __exit__ 中清理资源
   - 错误处理异常返回值
   - 在 __enter__ 中发生异常不会调用 __exit__
   - 循环引用导致资源不释放

9. 性能考虑
   - 上下文管理器有轻微性能开销
   - 频繁创建考虑使用资源池
   - 异步版本适合 I/O 密集型操作

10. 标准库示例
    - open(): 文件操作
    - threading.Lock(): 线程锁
    - decimal.localcontext(): 精度控制
    - unittest.mock.patch(): 模拟测试
    - contextlib 模块的各种工具

11. contextlib 实用工具
    - suppress: 抑制指定异常
    - closing: 自动调用 close()
    - redirect_stdout/stderr: 重定向输出
    - ExitStack: 动态管理多个上下文
    - nullcontext: 可选的上下文管理器
"""


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Python 高级教程 - 上下文管理器详解")
    print("=" * 60 + "\n")
    
    demo_basic_context_manager()
    demo_timer()
    demo_database()
    demo_temporary_attribute()
    demo_suppress()
    demo_lock()
    demo_reentrant()
    demo_exception_handler()
    demo_contextlib_utilities()
    demo_resource_pool()
    
    # 运行异步示例
    print("运行异步示例...")
    asyncio.run(demo_async_context_manager())
    
    print("=" * 60)
    print("上下文管理器教程完成!")
    print("=" * 60)

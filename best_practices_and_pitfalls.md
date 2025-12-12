# Asyncio 最佳实践与常见陷阱

## 目录
- [1. 最佳实践](#1-最佳实践)
- [2. 常见陷阱](#2-常见陷阱)
- [3. 性能优化](#3-性能优化)
- [4. 调试技巧](#4-调试技巧)
- [5. 错误处理](#5-错误处理)
- [6. 测试策略](#6-测试策略)
- [7. 生产环境注意事项](#7-生产环境注意事项)

---

## 1. 最佳实践

### 1.1 使用 `asyncio.run()` 作为入口点

```python
import asyncio

# ✅ 推荐：使用 asyncio.run()
async def main():
    await asyncio.sleep(1)
    print("完成")

if __name__ == "__main__":
    asyncio.run(main())

# ❌ 避免：手动管理事件循环（除非有特殊需求）
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

**原因**: `asyncio.run()` 会自动：
- 创建新的事件循环
- 运行协程
- 关闭事件循环
- 处理未完成的任务

### 1.2 始终 await 协程

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "数据"

# ❌ 错误：忘记 await
async def bad_example():
    result = fetch_data()  # 返回协程对象，不是结果！
    print(result)  # 打印：<coroutine object fetch_data at ...>

# ✅ 正确：使用 await
async def good_example():
    result = await fetch_data()
    print(result)  # 打印：数据
```

### 1.3 使用 `create_task()` 实现真正的并发

```python
import asyncio
import time

async def task(name, delay):
    await asyncio.sleep(delay)
    return f"{name} 完成"

# ❌ 错误：顺序执行（总共 6 秒）
async def sequential():
    start = time.time()
    r1 = await task("Task1", 2)
    r2 = await task("Task2", 2)
    r3 = await task("Task3", 2)
    print(f"耗时: {time.time() - start:.1f}秒")  # 约 6 秒

# ✅ 正确：并发执行（约 2 秒）
async def concurrent():
    start = time.time()
    t1 = asyncio.create_task(task("Task1", 2))
    t2 = asyncio.create_task(task("Task2", 2))
    t3 = asyncio.create_task(task("Task3", 2))
    
    results = await asyncio.gather(t1, t2, t3)
    print(f"耗时: {time.time() - start:.1f}秒")  # 约 2 秒
```

### 1.4 正确使用 `gather()` 和 `wait()`

```python
import asyncio

async def task(n):
    await asyncio.sleep(n)
    return n

# gather: 等待所有任务，返回结果列表
async def use_gather():
    results = await asyncio.gather(
        task(1),
        task(2),
        task(3)
    )
    print(results)  # [1, 2, 3]

# gather with return_exceptions: 不会因异常而中断
async def gather_with_exceptions():
    async def failing_task():
        raise ValueError("错误")
    
    results = await asyncio.gather(
        task(1),
        failing_task(),
        task(2),
        return_exceptions=True
    )
    print(results)  # [1, ValueError('错误'), 2]

# wait: 更灵活的控制
async def use_wait():
    tasks = {asyncio.create_task(task(i)) for i in range(1, 4)}
    
    # 等待第一个完成
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"完成: {len(done)}, 待完成: {len(pending)}")
    
    # 取消待完成的任务
    for t in pending:
        t.cancel()
```

### 1.5 使用异步上下文管理器管理资源

```python
import asyncio

# ✅ 推荐：使用异步上下文管理器
class AsyncResource:
    async def __aenter__(self):
        print("获取资源")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("释放资源")
        await asyncio.sleep(0.1)
        return False

async def good_example():
    async with AsyncResource() as resource:
        print("使用资源")
        await asyncio.sleep(0.5)
    # 自动释放资源

# ❌ 避免：手动管理（容易遗漏清理）
async def bad_example():
    resource = AsyncResource()
    await resource.__aenter__()
    try:
        print("使用资源")
        await asyncio.sleep(0.5)
    finally:
        await resource.__aexit__(None, None, None)
```

### 1.6 使用信号量限制并发

```python
import asyncio

# ✅ 推荐：使用 Semaphore 限制并发数
async def rate_limited_request(semaphore, url):
    async with semaphore:
        print(f"请求 {url}")
        await asyncio.sleep(1)
        return f"结果: {url}"

async def main():
    semaphore = asyncio.Semaphore(5)  # 最多 5 个并发
    
    urls = [f"url-{i}" for i in range(20)]
    tasks = [rate_limited_request(semaphore, url) for url in urls]
    
    results = await asyncio.gather(*tasks)
    print(f"完成 {len(results)} 个请求")
```

### 1.7 设置超时

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(10)
    return "完成"

# ✅ 推荐：始终设置超时
async def with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=3.0)
        print(result)
    except asyncio.TimeoutError:
        print("操作超时")

# Python 3.11+ 可以使用 timeout 上下文管理器
async def with_timeout_context():
    try:
        async with asyncio.timeout(3.0):
            result = await slow_operation()
            print(result)
    except asyncio.TimeoutError:
        print("操作超时")
```

---

## 2. 常见陷阱

### 2.1 阻塞事件循环

```python
import asyncio
import time

# ❌ 错误：在异步函数中使用阻塞调用
async def bad_example():
    time.sleep(2)  # 阻塞整个事件循环！
    return "完成"

# ✅ 正确：使用异步版本
async def good_example():
    await asyncio.sleep(2)  # 不阻塞事件循环
    return "完成"

# ✅ 如果必须使用阻塞调用，使用 run_in_executor
import concurrent.futures

def blocking_io():
    time.sleep(2)
    return "完成"

async def good_example_executor():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)
    return result
```

**常见的阻塞调用：**
- `time.sleep()` → 使用 `asyncio.sleep()`
- `requests.get()` → 使用 `aiohttp`
- `open()` / `read()` / `write()` → 使用 `aiofiles`
- 数据库查询 → 使用异步驱动（如 `asyncpg`, `motor`）

### 2.2 在循环中 await（失去并发）

```python
import asyncio

async def fetch_data(id):
    await asyncio.sleep(1)
    return f"数据-{id}"

# ❌ 错误：在循环中顺序 await（总共 10 秒）
async def bad_example():
    results = []
    for i in range(10):
        result = await fetch_data(i)  # 顺序执行
        results.append(result)
    return results

# ✅ 正确：先创建所有任务，再并发执行（约 1 秒）
async def good_example():
    tasks = [fetch_data(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    return results
```

### 2.3 忘记处理任务取消

```python
import asyncio

# ❌ 错误：忽略 CancelledError
async def bad_example():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("被取消了")
        # 没有重新抛出！任务不会被正确取消

# ✅ 正确：重新抛出 CancelledError
async def good_example():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("被取消，进行清理...")
        # 执行清理操作
        raise  # 重要：重新抛出
```

### 2.4 混用同步和异步代码

```python
import asyncio

# ❌ 错误：在同步函数中调用异步函数
def sync_function():
    result = async_function()  # 返回协程对象，不是结果
    print(result)  # <coroutine object...>

async def async_function():
    await asyncio.sleep(1)
    return "结果"

# ✅ 正确方式 1：在异步上下文中调用
async def caller():
    result = await async_function()
    print(result)

# ✅ 正确方式 2：从同步代码启动事件循环
def sync_caller():
    result = asyncio.run(async_function())
    print(result)
```

### 2.5 创建未 await 的任务

```python
import asyncio

async def background_task():
    await asyncio.sleep(1)
    print("后台任务完成")

# ❌ 错误：创建任务但不等待
async def bad_example():
    asyncio.create_task(background_task())
    # 主函数立即返回，任务可能未完成

# ✅ 正确：保持任务引用并在需要时等待
async def good_example():
    task = asyncio.create_task(background_task())
    # 做其他事情...
    await task  # 确保任务完成

# ✅ 或者使用 TaskGroup (Python 3.11+)
async def good_example_taskgroup():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(background_task())
        # TaskGroup 确保所有任务完成
```

### 2.6 不正确地共享状态

```python
import asyncio

# ❌ 错误：未保护的共享状态
class Counter:
    def __init__(self):
        self.value = 0
    
    async def increment(self):
        current = self.value
        await asyncio.sleep(0)  # 模拟上下文切换
        self.value = current + 1

async def bad_example():
    counter = Counter()
    await asyncio.gather(*[counter.increment() for _ in range(10)])
    print(counter.value)  # 可能不是 10！

# ✅ 正确：使用锁保护共享状态
class SafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()
    
    async def increment(self):
        async with self.lock:
            current = self.value
            await asyncio.sleep(0)
            self.value = current + 1

async def good_example():
    counter = SafeCounter()
    await asyncio.gather(*[counter.increment() for _ in range(10)])
    print(counter.value)  # 保证是 10
```

### 2.7 过度使用 asyncio

```python
# ❌ 错误：对 CPU 密集型任务使用 asyncio
async def cpu_intensive():
    # 大量计算
    total = sum(i * i for i in range(10_000_000))
    return total

# ✅ 正确：对 CPU 密集型任务使用 ProcessPoolExecutor
import concurrent.futures

def cpu_intensive_sync():
    return sum(i * i for i in range(10_000_000))

async def good_example():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_intensive_sync)
    return result
```

**何时使用 asyncio：**
- ✅ I/O 密集型任务（网络请求、文件 I/O、数据库查询）
- ✅ 需要管理大量并发连接
- ❌ CPU 密集型任务（使用 multiprocessing）
- ❌ 简单的顺序脚本

---

## 3. 性能优化

### 3.1 批量处理减少开销

```python
import asyncio

# ❌ 低效：逐个处理
async def process_one_by_one(items):
    results = []
    for item in items:
        result = await process_item(item)
        results.append(result)
    return results

# ✅ 高效：批量处理
async def process_in_batches(items, batch_size=100):
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await asyncio.gather(
            *[process_item(item) for item in batch]
        )
        results.extend(batch_results)
    return results

async def process_item(item):
    await asyncio.sleep(0.1)
    return item * 2
```

### 3.2 使用连接池

```python
import asyncio
import aiohttp

# ❌ 低效：每次请求创建新连接
async def without_pool(urls):
    results = []
    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                results.append(await response.text())
    return results

# ✅ 高效：使用连接池
async def with_pool(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
```

### 3.3 避免不必要的任务创建

```python
import asyncio

# ❌ 低效：为简单操作创建任务
async def inefficient():
    task1 = asyncio.create_task(asyncio.sleep(1))
    task2 = asyncio.create_task(asyncio.sleep(1))
    await task1
    await task2
    # 顺序等待，没有并发优势

# ✅ 高效：直接使用 gather
async def efficient():
    await asyncio.gather(
        asyncio.sleep(1),
        asyncio.sleep(1)
    )
```

### 3.4 使用 uvloop（生产环境）

```python
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    print("使用 uvloop")
except ImportError:
    print("使用标准 asyncio")

async def main():
    # 你的代码
    pass

asyncio.run(main())
```

**uvloop 性能提升：**
- 比标准 asyncio 快 2-4 倍
- 基于 libuv（Node.js 使用的事件循环）
- 安装：`pip install uvloop`

### 3.5 合理使用缓存

```python
import asyncio
from functools import lru_cache

# 同步函数缓存
@lru_cache(maxsize=128)
def expensive_calculation(n):
    return sum(i * i for i in range(n))

# 异步函数缓存（自定义实现）
class AsyncLRU:
    def __init__(self, maxsize=128):
        self.cache = {}
        self.maxsize = maxsize
    
    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in self.cache:
                return self.cache[key]
            
            result = await func(*args, **kwargs)
            
            if len(self.cache) >= self.maxsize:
                self.cache.pop(next(iter(self.cache)))
            
            self.cache[key] = result
            return result
        
        return wrapper

@AsyncLRU(maxsize=100)
async def expensive_async_operation(n):
    await asyncio.sleep(1)
    return n * 2
```

---

## 4. 调试技巧

### 4.1 启用调试模式

```python
import asyncio
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

async def main():
    # 你的代码
    await asyncio.sleep(1)

# 启用调试模式
asyncio.run(main(), debug=True)
```

**调试模式会：**
- 检查未 await 的协程
- 记录慢回调（默认 > 100ms）
- 显示详细的异常堆栈

### 4.2 追踪慢回调

```python
import asyncio

async def slow_callback():
    # 模拟慢操作
    import time
    time.sleep(0.5)  # 阻塞！

async def main():
    loop = asyncio.get_running_loop()
    
    # 设置慢回调阈值（秒）
    loop.slow_callback_duration = 0.1
    
    await slow_callback()
    # 调试模式会警告这个慢回调

asyncio.run(main(), debug=True)
```

### 4.3 检查未完成的任务

```python
import asyncio

async def leaked_task():
    await asyncio.sleep(10)

async def main():
    # 创建任务但不等待
    task = asyncio.create_task(leaked_task())
    
    await asyncio.sleep(1)
    
    # 检查所有任务
    all_tasks = asyncio.all_tasks()
    print(f"未完成的任务: {len(all_tasks)}")
    for task in all_tasks:
        print(f"  - {task.get_name()}: {task}")

asyncio.run(main())
```

### 4.4 使用任务名称

```python
import asyncio

async def worker(n):
    await asyncio.sleep(n)
    return n

async def main():
    # 给任务命名方便调试
    tasks = [
        asyncio.create_task(worker(i), name=f"worker-{i}")
        for i in range(5)
    ]
    
    # 可以通过名称识别任务
    for task in asyncio.all_tasks():
        print(f"任务: {task.get_name()}")
    
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### 4.5 捕获和记录异常

```python
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def task_with_error():
    await asyncio.sleep(1)
    raise ValueError("出错了！")

async def main():
    try:
        await task_with_error()
    except Exception as e:
        logger.exception("任务失败")
        # 记录完整的堆栈跟踪

asyncio.run(main())
```

---

## 5. 错误处理

### 5.1 处理 gather 中的异常

```python
import asyncio

async def task_that_fails():
    await asyncio.sleep(1)
    raise ValueError("失败")

async def task_that_succeeds():
    await asyncio.sleep(1)
    return "成功"

# 方式 1: 让异常传播（第一个异常会停止所有任务）
async def fail_fast():
    try:
        results = await asyncio.gather(
            task_that_succeeds(),
            task_that_fails(),
            task_that_succeeds()
        )
    except ValueError as e:
        print(f"捕获异常: {e}")

# 方式 2: 收集所有结果，包括异常
async def collect_all():
    results = await asyncio.gather(
        task_that_succeeds(),
        task_that_fails(),
        task_that_succeeds(),
        return_exceptions=True
    )
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"任务 {i} 失败: {result}")
        else:
            print(f"任务 {i} 成功: {result}")
```

### 5.2 超时处理

```python
import asyncio

async def operation_with_timeout():
    try:
        async with asyncio.timeout(5.0):
            await slow_operation()
    except asyncio.TimeoutError:
        print("操作超时")
        # 清理资源
        await cleanup()
    except Exception as e:
        print(f"其他错误: {e}")
        # 错误处理
    else:
        print("操作成功")
    finally:
        print("总是执行")

async def slow_operation():
    await asyncio.sleep(10)

async def cleanup():
    await asyncio.sleep(0.1)
```

### 5.3 重试逻辑

```python
import asyncio
from typing import TypeVar, Callable

T = TypeVar('T')

async def retry_async(
    func: Callable[..., T],
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> T:
    """通用异步重试函数"""
    last_exception = None
    current_delay = delay
    
    for attempt in range(max_retries):
        try:
            return await func()
        except exceptions as e:
            last_exception = e
            
            if attempt < max_retries - 1:
                print(f"尝试 {attempt + 1} 失败: {e}")
                print(f"等待 {current_delay:.1f} 秒后重试...")
                await asyncio.sleep(current_delay)
                current_delay *= backoff
            else:
                print(f"所有 {max_retries} 次尝试都失败")
    
    raise last_exception

# 使用示例
async def unstable_operation():
    import random
    if random.random() < 0.7:
        raise ConnectionError("连接失败")
    return "成功"

async def main():
    try:
        result = await retry_async(
            unstable_operation,
            max_retries=5,
            delay=1.0,
            backoff=2.0,
            exceptions=(ConnectionError,)
        )
        print(result)
    except ConnectionError:
        print("操作最终失败")
```

---

## 6. 测试策略

### 6.1 使用 pytest-asyncio

```python
import asyncio
import pytest

# 安装: pip install pytest-asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == "expected"

async def async_operation():
    await asyncio.sleep(0.1)
    return "expected"

# 测试超时
@pytest.mark.asyncio
async def test_timeout():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=1.0)

async def slow_operation():
    await asyncio.sleep(10)
```

### 6.2 模拟（Mock）异步函数

```python
import asyncio
from unittest.mock import AsyncMock, patch

async def fetch_data(url):
    # 实际的网络请求
    pass

@pytest.mark.asyncio
async def test_with_mock():
    # 创建异步 mock
    mock_fetch = AsyncMock(return_value="模拟数据")
    
    with patch('module.fetch_data', mock_fetch):
        result = await fetch_data("http://example.com")
        assert result == "模拟数据"
        mock_fetch.assert_called_once_with("http://example.com")
```

### 6.3 测试并发行为

```python
import asyncio
import pytest

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()
    
    async def increment(self):
        async with self.lock:
            current = self.value
            await asyncio.sleep(0)  # 模拟上下文切换
            self.value = current + 1

@pytest.mark.asyncio
async def test_concurrent_increments():
    counter = Counter()
    
    # 并发执行 100 次增量
    await asyncio.gather(*[counter.increment() for _ in range(100)])
    
    # 验证结果正确
    assert counter.value == 100
```

### 6.4 测试取消行为

```python
import asyncio
import pytest

async def cancellable_task():
    try:
        await asyncio.sleep(10)
        return "完成"
    except asyncio.CancelledError:
        # 清理资源
        await cleanup()
        raise

async def cleanup():
    await asyncio.sleep(0.1)

@pytest.mark.asyncio
async def test_cancellation():
    task = asyncio.create_task(cancellable_task())
    
    await asyncio.sleep(0.1)
    task.cancel()
    
    with pytest.raises(asyncio.CancelledError):
        await task
    
    assert task.cancelled()
```

---

## 7. 生产环境注意事项

### 7.1 优雅关闭

```python
import asyncio
import signal
from typing import Set

class Application:
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.tasks: Set[asyncio.Task] = set()
    
    def setup_signal_handlers(self):
        """设置信号处理"""
        for sig in (signal.SIGTERM, signal.SIGINT):
            asyncio.get_event_loop().add_signal_handler(
                sig,
                lambda: self.shutdown_event.set()
            )
    
    def create_task(self, coro):
        """创建并跟踪任务"""
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return task
    
    async def shutdown(self, timeout: float = 10.0):
        """优雅关闭"""
        print(f"开始关闭，取消 {len(self.tasks)} 个任务...")
        
        for task in self.tasks:
            task.cancel()
        
        try:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            print(f"警告: 部分任务未在 {timeout} 秒内完成")
        
        print("关闭完成")
    
    async def run(self):
        """运行应用"""
        self.setup_signal_handlers()
        
        # 创建工作任务
        self.create_task(self.worker())
        
        # 等待关闭信号
        await self.shutdown_event.wait()
        
        # 执行关闭
        await self.shutdown()
    
    async def worker(self):
        """示例工作任务"""
        try:
            while True:
                await asyncio.sleep(1)
                print("工作中...")
        except asyncio.CancelledError:
            print("Worker 被取消")
            raise

# 使用
# asyncio.run(Application().run())
```

### 7.2 监控和指标

```python
import asyncio
import time
from typing import Dict, Any

class Metrics:
    """简单的指标收集器"""
    
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.timings: Dict[str, list] = {}
    
    def increment(self, name: str, value: int = 1):
        """增加计数器"""
        self.counters[name] = self.counters.get(name, 0) + value
    
    def record_time(self, name: str, duration: float):
        """记录时间"""
        if name not in self.timings:
            self.timings[name] = []
        self.timings[name].append(duration)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {"counters": self.counters}
        
        for name, times in self.timings.items():
            stats[name] = {
                "count": len(times),
                "avg": sum(times) / len(times) if times else 0,
                "min": min(times) if times else 0,
                "max": max(times) if times else 0,
            }
        
        return stats

# 使用装饰器记录指标
def monitor_async(metrics: Metrics, operation_name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                metrics.increment(f"{operation_name}_success")
                return result
            except Exception as e:
                metrics.increment(f"{operation_name}_error")
                raise
            finally:
                duration = time.time() - start
                metrics.record_time(operation_name, duration)
        return wrapper
    return decorator

# 示例使用
metrics = Metrics()

@monitor_async(metrics, "api_call")
async def api_call():
    await asyncio.sleep(0.5)
    return "数据"

async def main():
    for _ in range(10):
        await api_call()
    
    print(metrics.get_stats())
```

### 7.3 连接池配置

```python
import asyncio
import aiohttp

async def create_http_client():
    """创建配置好的 HTTP 客户端"""
    connector = aiohttp.TCPConnector(
        limit=100,              # 总连接数限制
        limit_per_host=10,      # 每个主机的连接数限制
        ttl_dns_cache=300,      # DNS 缓存 TTL
        keepalive_timeout=30,   # Keep-alive 超时
    )
    
    timeout = aiohttp.ClientTimeout(
        total=60,               # 总超时
        connect=10,             # 连接超时
        sock_read=30,           # 读取超时
    )
    
    session = aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    )
    
    return session

async def main():
    async with await create_http_client() as session:
        # 使用 session 进行请求
        async with session.get('http://example.com') as response:
            data = await response.text()
```

### 7.4 错误报告和日志

```python
import asyncio
import logging
import sys
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

async def monitored_task(task_id: int):
    """带监控的任务"""
    logger.info(f"任务 {task_id} 开始")
    
    try:
        # 执行任务
        await asyncio.sleep(1)
        result = f"结果-{task_id}"
        
        logger.info(f"任务 {task_id} 完成: {result}")
        return result
    
    except asyncio.CancelledError:
        logger.warning(f"任务 {task_id} 被取消")
        raise
    
    except Exception as e:
        logger.exception(f"任务 {task_id} 失败")
        raise

async def main():
    tasks = [monitored_task(i) for i in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 统计结果
    successes = sum(1 for r in results if not isinstance(r, Exception))
    failures = len(results) - successes
    
    logger.info(f"完成: {successes} 成功, {failures} 失败")
```

### 7.5 资源限制

```python
import asyncio
import resource

def set_resource_limits():
    """设置资源限制"""
    # 文件描述符限制
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    print(f"文件描述符限制: soft={soft}, hard={hard}")
    
    # 尝试提高限制
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (10000, hard))
        print("提高文件描述符限制到 10000")
    except ValueError:
        print("无法提高限制")

async def main():
    set_resource_limits()
    
    # 你的应用代码
    pass

# asyncio.run(main())
```

---

## 总结

### 核心原则

1. **永远不要阻塞事件循环**
2. **正确使用 await 和 create_task**
3. **处理所有异常和取消**
4. **设置超时**
5. **限制并发数量**
6. **保护共享状态**
7. **优雅关闭**
8. **监控和日志**

### 检查清单

在将 asyncio 应用部署到生产环境前，检查：

- [ ] 所有阻塞 I/O 都已替换为异步版本
- [ ] 设置了适当的超时
- [ ] 实现了重试逻辑
- [ ] 有并发限制（Semaphore/连接池）
- [ ] 实现了优雅关闭
- [ ] 异常处理完善
- [ ] 添加了日志和监控
- [ ] 编写了测试
- [ ] 考虑了资源限制
- [ ] 性能测试通过

掌握这些最佳实践，你就能构建稳定、高效的异步 Python 应用！

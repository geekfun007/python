# Asyncio 速查表

> 快速参考手册，包含最常用的 asyncio 代码片段

---

## 基础语法

### 定义和运行协程

```python
import asyncio

# 定义协程
async def my_coroutine():
    await asyncio.sleep(1)
    return "完成"

# 运行协程（入口点）
asyncio.run(my_coroutine())
```

### 并发执行多个协程

```python
# 方式 1: gather（推荐）
results = await asyncio.gather(
    coro1(),
    coro2(),
    coro3()
)

# 方式 2: create_task
task1 = asyncio.create_task(coro1())
task2 = asyncio.create_task(coro2())
results = [await task1, await task2]

# 方式 3: TaskGroup（Python 3.11+）
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(coro1())
    task2 = tg.create_task(coro2())
```

---

## 常用函数

### asyncio.sleep()
```python
await asyncio.sleep(1)  # 异步休眠 1 秒
```

### asyncio.gather()
```python
# 并发执行，等待所有完成
results = await asyncio.gather(coro1(), coro2(), coro3())

# 忽略异常
results = await asyncio.gather(
    coro1(), coro2(), coro3(),
    return_exceptions=True
)
```

### asyncio.create_task()
```python
# 创建任务（立即开始执行）
task = asyncio.create_task(my_coroutine(), name="my-task")

# 等待任务完成
result = await task
```

### asyncio.wait_for()
```python
# 设置超时
try:
    result = await asyncio.wait_for(my_coroutine(), timeout=5.0)
except asyncio.TimeoutError:
    print("超时")
```

### asyncio.wait()
```python
# 等待任务完成
tasks = {asyncio.create_task(coro()) for _ in range(10)}

# 等待所有完成
done, pending = await asyncio.wait(tasks)

# 等待第一个完成
done, pending = await asyncio.wait(
    tasks,
    return_when=asyncio.FIRST_COMPLETED
)
```

### asyncio.timeout() (Python 3.11+)
```python
try:
    async with asyncio.timeout(10.0):
        await my_coroutine()
except asyncio.TimeoutError:
    print("超时")
```

---

## 并发控制

### Semaphore - 限制并发数
```python
semaphore = asyncio.Semaphore(5)  # 最多 5 个并发

async def limited_task():
    async with semaphore:
        # 受限的操作
        await asyncio.sleep(1)
```

### Lock - 互斥锁
```python
lock = asyncio.Lock()

async def protected_operation():
    async with lock:
        # 同时只有一个协程可以执行
        await asyncio.sleep(1)
```

### Event - 事件通知
```python
event = asyncio.Event()

# 等待事件
await event.wait()

# 触发事件
event.set()

# 清除事件
event.clear()
```

### Queue - 队列
```python
queue = asyncio.Queue(maxsize=10)

# 生产者
await queue.put(item)

# 消费者
item = await queue.get()
queue.task_done()

# 等待队列清空
await queue.join()
```

---

## 异步上下文管理器

### 定义
```python
class AsyncResource:
    async def __aenter__(self):
        # 获取资源
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 释放资源
        return False

# 使用
async with AsyncResource() as resource:
    # 使用资源
    pass
```

### 使用装饰器
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def my_resource():
    # 设置
    resource = await setup()
    try:
        yield resource
    finally:
        # 清理
        await cleanup(resource)
```

---

## 异步迭代器

### 定义
```python
class AsyncIterator:
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if condition:
            raise StopAsyncIteration
        return await get_next_value()

# 使用
async for item in AsyncIterator():
    print(item)
```

### 异步生成器
```python
async def async_generator():
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i

# 使用
async for value in async_generator():
    print(value)
```

---

## 任务管理

### 获取所有任务
```python
all_tasks = asyncio.all_tasks()
current_task = asyncio.current_task()
```

### 取消任务
```python
task = asyncio.create_task(my_coroutine())

# 取消任务
task.cancel()

# 检查是否被取消
if task.cancelled():
    print("任务已取消")

# 处理取消
try:
    await task
except asyncio.CancelledError:
    print("捕获取消")
```

### 任务回调
```python
def callback(task):
    print(f"任务完成: {task.result()}")

task = asyncio.create_task(my_coroutine())
task.add_done_callback(callback)
```

---

## 阻塞代码处理

### run_in_executor
```python
import concurrent.futures

def blocking_io():
    time.sleep(1)
    return "结果"

# 在线程池中运行
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(None, blocking_io)

# 使用自定义执行器
with concurrent.futures.ThreadPoolExecutor() as pool:
    result = await loop.run_in_executor(pool, blocking_io)
```

---

## 错误处理

### 基本异常处理
```python
try:
    result = await my_coroutine()
except ValueError as e:
    print(f"错误: {e}")
except asyncio.TimeoutError:
    print("超时")
except asyncio.CancelledError:
    print("取消")
    raise  # 重新抛出
```

### gather 异常处理
```python
# 方式 1: 第一个异常会中断所有
try:
    results = await asyncio.gather(coro1(), coro2())
except Exception as e:
    print(f"错误: {e}")

# 方式 2: 收集所有结果（包括异常）
results = await asyncio.gather(
    coro1(), coro2(),
    return_exceptions=True
)

for result in results:
    if isinstance(result, Exception):
        print(f"错误: {result}")
```

---

## 调试

### 启用调试模式
```python
asyncio.run(main(), debug=True)

# 或
import logging
logging.basicConfig(level=logging.DEBUG)
asyncio.run(main(), debug=True)
```

### 检查协程
```python
import inspect

coro = my_coroutine()
print(f"是协程: {inspect.iscoroutine(coro)}")
```

---

## 常用模式

### 重试
```python
async def retry(func, max_retries=3, delay=1.0):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(delay)
```

### 超时重试
```python
async def timeout_retry(func, timeout=5.0, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await asyncio.wait_for(func(), timeout=timeout)
        except asyncio.TimeoutError:
            if attempt == max_retries - 1:
                raise
```

### 批量处理
```python
async def batch_process(items, batch_size=100):
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await asyncio.gather(
            *[process_item(item) for item in batch]
        )
        results.extend(batch_results)
    return results
```

### 生产者-消费者
```python
queue = asyncio.Queue()

async def producer():
    for i in range(10):
        await queue.put(i)

async def consumer():
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=2.0)
            # 处理 item
            queue.task_done()
        except asyncio.TimeoutError:
            break

# 运行
await asyncio.gather(
    producer(),
    consumer(),
    consumer()
)
await queue.join()
```

---

## 性能优化

### 使用 uvloop
```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
```

### 连接池（aiohttp）
```python
import aiohttp

connector = aiohttp.TCPConnector(
    limit=100,           # 总连接数
    limit_per_host=10    # 每个主机连接数
)

async with aiohttp.ClientSession(connector=connector) as session:
    async with session.get(url) as response:
        data = await response.text()
```

---

## 测试

### pytest-asyncio
```python
import pytest

@pytest.mark.asyncio
async def test_my_coroutine():
    result = await my_coroutine()
    assert result == "expected"
```

### Mock 异步函数
```python
from unittest.mock import AsyncMock

mock_func = AsyncMock(return_value="mock result")
result = await mock_func()
assert result == "mock result"
```

---

## 常见错误

### ❌ 错误示例

```python
# 1. 忘记 await
result = my_coroutine()  # 返回协程对象，不是结果

# 2. 使用阻塞调用
time.sleep(1)  # 阻塞事件循环

# 3. 在循环中 await
for item in items:
    result = await process(item)  # 顺序执行，失去并发

# 4. 不处理取消
try:
    await asyncio.sleep(10)
except asyncio.CancelledError:
    pass  # 没有重新抛出
```

### ✅ 正确示例

```python
# 1. 使用 await
result = await my_coroutine()

# 2. 使用异步版本
await asyncio.sleep(1)

# 3. 并发执行
results = await asyncio.gather(*[process(item) for item in items])

# 4. 重新抛出取消
try:
    await asyncio.sleep(10)
except asyncio.CancelledError:
    # 清理...
    raise
```

---

## 快速参考

| 操作 | 代码 |
|------|------|
| 运行协程 | `asyncio.run(coro())` |
| 并发执行 | `await asyncio.gather(c1(), c2())` |
| 创建任务 | `asyncio.create_task(coro())` |
| 异步休眠 | `await asyncio.sleep(1)` |
| 超时 | `await asyncio.wait_for(coro(), 5.0)` |
| 限制并发 | `async with Semaphore(5)` |
| 互斥锁 | `async with Lock()` |
| 队列 | `await queue.put(item)` / `await queue.get()` |
| 取消任务 | `task.cancel()` |
| 获取事件循环 | `asyncio.get_running_loop()` |
| 运行阻塞代码 | `loop.run_in_executor(None, func)` |

---

## 最佳实践检查清单

- [ ] 使用 `asyncio.run()` 作为入口
- [ ] 所有 I/O 操作使用异步版本
- [ ] 使用 `create_task()` 实现并发
- [ ] 设置超时
- [ ] 使用 Semaphore 限制并发
- [ ] 正确处理 `CancelledError`
- [ ] 使用异步上下文管理器
- [ ] 添加日志
- [ ] 编写测试
- [ ] 实现优雅关闭

---

**更多详细内容请参考完整教程！**

[返回主页](./README.md)

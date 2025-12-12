# Python Asyncio 深度教程

## 目录
- [1. Asyncio 基础原理](#1-asyncio-基础原理)
- [2. 事件循环 (Event Loop)](#2-事件循环-event-loop)
- [3. 协程 (Coroutines)](#3-协程-coroutines)
- [4. Task 和 Future](#4-task-和-future)
- [5. 并发控制](#5-并发控制)
- [6. 异步上下文管理器和迭代器](#6-异步上下文管理器和迭代器)
- [7. 底层 API](#7-底层-api)

---

## 1. Asyncio 基础原理

### 1.1 什么是 Asyncio？

Asyncio 是 Python 的异步 I/O 框架，用于编写单线程并发代码。它使用事件循环来管理异步操作。

**核心概念：**
- **协程 (Coroutine)**: 使用 `async def` 定义的函数
- **事件循环 (Event Loop)**: 管理和调度协程执行的核心组件
- **任务 (Task)**: 封装协程的对象，用于并发执行
- **Future**: 表示异步操作的最终结果

### 1.2 同步 vs 异步

```python
# 同步代码 - 阻塞式
import time

def sync_task():
    time.sleep(1)  # 阻塞整个线程
    return "完成"

# 执行需要 3 秒
for i in range(3):
    result = sync_task()
    print(result)
```

```python
# 异步代码 - 非阻塞式
import asyncio

async def async_task():
    await asyncio.sleep(1)  # 释放控制权，允许其他任务运行
    return "完成"

# 执行只需要约 1 秒
async def main():
    tasks = [async_task() for _ in range(3)]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

### 1.3 工作原理

```
┌─────────────────────────────────────────┐
│           事件循环 (Event Loop)          │
├─────────────────────────────────────────┤
│  1. 检查就绪的任务                       │
│  2. 执行就绪任务直到遇到 await           │
│  3. 切换到另一个就绪任务                 │
│  4. 处理 I/O 事件和回调                  │
│  5. 重复循环                             │
└─────────────────────────────────────────┘
```

---

## 2. 事件循环 (Event Loop)

### 2.1 事件循环的生命周期

```python
import asyncio

# 方式 1: 使用 asyncio.run() (推荐 Python 3.7+)
async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(main())  # 自动创建、运行和关闭事件循环

# 方式 2: 手动管理事件循环 (低级 API)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.close()
```

### 2.2 获取和使用事件循环

```python
import asyncio

async def get_loop_info():
    # 获取当前运行的事件循环
    loop = asyncio.get_running_loop()
    
    print(f"事件循环: {loop}")
    print(f"是否正在运行: {loop.is_running()}")
    
    # 在事件循环中调度回调
    loop.call_soon(lambda: print("立即调度"))
    loop.call_later(2, lambda: print("2秒后调度"))
    
    await asyncio.sleep(3)

asyncio.run(get_loop_info())
```

### 2.3 事件循环的底层机制

事件循环基于以下技术：
- **Linux**: `epoll`
- **macOS**: `kqueue`
- **Windows**: `IOCP` (I/O Completion Ports)

这些都是操作系统提供的高效 I/O 多路复用机制。

---

## 3. 协程 (Coroutines)

### 3.1 定义和调用协程

```python
import asyncio

# 定义协程函数
async def fetch_data(id: int):
    print(f"开始获取数据 {id}")
    await asyncio.sleep(1)  # 模拟 I/O 操作
    print(f"完成获取数据 {id}")
    return f"数据 {id}"

async def main():
    # 方式 1: 直接 await
    result = await fetch_data(1)
    print(result)
    
    # 方式 2: 创建任务并发执行
    task1 = asyncio.create_task(fetch_data(2))
    task2 = asyncio.create_task(fetch_data(3))
    
    results = await asyncio.gather(task1, task2)
    print(results)

asyncio.run(main())
```

### 3.2 协程的状态

```python
import asyncio
import inspect

async def sample_coroutine():
    await asyncio.sleep(1)
    return "完成"

# 创建协程对象（未执行）
coro = sample_coroutine()
print(f"是协程对象: {inspect.iscoroutine(coro)}")  # True
print(f"协程状态: {inspect.getcoroutinestate(coro)}")  # CORO_CREATED

# 必须清理未执行的协程
coro.close()
```

### 3.3 协程链式调用

```python
import asyncio

async def step1():
    print("执行步骤 1")
    await asyncio.sleep(1)
    return "结果1"

async def step2(input_data):
    print(f"执行步骤 2，输入: {input_data}")
    await asyncio.sleep(1)
    return f"{input_data} -> 结果2"

async def step3(input_data):
    print(f"执行步骤 3，输入: {input_data}")
    await asyncio.sleep(1)
    return f"{input_data} -> 结果3"

async def pipeline():
    result1 = await step1()
    result2 = await step2(result1)
    result3 = await step3(result2)
    return result3

async def main():
    final_result = await pipeline()
    print(f"最终结果: {final_result}")

asyncio.run(main())
```

---

## 4. Task 和 Future

### 4.1 理解 Task

Task 是 Future 的子类，用于封装和管理协程的执行。

```python
import asyncio

async def compute(x, y):
    print(f"计算 {x} + {y}")
    await asyncio.sleep(1)
    return x + y

async def main():
    # 创建任务
    task = asyncio.create_task(compute(2, 3))
    
    # 任务属性
    print(f"任务名称: {task.get_name()}")
    print(f"任务完成: {task.done()}")
    
    # 等待任务完成
    result = await task
    print(f"结果: {result}")
    print(f"任务完成: {task.done()}")

asyncio.run(main())
```

### 4.2 任务管理

```python
import asyncio

async def worker(name, delay):
    print(f"Worker {name} 开始")
    await asyncio.sleep(delay)
    print(f"Worker {name} 完成")
    return f"结果 {name}"

async def main():
    # 创建多个任务
    tasks = [
        asyncio.create_task(worker("A", 2), name="task-A"),
        asyncio.create_task(worker("B", 1), name="task-B"),
        asyncio.create_task(worker("C", 3), name="task-C"),
    ]
    
    # 等待所有任务完成
    results = await asyncio.gather(*tasks)
    print(f"所有结果: {results}")
    
    # 获取所有任务
    all_tasks = asyncio.all_tasks()
    print(f"当前任务数: {len(all_tasks)}")

asyncio.run(main())
```

### 4.3 取消任务

```python
import asyncio

async def cancellable_task():
    try:
        print("任务开始")
        await asyncio.sleep(10)
        print("任务完成")
    except asyncio.CancelledError:
        print("任务被取消")
        # 可以进行清理工作
        raise  # 重新抛出以确保任务被标记为取消

async def main():
    task = asyncio.create_task(cancellable_task())
    
    # 等待 1 秒后取消任务
    await asyncio.sleep(1)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("捕获到取消异常")

asyncio.run(main())
```

### 4.4 Future 对象

```python
import asyncio

async def set_future_result(future, value, delay):
    await asyncio.sleep(delay)
    future.set_result(value)

async def main():
    # 创建 Future 对象
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    
    # 设置回调
    future.add_done_callback(lambda f: print(f"Future 完成: {f.result()}"))
    
    # 异步设置结果
    asyncio.create_task(set_future_result(future, "完成!", 2))
    
    # 等待 Future 完成
    result = await future
    print(f"最终结果: {result}")

asyncio.run(main())
```

---

## 5. 并发控制

### 5.1 使用 Semaphore 限制并发

```python
import asyncio

async def limited_task(semaphore, task_id):
    async with semaphore:  # 获取信号量
        print(f"任务 {task_id} 开始执行")
        await asyncio.sleep(2)
        print(f"任务 {task_id} 完成")
        return task_id

async def main():
    # 限制同时只有 3 个任务运行
    semaphore = asyncio.Semaphore(3)
    
    # 创建 10 个任务
    tasks = [limited_task(semaphore, i) for i in range(10)]
    
    results = await asyncio.gather(*tasks)
    print(f"所有结果: {results}")

asyncio.run(main())
```

### 5.2 使用 Lock 确保互斥访问

```python
import asyncio

class SharedResource:
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()
    
    async def increment(self):
        async with self.lock:  # 确保同时只有一个协程访问
            current = self.value
            await asyncio.sleep(0.1)  # 模拟处理时间
            self.value = current + 1

async def worker(resource, worker_id):
    for _ in range(5):
        await resource.increment()
        print(f"Worker {worker_id}: value = {resource.value}")

async def main():
    resource = SharedResource()
    
    # 创建多个 worker
    workers = [worker(resource, i) for i in range(3)]
    await asyncio.gather(*workers)
    
    print(f"最终值: {resource.value}")  # 应该是 15

asyncio.run(main())
```

### 5.3 使用 Event 进行协调

```python
import asyncio

async def waiter(event, name):
    print(f"{name} 等待事件")
    await event.wait()  # 阻塞直到事件被设置
    print(f"{name} 接收到事件")

async def setter(event):
    await asyncio.sleep(2)
    print("触发事件")
    event.set()  # 唤醒所有等待的协程

async def main():
    event = asyncio.Event()
    
    # 创建多个等待者
    waiters = [waiter(event, f"Waiter-{i}") for i in range(3)]
    
    # 创建事件触发器
    setter_task = setter(event)
    
    # 并发执行
    await asyncio.gather(*waiters, setter_task)

asyncio.run(main())
```

### 5.4 使用 Queue 进行任务分发

```python
import asyncio
import random

async def producer(queue, producer_id):
    for i in range(5):
        item = f"Item-{producer_id}-{i}"
        await queue.put(item)
        print(f"生产者 {producer_id} 生产: {item}")
        await asyncio.sleep(random.uniform(0.1, 0.5))

async def consumer(queue, consumer_id):
    while True:
        try:
            # 设置超时避免无限等待
            item = await asyncio.wait_for(queue.get(), timeout=3.0)
            print(f"消费者 {consumer_id} 消费: {item}")
            await asyncio.sleep(random.uniform(0.1, 0.5))
            queue.task_done()
        except asyncio.TimeoutError:
            print(f"消费者 {consumer_id} 超时退出")
            break

async def main():
    queue = asyncio.Queue(maxsize=10)
    
    # 创建生产者和消费者
    producers = [asyncio.create_task(producer(queue, i)) for i in range(2)]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(3)]
    
    # 等待生产者完成
    await asyncio.gather(*producers)
    
    # 等待队列清空
    await queue.join()
    
    # 取消消费者
    for c in consumers:
        c.cancel()

asyncio.run(main())
```

---

## 6. 异步上下文管理器和迭代器

### 6.1 异步上下文管理器

```python
import asyncio

class AsyncResource:
    def __init__(self, name):
        self.name = name
    
    async def __aenter__(self):
        print(f"获取资源: {self.name}")
        await asyncio.sleep(0.5)  # 模拟异步初始化
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"释放资源: {self.name}")
        await asyncio.sleep(0.5)  # 模拟异步清理
        return False

async def main():
    async with AsyncResource("数据库连接") as resource:
        print(f"使用资源: {resource.name}")
        await asyncio.sleep(1)

asyncio.run(main())
```

### 6.2 实用的异步上下文管理器

```python
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_timer(name):
    """测量异步代码执行时间"""
    start = asyncio.get_event_loop().time()
    print(f"{name} 开始")
    try:
        yield
    finally:
        end = asyncio.get_event_loop().time()
        print(f"{name} 耗时: {end - start:.2f} 秒")

async def main():
    async with async_timer("任务1"):
        await asyncio.sleep(1)
    
    async with async_timer("任务2"):
        await asyncio.sleep(2)

asyncio.run(main())
```

### 6.3 异步迭代器

```python
import asyncio

class AsyncRange:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.end:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.5)  # 模拟异步操作
        value = self.current
        self.current += 1
        return value

async def main():
    async for i in AsyncRange(0, 5):
        print(f"接收到: {i}")

asyncio.run(main())
```

### 6.4 异步生成器

```python
import asyncio

async def async_generator(n):
    """异步生成器"""
    for i in range(n):
        await asyncio.sleep(0.5)
        yield i

async def main():
    # 使用异步生成器
    async for value in async_generator(5):
        print(f"生成值: {value}")
    
    # 异步生成器推导式
    gen = (x async for x in async_generator(3))
    async for value in gen:
        print(f"推导式值: {value}")

asyncio.run(main())
```

---

## 7. 底层 API

### 7.1 Transports 和 Protocols

```python
import asyncio

class EchoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print("连接建立")
    
    def data_received(self, data):
        message = data.decode()
        print(f"接收数据: {message}")
        
        # 回显数据
        self.transport.write(data)
    
    def connection_lost(self, exc):
        print("连接关闭")

async def main():
    loop = asyncio.get_running_loop()
    
    # 创建服务器
    server = await loop.create_server(
        EchoProtocol,
        '127.0.0.1',
        8888
    )
    
    async with server:
        await server.serve_forever()

# asyncio.run(main())  # 运行服务器
```

### 7.2 使用 loop.run_in_executor 运行阻塞代码

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def blocking_io():
    """模拟阻塞 I/O 操作"""
    print("开始阻塞操作")
    time.sleep(2)  # 阻塞调用
    print("阻塞操作完成")
    return "结果"

async def main():
    loop = asyncio.get_running_loop()
    
    # 在线程池中运行阻塞代码
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)
        print(f"获得结果: {result}")
    
    # 使用默认执行器
    result2 = await loop.run_in_executor(None, blocking_io)
    print(f"获得结果2: {result2}")

asyncio.run(main())
```

### 7.3 底层回调 API

```python
import asyncio

def callback(future):
    print(f"回调执行，结果: {future.result()}")

async def set_result(future):
    await asyncio.sleep(1)
    future.set_result("完成!")

async def main():
    loop = asyncio.get_running_loop()
    
    # 创建 Future
    future = loop.create_future()
    
    # 添加回调
    future.add_done_callback(callback)
    
    # 使用 call_soon, call_later
    loop.call_soon(lambda: print("立即执行"))
    loop.call_later(1, lambda: print("1秒后执行"))
    
    # 设置 future 结果
    await set_result(future)
    await future

asyncio.run(main())
```

---

## 8. 性能优化技巧

### 8.1 避免常见陷阱

```python
import asyncio

# ❌ 错误：顺序执行（失去并发优势）
async def bad_example():
    result1 = await fetch_data(1)  # 等待
    result2 = await fetch_data(2)  # 等待
    result3 = await fetch_data(3)  # 等待
    return [result1, result2, result3]

# ✅ 正确：并发执行
async def good_example():
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    return results

async def fetch_data(id):
    await asyncio.sleep(1)
    return f"数据 {id}"
```

### 8.2 使用 TaskGroup (Python 3.11+)

```python
import asyncio

async def task_with_error(n):
    await asyncio.sleep(1)
    if n == 3:
        raise ValueError(f"任务 {n} 失败")
    return n

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(task_with_error(1))
            task2 = tg.create_task(task_with_error(2))
            task3 = tg.create_task(task_with_error(3))
            
        # 所有任务成功完成
        print("所有任务完成")
    except* ValueError as eg:
        print(f"捕获到 {len(eg.exceptions)} 个错误")
        for exc in eg.exceptions:
            print(f"  - {exc}")

# Python 3.11+ 才支持
# asyncio.run(main())
```

### 8.3 超时控制

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(5)
    return "完成"

async def main():
    try:
        # 方式 1: wait_for
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("操作超时")
    
    # 方式 2: timeout (Python 3.11+)
    # async with asyncio.timeout(2.0):
    #     result = await slow_operation()

asyncio.run(main())
```

---

## 9. 调试技巧

### 9.1 启用调试模式

```python
import asyncio
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

async def main():
    await asyncio.sleep(1)
    print("完成")

# 启用调试模式
asyncio.run(main(), debug=True)
```

### 9.2 检测长时间运行的任务

```python
import asyncio

async def slow_task():
    await asyncio.sleep(5)

async def main():
    loop = asyncio.get_running_loop()
    
    # 设置慢回调阈值（秒）
    loop.slow_callback_duration = 0.1
    
    await slow_task()

asyncio.run(main(), debug=True)
```

### 9.3 追踪未完成的任务

```python
import asyncio

async def leaked_task():
    await asyncio.sleep(10)

async def main():
    # 创建任务但不等待
    task = asyncio.create_task(leaked_task())
    await asyncio.sleep(1)
    # 任务仍在运行但没有被等待

try:
    asyncio.run(main())
except RuntimeError as e:
    print(f"错误: {e}")
```

---

## 总结

Asyncio 是 Python 中强大的异步编程框架。关键点：

1. **理解事件循环**: 所有异步操作的核心
2. **正确使用协程**: `async/await` 语法
3. **任务管理**: 使用 `create_task()` 实现真正的并发
4. **并发控制**: Semaphore, Lock, Event, Queue
5. **异常处理**: 正确处理异步代码中的异常
6. **性能优化**: 避免顺序等待，使用 gather/TaskGroup
7. **调试**: 启用调试模式追踪问题

掌握这些概念后，你就能编写高效的异步 Python 代码！

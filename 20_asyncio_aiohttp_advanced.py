"""
Python asyncio & aiohttp 详解与实战
=====================================
深入讲解异步编程的核心概念、高级技巧和实际应用

内容概览：
Part 1: asyncio 深度解析
Part 2: aiohttp 客户端详解
Part 3: aiohttp 服务端详解
Part 4: 实战项目案例
"""

import asyncio
import aiohttp
import time
import json
import sys
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from contextlib import asynccontextmanager


# ============================================================
# Part 1: asyncio 深度解析
# ============================================================

print("""
╔══════════════════════════════════════════════════════════════╗
║                 Part 1: asyncio 深度解析                      ║
╚══════════════════════════════════════════════════════════════╝
""")


# ------------------------------------------------------------
# 1.1 事件循环 (Event Loop) 详解
# ------------------------------------------------------------

async def event_loop_demo():
    """事件循环详解"""
    print("\n=== 1.1 事件循环 (Event Loop) ===")
    
    # 获取当前事件循环
    loop = asyncio.get_running_loop()
    print(f"  当前事件循环: {type(loop).__name__}")
    print(f"  是否运行中: {loop.is_running()}")
    print(f"  是否关闭: {loop.is_closed()}")
    
    # 事件循环的时间
    print(f"\n  事件循环时间: {loop.time():.6f} 秒")
    
    # 调度回调
    print("\n  调度回调函数:")
    
    def sync_callback(msg):
        print(f"    同步回调: {msg}")
    
    # call_soon - 尽快执行
    loop.call_soon(sync_callback, "call_soon 执行")
    
    # call_later - 延迟执行
    loop.call_later(0.1, sync_callback, "call_later 0.1秒后执行")
    
    # call_at - 在指定时间执行
    loop.call_at(loop.time() + 0.2, sync_callback, "call_at 0.2秒后执行")
    
    await asyncio.sleep(0.3)
    
    print("""
    事件循环核心概念:
    ┌─────────────────────────────────────────────────────┐
    │  Event Loop (事件循环)                               │
    │  ├── 管理所有异步任务的调度和执行                     │
    │  ├── 处理 I/O 事件 (网络、文件等)                    │
    │  ├── 调度回调函数                                    │
    │  └── 处理信号和子进程                                │
    │                                                      │
    │  运行方式:                                           │
    │  • asyncio.run(main())    - 推荐，自动管理循环       │
    │  • loop.run_forever()     - 手动控制                 │
    │  • loop.run_until_complete() - 运行直到完成          │
    └─────────────────────────────────────────────────────┘
    """)


# ------------------------------------------------------------
# 1.2 任务 (Task) 与协程 (Coroutine) 深入
# ------------------------------------------------------------

async def task_coroutine_deep():
    """任务与协程深入理解"""
    print("\n=== 1.2 任务与协程深入 ===")
    
    # 协程对象
    async def my_coroutine(x):
        await asyncio.sleep(0.1)
        return x * 2
    
    # 1. 协程对象 vs Task
    print("1. 协程 vs Task:")
    
    coro = my_coroutine(5)  # 创建协程对象（不会执行）
    print(f"  协程对象: {coro}")
    print(f"  类型: {type(coro)}")
    
    task = asyncio.create_task(my_coroutine(10))  # 创建Task（立即调度）
    print(f"  Task对象: {task}")
    print(f"  Task名称: {task.get_name()}")
    
    # 等待协程和任务
    result1 = await coro
    result2 = await task
    print(f"  协程结果: {result1}, Task结果: {result2}")
    
    # 2. Task 状态管理
    print("\n2. Task 状态:")
    
    async def long_task():
        await asyncio.sleep(1)
        return "完成"
    
    task = asyncio.create_task(long_task(), name="LongTask")
    print(f"  创建后 - done(): {task.done()}, cancelled(): {task.cancelled()}")
    
    await asyncio.sleep(0.1)
    print(f"  运行中 - done(): {task.done()}, cancelled(): {task.cancelled()}")
    
    task.cancel()  # 取消任务
    try:
        await task
    except asyncio.CancelledError:
        print(f"  取消后 - done(): {task.done()}, cancelled(): {task.cancelled()}")
    
    # 3. Task 回调
    print("\n3. Task 回调:")
    
    def task_done_callback(task):
        if task.cancelled():
            print(f"    任务 {task.get_name()} 被取消")
        elif task.exception():
            print(f"    任务 {task.get_name()} 异常: {task.exception()}")
        else:
            print(f"    任务 {task.get_name()} 完成: {task.result()}")
    
    task = asyncio.create_task(my_coroutine(100), name="CallbackDemo")
    task.add_done_callback(task_done_callback)
    await task
    
    # 4. 获取当前任务
    print("\n4. 当前任务:")
    current = asyncio.current_task()
    print(f"  当前任务: {current.get_name()}")
    
    all_tasks = asyncio.all_tasks()
    print(f"  所有任务数: {len(all_tasks)}")


# ------------------------------------------------------------
# 1.3 TaskGroup (Python 3.11+) 结构化并发
# ------------------------------------------------------------

async def task_group_demo():
    """TaskGroup 结构化并发"""
    print("\n=== 1.3 TaskGroup 结构化并发 ===")
    
    async def worker(name, delay):
        print(f"    {name} 开始")
        await asyncio.sleep(delay)
        print(f"    {name} 完成")
        return f"{name}-result"
    
    # Python 3.11+ TaskGroup
    print("1. TaskGroup 基本用法:")
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(worker("Worker-A", 0.2))
            task2 = tg.create_task(worker("Worker-B", 0.1))
            task3 = tg.create_task(worker("Worker-C", 0.3))
        
        # 所有任务完成后才会继续
        print(f"  结果: {task1.result()}, {task2.result()}, {task3.result()}")
    except Exception as e:
        print(f"  TaskGroup 异常: {e}")
    
    # TaskGroup 异常处理
    print("\n2. TaskGroup 异常处理:")
    
    async def failing_worker(name):
        await asyncio.sleep(0.1)
        raise ValueError(f"{name} 失败了!")
    
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(worker("Good-1", 0.2))
            tg.create_task(failing_worker("Bad"))
            tg.create_task(worker("Good-2", 0.3))
    except* ValueError as eg:
        print(f"  捕获异常组: {eg.exceptions}")
    
    print("""
    TaskGroup vs gather:
    ┌────────────────────┬─────────────────────────────────┐
    │     TaskGroup      │            gather               │
    ├────────────────────┼─────────────────────────────────┤
    │ 结构化并发          │ 非结构化并发                     │
    │ 一个失败全部取消    │ return_exceptions=True 可继续   │
    │ 更清晰的异常处理    │ 异常可能被吞掉                   │
    │ Python 3.11+       │ Python 3.4+                     │
    │ 推荐用于生产环境    │ 简单场景依然适用                 │
    └────────────────────┴─────────────────────────────────┘
    """)


# ------------------------------------------------------------
# 1.4 同步原语 (Synchronization Primitives)
# ------------------------------------------------------------

async def sync_primitives_demo():
    """同步原语详解"""
    print("\n=== 1.4 同步原语 ===")
    
    # 1. Lock - 互斥锁
    print("1. Lock (互斥锁):")
    lock = asyncio.Lock()
    shared_resource = []
    
    async def critical_section(name, lock):
        async with lock:
            print(f"    {name} 进入临界区")
            shared_resource.append(name)
            await asyncio.sleep(0.1)
            print(f"    {name} 离开临界区")
    
    await asyncio.gather(
        critical_section("A", lock),
        critical_section("B", lock),
        critical_section("C", lock)
    )
    print(f"  执行顺序: {shared_resource}")
    
    # 2. Semaphore - 信号量（限流器）
    print("\n2. Semaphore (信号量/限流器):")
    semaphore = asyncio.Semaphore(2)  # 最多2个并发
    
    async def limited_task(name, sem):
        async with sem:
            print(f"    {name} 开始 (并发数: {2 - sem._value})")
            await asyncio.sleep(0.2)
            print(f"    {name} 结束")
    
    await asyncio.gather(*[
        limited_task(f"Task-{i}", semaphore) 
        for i in range(5)
    ])
    
    # 3. BoundedSemaphore - 有界信号量
    print("\n3. BoundedSemaphore (有界信号量):")
    bounded_sem = asyncio.BoundedSemaphore(2)
    print(f"  初始值: 2")
    try:
        bounded_sem.release()  # 超出初始值会报错
    except ValueError as e:
        print(f"  release() 超出边界: ValueError")
    
    # 4. Event - 事件
    print("\n4. Event (事件):")
    event = asyncio.Event()
    
    async def waiter(name, event):
        print(f"    {name} 等待事件...")
        await event.wait()
        print(f"    {name} 收到事件!")
    
    async def setter(event):
        await asyncio.sleep(0.2)
        print("    触发事件!")
        event.set()
    
    await asyncio.gather(
        waiter("W1", event),
        waiter("W2", event),
        setter(event)
    )
    
    # 5. Condition - 条件变量
    print("\n5. Condition (条件变量):")
    condition = asyncio.Condition()
    queue = []
    
    async def producer(cond):
        async with cond:
            queue.append("item")
            print(f"    生产者: 添加item, 通知消费者")
            cond.notify()
    
    async def consumer(cond):
        async with cond:
            await cond.wait_for(lambda: len(queue) > 0)
            item = queue.pop()
            print(f"    消费者: 消费 {item}")
    
    await asyncio.gather(consumer(condition), producer(condition))
    
    # 6. Barrier - 屏障 (Python 3.11+)
    print("\n6. Barrier (屏障):")
    barrier = asyncio.Barrier(3)
    
    async def barrier_task(name, barrier):
        print(f"    {name} 到达屏障")
        await barrier.wait()
        print(f"    {name} 通过屏障!")
    
    await asyncio.gather(
        barrier_task("T1", barrier),
        barrier_task("T2", barrier),
        barrier_task("T3", barrier)
    )


# ------------------------------------------------------------
# 1.5 超时与取消
# ------------------------------------------------------------

async def timeout_cancellation_demo():
    """超时与取消机制"""
    print("\n=== 1.5 超时与取消 ===")
    
    async def slow_operation(name, duration):
        try:
            print(f"    {name} 开始 (需要 {duration}秒)")
            await asyncio.sleep(duration)
            print(f"    {name} 完成")
            return f"{name} 结果"
        except asyncio.CancelledError:
            print(f"    {name} 被取消!")
            raise  # 重要：要重新抛出
    
    # 1. wait_for - 超时
    print("1. wait_for (超时):")
    try:
        result = await asyncio.wait_for(
            slow_operation("SlowTask", 3),
            timeout=0.5
        )
        print(f"  结果: {result}")
    except asyncio.TimeoutError:
        print("  超时!")
    
    # 2. timeout (Python 3.11+) - 上下文管理器
    print("\n2. timeout 上下文管理器:")
    try:
        async with asyncio.timeout(0.5):
            await slow_operation("ContextTask", 3)
    except asyncio.TimeoutError:
        print("  超时!")
    
    # 3. timeout_at - 绝对时间超时
    print("\n3. timeout_at (绝对时间):")
    loop = asyncio.get_running_loop()
    deadline = loop.time() + 0.5
    try:
        async with asyncio.timeout_at(deadline):
            await slow_operation("DeadlineTask", 3)
    except asyncio.TimeoutError:
        print("  超时!")
    
    # 4. 手动取消
    print("\n4. 手动取消任务:")
    task = asyncio.create_task(slow_operation("ManualCancel", 5))
    
    await asyncio.sleep(0.2)
    task.cancel("用户请求取消")  # 可以传递取消消息
    
    try:
        await task
    except asyncio.CancelledError as e:
        print(f"  任务被取消: {e}")
    
    # 5. shield - 保护任务不被取消
    print("\n5. shield (保护任务):")
    
    async def important_operation():
        print("    重要操作开始")
        await asyncio.sleep(0.3)
        print("    重要操作完成")
        return "重要结果"
    
    async def try_cancel():
        await asyncio.sleep(0.1)
        return "trigger"
    
    task = asyncio.create_task(important_operation())
    shielded = asyncio.shield(task)
    
    try:
        # 模拟超时
        result = await asyncio.wait_for(shielded, timeout=0.1)
    except asyncio.TimeoutError:
        print("  shield 超时，但原任务继续执行")
        # 原任务仍在运行，等待它完成
        result = await task
        print(f"  原任务结果: {result}")


# ------------------------------------------------------------
# 1.6 异步队列高级用法
# ------------------------------------------------------------

async def async_queue_advanced():
    """异步队列高级用法"""
    print("\n=== 1.6 异步队列高级用法 ===")
    
    # 1. PriorityQueue - 优先级队列
    print("1. PriorityQueue (优先级队列):")
    pq = asyncio.PriorityQueue()
    
    # 添加带优先级的元素 (priority, data)
    await pq.put((3, "低优先级"))
    await pq.put((1, "高优先级"))
    await pq.put((2, "中优先级"))
    
    while not pq.empty():
        priority, item = await pq.get()
        print(f"    优先级 {priority}: {item}")
    
    # 2. LifoQueue - 后进先出队列（栈）
    print("\n2. LifoQueue (栈):")
    lifo = asyncio.LifoQueue()
    
    for i in range(3):
        await lifo.put(f"item-{i}")
    
    while not lifo.empty():
        item = await lifo.get()
        print(f"    出栈: {item}")
    
    # 3. 生产者-消费者模式 (带优雅关闭)
    print("\n3. 生产者-消费者模式 (带优雅关闭):")
    
    queue = asyncio.Queue(maxsize=5)
    shutdown_event = asyncio.Event()
    
    async def producer(queue, shutdown):
        for i in range(10):
            if shutdown.is_set():
                break
            await queue.put(f"item-{i}")
            print(f"    生产: item-{i} (队列大小: {queue.qsize()})")
            await asyncio.sleep(0.05)
        print("    生产者结束")
    
    async def consumer(name, queue, shutdown):
        while not shutdown.is_set() or not queue.empty():
            try:
                item = await asyncio.wait_for(queue.get(), timeout=0.2)
                print(f"    {name} 消费: {item}")
                queue.task_done()
                await asyncio.sleep(0.1)
            except asyncio.TimeoutError:
                if shutdown.is_set():
                    break
        print(f"    {name} 结束")
    
    # 启动
    producer_task = asyncio.create_task(producer(queue, shutdown_event))
    consumer_tasks = [
        asyncio.create_task(consumer(f"C{i}", queue, shutdown_event))
        for i in range(2)
    ]
    
    # 等待生产者完成
    await producer_task
    
    # 发送关闭信号
    shutdown_event.set()
    
    # 等待消费者完成
    await asyncio.gather(*consumer_tasks)


# ------------------------------------------------------------
# 1.7 在异步中运行同步代码
# ------------------------------------------------------------

async def run_sync_in_async():
    """在异步中运行同步代码"""
    print("\n=== 1.7 在异步中运行同步代码 ===")
    
    import concurrent.futures
    
    def blocking_io(seconds):
        """阻塞的 IO 操作"""
        time.sleep(seconds)
        return f"阻塞 {seconds}秒 完成"
    
    def cpu_intensive(n):
        """CPU 密集型操作"""
        total = sum(i * i for i in range(n))
        return f"计算结果: {total}"
    
    # 1. 默认线程池执行器
    print("1. 线程池执行器 (IO操作):")
    loop = asyncio.get_running_loop()
    
    start = time.time()
    results = await asyncio.gather(
        loop.run_in_executor(None, blocking_io, 0.5),
        loop.run_in_executor(None, blocking_io, 0.5),
        loop.run_in_executor(None, blocking_io, 0.5),
    )
    duration = time.time() - start
    print(f"  3个0.5秒阻塞操作并行: {duration:.2f}秒")
    
    # 2. 进程池执行器 (CPU密集型)
    print("\n2. 进程池执行器 (CPU操作):")
    print("  注意: ProcessPoolExecutor 需要在模块顶层定义函数")
    print("  示例代码:")
    print("    with ProcessPoolExecutor() as pool:")
    print("        result = await loop.run_in_executor(pool, cpu_func, arg)")
    
    # 3. to_thread (Python 3.9+) - 更简洁的方式
    print("\n3. asyncio.to_thread (Python 3.9+):")
    result = await asyncio.to_thread(blocking_io, 0.3)
    print(f"  结果: {result}")
    
    print("""
    同步代码运行指南:
    ┌─────────────────────────────────────────────────────────┐
    │  操作类型        │  推荐执行器        │  原因            │
    ├─────────────────────────────────────────────────────────┤
    │  阻塞 IO         │  ThreadPoolExecutor │  线程可并行等待  │
    │  文件读写        │  ThreadPoolExecutor │  避免阻塞事件循环 │
    │  CPU 密集型      │  ProcessPoolExecutor│  绕过 GIL        │
    │  同步库调用      │  ThreadPoolExecutor │  保持异步非阻塞  │
    └─────────────────────────────────────────────────────────┘
    """)


# ============================================================
# Part 2: aiohttp 客户端详解
# ============================================================

print("""
╔══════════════════════════════════════════════════════════════╗
║                Part 2: aiohttp 客户端详解                     ║
╚══════════════════════════════════════════════════════════════╝
""")


# ------------------------------------------------------------
# 2.1 ClientSession 详解
# ------------------------------------------------------------

async def aiohttp_client_session():
    """ClientSession 详解"""
    print("\n=== 2.1 ClientSession 详解 ===")
    
    print("""
    ClientSession 是 aiohttp 的核心:
    • 管理连接池
    • 保持 cookies
    • 共享配置
    • 自动处理连接复用
    
    重要: 应该复用 session，而不是每次请求都创建新的!
    """)
    
    # 1. 基本用法
    print("1. 基本用法:")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://httpbin.org/get') as response:
                print(f"  状态码: {response.status}")
                print(f"  Content-Type: {response.headers.get('Content-Type')}")
        except aiohttp.ClientError as e:
            print(f"  请求失败: {e}")
    
    # 2. 自定义配置
    print("\n2. 自定义 Session 配置:")
    
    # 超时配置
    timeout = aiohttp.ClientTimeout(
        total=30,        # 总超时
        connect=10,      # 连接超时
        sock_read=10,    # 读取超时
        sock_connect=10  # socket连接超时
    )
    
    # 连接器配置
    connector = aiohttp.TCPConnector(
        limit=100,           # 总连接数限制
        limit_per_host=10,   # 每个主机连接数
        ttl_dns_cache=300,   # DNS缓存时间
        use_dns_cache=True,  # 启用DNS缓存
        keepalive_timeout=30 # keepalive超时
    )
    
    # 默认请求头
    headers = {
        'User-Agent': 'MyApp/1.0',
        'Accept': 'application/json'
    }
    
    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers=headers
    ) as session:
        try:
            async with session.get('https://httpbin.org/headers') as resp:
                data = await resp.json()
                print(f"  User-Agent: {data['headers'].get('User-Agent')}")
        except:
            print("  请求失败")
    
    # 3. Cookie 管理
    print("\n3. Cookie 管理:")
    jar = aiohttp.CookieJar(unsafe=True)  # unsafe允许IP地址的cookie
    
    async with aiohttp.ClientSession(cookie_jar=jar) as session:
        try:
            # 设置cookie
            await session.get('https://httpbin.org/cookies/set/mycookie/myvalue')
            # 读取cookie
            async with session.get('https://httpbin.org/cookies') as resp:
                data = await resp.json()
                print(f"  Cookies: {data.get('cookies')}")
        except:
            print("  Cookie 测试失败")


# ------------------------------------------------------------
# 2.2 HTTP 请求方法详解
# ------------------------------------------------------------

async def aiohttp_http_methods():
    """HTTP 请求方法详解"""
    print("\n=== 2.2 HTTP 请求方法详解 ===")
    
    async with aiohttp.ClientSession() as session:
        
        # 1. GET 请求
        print("1. GET 请求:")
        try:
            params = {'key1': 'value1', 'key2': 'value2'}
            async with session.get('https://httpbin.org/get', params=params) as resp:
                data = await resp.json()
                print(f"  查询参数: {data.get('args')}")
        except:
            print("  GET 请求失败")
        
        # 2. POST 表单数据
        print("\n2. POST 表单数据:")
        try:
            form_data = {'username': 'alice', 'password': 'secret'}
            async with session.post('https://httpbin.org/post', data=form_data) as resp:
                data = await resp.json()
                print(f"  表单数据: {data.get('form')}")
        except:
            print("  POST 表单失败")
        
        # 3. POST JSON 数据
        print("\n3. POST JSON 数据:")
        try:
            json_data = {'name': 'Alice', 'age': 25}
            async with session.post('https://httpbin.org/post', json=json_data) as resp:
                data = await resp.json()
                print(f"  JSON数据: {data.get('json')}")
        except:
            print("  POST JSON 失败")
        
        # 4. PUT 请求
        print("\n4. PUT 请求:")
        try:
            async with session.put('https://httpbin.org/put', json={'update': 'data'}) as resp:
                print(f"  状态码: {resp.status}")
        except:
            print("  PUT 请求失败")
        
        # 5. PATCH 请求
        print("\n5. PATCH 请求:")
        try:
            async with session.patch('https://httpbin.org/patch', json={'partial': 'update'}) as resp:
                print(f"  状态码: {resp.status}")
        except:
            print("  PATCH 请求失败")
        
        # 6. DELETE 请求
        print("\n6. DELETE 请求:")
        try:
            async with session.delete('https://httpbin.org/delete') as resp:
                print(f"  状态码: {resp.status}")
        except:
            print("  DELETE 请求失败")
        
        # 7. HEAD 请求 (只获取头部)
        print("\n7. HEAD 请求:")
        try:
            async with session.head('https://httpbin.org/get') as resp:
                print(f"  状态码: {resp.status}")
                print(f"  Content-Type: {resp.headers.get('Content-Type')}")
        except:
            print("  HEAD 请求失败")


# ------------------------------------------------------------
# 2.3 响应处理
# ------------------------------------------------------------

async def aiohttp_response_handling():
    """响应处理详解"""
    print("\n=== 2.3 响应处理 ===")
    
    async with aiohttp.ClientSession() as session:
        
        try:
            async with session.get('https://httpbin.org/get') as response:
                # 1. 响应状态
                print("1. 响应状态:")
                print(f"  状态码: {response.status}")
                print(f"  状态原因: {response.reason}")
                print(f"  OK: {response.ok}")  # 200 <= status < 400
                
                # 2. 响应头
                print("\n2. 响应头:")
                print(f"  Content-Type: {response.headers.get('Content-Type')}")
                print(f"  所有头部: {dict(list(response.headers.items())[:3])}")
                
                # 3. 响应 URL (可能重定向后不同)
                print(f"\n3. 最终URL: {response.url}")
                
                # 4. 响应内容
                print("\n4. 响应内容读取方式:")
                # 已经读取过的响应不能再次读取，这里只演示
                
        except aiohttp.ClientError:
            print("  请求失败")
        
        # 演示不同的内容读取方式
        print("\n5. 内容读取方法演示:")
        
        # text() - 文本
        try:
            async with session.get('https://httpbin.org/html') as resp:
                text = await resp.text()
                print(f"  text(): {text[:50]}...")
        except:
            print("  text() 获取失败")
        
        # json() - JSON
        try:
            async with session.get('https://httpbin.org/json') as resp:
                json_data = await resp.json()
                print(f"  json(): {type(json_data)}")
        except:
            print("  json() 获取失败")
        
        # read() - 字节
        try:
            async with session.get('https://httpbin.org/bytes/100') as resp:
                bytes_data = await resp.read()
                print(f"  read(): {len(bytes_data)} bytes")
        except:
            print("  read() 获取失败")


# ------------------------------------------------------------
# 2.4 流式处理
# ------------------------------------------------------------

async def aiohttp_streaming():
    """流式处理"""
    print("\n=== 2.4 流式处理 ===")
    
    async with aiohttp.ClientSession() as session:
        
        # 1. 流式读取响应
        print("1. 流式读取响应:")
        try:
            async with session.get('https://httpbin.org/bytes/1024') as resp:
                total_bytes = 0
                async for chunk in resp.content.iter_chunked(256):
                    total_bytes += len(chunk)
                    print(f"    接收到 {len(chunk)} 字节")
                print(f"  总计: {total_bytes} 字节")
        except:
            print("  流式读取失败")
        
        # 2. 逐行读取
        print("\n2. 逐行读取:")
        try:
            async with session.get('https://httpbin.org/robots.txt') as resp:
                line_count = 0
                async for line in resp.content:
                    line_count += 1
                    if line_count <= 3:
                        print(f"    行 {line_count}: {line.decode().strip()}")
                print(f"  总行数: {line_count}")
        except:
            print("  逐行读取失败")
        
        # 3. 流式上传
        print("\n3. 流式上传:")
        
        async def file_sender():
            """异步生成器模拟文件内容"""
            for i in range(5):
                yield f"chunk-{i}\n".encode()
                await asyncio.sleep(0.1)
        
        try:
            async with session.post(
                'https://httpbin.org/post',
                data=file_sender()
            ) as resp:
                data = await resp.json()
                print(f"  上传成功，接收数据长度: {len(data.get('data', ''))}")
        except:
            print("  流式上传失败")


# ------------------------------------------------------------
# 2.5 文件上传与下载
# ------------------------------------------------------------

async def aiohttp_file_operations():
    """文件上传与下载"""
    print("\n=== 2.5 文件上传与下载 ===")
    
    async with aiohttp.ClientSession() as session:
        
        # 1. 简单文件上传
        print("1. 简单文件上传:")
        try:
            # 使用 FormData
            data = aiohttp.FormData()
            data.add_field('file',
                          b'Hello, this is file content!',
                          filename='test.txt',
                          content_type='text/plain')
            
            async with session.post('https://httpbin.org/post', data=data) as resp:
                result = await resp.json()
                print(f"  上传的文件: {list(result.get('files', {}).keys())}")
        except:
            print("  文件上传失败")
        
        # 2. 多文件上传
        print("\n2. 多文件上传:")
        try:
            data = aiohttp.FormData()
            data.add_field('file1', b'Content 1', filename='file1.txt')
            data.add_field('file2', b'Content 2', filename='file2.txt')
            
            async with session.post('https://httpbin.org/post', data=data) as resp:
                result = await resp.json()
                print(f"  上传的文件: {list(result.get('files', {}).keys())}")
        except:
            print("  多文件上传失败")
        
        # 3. 下载文件
        print("\n3. 下载文件:")
        try:
            async with session.get('https://httpbin.org/bytes/2048') as resp:
                # 流式下载到文件
                total = 0
                import aiofiles
            
                async with aiofiles.open('/tmp/download_test.bin', 'wb') as f:
                    async for chunk in resp.content.iter_chunked(512):
                        await f.write(chunk)
                        total += len(chunk)
                
                print(f"  下载完成: {total} 字节")
        except ImportError:
            # 没有 aiofiles，使用普通方式
            async with session.get('https://httpbin.org/bytes/2048') as resp:
                content = await resp.read()
                with open('/tmp/download_test.bin', 'wb') as f:
                    f.write(content)
                print(f"  下载完成: {len(content)} 字节 (同步写入)")
        except:
            print("  下载失败")


# ------------------------------------------------------------
# 2.6 错误处理与重试
# ------------------------------------------------------------

async def aiohttp_error_handling():
    """错误处理与重试"""
    print("\n=== 2.6 错误处理与重试 ===")
    
    # 1. 异常类型
    print("1. aiohttp 异常类型:")
    print("""
    aiohttp.ClientError          - 所有客户端异常的基类
    ├── aiohttp.ClientConnectionError  - 连接错误
    │   ├── aiohttp.ClientOSError      - 系统错误
    │   └── aiohttp.ServerDisconnectedError - 服务器断开
    ├── aiohttp.ClientResponseError    - HTTP响应错误
    ├── aiohttp.ClientPayloadError     - 响应体错误
    └── aiohttp.InvalidURL             - URL无效
    
    asyncio.TimeoutError         - 超时错误
    """)
    
    # 2. 完整的错误处理
    print("2. 完整的错误处理示例:")
    
    async def safe_request(session, url):
        """安全的请求函数"""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                resp.raise_for_status()  # 抛出HTTP错误
                return await resp.json()
        except aiohttp.ClientResponseError as e:
            print(f"    HTTP错误: {e.status} - {e.message}")
        except aiohttp.ClientConnectionError:
            print(f"    连接错误")
        except asyncio.TimeoutError:
            print(f"    请求超时")
        except aiohttp.ClientError as e:
            print(f"    客户端错误: {e}")
        return None
    
    async with aiohttp.ClientSession() as session:
        # 测试各种错误
        print("  测试 404 错误:")
        await safe_request(session, 'https://httpbin.org/status/404')
        
        print("  测试连接错误:")
        await safe_request(session, 'http://invalid-domain-12345.com')
    
    # 3. 重试机制
    print("\n3. 重试机制:")
    
    async def request_with_retry(
        session: aiohttp.ClientSession,
        url: str,
        max_retries: int = 3,
        backoff_factor: float = 0.5
    ):
        """带重试的请求"""
        for attempt in range(max_retries):
            try:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = backoff_factor * (2 ** attempt)
                print(f"    尝试 {attempt + 1} 失败，{wait_time}秒后重试...")
                await asyncio.sleep(wait_time)
        return None
    
    async with aiohttp.ClientSession() as session:
        try:
            # 这个会失败并重试
            result = await request_with_retry(
                session, 
                'https://httpbin.org/status/500',
                max_retries=2
            )
        except aiohttp.ClientResponseError:
            print("    所有重试均失败")


# ------------------------------------------------------------
# 2.7 并发请求控制
# ------------------------------------------------------------

async def aiohttp_concurrency_control():
    """并发请求控制"""
    print("\n=== 2.7 并发请求控制 ===")
    
    urls = [f'https://httpbin.org/delay/0.5' for _ in range(10)]
    
    # 1. 无限制并发
    print("1. 无限制并发 (不推荐):")
    
    async def fetch(session, url):
        async with session.get(url) as resp:
            return resp.status
    
    async with aiohttp.ClientSession() as session:
        start = time.time()
        try:
            # 限时执行，避免太慢
            tasks = [fetch(session, url) for url in urls[:3]]
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=5
            )
            print(f"  3个请求耗时: {time.time() - start:.2f}秒")
        except asyncio.TimeoutError:
            print("  请求超时")
        except:
            print("  请求失败")
    
    # 2. 使用 Semaphore 限制并发
    print("\n2. 使用 Semaphore 限制并发:")
    
    async def fetch_with_semaphore(session, url, semaphore):
        async with semaphore:
            async with session.get(url) as resp:
                return resp.status
    
    semaphore = asyncio.Semaphore(2)  # 最多2个并发
    
    async with aiohttp.ClientSession() as session:
        start = time.time()
        try:
            tasks = [fetch_with_semaphore(session, url, semaphore) for url in urls[:4]]
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=10
            )
            print(f"  4个请求 (并发2) 耗时: {time.time() - start:.2f}秒")
        except asyncio.TimeoutError:
            print("  请求超时")
        except:
            print("  请求失败")
    
    # 3. 使用 Connector 限制
    print("\n3. 使用 Connector 限制连接数:")
    
    connector = aiohttp.TCPConnector(
        limit=5,          # 总连接数
        limit_per_host=2  # 每个主机连接数
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        print(f"  Connector 总连接限制: {connector.limit}")
        print(f"  每主机连接限制: {connector.limit_per_host}")
    
    # 4. 批量请求处理
    print("\n4. 批量请求处理 (分批执行):")
    
    async def fetch_batch(session, urls, batch_size=3):
        """分批获取"""
        results = []
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            batch_results = await asyncio.gather(
                *[fetch(session, url) for url in batch],
                return_exceptions=True
            )
            results.extend(batch_results)
            print(f"    批次 {i//batch_size + 1} 完成")
        return results
    
    async with aiohttp.ClientSession() as session:
        try:
            results = await asyncio.wait_for(
                fetch_batch(session, urls[:6], batch_size=2),
                timeout=15
            )
            print(f"  总计完成: {len(results)} 个请求")
        except asyncio.TimeoutError:
            print("  批量请求超时")
        except:
            print("  批量请求失败")


# ============================================================
# Part 3: aiohttp 服务端详解
# ============================================================

print("""
╔══════════════════════════════════════════════════════════════╗
║                Part 3: aiohttp 服务端详解                     ║
╚══════════════════════════════════════════════════════════════╝
""")


# ------------------------------------------------------------
# 3.1 基础服务器
# ------------------------------------------------------------

def aiohttp_server_basics():
    """基础服务器示例代码"""
    print("\n=== 3.1 基础服务器 ===")
    
    code = '''
from aiohttp import web
import json

# 路由处理函数
async def hello(request):
    """简单的 GET 处理"""
    name = request.match_info.get('name', 'World')
    return web.Response(text=f"Hello, {name}!")

async def get_json(request):
    """返回 JSON"""
    data = {"message": "Hello", "status": "ok"}
    return web.json_response(data)

async def post_handler(request):
    """POST 请求处理"""
    data = await request.json()
    return web.json_response({"received": data})

async def form_handler(request):
    """表单处理"""
    data = await request.post()
    return web.json_response({"form": dict(data)})

async def query_params(request):
    """查询参数"""
    params = dict(request.query)
    return web.json_response({"params": params})

# 创建应用
app = web.Application()

# 添加路由
app.router.add_get('/', hello)
app.router.add_get('/hello/{name}', hello)
app.router.add_get('/json', get_json)
app.router.add_post('/post', post_handler)
app.router.add_post('/form', form_handler)
app.router.add_get('/query', query_params)

# 运行服务器
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
'''
    print(code)
    
    print("""
    启动后可以测试:
    curl http://localhost:8080/
    curl http://localhost:8080/hello/Alice
    curl http://localhost:8080/json
    curl -X POST http://localhost:8080/post -H "Content-Type: application/json" -d '{"key":"value"}'
    curl http://localhost:8080/query?name=test&age=25
    """)


# ------------------------------------------------------------
# 3.2 路由和视图
# ------------------------------------------------------------

def aiohttp_routing():
    """路由和视图"""
    print("\n=== 3.2 路由和视图 ===")
    
    code = r'''
from aiohttp import web

# 1. 函数视图
async def index(request):
    return web.Response(text="Index Page")

# 2. 类视图
class UserView(web.View):
    async def get(self):
        """GET /users/{id}"""
        user_id = self.request.match_info['id']
        return web.json_response({"id": user_id, "name": "User"})
    
    async def post(self):
        """POST /users/{id}"""
        data = await self.request.json()
        return web.json_response({"created": data})
    
    async def put(self):
        """PUT /users/{id}"""
        data = await self.request.json()
        return web.json_response({"updated": data})
    
    async def delete(self):
        """DELETE /users/{id}"""
        return web.Response(status=204)

# 3. 路由分组
def setup_routes(app):
    # 基本路由
    app.router.add_get('/', index)
    
    # 类视图路由
    app.router.add_view('/users/{id}', UserView)
    
    # 路由前缀分组
    api = app.router.add_prefix('/api/v1')
    
    # 静态文件
    app.router.add_static('/static/', path='./static', name='static')

# 4. 路由参数类型
# {name} - 任意字符串
# {id:\d+} - 数字正则
# {path:.*} - 匹配路径

app = web.Application()
app.router.add_get('/items/{id:\d+}', lambda r: web.Response(text="Item"))
app.router.add_get('/files/{path:.*}', lambda r: web.Response(text="File"))

# 5. 命名路由
app.router.add_get('/users', index, name='users_list')

# 获取命名路由的URL
# url = request.app.router['users_list'].url_for()
'''
    print(code)


# ------------------------------------------------------------
# 3.3 中间件
# ------------------------------------------------------------

def aiohttp_middleware():
    """中间件"""
    print("\n=== 3.3 中间件 ===")
    
    code = '''
from aiohttp import web
import time
import logging

# 1. 函数中间件
@web.middleware
async def logging_middleware(request, handler):
    """请求日志中间件"""
    start = time.time()
    
    # 调用下一个处理器
    response = await handler(request)
    
    duration = time.time() - start
    logging.info(f"{request.method} {request.path} - {response.status} - {duration:.3f}s")
    
    return response

@web.middleware
async def error_middleware(request, handler):
    """错误处理中间件"""
    try:
        return await handler(request)
    except web.HTTPException:
        raise  # 重新抛出 HTTP 异常
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        return web.json_response(
            {"error": "Internal Server Error"},
            status=500
        )

@web.middleware
async def auth_middleware(request, handler):
    """认证中间件"""
    # 跳过公开路由
    if request.path in ['/login', '/health']:
        return await handler(request)
    
    # 检查认证
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise web.HTTPUnauthorized(text='Missing or invalid token')
    
    # 验证token (简化示例)
    token = auth_header[7:]
    request['user'] = {'id': 1, 'name': 'User'}  # 存储用户信息
    
    return await handler(request)

@web.middleware
async def cors_middleware(request, handler):
    """CORS 中间件"""
    if request.method == 'OPTIONS':
        response = web.Response()
    else:
        response = await handler(request)
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    return response

# 2. 应用中间件
app = web.Application(middlewares=[
    cors_middleware,
    logging_middleware,
    error_middleware,
    auth_middleware,
])

# 中间件执行顺序: cors -> logging -> error -> auth -> handler
'''
    print(code)


# ------------------------------------------------------------
# 3.4 应用生命周期
# ------------------------------------------------------------

def aiohttp_lifecycle():
    """应用生命周期"""
    print("\n=== 3.4 应用生命周期 ===")
    
    code = '''
from aiohttp import web
import aiohttp
import asyncpg  # 假设使用 PostgreSQL

# 应用上下文 - 存储共享资源
async def create_db_pool(app):
    """创建数据库连接池"""
    app['db'] = await asyncpg.create_pool(
        'postgresql://user:pass@localhost/dbname',
        min_size=5,
        max_size=20
    )
    print("Database pool created")

async def create_http_session(app):
    """创建 HTTP 客户端会话"""
    app['http_session'] = aiohttp.ClientSession()
    print("HTTP session created")

async def close_db_pool(app):
    """关闭数据库连接池"""
    await app['db'].close()
    print("Database pool closed")

async def close_http_session(app):
    """关闭 HTTP 客户端会话"""
    await app['http_session'].close()
    print("HTTP session closed")

# 信号处理
async def on_startup(app):
    """启动时执行"""
    print("Application starting...")
    
async def on_shutdown(app):
    """关闭时执行"""
    print("Application shutting down...")

async def on_cleanup(app):
    """清理时执行"""
    print("Application cleanup...")

# 路由处理器中使用共享资源
async def get_users(request):
    db = request.app['db']
    async with db.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM users')
        return web.json_response([dict(r) for r in rows])

async def call_external_api(request):
    session = request.app['http_session']
    async with session.get('https://api.example.com/data') as resp:
        data = await resp.json()
        return web.json_response(data)

# 创建应用
app = web.Application()

# 注册生命周期回调
app.on_startup.append(create_db_pool)
app.on_startup.append(create_http_session)
app.on_startup.append(on_startup)

app.on_shutdown.append(on_shutdown)

app.on_cleanup.append(close_http_session)
app.on_cleanup.append(close_db_pool)
app.on_cleanup.append(on_cleanup)

# 路由
app.router.add_get('/users', get_users)
app.router.add_get('/external', call_external_api)

if __name__ == '__main__':
    web.run_app(app, port=8080)

# 生命周期顺序:
# 启动: on_startup callbacks -> server starts
# 关闭: on_shutdown callbacks -> server stops -> on_cleanup callbacks
'''
    print(code)


# ------------------------------------------------------------
# 3.5 WebSocket
# ------------------------------------------------------------

def aiohttp_websocket():
    """WebSocket"""
    print("\n=== 3.5 WebSocket ===")
    
    code = '''
from aiohttp import web
import aiohttp
import asyncio
import json

# WebSocket 连接管理器
class WebSocketManager:
    def __init__(self):
        self.connections = set()
    
    async def connect(self, ws):
        self.connections.add(ws)
        print(f"New connection. Total: {len(self.connections)}")
    
    async def disconnect(self, ws):
        self.connections.discard(ws)
        print(f"Connection closed. Total: {len(self.connections)}")
    
    async def broadcast(self, message):
        """广播消息到所有连接"""
        if self.connections:
            await asyncio.gather(
                *[ws.send_str(message) for ws in self.connections],
                return_exceptions=True
            )

ws_manager = WebSocketManager()

# WebSocket 处理器
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    await ws_manager.connect(ws)
    
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    # 回显消息
                    await ws.send_str(f"Echo: {msg.data}")
                    
                    # 或者广播
                    # await ws_manager.broadcast(msg.data)
                    
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f'WebSocket error: {ws.exception()}')
    finally:
        await ws_manager.disconnect(ws)
    
    return ws

# 聊天室示例
async def chat_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    # 获取用户名
    username = request.query.get('username', 'Anonymous')
    await ws_manager.connect(ws)
    await ws_manager.broadcast(json.dumps({
        'type': 'join',
        'user': username,
        'message': f'{username} joined the chat'
    }))
    
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                await ws_manager.broadcast(json.dumps({
                    'type': 'message',
                    'user': username,
                    'message': data.get('message', '')
                }))
    finally:
        await ws_manager.disconnect(ws)
        await ws_manager.broadcast(json.dumps({
            'type': 'leave',
            'user': username,
            'message': f'{username} left the chat'
        }))
    
    return ws

# 路由
app = web.Application()
app.router.add_get('/ws', websocket_handler)
app.router.add_get('/chat', chat_handler)

# WebSocket 客户端示例
async def ws_client():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://localhost:8080/ws') as ws:
            await ws.send_str('Hello, Server!')
            
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(f'Received: {msg.data}')
                    break
            
            await ws.close()
'''
    print(code)


# ============================================================
# Part 4: 实战项目案例
# ============================================================

print("""
╔══════════════════════════════════════════════════════════════╗
║                 Part 4: 实战项目案例                          ║
╚══════════════════════════════════════════════════════════════╝
""")


# ------------------------------------------------------------
# 4.1 异步爬虫
# ------------------------------------------------------------

async def async_crawler_demo():
    """异步爬虫示例"""
    print("\n=== 4.1 异步爬虫 ===")
    
    @dataclass
    class CrawlResult:
        url: str
        status: int
        content_length: int
        title: Optional[str] = None
        error: Optional[str] = None
    
    class AsyncCrawler:
        """异步爬虫"""
        
        def __init__(self, concurrency: int = 10):
            self.concurrency = concurrency
            self.semaphore = asyncio.Semaphore(concurrency)
            self.results: List[CrawlResult] = []
        
        async def fetch_one(
            self, 
            session: aiohttp.ClientSession, 
            url: str
        ) -> CrawlResult:
            """获取单个URL"""
            async with self.semaphore:
                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                        content = await resp.text()
                        
                        # 简单提取标题
                        title = None
                        if '<title>' in content.lower():
                            start = content.lower().find('<title>') + 7
                            end = content.lower().find('</title>')
                            if end > start:
                                title = content[start:end].strip()[:50]
                        
                        return CrawlResult(
                            url=url,
                            status=resp.status,
                            content_length=len(content),
                            title=title
                        )
                except asyncio.TimeoutError:
                    return CrawlResult(url=url, status=0, content_length=0, error="Timeout")
                except Exception as e:
                    return CrawlResult(url=url, status=0, content_length=0, error=str(e))
        
        async def crawl(self, urls: List[str]) -> List[CrawlResult]:
            """批量爬取"""
            connector = aiohttp.TCPConnector(limit=self.concurrency * 2)
            async with aiohttp.ClientSession(connector=connector) as session:
                tasks = [self.fetch_one(session, url) for url in urls]
                self.results = await asyncio.gather(*tasks)
                return self.results
    
    # 演示
    print("  异步爬虫示例:")
    crawler = AsyncCrawler(concurrency=3)
    
    urls = [
        'https://httpbin.org/html',
        'https://httpbin.org/json',
        'https://httpbin.org/xml',
    ]
    
    try:
        start = time.time()
        results = await asyncio.wait_for(crawler.crawl(urls), timeout=15)
        duration = time.time() - start
        
        for result in results:
            status = "✓" if result.status == 200 else "✗"
            print(f"    {status} {result.url}: {result.status}, {result.content_length} bytes")
        
        print(f"\n  总耗时: {duration:.2f}秒")
    except asyncio.TimeoutError:
        print("  爬取超时")
    except Exception as e:
        print(f"  爬取失败: {e}")


# ------------------------------------------------------------
# 4.2 异步 API 客户端
# ------------------------------------------------------------

async def async_api_client_demo():
    """异步 API 客户端"""
    print("\n=== 4.2 异步 API 客户端 ===")
    
    class AsyncAPIClient:
        """通用异步 API 客户端"""
        
        def __init__(
            self,
            base_url: str,
            timeout: int = 30,
            max_retries: int = 3
        ):
            self.base_url = base_url.rstrip('/')
            self.timeout = aiohttp.ClientTimeout(total=timeout)
            self.max_retries = max_retries
            self._session: Optional[aiohttp.ClientSession] = None
        
        async def __aenter__(self):
            self._session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if self._session:
                await self._session.close()
        
        async def _request(
            self,
            method: str,
            endpoint: str,
            **kwargs
        ) -> Dict[str, Any]:
            """发送请求"""
            url = f"{self.base_url}{endpoint}"
            
            for attempt in range(self.max_retries):
                try:
                    async with self._session.request(method, url, **kwargs) as resp:
                        resp.raise_for_status()
                        return await resp.json()
                except aiohttp.ClientResponseError as e:
                    if e.status < 500:  # 客户端错误不重试
                        raise
                    if attempt == self.max_retries - 1:
                        raise
                except (aiohttp.ClientError, asyncio.TimeoutError):
                    if attempt == self.max_retries - 1:
                        raise
                
                await asyncio.sleep(0.5 * (2 ** attempt))  # 指数退避
            
            return {}
        
        async def get(self, endpoint: str, params: dict = None) -> Dict:
            return await self._request('GET', endpoint, params=params)
        
        async def post(self, endpoint: str, data: dict = None) -> Dict:
            return await self._request('POST', endpoint, json=data)
        
        async def put(self, endpoint: str, data: dict = None) -> Dict:
            return await self._request('PUT', endpoint, json=data)
        
        async def delete(self, endpoint: str) -> Dict:
            return await self._request('DELETE', endpoint)
    
    # 使用示例
    print("  API 客户端示例:")
    
    try:
        async with AsyncAPIClient('https://httpbin.org') as client:
            # GET
            result = await client.get('/get', params={'key': 'value'})
            print(f"    GET /get: {result.get('args')}")
            
            # POST
            result = await client.post('/post', data={'name': 'Alice'})
            print(f"    POST /post: {result.get('json')}")
    except Exception as e:
        print(f"    API 请求失败: {e}")


# ------------------------------------------------------------
# 4.3 并发任务调度器
# ------------------------------------------------------------

async def task_scheduler_demo():
    """并发任务调度器"""
    print("\n=== 4.3 并发任务调度器 ===")
    
    class AsyncTaskScheduler:
        """异步任务调度器"""
        
        def __init__(self, max_workers: int = 5):
            self.max_workers = max_workers
            self.semaphore = asyncio.Semaphore(max_workers)
            self.queue = asyncio.Queue()
            self.results = {}
            self.running = False
            self._workers = []
        
        async def add_task(self, task_id: str, coro):
            """添加任务"""
            await self.queue.put((task_id, coro))
        
        async def _worker(self, worker_id: int):
            """工作协程"""
            while self.running:
                try:
                    task_id, coro = await asyncio.wait_for(
                        self.queue.get(), 
                        timeout=0.5
                    )
                except asyncio.TimeoutError:
                    continue
                
                async with self.semaphore:
                    try:
                        result = await coro
                        self.results[task_id] = {'status': 'success', 'result': result}
                    except Exception as e:
                        self.results[task_id] = {'status': 'error', 'error': str(e)}
                    finally:
                        self.queue.task_done()
        
        async def start(self):
            """启动调度器"""
            self.running = True
            self._workers = [
                asyncio.create_task(self._worker(i))
                for i in range(self.max_workers)
            ]
        
        async def stop(self):
            """停止调度器"""
            await self.queue.join()  # 等待所有任务完成
            self.running = False
            for worker in self._workers:
                worker.cancel()
        
        def get_results(self) -> Dict:
            return self.results
    
    # 演示
    print("  任务调度器示例:")
    
    async def sample_task(task_id: int, duration: float):
        await asyncio.sleep(duration)
        return f"Task-{task_id} completed"
    
    scheduler = AsyncTaskScheduler(max_workers=3)
    await scheduler.start()
    
    # 添加任务
    for i in range(5):
        await scheduler.add_task(
            f"task-{i}",
            sample_task(i, 0.2)
        )
    
    await scheduler.stop()
    
    results = scheduler.get_results()
    for task_id, result in results.items():
        print(f"    {task_id}: {result['status']}")


# ------------------------------------------------------------
# 4.4 实时数据管道
# ------------------------------------------------------------

async def data_pipeline_demo():
    """实时数据管道"""
    print("\n=== 4.4 实时数据管道 ===")
    
    class AsyncDataPipeline:
        """异步数据处理管道"""
        
        def __init__(self):
            self.stages: List[Callable] = []
        
        def add_stage(self, processor: Callable):
            """添加处理阶段"""
            self.stages.append(processor)
            return self
        
        async def process(self, data):
            """处理数据"""
            result = data
            for stage in self.stages:
                if asyncio.iscoroutinefunction(stage):
                    result = await stage(result)
                else:
                    result = stage(result)
            return result
        
        async def process_batch(self, items: List, concurrency: int = 5):
            """批量处理"""
            semaphore = asyncio.Semaphore(concurrency)
            
            async def process_one(item):
                async with semaphore:
                    return await self.process(item)
            
            return await asyncio.gather(*[process_one(item) for item in items])
    
    # 演示
    print("  数据管道示例:")
    
    # 定义处理阶段
    async def fetch_data(item):
        await asyncio.sleep(0.1)  # 模拟 IO
        return {'id': item, 'raw': f'data-{item}'}
    
    def transform(data):
        data['transformed'] = data['raw'].upper()
        return data
    
    async def enrich(data):
        await asyncio.sleep(0.05)  # 模拟 IO
        data['enriched'] = True
        return data
    
    def validate(data):
        data['valid'] = len(data['raw']) > 0
        return data
    
    # 创建管道
    pipeline = AsyncDataPipeline()
    pipeline.add_stage(fetch_data)\
            .add_stage(transform)\
            .add_stage(enrich)\
            .add_stage(validate)
    
    # 处理数据
    items = [1, 2, 3, 4, 5]
    results = await pipeline.process_batch(items, concurrency=3)
    
    for result in results:
        print(f"    ID {result['id']}: {result['transformed']}, valid={result['valid']}")


# ------------------------------------------------------------
# 4.5 完整的 REST API 服务器
# ------------------------------------------------------------

def complete_rest_api_example():
    """完整的 REST API 服务器示例"""
    print("\n=== 4.5 完整的 REST API 服务器 ===")
    
    code = '''
"""
完整的 REST API 服务器示例
使用 aiohttp 构建的用户管理 API
"""
from aiohttp import web
import aiohttp
import asyncio
import json
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime

# ==================== 数据模型 ====================

@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: str
    
    @classmethod
    def create(cls, name: str, email: str) -> 'User':
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            created_at=datetime.now().isoformat()
        )
    
    def to_dict(self) -> dict:
        return asdict(self)

# ==================== 数据存储 ====================

class UserRepository:
    """用户数据存储（内存实现，生产环境应使用数据库）"""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
    
    async def get_all(self) -> List[User]:
        return list(self._users.values())
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    async def create(self, user: User) -> User:
        self._users[user.id] = user
        return user
    
    async def update(self, user_id: str, data: dict) -> Optional[User]:
        if user_id not in self._users:
            return None
        user = self._users[user_id]
        for key, value in data.items():
            if hasattr(user, key) and key not in ['id', 'created_at']:
                setattr(user, key, value)
        return user
    
    async def delete(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

# ==================== 中间件 ====================

@web.middleware
async def logging_middleware(request, handler):
    """请求日志"""
    start = asyncio.get_event_loop().time()
    response = await handler(request)
    duration = asyncio.get_event_loop().time() - start
    print(f"{request.method} {request.path} - {response.status} - {duration*1000:.2f}ms")
    return response

@web.middleware
async def error_middleware(request, handler):
    """错误处理"""
    try:
        return await handler(request)
    except web.HTTPException:
        raise
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

@web.middleware
async def cors_middleware(request, handler):
    """CORS 处理"""
    if request.method == 'OPTIONS':
        response = web.Response()
    else:
        response = await handler(request)
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# ==================== 路由处理器 ====================

class UserHandler:
    """用户 API 处理器"""
    
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    async def list_users(self, request):
        """GET /api/users - 获取所有用户"""
        users = await self.repo.get_all()
        return web.json_response({
            "users": [u.to_dict() for u in users],
            "count": len(users)
        })
    
    async def get_user(self, request):
        """GET /api/users/{id} - 获取单个用户"""
        user_id = request.match_info['id']
        user = await self.repo.get_by_id(user_id)
        
        if not user:
            raise web.HTTPNotFound(text=json.dumps({"error": "User not found"}))
        
        return web.json_response(user.to_dict())
    
    async def create_user(self, request):
        """POST /api/users - 创建用户"""
        data = await request.json()
        
        # 验证
        if not data.get('name') or not data.get('email'):
            raise web.HTTPBadRequest(text=json.dumps({
                "error": "name and email are required"
            }))
        
        user = User.create(data['name'], data['email'])
        await self.repo.create(user)
        
        return web.json_response(user.to_dict(), status=201)
    
    async def update_user(self, request):
        """PUT /api/users/{id} - 更新用户"""
        user_id = request.match_info['id']
        data = await request.json()
        
        user = await self.repo.update(user_id, data)
        if not user:
            raise web.HTTPNotFound(text=json.dumps({"error": "User not found"}))
        
        return web.json_response(user.to_dict())
    
    async def delete_user(self, request):
        """DELETE /api/users/{id} - 删除用户"""
        user_id = request.match_info['id']
        
        if not await self.repo.delete(user_id):
            raise web.HTTPNotFound(text=json.dumps({"error": "User not found"}))
        
        return web.Response(status=204)

# ==================== 健康检查 ====================

async def health_check(request):
    """GET /health - 健康检查"""
    return web.json_response({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# ==================== 应用工厂 ====================

def create_app() -> web.Application:
    """创建应用"""
    app = web.Application(middlewares=[
        cors_middleware,
        logging_middleware,
        error_middleware,
    ])
    
    # 初始化存储
    repo = UserRepository()
    handler = UserHandler(repo)
    
    # 路由
    app.router.add_get('/health', health_check)
    app.router.add_get('/api/users', handler.list_users)
    app.router.add_get('/api/users/{id}', handler.get_user)
    app.router.add_post('/api/users', handler.create_user)
    app.router.add_put('/api/users/{id}', handler.update_user)
    app.router.add_delete('/api/users/{id}', handler.delete_user)
    
    return app

# ==================== 启动 ====================

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8080)

# ==================== 测试命令 ====================
"""
# 健康检查
curl http://localhost:8080/health

# 创建用户
curl -X POST http://localhost:8080/api/users \\
    -H "Content-Type: application/json" \\
    -d '{"name": "Alice", "email": "alice@example.com"}'

# 获取所有用户
curl http://localhost:8080/api/users

# 获取单个用户
curl http://localhost:8080/api/users/{user_id}

# 更新用户
curl -X PUT http://localhost:8080/api/users/{user_id} \\
    -H "Content-Type: application/json" \\
    -d '{"name": "Alice Updated"}'

# 删除用户
curl -X DELETE http://localhost:8080/api/users/{user_id}
"""
'''
    print(code)


# ============================================================
# 主函数
# ============================================================

async def main():
    """主函数"""
    print("=" * 70)
    print("    Python asyncio & aiohttp 详解与实战")
    print("=" * 70)
    
    # Part 1: asyncio 深度解析
    await event_loop_demo()
    await task_coroutine_deep()
    await task_group_demo()
    await sync_primitives_demo()
    await timeout_cancellation_demo()
    await async_queue_advanced()
    await run_sync_in_async()
    
    # Part 2: aiohttp 客户端
    await aiohttp_client_session()
    await aiohttp_http_methods()
    await aiohttp_response_handling()
    await aiohttp_streaming()
    await aiohttp_file_operations()
    await aiohttp_error_handling()
    await aiohttp_concurrency_control()
    
    # Part 3: aiohttp 服务端 (代码展示)
    aiohttp_server_basics()
    aiohttp_routing()
    aiohttp_middleware()
    aiohttp_lifecycle()
    aiohttp_websocket()
    
    # Part 4: 实战案例
    await async_crawler_demo()
    await async_api_client_demo()
    await task_scheduler_demo()
    await data_pipeline_demo()
    complete_rest_api_example()
    
    # 总结
    print("\n" + "=" * 70)
    print("    总结")
    print("=" * 70)
    
    print("""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                     asyncio & aiohttp 知识要点                       │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                      │
    │  asyncio 核心概念:                                                   │
    │  • 事件循环 (Event Loop) - 异步任务的调度中心                         │
    │  • 协程 (Coroutine) - async def 定义的异步函数                       │
    │  • 任务 (Task) - 协程的包装，可调度执行                               │
    │  • Future - 异步操作的结果占位符                                      │
    │                                                                      │
    │  asyncio 常用 API:                                                   │
    │  • asyncio.run()         - 运行异步程序                              │
    │  • asyncio.create_task() - 创建任务                                  │
    │  • asyncio.gather()      - 并发执行多个协程                          │
    │  • asyncio.wait_for()    - 带超时等待                                │
    │  • asyncio.TaskGroup     - 结构化并发 (3.11+)                        │
    │  • asyncio.to_thread()   - 在线程中运行同步代码                       │
    │                                                                      │
    │  同步原语:                                                           │
    │  • Lock        - 互斥锁                                              │
    │  • Semaphore   - 信号量/限流器                                       │
    │  • Event       - 事件通知                                            │
    │  • Condition   - 条件变量                                            │
    │  • Barrier     - 屏障同步                                            │
    │                                                                      │
    │  aiohttp 客户端:                                                     │
    │  • ClientSession - 连接管理、Cookie、连接池                          │
    │  • 支持所有 HTTP 方法                                                 │
    │  • 流式上传/下载                                                      │
    │  • 完善的错误处理                                                     │
    │                                                                      │
    │  aiohttp 服务端:                                                     │
    │  • web.Application - 应用实例                                        │
    │  • 路由和视图                                                         │
    │  • 中间件链                                                          │
    │  • WebSocket 支持                                                    │
    │  • 生命周期管理                                                       │
    │                                                                      │
    │  最佳实践:                                                           │
    │  ✓ 复用 ClientSession                                               │
    │  ✓ 使用 Semaphore 控制并发                                           │
    │  ✓ 设置合理的超时                                                    │
    │  ✓ 正确处理取消和异常                                                │
    │  ✓ 使用 TaskGroup 进行结构化并发                                     │
    │  ✗ 避免在协程中使用阻塞调用                                          │
    │  ✗ 不要忘记 await                                                    │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
    """)
    
    print("\n示例演示完成！")


if __name__ == "__main__":
    asyncio.run(main())

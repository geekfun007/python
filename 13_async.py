"""
Python 异步编程详解
包含：async/await、asyncio、协程、事件循环等
"""

import asyncio
import time
import aiohttp
from typing import List


# ============================================
# 1. 异步基础
# ============================================

async def async_basics():
    """异步基础"""
    print("\n=== 异步基础 ===")
    
    # 基本异步函数
    async def say_hello(name, delay):
        """异步问候"""
        print(f"  Hello, {name}!")
        await asyncio.sleep(delay)  # 异步睡眠
        print(f"  Goodbye, {name}!")
        return f"Done with {name}"
    
    # 运行异步函数
    print("1. 单个异步函数:")
    result = await say_hello("Alice", 1)
    print(f"  返回值: {result}")
    
    # 并发运行多个异步函数
    print("\n2. 并发运行:")
    results = await asyncio.gather(
        say_hello("Bob", 1),
        say_hello("Charlie", 0.5),
        say_hello("David", 0.3)
    )
    print(f"  返回值: {results}")


async def coroutine_demo():
    """协程示例"""
    print("\n=== 协程 ===")
    
    # 协程函数
    async def counter(name, n):
        """计数协程"""
        for i in range(n):
            print(f"  {name}: {i}")
            await asyncio.sleep(0.2)
    
    # 创建任务
    print("1. 创建任务:")
    task1 = asyncio.create_task(counter("A", 3))
    task2 = asyncio.create_task(counter("B", 3))
    
    # 等待任务完成
    await task1
    await task2
    
    # 使用 TaskGroup (Python 3.11+)
    print("\n2. 使用 gather:")
    await asyncio.gather(
        counter("X", 2),
        counter("Y", 2),
        counter("Z", 2)
    )


# ============================================
# 2. 异步任务管理
# ============================================

async def task_management():
    """任务管理"""
    print("\n=== 任务管理 ===")
    
    async def task(name, duration):
        """任务函数"""
        print(f"  {name} 开始")
        await asyncio.sleep(duration)
        print(f"  {name} 完成")
        return f"{name} result"
    
    # create_task
    print("1. create_task:")
    t1 = asyncio.create_task(task("Task-1", 1))
    t2 = asyncio.create_task(task("Task-2", 0.5))
    
    # 等待任务
    r1 = await t1
    r2 = await t2
    print(f"  结果: {r1}, {r2}")
    
    # gather - 等待所有任务
    print("\n2. gather:")
    results = await asyncio.gather(
        task("A", 0.3),
        task("B", 0.2),
        task("C", 0.1)
    )
    print(f"  结果: {results}")
    
    # wait_for - 超时
    print("\n3. wait_for (超时):")
    try:
        result = await asyncio.wait_for(task("Slow", 5), timeout=1.0)
    except asyncio.TimeoutError:
        print("  超时!")
    
    # as_completed - 按完成顺序
    print("\n4. as_completed:")
    tasks = [
        asyncio.create_task(task(f"Task-{i}", i * 0.3))
        for i in range(1, 4)
    ]
    
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  完成: {result}")


# ============================================
# 3. 异步上下文管理器
# ============================================

async def async_context_manager():
    """异步上下文管理器"""
    print("\n=== 异步上下文管理器 ===")
    
    class AsyncConnection:
        """异步连接"""
        def __init__(self, name):
            self.name = name
        
        async def __aenter__(self):
            print(f"  连接 {self.name}")
            await asyncio.sleep(0.1)
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            print(f"  断开 {self.name}")
            await asyncio.sleep(0.1)
        
        async def query(self, sql):
            print(f"  执行查询: {sql}")
            await asyncio.sleep(0.2)
            return ["结果1", "结果2"]
    
    # 使用异步上下文管理器
    async with AsyncConnection("DB") as conn:
        results = await conn.query("SELECT * FROM users")
        print(f"  查询结果: {results}")


# ============================================
# 4. 异步迭代器
# ============================================

async def async_iterator():
    """异步迭代器"""
    print("\n=== 异步迭代器 ===")
    
    class AsyncRange:
        """异步范围迭代器"""
        def __init__(self, n):
            self.n = n
            self.i = 0
        
        def __aiter__(self):
            return self
        
        async def __anext__(self):
            if self.i >= self.n:
                raise StopAsyncIteration
            await asyncio.sleep(0.1)
            self.i += 1
            return self.i
    
    # 使用异步迭代器
    print("异步迭代:")
    async for num in AsyncRange(5):
        print(f"  {num}")


async def async_generator():
    """异步生成器"""
    print("\n=== 异步生成器 ===")
    
    async def async_range(n):
        """异步生成器"""
        for i in range(n):
            await asyncio.sleep(0.1)
            yield i
    
    print("异步生成器:")
    async for num in async_range(5):
        print(f"  {num}")


# ============================================
# 5. 异步队列
# ============================================

async def async_queue():
    """异步队列"""
    print("\n=== 异步队列 ===")
    
    queue = asyncio.Queue(maxsize=3)
    
    async def producer(name, queue):
        """生产者"""
        for i in range(5):
            item = f"{name}-{i}"
            await queue.put(item)
            print(f"  {name} 生产: {item}")
            await asyncio.sleep(0.2)
    
    async def consumer(name, queue):
        """消费者"""
        while True:
            item = await queue.get()
            print(f"  {name} 消费: {item}")
            await asyncio.sleep(0.3)
            queue.task_done()
    
    # 创建生产者和消费者
    producers = [
        asyncio.create_task(producer(f"Producer-{i}", queue))
        for i in range(2)
    ]
    
    consumers = [
        asyncio.create_task(consumer(f"Consumer-{i}", queue))
        for i in range(3)
    ]
    
    # 等待生产者完成
    await asyncio.gather(*producers)
    
    # 等待队列清空
    await queue.join()
    
    # 取消消费者
    for c in consumers:
        c.cancel()


# ============================================
# 6. 异步锁
# ============================================

async def async_lock():
    """异步锁"""
    print("\n=== 异步锁 ===")
    
    lock = asyncio.Lock()
    counter = 0
    
    async def increment():
        """增加计数"""
        nonlocal counter
        async with lock:
            current = counter
            await asyncio.sleep(0.01)
            counter = current + 1
    
    # 并发增加
    await asyncio.gather(*[increment() for _ in range(10)])
    print(f"  最终计数: {counter}")


# ============================================
# 7. 实战示例
# ============================================

async def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 异步HTTP请求
    print("1. 异步HTTP请求:")
    
    async def fetch(session, url):
        """获取URL"""
        async with session.get(url) as response:
            return await response.text()
    
    async def fetch_all(urls):
        """批量获取"""
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]
    
    try:
        start = time.time()
        results = await fetch_all(urls)
        duration = time.time() - start
        print(f"  获取 {len(results)} 个URL，耗时 {duration:.2f}秒")
    except Exception as e:
        print(f"  请求失败: {e}")
    
    # 2. 并发文件处理
    print("\n2. 异步文件处理:")
    
    async def process_file(filename, content):
        """处理文件"""
        print(f"  处理 {filename}")
        await asyncio.sleep(0.5)  # 模拟IO操作
        return f"{filename}: {len(content)} bytes"
    
    files = {
        "file1.txt": "内容1" * 100,
        "file2.txt": "内容2" * 200,
        "file3.txt": "内容3" * 150,
    }
    
    tasks = [process_file(name, content) for name, content in files.items()]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(f"  {result}")
    
    # 3. 定时任务
    print("\n3. 定时任务:")
    
    async def periodic_task(name, interval):
        """周期性任务"""
        for i in range(3):
            print(f"  {name} 执行 #{i+1}")
            await asyncio.sleep(interval)
    
    await asyncio.gather(
        periodic_task("Task-A", 0.5),
        periodic_task("Task-B", 0.3),
    )
    
    # 4. 超时处理
    print("\n4. 超时处理:")
    
    async def slow_operation():
        """慢操作"""
        print("  开始慢操作...")
        await asyncio.sleep(5)
        return "完成"
    
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
        print(f"  结果: {result}")
    except asyncio.TimeoutError:
        print("  操作超时")
    
    # 5. 重试机制
    print("\n5. 重试机制:")
    
    async def unstable_operation(success_rate=0.3):
        """不稳定操作"""
        import random
        if random.random() < success_rate:
            return "成功"
        raise RuntimeError("操作失败")
    
    async def retry_operation(max_attempts=3):
        """重试操作"""
        for attempt in range(max_attempts):
            try:
                result = await unstable_operation(0.7)
                print(f"  尝试 {attempt + 1}: {result}")
                return result
            except RuntimeError as e:
                print(f"  尝试 {attempt + 1}: {e}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(0.5)
                else:
                    raise
    
    try:
        await retry_operation()
    except RuntimeError:
        print("  所有尝试均失败")


# ============================================
# 8. 同步与异步混合
# ============================================

async def sync_async_mix():
    """同步与异步混合"""
    print("\n=== 同步与异步混合 ===")
    
    def blocking_operation():
        """阻塞操作（同步）"""
        print("  执行阻塞操作")
        time.sleep(1)
        return "阻塞完成"
    
    # 在异步中运行同步代码
    print("1. run_in_executor:")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_operation)
    print(f"  结果: {result}")
    
    # 在同步中运行异步代码
    print("\n2. asyncio.run:")
    
    async def async_operation():
        await asyncio.sleep(0.5)
        return "异步完成"
    
    # 注意：这个例子只是说明，实际在async函数中不能这样用
    print("  (在主函数中使用 asyncio.run())")


# ============================================
# 9. 性能对比
# ============================================

async def performance_comparison():
    """性能对比"""
    print("\n=== 性能对比 ===")
    
    async def io_task(n):
        """IO任务"""
        await asyncio.sleep(0.1)
        return n * n
    
    # 顺序执行
    print("1. 顺序执行:")
    start = time.time()
    results = []
    for i in range(10):
        result = await io_task(i)
        results.append(result)
    sequential_time = time.time() - start
    print(f"  耗时: {sequential_time:.2f}秒")
    
    # 并发执行
    print("\n2. 并发执行:")
    start = time.time()
    results = await asyncio.gather(*[io_task(i) for i in range(10)])
    concurrent_time = time.time() - start
    print(f"  耗时: {concurrent_time:.2f}秒")
    
    print(f"\n  加速比: {sequential_time/concurrent_time:.2f}x")


# ============================================
# 10. 最佳实践
# ============================================

def best_practices():
    """最佳实践"""
    print("\n=== 最佳实践 ===")
    
    print("""
    异步编程最佳实践:
    
    1. 使用 asyncio.run() 启动
       - 主入口使用 asyncio.run(main())
       - 自动处理事件循环
    
    2. 正确使用 await
       - await 只能在 async 函数中使用
       - 所有 IO 操作都应该 await
    
    3. 避免阻塞操作
       ✗ time.sleep()
       ✓ await asyncio.sleep()
       
       ✗ requests.get()
       ✓ await aiohttp.get()
    
    4. 使用 asyncio.gather() 并发
       - 同时运行多个协程
       - 收集所有结果
    
    5. 异常处理
       - 在协程中捕获异常
       - gather() 使用 return_exceptions=True
    
    6. 超时处理
       - 使用 asyncio.wait_for()
       - 防止协程无限等待
    
    7. 任务取消
       - task.cancel()
       - 处理 CancelledError
    
    8. 资源管理
       - 使用 async with
       - 确保资源释放
    
    9. 避免CPU密集型
       - asyncio 适合IO密集型
       - CPU密集型用多进程
    
    10. 调试
        - asyncio.set_debug(True)
        - 使用日志
        - 注意协程泄漏
    
    适用场景:
    ✓ 网络请求（HTTP、WebSocket）
    ✓ 数据库查询
    ✓ 文件IO
    ✓ 并发多个IO操作
    
    不适用场景:
    ✗ CPU密集型计算
    ✗ 同步库（需要包装）
    ✗ 简单脚本（过度工程）
    """)


# ============================================
# 主函数
# ============================================

async def main():
    """主异步函数"""
    print("=" * 60)
    print("Python 异步编程详解")
    print("=" * 60)
    
    await async_basics()
    await coroutine_demo()
    await task_management()
    await async_context_manager()
    await async_iterator()
    await async_generator()
    await async_queue()
    await async_lock()
    
    print("\n" + "=" * 60)
    print("实战示例")
    print("=" * 60)
    
    await practical_examples()
    await sync_async_mix()
    await performance_comparison()
    
    best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    # Python 3.7+ 推荐方式
    asyncio.run(main())

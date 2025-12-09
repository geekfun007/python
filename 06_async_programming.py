"""
Python 高级教程 - 异步编程详解

异步编程是处理 I/O 密集型任务的高效方式。
本模块涵盖:
1. async/await 语法
2. asyncio 事件循环
3. 协程和任务
4. 并发控制
5. 实战应用
"""

import asyncio
import aiohttp
import time
from typing import List, Any
import random

# ============================================================================
# 1. 基础异步函数
# ============================================================================

async def hello_async():
    """基础异步函数"""
    print("Hello")
    await asyncio.sleep(1)  # 异步睡眠
    print("World")
    return "完成"


async def fetch_data(id: int, delay: float = 1.0):
    """模拟异步获取数据"""
    print(f"[{id}] 开始获取数据...")
    await asyncio.sleep(delay)
    print(f"[{id}] 数据获取完成")
    return f"数据-{id}"


# ============================================================================
# 2. 并发执行多个协程
# ============================================================================

async def run_concurrent():
    """并发执行多个协程"""
    print("=" * 60)
    print("并发执行多个协程")
    print("=" * 60)
    
    start = time.time()
    
    # 方法 1: asyncio.gather
    results = await asyncio.gather(
        fetch_data(1, 1.0),
        fetch_data(2, 0.5),
        fetch_data(3, 0.8)
    )
    print(f"gather 结果: {results}")
    
    elapsed = time.time() - start
    print(f"总耗时: {elapsed:.2f}秒\n")


async def run_as_tasks():
    """使用任务并发执行"""
    print("=" * 60)
    print("使用 Task 对象")
    print("=" * 60)
    
    # 创建任务
    task1 = asyncio.create_task(fetch_data(1, 1.0))
    task2 = asyncio.create_task(fetch_data(2, 0.5))
    task3 = asyncio.create_task(fetch_data(3, 0.8))
    
    # 等待所有任务完成
    results = await asyncio.gather(task1, task2, task3)
    print(f"任务结果: {results}\n")


# ============================================================================
# 3. 异步迭代器
# ============================================================================

class AsyncRange:
    """异步范围迭代器"""
    
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.current = start
    
    def __aiter__(self):
        """返回异步迭代器"""
        return self
    
    async def __anext__(self):
        """返回下一个值"""
        if self.current >= self.end:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.1)  # 模拟异步操作
        value = self.current
        self.current += 1
        return value


async def demo_async_iterator():
    """演示异步迭代器"""
    print("=" * 60)
    print("异步迭代器")
    print("=" * 60)
    
    async for num in AsyncRange(0, 5):
        print(f"异步迭代: {num}")
    print()


# ============================================================================
# 4. 异步生成器
# ============================================================================

async def async_fibonacci(n: int):
    """异步斐波那契生成器"""
    a, b = 0, 1
    for _ in range(n):
        await asyncio.sleep(0.1)
        yield a
        a, b = b, a + b


async def demo_async_generator():
    """演示异步生成器"""
    print("=" * 60)
    print("异步生成器")
    print("=" * 60)
    
    async for num in async_fibonacci(10):
        print(f"斐波那契: {num}")
    print()


# ============================================================================
# 5. 异步上下文管理器
# ============================================================================

class AsyncDatabaseConnection:
    """异步数据库连接"""
    
    def __init__(self, host: str):
        self.host = host
        self.connected = False
    
    async def __aenter__(self):
        print(f"异步连接到 {self.host}...")
        await asyncio.sleep(0.2)
        self.connected = True
        print("连接成功")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"异步关闭连接...")
        await asyncio.sleep(0.1)
        self.connected = False
        print("连接已关闭")
        return False
    
    async def query(self, sql: str):
        """执行查询"""
        if not self.connected:
            raise RuntimeError("未连接数据库")
        await asyncio.sleep(0.1)
        return f"查询结果: {sql}"


async def demo_async_context_manager():
    """演示异步上下文管理器"""
    print("=" * 60)
    print("异步上下文管理器")
    print("=" * 60)
    
    async with AsyncDatabaseConnection("localhost") as db:
        result = await db.query("SELECT * FROM users")
        print(result)
    print()


# ============================================================================
# 6. 超时控制
# ============================================================================

async def slow_operation(duration: float):
    """慢速操作"""
    print(f"开始慢速操作 ({duration}秒)...")
    await asyncio.sleep(duration)
    print("慢速操作完成")
    return "结果"


async def demo_timeout():
    """演示超时控制"""
    print("=" * 60)
    print("超时控制")
    print("=" * 60)
    
    # 成功完成
    try:
        result = await asyncio.wait_for(slow_operation(1), timeout=2.0)
        print(f"操作完成: {result}")
    except asyncio.TimeoutError:
        print("操作超时")
    
    # 超时
    try:
        result = await asyncio.wait_for(slow_operation(3), timeout=1.0)
        print(f"操作完成: {result}")
    except asyncio.TimeoutError:
        print("操作超时")
    print()


# ============================================================================
# 7. 信号量 (Semaphore) - 并发限制
# ============================================================================

async def limited_concurrency_fetch(id: int, semaphore: asyncio.Semaphore):
    """限制并发数的获取操作"""
    async with semaphore:
        print(f"[{id}] 开始获取 (并发限制)")
        await asyncio.sleep(1)
        print(f"[{id}] 获取完成")
        return f"结果-{id}"


async def demo_semaphore():
    """演示信号量"""
    print("=" * 60)
    print("信号量 - 限制并发数")
    print("=" * 60)
    
    # 最多 3 个并发
    semaphore = asyncio.Semaphore(3)
    
    tasks = [
        limited_concurrency_fetch(i, semaphore)
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"所有结果: {results}\n")


# ============================================================================
# 8. 锁 (Lock) - 互斥访问
# ============================================================================

shared_resource = 0
lock = asyncio.Lock()


async def increment_with_lock(name: str, count: int):
    """使用锁保护的增量操作"""
    global shared_resource
    
    for i in range(count):
        async with lock:
            current = shared_resource
            await asyncio.sleep(0.01)  # 模拟处理
            shared_resource = current + 1
            print(f"[{name}] 增量到: {shared_resource}")


async def demo_lock():
    """演示异步锁"""
    print("=" * 60)
    print("异步锁 - 互斥访问")
    print("=" * 60)
    
    global shared_resource
    shared_resource = 0
    
    await asyncio.gather(
        increment_with_lock("协程A", 3),
        increment_with_lock("协程B", 3)
    )
    
    print(f"最终值: {shared_resource}\n")


# ============================================================================
# 9. 事件 (Event) - 同步协调
# ============================================================================

async def waiter(event: asyncio.Event, name: str):
    """等待事件的协程"""
    print(f"[{name}] 等待事件...")
    await event.wait()
    print(f"[{name}] 事件已触发，继续执行")


async def trigger(event: asyncio.Event, delay: float):
    """触发事件的协程"""
    await asyncio.sleep(delay)
    print("[触发器] 设置事件")
    event.set()


async def demo_event():
    """演示异步事件"""
    print("=" * 60)
    print("异步事件 - 协程同步")
    print("=" * 60)
    
    event = asyncio.Event()
    
    await asyncio.gather(
        waiter(event, "协程1"),
        waiter(event, "协程2"),
        waiter(event, "协程3"),
        trigger(event, 2.0)
    )
    print()


# ============================================================================
# 10. 队列 (Queue) - 生产者消费者模式
# ============================================================================

async def producer(queue: asyncio.Queue, id: int):
    """生产者"""
    for i in range(3):
        item = f"生产者{id}-项目{i}"
        await asyncio.sleep(random.uniform(0.1, 0.5))
        await queue.put(item)
        print(f"[生产者{id}] 生产: {item}")
    
    await queue.put(None)  # 结束标记


async def consumer(queue: asyncio.Queue, id: int):
    """消费者"""
    while True:
        item = await queue.get()
        
        if item is None:
            queue.task_done()
            await queue.put(None)  # 传递结束标记
            break
        
        print(f"[消费者{id}] 消费: {item}")
        await asyncio.sleep(random.uniform(0.2, 0.6))
        queue.task_done()


async def demo_queue():
    """演示异步队列"""
    print("=" * 60)
    print("异步队列 - 生产者消费者")
    print("=" * 60)
    
    queue = asyncio.Queue(maxsize=5)
    
    producers = [producer(queue, i) for i in range(2)]
    consumers = [consumer(queue, i) for i in range(3)]
    
    await asyncio.gather(*producers)
    await asyncio.gather(*consumers)
    
    await queue.join()
    print()


# ============================================================================
# 11. 异步 HTTP 请求 (使用 aiohttp)
# ============================================================================

async def fetch_url(session: aiohttp.ClientSession, url: str):
    """异步获取 URL"""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return {
                'url': url,
                'status': response.status,
                'length': len(await response.text())
            }
    except Exception as e:
        return {'url': url, 'error': str(e)}


async def demo_http_requests():
    """演示异步 HTTP 请求"""
    print("=" * 60)
    print("异步 HTTP 请求")
    print("=" * 60)
    
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/1'
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            print(f"结果: {result}")
    print()


# ============================================================================
# 12. 实战示例: 异步爬虫
# ============================================================================

class AsyncWebScraper:
    """异步网页爬虫"""
    
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results = []
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str):
        """获取单个页面"""
        async with self.semaphore:
            try:
                print(f"爬取: {url}")
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    content = await response.text()
                    return {
                        'url': url,
                        'status': response.status,
                        'size': len(content),
                        'success': True
                    }
            except Exception as e:
                print(f"错误 {url}: {e}")
                return {
                    'url': url,
                    'error': str(e),
                    'success': False
                }
    
    async def scrape(self, urls: List[str]):
        """爬取多个页面"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_page(session, url) for url in urls]
            self.results = await asyncio.gather(*tasks)
        return self.results


async def demo_web_scraper():
    """演示异步爬虫"""
    print("=" * 60)
    print("异步网页爬虫")
    print("=" * 60)
    
    urls = [
        'https://httpbin.org/html',
        'https://httpbin.org/json',
        'https://httpbin.org/xml'
    ]
    
    scraper = AsyncWebScraper(max_concurrent=2)
    results = await scraper.scrape(urls)
    
    successful = sum(1 for r in results if r.get('success'))
    print(f"\n成功: {successful}/{len(results)}")
    print()


# ============================================================================
# 13. 异步任务管理
# ============================================================================

async def cancellable_task(id: int, duration: float):
    """可取消的任务"""
    try:
        print(f"[任务{id}] 开始")
        await asyncio.sleep(duration)
        print(f"[任务{id}] 完成")
        return f"结果-{id}"
    except asyncio.CancelledError:
        print(f"[任务{id}] 已取消")
        raise


async def demo_task_cancellation():
    """演示任务取消"""
    print("=" * 60)
    print("任务取消")
    print("=" * 60)
    
    task1 = asyncio.create_task(cancellable_task(1, 5))
    task2 = asyncio.create_task(cancellable_task(2, 1))
    
    await asyncio.sleep(2)
    
    # 取消长任务
    task1.cancel()
    
    results = await asyncio.gather(task1, task2, return_exceptions=True)
    print(f"结果: {results}\n")


# ============================================================================
# 14. 异步上下文变量
# ============================================================================

from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar('request_id', default='unknown')


async def process_request(id: str):
    """处理请求 - 使用上下文变量"""
    request_id.set(id)
    print(f"[{request_id.get()}] 处理请求")
    await asyncio.sleep(0.5)
    print(f"[{request_id.get()}] 请求完成")


async def demo_context_vars():
    """演示上下文变量"""
    print("=" * 60)
    print("异步上下文变量")
    print("=" * 60)
    
    await asyncio.gather(
        process_request("REQ-001"),
        process_request("REQ-002"),
        process_request("REQ-003")
    )
    print()


# ============================================================================
# 15. 混合同步和异步代码
# ============================================================================

def blocking_io():
    """阻塞 I/O 操作"""
    print("执行阻塞操作...")
    time.sleep(1)
    return "阻塞操作结果"


async def run_in_executor():
    """在执行器中运行阻塞代码"""
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, blocking_io)
    return result


async def demo_executor():
    """演示执行器"""
    print("=" * 60)
    print("在执行器中运行阻塞代码")
    print("=" * 60)
    
    # 并发运行多个阻塞操作
    results = await asyncio.gather(
        run_in_executor(),
        run_in_executor(),
        run_in_executor()
    )
    print(f"结果: {results}\n")


# ============================================================================
# 重要注意事项
# ============================================================================

"""
异步编程最佳实践和注意事项:

1. async/await 语法
   - async def: 定义协程函数
   - await: 等待异步操作完成
   - 只能在 async 函数中使用 await
   - 协程必须被 await 或加入事件循环

2. 事件循环
   - asyncio.run(): Python 3.7+ 推荐方式
   - asyncio.get_event_loop(): 获取当前循环
   - 一个线程只能有一个运行中的事件循环

3. 并发执行
   - asyncio.gather(): 并发运行多个协程，收集结果
   - asyncio.create_task(): 创建任务立即调度
   - asyncio.wait(): 更细粒度的控制

4. 何时使用异步
   ✓ I/O 密集型任务 (网络请求、文件读写)
   ✓ 需要高并发的场景
   ✗ CPU 密集型任务 (使用 multiprocessing)
   ✗ 简单的顺序操作

5. 同步原语
   - Lock: 互斥锁
   - Semaphore: 限制并发数
   - Event: 事件通知
   - Condition: 条件变量
   - Queue: 异步队列

6. 异常处理
   - 使用 try/except 捕获异常
   - asyncio.gather(return_exceptions=True) 收集异常
   - 任务取消会抛出 CancelledError

7. 超时控制
   - asyncio.wait_for(): 设置操作超时
   - asyncio.timeout(): Python 3.11+ 上下文管理器

8. 调试技巧
   - asyncio.run(debug=True): 启用调试模式
   - warnings.simplefilter('always', ResourceWarning)
   - 使用日志记录异步操作
   - aiodebug 等调试工具

9. 性能优化
   - 使用连接池 (aiohttp.ClientSession)
   - 限制并发数 (Semaphore)
   - 批量操作代替单个操作
   - 避免在协程中使用阻塞操作

10. 常见陷阱
    - 忘记 await 协程
    - 在协程中使用阻塞函数
    - 不正确的异常处理
    - 任务泄漏 (未等待的任务)
    - 循环引用导致的内存泄漏

11. 库生态
    - aiohttp: HTTP 客户端/服务器
    - aiofiles: 异步文件操作
    - aiomysql/asyncpg: 异步数据库
    - aioredis: 异步 Redis
    
12. 迁移到异步
    - 从外向内迁移 (先迁移 I/O 边界)
    - 使用 run_in_executor 包装同步代码
    - 考虑使用 asyncio 兼容的库
    - 渐进式迁移，不必全部异步化
"""


# ============================================================================
# 主程序
# ============================================================================

async def main():
    """主异步函数"""
    print("\n" + "=" * 60)
    print("Python 高级教程 - 异步编程详解")
    print("=" * 60 + "\n")
    
    # 基础示例
    result = await hello_async()
    print(f"基础异步函数结果: {result}\n")
    
    # 并发示例
    await run_concurrent()
    await run_as_tasks()
    
    # 高级特性
    await demo_async_iterator()
    await demo_async_generator()
    await demo_async_context_manager()
    await demo_timeout()
    
    # 同步原语
    await demo_semaphore()
    await demo_lock()
    await demo_event()
    await demo_queue()
    
    # 实战应用 (需要网络连接)
    # await demo_http_requests()
    # await demo_web_scraper()
    
    # 任务管理
    await demo_task_cancellation()
    await demo_context_vars()
    await demo_executor()
    
    print("=" * 60)
    print("异步编程教程完成!")
    print("=" * 60)


if __name__ == "__main__":
    # 运行主异步函数
    asyncio.run(main())

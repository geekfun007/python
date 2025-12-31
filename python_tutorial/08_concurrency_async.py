"""
Python 进程、并发与异步编程 (with Type Hints)
=============================================

本文件涵盖：
- 多进程 (multiprocessing)
- 多线程 (threading)
- 协程与异步 (asyncio)
- concurrent.futures
- 线程安全与同步原语
"""

from typing import Any, Callable, TypeVar, Coroutine
import os
import time
import threading
import multiprocessing as mp
from multiprocessing import Process, Pool, Queue, Pipe, Value, Array
from threading import Thread, Lock, RLock, Semaphore, Event, Condition, Barrier
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future, as_completed
import asyncio
from asyncio import Task, Queue as AsyncQueue
from queue import Queue as ThreadQueue, Empty
from contextlib import contextmanager
from dataclasses import dataclass

T = TypeVar('T')
R = TypeVar('R')

# ============================================================================
# 1. 多进程 (multiprocessing)
# ============================================================================

class MultiprocessingDemo:
    """多进程演示"""
    
    @staticmethod
    def cpu_bound_task(n: int) -> int:
        """CPU 密集型任务：计算素数"""
        count = 0
        for num in range(2, n):
            is_prime = True
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                count += 1
        return count
    
    @staticmethod
    def basic_process() -> None:
        """基本进程使用"""
        def worker(name: str) -> None:
            """工作函数"""
            print(f"Worker {name} started, PID: {os.getpid()}")
            time.sleep(1)
            print(f"Worker {name} finished")
        
        print(f"Main process PID: {os.getpid()}")
        
        # 创建进程
        processes: list[Process] = []
        for i in range(3):
            p = Process(target=worker, args=(f"Process-{i}",))
            processes.append(p)
            p.start()
        
        # 等待所有进程完成
        for p in processes:
            p.join()
        
        print("All processes finished")
    
    @staticmethod
    def process_pool() -> None:
        """进程池"""
        numbers = [100000, 150000, 200000, 250000]
        
        # 串行执行（对比）
        start = time.time()
        serial_results = [MultiprocessingDemo.cpu_bound_task(n) for n in numbers]
        serial_time = time.time() - start
        print(f"Serial: {serial_results}, Time: {serial_time:.2f}s")
        
        # 进程池并行
        start = time.time()
        with Pool(processes=4) as pool:
            parallel_results = pool.map(MultiprocessingDemo.cpu_bound_task, numbers)
        parallel_time = time.time() - start
        print(f"Parallel: {parallel_results}, Time: {parallel_time:.2f}s")
        print(f"Speedup: {serial_time / parallel_time:.2f}x")
    
    @staticmethod
    def process_communication() -> None:
        """进程间通信"""
        # 使用 Queue
        def producer(q: "mp.Queue[int]") -> None:
            for i in range(5):
                print(f"Producing {i}")
                q.put(i)
                time.sleep(0.1)
            q.put(None)  # 结束信号
        
        def consumer(q: "mp.Queue[int]") -> None:
            while True:
                item = q.get()
                if item is None:
                    break
                print(f"Consuming {item}")
        
        q: mp.Queue[int] = Queue()
        p1 = Process(target=producer, args=(q,))
        p2 = Process(target=consumer, args=(q,))
        
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        
        print("\n--- Using Pipe ---")
        
        # 使用 Pipe
        def sender(conn: Any) -> None:
            for msg in ["Hello", "World", "END"]:
                conn.send(msg)
                time.sleep(0.1)
            conn.close()
        
        def receiver(conn: Any) -> None:
            while True:
                msg = conn.recv()
                if msg == "END":
                    break
                print(f"Received: {msg}")
        
        parent_conn, child_conn = Pipe()
        p1 = Process(target=sender, args=(parent_conn,))
        p2 = Process(target=receiver, args=(child_conn,))
        
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    
    @staticmethod
    def shared_memory() -> None:
        """共享内存"""
        def increment(counter: Any, lock: Any) -> None:
            for _ in range(1000):
                with lock:
                    counter.value += 1
        
        # 共享计数器
        counter = Value('i', 0)  # 'i' = integer
        lock = mp.Lock()
        
        processes = [
            Process(target=increment, args=(counter, lock))
            for _ in range(4)
        ]
        
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        
        print(f"Final counter: {counter.value}")  # 应该是 4000
        
        # 共享数组
        arr = Array('d', [0.0] * 5)  # 'd' = double
        
        def init_array(shared_arr: Any, idx: int) -> None:
            shared_arr[idx] = idx * 1.5
        
        processes = [
            Process(target=init_array, args=(arr, i))
            for i in range(5)
        ]
        
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        
        print(f"Shared array: {list(arr)}")


# ============================================================================
# 2. 多线程 (threading)
# ============================================================================

class ThreadingDemo:
    """多线程演示"""
    
    @staticmethod
    def io_bound_task(url: str) -> str:
        """IO 密集型任务模拟"""
        time.sleep(0.5)  # 模拟网络请求
        return f"Downloaded {url}"
    
    @staticmethod
    def basic_threading() -> None:
        """基本线程使用"""
        def worker(name: str, duration: float) -> None:
            thread_id = threading.current_thread().name
            print(f"Thread {name} ({thread_id}) started")
            time.sleep(duration)
            print(f"Thread {name} ({thread_id}) finished")
        
        # 创建线程
        threads: list[Thread] = []
        for i in range(3):
            t = Thread(
                target=worker,
                args=(f"Worker-{i}", 0.5),
                name=f"MyThread-{i}"
            )
            threads.append(t)
            t.start()
        
        # 等待所有线程
        for t in threads:
            t.join()
        
        print("All threads finished")
    
    @staticmethod
    def daemon_threads() -> None:
        """守护线程"""
        def background_task() -> None:
            while True:
                print("Background task running...")
                time.sleep(0.3)
        
        # 守护线程在主线程退出时自动终止
        daemon = Thread(target=background_task, daemon=True)
        daemon.start()
        
        time.sleep(1)
        print("Main thread exiting (daemon will be terminated)")
    
    @staticmethod
    def thread_synchronization() -> None:
        """线程同步"""
        # 不安全的计数器
        class UnsafeCounter:
            def __init__(self) -> None:
                self.count = 0
            
            def increment(self) -> None:
                # 这不是原子操作！
                current = self.count
                time.sleep(0.0001)  # 模拟一些处理
                self.count = current + 1
        
        # 安全的计数器
        class SafeCounter:
            def __init__(self) -> None:
                self.count = 0
                self._lock = Lock()
            
            def increment(self) -> None:
                with self._lock:
                    current = self.count
                    time.sleep(0.0001)
                    self.count = current + 1
        
        def increment_many(counter: Any, times: int) -> None:
            for _ in range(times):
                counter.increment()
        
        # 测试不安全计数器
        unsafe = UnsafeCounter()
        threads = [Thread(target=increment_many, args=(unsafe, 100)) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"Unsafe counter (expected 500): {unsafe.count}")
        
        # 测试安全计数器
        safe = SafeCounter()
        threads = [Thread(target=increment_many, args=(safe, 100)) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"Safe counter (expected 500): {safe.count}")
    
    @staticmethod
    def synchronization_primitives() -> None:
        """同步原语"""
        # RLock - 可重入锁
        rlock = RLock()
        
        def recursive_function(n: int) -> int:
            with rlock:  # 同一线程可以多次获取
                if n <= 1:
                    return 1
                return n * recursive_function(n - 1)
        
        print(f"Factorial(5) with RLock: {recursive_function(5)}")
        
        # Semaphore - 信号量（限制并发数）
        sem = Semaphore(2)  # 最多 2 个线程同时访问
        
        def limited_access(name: str) -> None:
            with sem:
                print(f"{name} acquired semaphore")
                time.sleep(0.5)
                print(f"{name} released semaphore")
        
        threads = [Thread(target=limited_access, args=(f"Thread-{i}",)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Event - 线程间信号
        event = Event()
        
        def waiter(name: str) -> None:
            print(f"{name} waiting for event...")
            event.wait()
            print(f"{name} received event!")
        
        def setter() -> None:
            time.sleep(1)
            print("Setting event!")
            event.set()
        
        threads = [Thread(target=waiter, args=(f"Waiter-{i}",)) for i in range(3)]
        threads.append(Thread(target=setter))
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    
    @staticmethod
    def producer_consumer() -> None:
        """生产者-消费者模式"""
        queue: ThreadQueue[int | None] = ThreadQueue(maxsize=10)
        
        def producer(q: ThreadQueue[int | None], items: int) -> None:
            for i in range(items):
                q.put(i)
                print(f"Produced: {i}")
                time.sleep(0.1)
            q.put(None)  # 结束信号
        
        def consumer(q: ThreadQueue[int | None]) -> None:
            while True:
                item = q.get()
                if item is None:
                    q.task_done()
                    break
                print(f"Consumed: {item}")
                q.task_done()
                time.sleep(0.15)
        
        prod = Thread(target=producer, args=(queue, 5))
        cons = Thread(target=consumer, args=(queue,))
        
        prod.start()
        cons.start()
        
        prod.join()
        cons.join()


# ============================================================================
# 3. concurrent.futures
# ============================================================================

class ConcurrentFuturesDemo:
    """concurrent.futures 演示"""
    
    @staticmethod
    def io_task(url: str) -> dict[str, Any]:
        """模拟 IO 任务"""
        time.sleep(0.5)
        return {"url": url, "size": len(url) * 100}
    
    @staticmethod
    def cpu_task(n: int) -> int:
        """CPU 任务"""
        return sum(i * i for i in range(n))
    
    @staticmethod
    def thread_pool_executor() -> None:
        """线程池执行器"""
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3",
            "https://example.com/page4",
        ]
        
        # 方式 1: map
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(ConcurrentFuturesDemo.io_task, urls))
        
        print("Thread pool results (map):")
        for r in results:
            print(f"  {r}")
        
        # 方式 2: submit + as_completed
        print("\nThread pool results (as_completed):")
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures: dict[Future[dict[str, Any]], str] = {
                executor.submit(ConcurrentFuturesDemo.io_task, url): url
                for url in urls
            }
            
            for future in as_completed(futures):
                url = futures[future]
                try:
                    result = future.result()
                    print(f"  {url}: {result['size']} bytes")
                except Exception as e:
                    print(f"  {url}: error - {e}")
    
    @staticmethod
    def process_pool_executor() -> None:
        """进程池执行器"""
        numbers = [1000000, 2000000, 3000000, 4000000]
        
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(ConcurrentFuturesDemo.cpu_task, numbers))
        
        print("Process pool results:")
        for n, r in zip(numbers, results):
            print(f"  cpu_task({n}) = {r}")
    
    @staticmethod
    def future_callbacks() -> None:
        """Future 回调"""
        def on_complete(future: Future[dict[str, Any]]) -> None:
            result = future.result()
            print(f"Callback: Task completed with {result}")
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            future = executor.submit(ConcurrentFuturesDemo.io_task, "https://example.com")
            future.add_done_callback(on_complete)
            
            # 主线程可以继续其他工作
            print("Main thread continues...")
            time.sleep(1)


# ============================================================================
# 4. asyncio 异步编程
# ============================================================================

class AsyncioDemo:
    """asyncio 异步编程演示"""
    
    @staticmethod
    async def fetch_data(url: str, delay: float = 0.5) -> dict[str, Any]:
        """模拟异步数据获取"""
        print(f"Fetching {url}...")
        await asyncio.sleep(delay)
        print(f"Got {url}")
        return {"url": url, "data": f"Data from {url}"}
    
    @staticmethod
    async def basic_async() -> None:
        """基本异步操作"""
        # 单个协程
        result = await AsyncioDemo.fetch_data("https://example.com")
        print(f"Single result: {result}")
    
    @staticmethod
    async def concurrent_tasks() -> None:
        """并发任务"""
        urls = [
            "https://api.example.com/users",
            "https://api.example.com/posts",
            "https://api.example.com/comments",
        ]
        
        # 方式 1: gather - 等待所有任务完成
        print("Using gather:")
        start = time.time()
        results = await asyncio.gather(
            *[AsyncioDemo.fetch_data(url) for url in urls]
        )
        print(f"Time: {time.time() - start:.2f}s")
        for r in results:
            print(f"  {r['url']}: {r['data']}")
        
        # 方式 2: create_task - 更多控制
        print("\nUsing create_task:")
        tasks: list[Task[dict[str, Any]]] = []
        for url in urls:
            task = asyncio.create_task(AsyncioDemo.fetch_data(url))
            tasks.append(task)
        
        # 可以在等待期间做其他事
        print("Tasks created, doing other work...")
        await asyncio.sleep(0.1)
        
        results = await asyncio.gather(*tasks)
        print(f"All done: {len(results)} results")
    
    @staticmethod
    async def task_timeout() -> None:
        """任务超时"""
        async def slow_task() -> str:
            await asyncio.sleep(5)
            return "Done"
        
        try:
            result = await asyncio.wait_for(slow_task(), timeout=1.0)
            print(f"Result: {result}")
        except asyncio.TimeoutError:
            print("Task timed out!")
    
    @staticmethod
    async def async_iteration() -> None:
        """异步迭代"""
        async def async_range(start: int, stop: int, delay: float = 0.1):
            """异步生成器"""
            for i in range(start, stop):
                await asyncio.sleep(delay)
                yield i
        
        print("Async iteration:")
        async for num in async_range(0, 5):
            print(f"  Got: {num}")
        
        # 异步推导式
        numbers = [x async for x in async_range(0, 5, 0.05)]
        print(f"Async comprehension: {numbers}")
    
    @staticmethod
    async def async_context_manager() -> None:
        """异步上下文管理器"""
        class AsyncResource:
            async def __aenter__(self) -> "AsyncResource":
                print("Acquiring resource...")
                await asyncio.sleep(0.2)
                print("Resource acquired")
                return self
            
            async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
                print("Releasing resource...")
                await asyncio.sleep(0.1)
                print("Resource released")
            
            async def do_work(self) -> str:
                await asyncio.sleep(0.1)
                return "Work done"
        
        async with AsyncResource() as resource:
            result = await resource.do_work()
            print(f"Result: {result}")
    
    @staticmethod
    async def async_queue() -> None:
        """异步队列"""
        queue: AsyncQueue[int | None] = asyncio.Queue(maxsize=10)
        
        async def producer(q: AsyncQueue[int | None]) -> None:
            for i in range(5):
                await q.put(i)
                print(f"Produced: {i}")
                await asyncio.sleep(0.1)
            await q.put(None)
        
        async def consumer(q: AsyncQueue[int | None]) -> None:
            while True:
                item = await q.get()
                if item is None:
                    break
                print(f"Consumed: {item}")
                await asyncio.sleep(0.15)
        
        await asyncio.gather(producer(queue), consumer(queue))
    
    @staticmethod
    async def semaphore_limit() -> None:
        """使用信号量限制并发"""
        sem = asyncio.Semaphore(2)  # 最多 2 个并发
        
        async def limited_task(name: str) -> str:
            async with sem:
                print(f"{name} started")
                await asyncio.sleep(0.5)
                print(f"{name} finished")
                return f"Result from {name}"
        
        tasks = [limited_task(f"Task-{i}") for i in range(5)]
        results = await asyncio.gather(*tasks)
        print(f"All results: {results}")


# ============================================================================
# 5. 实战模式
# ============================================================================

@dataclass
class WorkItem:
    """工作项"""
    id: int
    data: str


class WorkerPool:
    """工作线程池模式"""
    
    def __init__(self, num_workers: int = 4) -> None:
        self.num_workers = num_workers
        self.queue: ThreadQueue[WorkItem | None] = ThreadQueue()
        self.results: dict[int, str] = {}
        self._lock = Lock()
        self._workers: list[Thread] = []
    
    def _worker(self) -> None:
        """工作线程"""
        while True:
            item = self.queue.get()
            if item is None:
                self.queue.task_done()
                break
            
            # 处理工作
            result = self._process(item)
            
            with self._lock:
                self.results[item.id] = result
            
            self.queue.task_done()
    
    def _process(self, item: WorkItem) -> str:
        """处理工作项"""
        time.sleep(0.1)  # 模拟处理
        return f"Processed: {item.data.upper()}"
    
    def start(self) -> None:
        """启动工作线程"""
        for i in range(self.num_workers):
            t = Thread(target=self._worker, name=f"Worker-{i}")
            t.start()
            self._workers.append(t)
    
    def submit(self, item: WorkItem) -> None:
        """提交工作"""
        self.queue.put(item)
    
    def shutdown(self) -> None:
        """关闭线程池"""
        # 发送终止信号
        for _ in self._workers:
            self.queue.put(None)
        
        # 等待所有工作完成
        for t in self._workers:
            t.join()


class AsyncRateLimiter:
    """异步速率限制器"""
    
    def __init__(self, rate: int, per: float = 1.0) -> None:
        """
        Args:
            rate: 每个时间窗口允许的请求数
            per: 时间窗口（秒）
        """
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """获取令牌"""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            
            # 补充令牌
            self.tokens = min(
                self.rate,
                self.tokens + elapsed * (self.rate / self.per)
            )
            self.last_update = now
            
            if self.tokens < 1:
                wait_time = (1 - self.tokens) * (self.per / self.rate)
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1


class PatternsDemo:
    """实战模式演示"""
    
    @staticmethod
    def worker_pool_demo() -> None:
        """工作池模式"""
        pool = WorkerPool(num_workers=3)
        pool.start()
        
        # 提交工作
        for i in range(10):
            pool.submit(WorkItem(id=i, data=f"item-{i}"))
        
        pool.shutdown()
        
        print("Worker pool results:")
        for id_, result in sorted(pool.results.items()):
            print(f"  {id_}: {result}")
    
    @staticmethod
    async def rate_limiter_demo() -> None:
        """速率限制器演示"""
        limiter = AsyncRateLimiter(rate=3, per=1.0)  # 每秒 3 个请求
        
        async def make_request(i: int) -> None:
            await limiter.acquire()
            print(f"Request {i} at {time.time():.2f}")
        
        # 快速发送 10 个请求，应该被限速
        start = time.time()
        await asyncio.gather(*[make_request(i) for i in range(10)])
        print(f"Total time: {time.time() - start:.2f}s")


# ============================================================================
# 运行演示
# ============================================================================

def run_sync_demos() -> None:
    """运行同步演示"""
    print("=" * 60)
    print("THREADING DEMO")
    print("=" * 60)
    ThreadingDemo.basic_threading()
    print()
    ThreadingDemo.thread_synchronization()
    print()
    ThreadingDemo.synchronization_primitives()
    print()
    ThreadingDemo.producer_consumer()
    
    print("\n" + "=" * 60)
    print("CONCURRENT FUTURES DEMO")
    print("=" * 60)
    ConcurrentFuturesDemo.thread_pool_executor()
    print()
    ConcurrentFuturesDemo.future_callbacks()
    
    print("\n" + "=" * 60)
    print("PATTERNS DEMO")
    print("=" * 60)
    PatternsDemo.worker_pool_demo()


async def run_async_demos() -> None:
    """运行异步演示"""
    print("\n" + "=" * 60)
    print("ASYNCIO DEMO")
    print("=" * 60)
    
    print("\n--- Basic Async ---")
    await AsyncioDemo.basic_async()
    
    print("\n--- Concurrent Tasks ---")
    await AsyncioDemo.concurrent_tasks()
    
    print("\n--- Task Timeout ---")
    await AsyncioDemo.task_timeout()
    
    print("\n--- Async Iteration ---")
    await AsyncioDemo.async_iteration()
    
    print("\n--- Async Context Manager ---")
    await AsyncioDemo.async_context_manager()
    
    print("\n--- Async Queue ---")
    await AsyncioDemo.async_queue()
    
    print("\n--- Semaphore Limit ---")
    await AsyncioDemo.semaphore_limit()
    
    print("\n--- Rate Limiter ---")
    await PatternsDemo.rate_limiter_demo()


def main() -> None:
    """主函数"""
    print("NOTE: Multiprocessing demos are skipped in main()")
    print("They should be run separately to avoid issues.")
    print()
    
    # 同步演示
    run_sync_demos()
    
    # 异步演示
    asyncio.run(run_async_demos())


if __name__ == "__main__":
    main()

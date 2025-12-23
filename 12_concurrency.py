"""
Python 多线程并发编程详解
包含：threading、Thread、Lock、Queue、线程池等
"""

import threading
import time
import queue
from threading import Thread, Lock, RLock, Semaphore, Event, Condition
from threading import current_thread, active_count
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


# ============================================
# 1. 线程基础
# ============================================

def thread_basics():
    """线程基础"""
    print("\n=== 线程基础 ===")
    
    # 创建线程
    def worker(name, duration):
        """工作线程"""
        print(f"  线程 {name} 开始 (ID: {current_thread().ident})")
        time.sleep(duration)
        print(f"  线程 {name} 结束")
    
    print("1. 创建线程:")
    print(f"主线程 ID: {current_thread().ident}")
    
    # 创建并启动线程
    t1 = Thread(target=worker, args=("Worker-1", 1))
    t2 = Thread(target=worker, args=("Worker-2", 0.5))
    
    t1.start()
    t2.start()
    
    # 等待线程完成
    t1.join()
    t2.join()
    
    print("所有线程完成")
    
    # 守护线程
    print("\n2. 守护线程:")
    def daemon_worker():
        print("  守护线程启动")
        time.sleep(2)
        print("  守护线程结束（可能看不到这条）")
    
    t = Thread(target=daemon_worker)
    t.daemon = True  # 设置为守护线程
    t.start()
    time.sleep(0.5)
    print("  主线程结束（守护线程会被终止）")


def thread_class():
    """继承 Thread 类"""
    print("\n=== 继承 Thread 类 ===")
    
    class MyThread(Thread):
        def __init__(self, name, count):
            super().__init__()
            self.name = name
            self.count = count
        
        def run(self):
            """线程执行的代码"""
            print(f"  {self.name} 开始")
            for i in range(self.count):
                print(f"  {self.name}: {i}")
                time.sleep(0.2)
            print(f"  {self.name} 结束")
    
    threads = [
        MyThread("Thread-A", 3),
        MyThread("Thread-B", 3)
    ]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()


# ============================================
# 2. 线程同步
# ============================================

def thread_synchronization():
    """线程同步"""
    print("\n=== 线程同步 ===")
    
    # Lock - 互斥锁
    print("1. Lock:")
    counter = 0
    lock = Lock()
    
    def increment_with_lock():
        global counter
        for _ in range(100000):
            with lock:
                counter += 1
    
    threads = [Thread(target=increment_with_lock) for _ in range(5)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"  最终计数（使用锁）: {counter}")
    
    # 不使用锁的对比
    print("\n2. 不使用锁（竞态条件）:")
    counter = 0
    
    def increment_without_lock():
        global counter
        for _ in range(100000):
            counter += 1
    
    threads = [Thread(target=increment_without_lock) for _ in range(5)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"  最终计数（无锁）: {counter}")  # 可能不是 500000
    
    # RLock - 可重入锁
    print("\n3. RLock:")
    rlock = RLock()
    
    def recursive_function(n):
        with rlock:
            print(f"  层级 {n}")
            if n > 0:
                recursive_function(n - 1)
    
    Thread(target=recursive_function, args=(3,)).start()
    time.sleep(0.5)


def semaphore_demo():
    """信号量"""
    print("\n=== Semaphore ===")
    
    # 限制同时访问的线程数
    semaphore = Semaphore(3)  # 最多3个线程
    
    def access_resource(name):
        print(f"  {name} 等待...")
        with semaphore:
            print(f"  {name} 获得访问权")
            time.sleep(1)
            print(f"  {name} 释放资源")
    
    threads = [Thread(target=access_resource, args=(f"Thread-{i}",)) 
               for i in range(6)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def event_demo():
    """事件"""
    print("\n=== Event ===")
    
    event = Event()
    
    def waiter(name):
        print(f"  {name} 等待事件...")
        event.wait()  # 等待事件被设置
        print(f"  {name} 继续执行")
    
    def setter():
        print("  Setter 准备...")
        time.sleep(2)
        print("  Setter 设置事件")
        event.set()  # 设置事件
    
    threads = [
        Thread(target=waiter, args=("Waiter-1",)),
        Thread(target=waiter, args=("Waiter-2",)),
        Thread(target=setter)
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def condition_demo():
    """条件变量"""
    print("\n=== Condition ===")
    
    condition = Condition()
    items = []
    
    def producer():
        """生产者"""
        for i in range(5):
            time.sleep(0.5)
            with condition:
                items.append(i)
                print(f"  生产: {i}")
                condition.notify()  # 通知消费者
    
    def consumer():
        """消费者"""
        while True:
            with condition:
                while not items:
                    condition.wait()  # 等待通知
                item = items.pop(0)
                print(f"  消费: {item}")
                if item == 4:  # 最后一个
                    break
    
    t1 = Thread(target=producer)
    t2 = Thread(target=consumer)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()


# ============================================
# 3. 线程通信
# ============================================

def thread_communication():
    """线程间通信"""
    print("\n=== 线程间通信 ===")
    
    # Queue - 线程安全的队列
    print("1. Queue:")
    q = queue.Queue()
    
    def producer(queue):
        """生产者"""
        for i in range(5):
            print(f"  生产: {i}")
            queue.put(i)
            time.sleep(0.3)
        queue.put(None)  # 结束信号
    
    def consumer(queue):
        """消费者"""
        while True:
            item = queue.get()
            if item is None:
                break
            print(f"  消费: {item}")
            queue.task_done()
    
    prod = Thread(target=producer, args=(q,))
    cons = Thread(target=consumer, args=(q,))
    
    prod.start()
    cons.start()
    
    prod.join()
    cons.join()
    
    # LifoQueue - 后进先出
    print("\n2. LifoQueue (栈):")
    lifo_q = queue.LifoQueue()
    
    for i in range(5):
        lifo_q.put(i)
    
    print("  ", end="")
    while not lifo_q.empty():
        print(lifo_q.get(), end=" ")
    print()
    
    # PriorityQueue - 优先级队列
    print("\n3. PriorityQueue:")
    pq = queue.PriorityQueue()
    
    # 添加元素 (优先级, 值)
    pq.put((3, "低优先级"))
    pq.put((1, "高优先级"))
    pq.put((2, "中优先级"))
    
    while not pq.empty():
        priority, item = pq.get()
        print(f"  优先级 {priority}: {item}")


# ============================================
# 4. 线程池
# ============================================

def thread_pool():
    """线程池"""
    print("\n=== 线程池 (ThreadPoolExecutor) ===")
    
    def task(n):
        """任务函数"""
        print(f"  处理 {n} (线程: {current_thread().name})")
        time.sleep(0.5)
        return n * n
    
    # 使用线程池
    print("1. submit():")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(task, i) for i in range(6)]
        
        for future in as_completed(futures):
            result = future.result()
            print(f"  结果: {result}")
    
    # map 方法
    print("\n2. map():")
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(task, range(5))
        print(f"  结果: {list(results)}")


# ============================================
# 5. 线程局部存储
# ============================================

def thread_local_storage():
    """线程局部存储"""
    print("\n=== 线程局部存储 ===")
    
    # 线程局部数据
    local_data = threading.local()
    
    def worker(name, value):
        """工作线程"""
        local_data.name = name
        local_data.value = value
        
        print(f"  {name} 设置值: {value}")
        time.sleep(0.5)
        
        # 每个线程看到自己的值
        print(f"  {name} 读取值: {local_data.value}")
    
    threads = [
        Thread(target=worker, args=("Thread-A", 100)),
        Thread(target=worker, args=("Thread-B", 200)),
        Thread(target=worker, args=("Thread-C", 300))
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ============================================
# 6. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 网页下载（IO密集型）
    print("1. 多线程下载:")
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]
    
    def download(url):
        """下载网页"""
        try:
            response = requests.get(url, timeout=5)
            return len(response.content)
        except:
            return 0
    
    # 单线程
    start = time.time()
    results = [download(url) for url in urls]
    single_time = time.time() - start
    print(f"  单线程: {single_time:.2f}秒")
    
    # 多线程
    start = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(download, urls))
    multi_time = time.time() - start
    print(f"  多线程: {multi_time:.2f}秒")
    print(f"  加速: {single_time/multi_time:.2f}x")
    
    # 2. 生产者-消费者模式
    print("\n2. 生产者-消费者:")
    
    q = queue.Queue(maxsize=5)
    stop_event = Event()
    
    def producer(name):
        """生产者"""
        count = 0
        while not stop_event.is_set():
            item = f"{name}-{count}"
            q.put(item)
            print(f"  {name} 生产: {item}")
            count += 1
            time.sleep(0.2)
    
    def consumer(name):
        """消费者"""
        while not stop_event.is_set() or not q.empty():
            try:
                item = q.get(timeout=1)
                print(f"  {name} 消费: {item}")
                q.task_done()
                time.sleep(0.3)
            except queue.Empty:
                continue
    
    # 创建生产者和消费者
    producers = [Thread(target=producer, args=(f"Producer-{i}",)) 
                 for i in range(2)]
    consumers = [Thread(target=consumer, args=(f"Consumer-{i}",)) 
                 for i in range(3)]
    
    for t in producers + consumers:
        t.start()
    
    time.sleep(2)  # 运行2秒
    stop_event.set()  # 停止生产
    
    for t in producers + consumers:
        t.join()
    
    # 3. 并发任务监控
    print("\n3. 任务监控:")
    
    class TaskMonitor:
        """任务监控器"""
        def __init__(self):
            self.lock = Lock()
            self.completed = 0
            self.failed = 0
        
        def task_completed(self):
            with self.lock:
                self.completed += 1
        
        def task_failed(self):
            with self.lock:
                self.failed += 1
        
        def report(self):
            with self.lock:
                total = self.completed + self.failed
                print(f"\n  完成: {self.completed}/{total}")
                print(f"  失败: {self.failed}/{total}")
    
    monitor = TaskMonitor()
    
    def monitored_task(task_id, monitor):
        """被监控的任务"""
        try:
            time.sleep(0.1)
            if task_id % 5 == 0:
                raise Exception("模拟失败")
            monitor.task_completed()
        except:
            monitor.task_failed()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(monitored_task, i, monitor) 
                   for i in range(20)]
        
        for future in as_completed(futures):
            pass  # 等待完成
    
    monitor.report()


# ============================================
# 7. 死锁示例与解决
# ============================================

def deadlock_demo():
    """死锁示例"""
    print("\n=== 死锁与解决 ===")
    
    print("1. 死锁示例（注释掉避免卡住）:")
    print("""
    lock1 = Lock()
    lock2 = Lock()
    
    def thread1():
        with lock1:
            time.sleep(0.1)
            with lock2:  # 等待 lock2
                print("Thread 1")
    
    def thread2():
        with lock2:
            time.sleep(0.1)
            with lock1:  # 等待 lock1
                print("Thread 2")
    
    # 这会导致死锁！
    """)
    
    print("\n2. 解决方案 - 按顺序获取锁:")
    lock1 = Lock()
    lock2 = Lock()
    
    def thread1():
        with lock1:
            with lock2:
                print("  Thread 1 完成")
    
    def thread2():
        with lock1:  # 与 thread1 相同的顺序
            with lock2:
                print("  Thread 2 完成")
    
    t1 = Thread(target=thread1)
    t2 = Thread(target=thread2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()


# ============================================
# 8. GIL 与最佳实践
# ============================================

def gil_and_best_practices():
    """GIL 与最佳实践"""
    print("\n=== GIL 与最佳实践 ===")
    
    print("""
    全局解释器锁 (GIL):
    - CPython 的 GIL 限制了真正的并行执行
    - 同一时间只有一个线程执行 Python 代码
    - IO操作会释放 GIL
    
    适用场景:
    ✓ IO密集型任务（网络、文件）
    ✓ 需要快速响应的任务
    ✓ 需要共享内存的任务
    
    不适用场景:
    ✗ CPU密集型任务（使用多进程）
    ✗ 需要真正并行的计算
    
    最佳实践:
    
    1. 选择合适的并发模型
       - IO密集型: 多线程
       - CPU密集型: 多进程
       - 混合: asyncio
    
    2. 使用线程池
       - ThreadPoolExecutor
       - 避免创建过多线程
    
    3. 避免共享状态
       - 使用 Queue 通信
       - 必要时使用锁
    
    4. 锁的使用
       - 尽量减少锁的范围
       - 避免嵌套锁
       - 使用 with 语句
    
    5. 异常处理
       - 线程中的异常不会传播
       - 使用 Future.result()
    
    6. 守护线程
       - 用于后台任务
       - 主线程结束时自动终止
    
    7. 线程数量
       - IO密集型: CPU核心数 * 2-4
       - 不要创建过多线程
    
    8. 性能分析
       - 测量实际性能提升
       - 考虑上下文切换开销
    
    9. 调试
       - 使用日志
       - 线程名称标识
       - 避免print（非线程安全）
    
    10. 资源清理
        - 使用 with 语句
        - join() 等待线程
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 多线程并发编程详解")
    print("=" * 60)
    
    thread_basics()
    thread_class()
    thread_synchronization()
    semaphore_demo()
    event_demo()
    condition_demo()
    thread_communication()
    thread_pool()
    thread_local_storage()
    
    print("\n" + "=" * 60)
    print("实战示例（需要网络）")
    print("=" * 60)
    try:
        practical_examples()
    except Exception as e:
        print(f"实战示例失败: {e}")
    
    deadlock_demo()
    gil_and_best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

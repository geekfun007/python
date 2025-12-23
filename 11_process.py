"""
Python 多进程编程详解
包含：multiprocessing、Process、Pool、进程通信等
"""

import multiprocessing as mp
from multiprocessing import Process, Queue, Pipe, Lock, Value, Array
from multiprocessing import Pool, Manager
import time
import os


# ============================================
# 1. 进程基础
# ============================================

def process_basics():
    """进程基础"""
    print("\n=== 进程基础 ===")
    
    # 创建进程
    def worker(name):
        """工作进程"""
        print(f"  进程 {name} (PID: {os.getpid()}) 开始")
        time.sleep(1)
        print(f"  进程 {name} 结束")
    
    print("1. 创建进程:")
    print(f"主进程 PID: {os.getpid()}")
    
    # 创建并启动进程
    p1 = Process(target=worker, args=("Worker-1",))
    p2 = Process(target=worker, args=("Worker-2",))
    
    p1.start()
    p2.start()
    
    # 等待进程完成
    p1.join()
    p2.join()
    
    print("所有进程完成")


def process_with_return():
    """进程返回值"""
    print("\n=== 进程返回值 ===")
    
    def square(n, result_queue):
        """计算平方并放入队列"""
        result = n * n
        result_queue.put((n, result))
    
    # 使用队列获取返回值
    result_queue = Queue()
    processes = []
    
    for i in range(5):
        p = Process(target=square, args=(i, result_queue))
        processes.append(p)
        p.start()
    
    # 等待所有进程完成
    for p in processes:
        p.join()
    
    # 获取结果
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    print("结果:", sorted(results))


# ============================================
# 2. 进程池
# ============================================

def process_pool():
    """进程池"""
    print("\n=== 进程池 ===")
    
    def task(x):
        """任务函数"""
        print(f"  处理 {x} (PID: {os.getpid()})")
        time.sleep(0.5)
        return x * x
    
    # 创建进程池
    print("1. Pool.map():")
    with Pool(processes=4) as pool:
        results = pool.map(task, range(8))
        print(f"结果: {results}")
    
    # apply_async - 异步执行
    print("\n2. Pool.apply_async():")
    with Pool(processes=4) as pool:
        async_results = [pool.apply_async(task, (i,)) for i in range(5)]
        results = [r.get() for r in async_results]
        print(f"结果: {results}")
    
    # starmap - 多个参数
    print("\n3. Pool.starmap():")
    def multiply(x, y):
        return x * y
    
    with Pool(processes=4) as pool:
        pairs = [(1, 2), (3, 4), (5, 6), (7, 8)]
        results = pool.starmap(multiply, pairs)
        print(f"结果: {results}")


# ============================================
# 3. 进程通信
# ============================================

def process_communication():
    """进程间通信"""
    print("\n=== 进程间通信 ===")
    
    # 1. Queue - 队列
    print("1. Queue:")
    def producer(queue):
        """生产者"""
        for i in range(5):
            print(f"  生产: {i}")
            queue.put(i)
            time.sleep(0.1)
        queue.put(None)  # 结束信号
    
    def consumer(queue):
        """消费者"""
        while True:
            item = queue.get()
            if item is None:
                break
            print(f"  消费: {item}")
            time.sleep(0.2)
    
    q = Queue()
    prod = Process(target=producer, args=(q,))
    cons = Process(target=consumer, args=(q,))
    
    prod.start()
    cons.start()
    
    prod.join()
    cons.join()
    
    # 2. Pipe - 管道
    print("\n2. Pipe:")
    def sender(conn):
        """发送者"""
        for i in range(5):
            conn.send(f"消息 {i}")
            time.sleep(0.1)
        conn.close()
    
    def receiver(conn):
        """接收者"""
        while True:
            try:
                msg = conn.recv()
                print(f"  接收: {msg}")
            except EOFError:
                break
    
    parent_conn, child_conn = Pipe()
    
    p1 = Process(target=sender, args=(child_conn,))
    p2 = Process(target=receiver, args=(parent_conn,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()


# ============================================
# 4. 进程同步
# ============================================

def process_synchronization():
    """进程同步"""
    print("\n=== 进程同步 ===")
    
    # Lock - 锁
    def increment_with_lock(counter, lock, n):
        """使用锁增加计数"""
        for _ in range(n):
            with lock:
                counter.value += 1
    
    def increment_without_lock(counter, n):
        """不使用锁增加计数"""
        for _ in range(n):
            counter.value += 1
    
    # 使用锁
    print("1. 使用 Lock:")
    counter = Value('i', 0)
    lock = Lock()
    
    processes = []
    for _ in range(4):
        p = Process(target=increment_with_lock, args=(counter, lock, 1000))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"  最终计数（使用锁）: {counter.value}")  # 应该是 4000
    
    # 不使用锁（可能出现竞态条件）
    print("\n2. 不使用 Lock（竞态条件）:")
    counter = Value('i', 0)
    
    processes = []
    for _ in range(4):
        p = Process(target=increment_without_lock, args=(counter, 1000))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"  最终计数（无锁）: {counter.value}")  # 可能小于 4000


# ============================================
# 5. 共享内存
# ============================================

def shared_memory():
    """共享内存"""
    print("\n=== 共享内存 ===")
    
    # Value - 共享值
    print("1. Value:")
    def worker(shared_num):
        shared_num.value += 10
        print(f"  进程 {os.getpid()}: {shared_num.value}")
    
    num = Value('i', 0)
    processes = [Process(target=worker, args=(num,)) for _ in range(3)]
    
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    
    print(f"最终值: {num.value}")
    
    # Array - 共享数组
    print("\n2. Array:")
    def fill_array(shared_array, index, value):
        shared_array[index] = value
        print(f"  设置 array[{index}] = {value}")
    
    arr = Array('i', 5)  # 5个整数的数组
    processes = []
    
    for i in range(5):
        p = Process(target=fill_array, args=(arr, i, i * 10))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"数组内容: {list(arr)}")


# ============================================
# 6. Manager - 高级共享
# ============================================

def manager_demo():
    """Manager 示例"""
    print("\n=== Manager ===")
    
    def worker(shared_dict, shared_list, index):
        """修改共享数据"""
        shared_dict[index] = index * index
        shared_list.append(index)
        print(f"  进程 {index}: 更新完成")
    
    with Manager() as manager:
        # 共享字典和列表
        shared_dict = manager.dict()
        shared_list = manager.list()
        
        processes = []
        for i in range(5):
            p = Process(target=worker, args=(shared_dict, shared_list, i))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
        
        print(f"共享字典: {dict(shared_dict)}")
        print(f"共享列表: {list(shared_list)}")


# ============================================
# 7. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 并行计算
    print("1. 并行计算素数:")
    def is_prime(n):
        """判断素数"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def find_primes(start, end):
        """查找范围内的素数"""
        primes = [n for n in range(start, end) if is_prime(n)]
        return primes
    
    # 单进程
    start_time = time.time()
    result = find_primes(1, 10000)
    single_time = time.time() - start_time
    print(f"  单进程找到 {len(result)} 个素数，耗时 {single_time:.2f}秒")
    
    # 多进程
    start_time = time.time()
    with Pool(processes=4) as pool:
        ranges = [(1, 2500), (2500, 5000), (5000, 7500), (7500, 10000)]
        results = pool.starmap(find_primes, ranges)
        all_primes = [p for sublist in results for p in sublist]
    multi_time = time.time() - start_time
    print(f"  多进程找到 {len(all_primes)} 个素数，耗时 {multi_time:.2f}秒")
    print(f"  加速比: {single_time/multi_time:.2f}x")
    
    # 2. 数据处理管道
    print("\n2. 数据处理管道:")
    def stage1(input_queue, output_queue):
        """阶段1: 数据生成"""
        for i in range(10):
            output_queue.put(i)
            time.sleep(0.05)
        output_queue.put(None)
    
    def stage2(input_queue, output_queue):
        """阶段2: 数据处理"""
        while True:
            data = input_queue.get()
            if data is None:
                output_queue.put(None)
                break
            output_queue.put(data * 2)
    
    def stage3(input_queue):
        """阶段3: 数据消费"""
        results = []
        while True:
            data = input_queue.get()
            if data is None:
                break
            results.append(data)
        print(f"  最终结果: {results}")
    
    q1 = Queue()
    q2 = Queue()
    
    p1 = Process(target=stage1, args=(None, q1))
    p2 = Process(target=stage2, args=(q1, q2))
    p3 = Process(target=stage3, args=(q2,))
    
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()


# ============================================
# 8. 最佳实践
# ============================================

def best_practices():
    """最佳实践"""
    print("\n=== 最佳实践 ===")
    
    print("""
    1. 使用进程池
       - Pool 自动管理进程
       - 避免创建过多进程
    
    2. 进程数量
       - CPU密集型: cpu_count()
       - IO密集型: 可以更多
    
    3. 进程通信
       - Queue: 多对多通信
       - Pipe: 一对一通信
       - Manager: 复杂数据结构
    
    4. 避免共享状态
       - 尽量使用消息传递
       - 必要时使用 Lock
    
    5. 异常处理
       - 子进程中捕获异常
       - 通过队列传递错误
    
    6. 资源清理
       - 使用 with 语句
       - join() 等待进程
    
    7. 进程启动方法
       - spawn (Windows默认)
       - fork (Unix默认)
       - forkserver
    
    8. 适用场景
       - CPU密集型任务
       - 需要真正并行
       - 避免GIL限制
    
    9. 注意事项
       - 进程开销大于线程
       - 进程间通信成本
       - 序列化限制
    
    10. 调试
        - 日志记录
        - 进程ID跟踪
        - 超时处理
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 多进程编程详解")
    print("=" * 60)
    
    # 注意：某些示例在非 __main__ 环境下可能不工作
    if __name__ == "__main__":
        process_basics()
        process_with_return()
        process_pool()
        process_communication()
        process_synchronization()
        shared_memory()
        manager_demo()
        practical_examples()
    
    best_practices()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    # Windows 需要这个保护
    mp.freeze_support()
    main()

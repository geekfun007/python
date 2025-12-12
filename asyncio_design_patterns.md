# Asyncio 设计模式

## 目录
- [1. 生产者-消费者模式](#1-生产者-消费者模式)
- [2. 任务池模式](#2-任务池模式)
- [3. 管道模式](#3-管道模式)
- [4. 扇出-扇入模式](#4-扇出-扇入模式)
- [5. 超时和重试模式](#5-超时和重试模式)
- [6. 断路器模式](#6-断路器模式)
- [7. 背压处理模式](#7-背压处理模式)
- [8. 优雅关闭模式](#8-优雅关闭模式)

---

## 1. 生产者-消费者模式

### 基本实现

```python
import asyncio
import random
from typing import Any

class ProducerConsumerPattern:
    def __init__(self, queue_size: int = 10):
        self.queue = asyncio.Queue(maxsize=queue_size)
    
    async def producer(self, name: str, num_items: int):
        """生产者：生成数据并放入队列"""
        for i in range(num_items):
            item = f"{name}-item-{i}"
            await self.queue.put(item)
            print(f"📦 生产者 {name} 生产: {item} (队列大小: {self.queue.qsize()})")
            await asyncio.sleep(random.uniform(0.1, 0.3))
        
        print(f"✅ 生产者 {name} 完成")
    
    async def consumer(self, name: str):
        """消费者：从队列获取并处理数据"""
        while True:
            try:
                item = await asyncio.wait_for(self.queue.get(), timeout=2.0)
                print(f"🔨 消费者 {name} 处理: {item}")
                await asyncio.sleep(random.uniform(0.2, 0.5))  # 模拟处理
                self.queue.task_done()
            except asyncio.TimeoutError:
                print(f"⏰ 消费者 {name} 超时退出")
                break
    
    async def run(self, num_producers: int = 2, num_consumers: int = 3, items_per_producer: int = 5):
        """运行生产者-消费者系统"""
        # 创建生产者任务
        producers = [
            asyncio.create_task(self.producer(f"P{i}", items_per_producer))
            for i in range(num_producers)
        ]
        
        # 创建消费者任务
        consumers = [
            asyncio.create_task(self.consumer(f"C{i}"))
            for i in range(num_consumers)
        ]
        
        # 等待所有生产者完成
        await asyncio.gather(*producers)
        print("\n✅ 所有生产者完成，等待队列清空...")
        
        # 等待队列被消费完
        await self.queue.join()
        print("✅ 队列已清空\n")
        
        # 取消消费者
        for consumer in consumers:
            consumer.cancel()
        
        await asyncio.gather(*consumers, return_exceptions=True)

# 使用示例
async def main():
    pattern = ProducerConsumerPattern(queue_size=5)
    await pattern.run(num_producers=2, num_consumers=3, items_per_producer=5)

# asyncio.run(main())
```

### 优先级队列版本

```python
import asyncio
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PriorityItem:
    priority: int
    data: Any = field(compare=False)

class PriorityProducerConsumer:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
    
    async def producer(self, name: str):
        for i in range(5):
            priority = random.randint(1, 5)
            item = PriorityItem(priority=priority, data=f"{name}-{i}")
            await self.queue.put(item)
            print(f"生产 (优先级 {priority}): {item.data}")
            await asyncio.sleep(0.5)
    
    async def consumer(self, name: str):
        while True:
            try:
                item = await asyncio.wait_for(self.queue.get(), timeout=3.0)
                print(f"{name} 处理 (优先级 {item.priority}): {item.data}")
                await asyncio.sleep(0.3)
                self.queue.task_done()
            except asyncio.TimeoutError:
                break

# 使用示例类似上面
```

---

## 2. 任务池模式

### Worker Pool 实现

```python
import asyncio
from typing import Callable, Any, List
import random

class WorkerPool:
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self.task_queue = asyncio.Queue()
        self.results = []
        self.workers = []
    
    async def worker(self, worker_id: int):
        """工作线程从队列获取任务并执行"""
        print(f"🏃 Worker-{worker_id} 启动")
        
        while True:
            try:
                # 获取任务
                task_func, args = await self.task_queue.get()
                
                if task_func is None:  # 毒丸：停止信号
                    print(f"💊 Worker-{worker_id} 收到停止信号")
                    break
                
                print(f"🔨 Worker-{worker_id} 执行任务 {args}")
                
                # 执行任务
                result = await task_func(*args)
                self.results.append(result)
                
                print(f"✅ Worker-{worker_id} 完成任务 {args}")
                
                self.task_queue.task_done()
            
            except Exception as e:
                print(f"❌ Worker-{worker_id} 错误: {e}")
                self.task_queue.task_done()
        
        print(f"🛑 Worker-{worker_id} 退出")
    
    async def submit(self, task_func: Callable, *args):
        """提交任务到队列"""
        await self.task_queue.put((task_func, args))
    
    async def start(self):
        """启动所有工作线程"""
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.num_workers)
        ]
    
    async def shutdown(self, wait: bool = True):
        """关闭工作池"""
        if wait:
            # 等待所有任务完成
            await self.task_queue.join()
        
        # 发送停止信号给所有 worker
        for _ in range(self.num_workers):
            await self.task_queue.put((None, None))
        
        # 等待所有 worker 退出
        await asyncio.gather(*self.workers)
        
        print(f"🏁 Worker Pool 关闭，处理了 {len(self.results)} 个任务")

# 示例任务
async def process_data(data_id: int):
    """模拟数据处理"""
    await asyncio.sleep(random.uniform(0.5, 1.5))
    return f"结果-{data_id}"

async def main():
    # 创建 3 个 worker 的池
    pool = WorkerPool(num_workers=3)
    await pool.start()
    
    # 提交 10 个任务
    for i in range(10):
        await pool.submit(process_data, i)
    
    # 关闭池
    await pool.shutdown(wait=True)
    
    print(f"所有结果: {pool.results}")

# asyncio.run(main())
```

### 使用 Semaphore 的简化版本

```python
import asyncio
from typing import List, Callable

class SimplePool:
    def __init__(self, max_workers: int):
        self.semaphore = asyncio.Semaphore(max_workers)
    
    async def execute(self, func: Callable, *args):
        """在池中执行函数"""
        async with self.semaphore:
            return await func(*args)
    
    async def map(self, func: Callable, items: List[Any]) -> List[Any]:
        """并发执行多个任务"""
        tasks = [self.execute(func, item) for item in items]
        return await asyncio.gather(*tasks)

# 使用示例
async def process(item):
    await asyncio.sleep(1)
    return item * 2

async def main():
    pool = SimplePool(max_workers=3)
    results = await pool.map(process, range(10))
    print(results)

# asyncio.run(main())
```

---

## 3. 管道模式

### 数据处理管道

```python
import asyncio
from typing import AsyncIterator, Callable, Any

class Pipeline:
    def __init__(self):
        self.stages = []
    
    def add_stage(self, func: Callable):
        """添加管道阶段"""
        self.stages.append(func)
        return self
    
    async def process(self, data_stream: AsyncIterator[Any]) -> AsyncIterator[Any]:
        """通过管道处理数据流"""
        async for data in data_stream:
            result = data
            
            # 依次通过每个阶段
            for stage in self.stages:
                result = await stage(result)
            
            yield result

# 定义管道阶段
async def fetch_stage(url: str):
    """阶段 1: 获取数据"""
    print(f"📥 获取: {url}")
    await asyncio.sleep(0.5)
    return {"url": url, "data": f"content-from-{url}"}

async def parse_stage(data: dict):
    """阶段 2: 解析数据"""
    print(f"🔍 解析: {data['url']}")
    await asyncio.sleep(0.3)
    data["parsed"] = data["data"].upper()
    return data

async def transform_stage(data: dict):
    """阶段 3: 转换数据"""
    print(f"🔄 转换: {data['url']}")
    await asyncio.sleep(0.2)
    data["transformed"] = f"[{data['parsed']}]"
    return data

async def save_stage(data: dict):
    """阶段 4: 保存数据"""
    print(f"💾 保存: {data['url']}")
    await asyncio.sleep(0.3)
    return data["transformed"]

# 数据源生成器
async def data_source():
    """生成输入数据"""
    urls = ["url1", "url2", "url3", "url4", "url5"]
    for url in urls:
        yield url
        await asyncio.sleep(0.1)

async def main():
    # 构建管道
    pipeline = Pipeline()
    pipeline.add_stage(fetch_stage)
    pipeline.add_stage(parse_stage)
    pipeline.add_stage(transform_stage)
    pipeline.add_stage(save_stage)
    
    # 处理数据
    results = []
    async for result in pipeline.process(data_source()):
        print(f"✅ 完成: {result}\n")
        results.append(result)
    
    print(f"所有结果: {results}")

# asyncio.run(main())
```

### 并发管道（每个阶段并发处理）

```python
import asyncio
from typing import AsyncIterator

class ConcurrentPipeline:
    def __init__(self, max_concurrent: int = 3):
        self.stages = []
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    def add_stage(self, func):
        self.stages.append(func)
        return self
    
    async def _process_item(self, item):
        """处理单个项目通过所有阶段"""
        async with self.semaphore:
            result = item
            for stage in self.stages:
                result = await stage(result)
            return result
    
    async def process(self, data_stream: AsyncIterator):
        """并发处理数据流"""
        tasks = []
        async for item in data_stream:
            task = asyncio.create_task(self._process_item(item))
            tasks.append(task)
        
        return await asyncio.gather(*tasks)

# 使用方式类似上面
```

---

## 4. 扇出-扇入模式

### Fan-Out / Fan-In

```python
import asyncio
from typing import List, Any

class FanOutFanIn:
    """扇出-扇入模式：将任务分发到多个 worker，然后聚合结果"""
    
    @staticmethod
    async def fan_out(data: Any, workers: List[callable]) -> List[Any]:
        """扇出：将数据分发给多个 worker 并发处理"""
        print(f"🌟 扇出: 分发数据到 {len(workers)} 个 worker")
        
        tasks = [worker(data) for worker in workers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    @staticmethod
    async def fan_in(results: List[Any]) -> Any:
        """扇入：聚合多个结果"""
        print(f"🌟 扇入: 聚合 {len(results)} 个结果")
        
        # 过滤掉异常
        valid_results = [r for r in results if not isinstance(r, Exception)]
        
        # 简单聚合示例：求和
        if all(isinstance(r, (int, float)) for r in valid_results):
            return sum(valid_results)
        else:
            return valid_results

# 定义不同的 worker
async def worker_add(data: int) -> int:
    """Worker 1: 加 10"""
    await asyncio.sleep(0.5)
    result = data + 10
    print(f"  Worker-Add: {data} + 10 = {result}")
    return result

async def worker_multiply(data: int) -> int:
    """Worker 2: 乘 2"""
    await asyncio.sleep(0.7)
    result = data * 2
    print(f"  Worker-Multiply: {data} * 2 = {result}")
    return result

async def worker_square(data: int) -> int:
    """Worker 3: 平方"""
    await asyncio.sleep(0.3)
    result = data ** 2
    print(f"  Worker-Square: {data} ** 2 = {result}")
    return result

async def worker_with_error(data: int) -> int:
    """Worker 4: 会抛出异常"""
    await asyncio.sleep(0.2)
    raise ValueError("模拟错误")

async def main():
    pattern = FanOutFanIn()
    
    # 输入数据
    input_data = 5
    
    # 定义 workers
    workers = [
        worker_add,
        worker_multiply,
        worker_square,
        worker_with_error,  # 这个会失败
    ]
    
    # 扇出
    results = await pattern.fan_out(input_data, workers)
    print(f"\n扇出结果: {results}")
    
    # 扇入
    final_result = await pattern.fan_in(results)
    print(f"扇入最终结果: {final_result}")

# asyncio.run(main())
```

### Map-Reduce 模式

```python
import asyncio
from typing import List, Callable, Any

class MapReduce:
    """Map-Reduce 模式实现"""
    
    @staticmethod
    async def map_async(mapper: Callable, data: List[Any], max_concurrent: int = 5) -> List[Any]:
        """Map 阶段：并发应用映射函数"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def bounded_map(item):
            async with semaphore:
                return await mapper(item)
        
        tasks = [bounded_map(item) for item in data]
        return await asyncio.gather(*tasks)
    
    @staticmethod
    async def reduce_async(reducer: Callable, data: List[Any], initial: Any = None) -> Any:
        """Reduce 阶段：归约结果"""
        result = initial if initial is not None else data[0]
        
        for item in data if initial is None else data:
            result = await reducer(result, item)
        
        return result

# 示例：并发计算平方和
async def square_mapper(x: int) -> int:
    """映射函数：计算平方"""
    await asyncio.sleep(0.1)  # 模拟异步操作
    result = x ** 2
    print(f"Map: {x} -> {result}")
    return result

async def sum_reducer(acc: int, x: int) -> int:
    """归约函数：求和"""
    await asyncio.sleep(0.05)
    result = acc + x
    print(f"Reduce: {acc} + {x} = {result}")
    return result

async def main():
    mr = MapReduce()
    
    # 数据
    numbers = list(range(1, 11))  # [1, 2, 3, ..., 10]
    
    print("=== Map 阶段 ===")
    mapped = await mr.map_async(square_mapper, numbers, max_concurrent=3)
    print(f"映射结果: {mapped}")
    
    print("\n=== Reduce 阶段 ===")
    total = await mr.reduce_async(sum_reducer, mapped, initial=0)
    print(f"最终结果: {total}")  # 1^2 + 2^2 + ... + 10^2 = 385

# asyncio.run(main())
```

---

## 5. 超时和重试模式

### 带重试的异步操作

```python
import asyncio
from typing import Callable, Any
import random

class RetryPattern:
    """重试模式实现"""
    
    @staticmethod
    async def retry_with_exponential_backoff(
        func: Callable,
        *args,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
        max_delay: float = 60.0,
        **kwargs
    ) -> Any:
        """指数退避重试"""
        delay = initial_delay
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                print(f"🔄 尝试 {attempt + 1}/{max_retries + 1}")
                result = await func(*args, **kwargs)
                print(f"✅ 成功!")
                return result
            
            except Exception as e:
                last_exception = e
                
                if attempt < max_retries:
                    print(f"❌ 失败: {e}，{delay:.1f}秒后重试...")
                    await asyncio.sleep(delay)
                    delay = min(delay * backoff_factor, max_delay)
                else:
                    print(f"❌ 已达最大重试次数")
        
        raise last_exception
    
    @staticmethod
    async def retry_with_timeout(
        func: Callable,
        *args,
        max_retries: int = 3,
        timeout: float = 5.0,
        delay: float = 1.0,
        **kwargs
    ) -> Any:
        """带超时的重试"""
        for attempt in range(max_retries):
            try:
                print(f"🔄 尝试 {attempt + 1}/{max_retries} (超时: {timeout}秒)")
                result = await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=timeout
                )
                print(f"✅ 成功!")
                return result
            
            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    print(f"⏰ 超时，{delay}秒后重试...")
                    await asyncio.sleep(delay)
                else:
                    print(f"❌ 超时，已达最大重试次数")
                    raise
            
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"❌ 错误: {e}，{delay}秒后重试...")
                    await asyncio.sleep(delay)
                else:
                    print(f"❌ 错误，已达最大重试次数")
                    raise

# 模拟不稳定的异步操作
async def unstable_operation(success_rate: float = 0.3):
    """模拟不稳定的操作"""
    await asyncio.sleep(0.5)
    
    if random.random() < success_rate:
        return "操作成功!"
    else:
        raise ConnectionError("网络错误")

async def slow_operation():
    """模拟慢操作"""
    await asyncio.sleep(10)  # 会超时
    return "完成"

async def main():
    retry = RetryPattern()
    
    print("=== 测试指数退避重试 ===")
    try:
        result = await retry.retry_with_exponential_backoff(
            unstable_operation,
            success_rate=0.4,
            max_retries=5,
            initial_delay=0.5,
            backoff_factor=2.0
        )
        print(f"结果: {result}\n")
    except Exception as e:
        print(f"最终失败: {e}\n")
    
    print("=== 测试带超时的重试 ===")
    try:
        result = await retry.retry_with_timeout(
            slow_operation,
            max_retries=3,
            timeout=2.0,
            delay=0.5
        )
        print(f"结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")

# asyncio.run(main())
```

### 装饰器版本

```python
import asyncio
from functools import wraps
from typing import Callable

def async_retry(max_retries: int = 3, delay: float = 1.0):
    """异步重试装饰器"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        print(f"重试 {attempt + 1}/{max_retries}: {e}")
                        await asyncio.sleep(delay)
            
            raise last_exception
        
        return wrapper
    return decorator

# 使用装饰器
@async_retry(max_retries=3, delay=0.5)
async def fetch_data(url: str):
    if random.random() < 0.7:
        raise ConnectionError(f"无法连接到 {url}")
    return f"数据来自 {url}"

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

# asyncio.run(main())
```

---

## 6. 断路器模式

### Circuit Breaker 实现

```python
import asyncio
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"      # 正常状态
    OPEN = "open"          # 断开状态（快速失败）
    HALF_OPEN = "half_open"  # 半开状态（尝试恢复）

class CircuitBreaker:
    """断路器模式实现"""
    
    def __init__(
        self,
        failure_threshold: int = 5,      # 失败阈值
        success_threshold: int = 2,      # 成功阈值（半开状态）
        timeout: float = 60.0,           # 打开状态持续时间
    ):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
    
    def _should_attempt_reset(self) -> bool:
        """检查是否应该尝试重置"""
        if self.state == CircuitState.OPEN and self.last_failure_time:
            elapsed = (datetime.now() - self.last_failure_time).total_seconds()
            return elapsed >= self.timeout
        return False
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """通过断路器调用函数"""
        
        # 如果断路器打开且超时，尝试半开状态
        if self._should_attempt_reset():
            self.state = CircuitState.HALF_OPEN
            self.success_count = 0
            print("🔄 断路器进入半开状态")
        
        # 如果断路器打开，快速失败
        if self.state == CircuitState.OPEN:
            raise Exception("断路器打开：服务不可用")
        
        try:
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 成功处理
            self._on_success()
            
            return result
        
        except Exception as e:
            # 失败处理
            self._on_failure()
            raise
    
    def _on_success(self):
        """成功回调"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            print(f"✅ 半开状态成功 {self.success_count}/{self.success_threshold}")
            
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                print("✅ 断路器关闭：服务恢复正常")
    
    def _on_failure(self):
        """失败回调"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        print(f"❌ 失败 {self.failure_count}/{self.failure_threshold}")
        
        if self.state == CircuitState.HALF_OPEN:
            # 半开状态失败，重新打开
            self.state = CircuitState.OPEN
            self.failure_count = 0
            print("⚠️ 断路器重新打开")
        
        elif self.failure_count >= self.failure_threshold:
            # 达到失败阈值，打开断路器
            self.state = CircuitState.OPEN
            print("⚠️ 断路器打开：服务暂时不可用")
    
    def get_state(self) -> CircuitState:
        """获取当前状态"""
        return self.state

# 模拟不稳定的服务
class UnstableService:
    def __init__(self):
        self.call_count = 0
        self.should_fail = True
    
    async def call(self, data: str):
        """模拟服务调用"""
        self.call_count += 1
        await asyncio.sleep(0.5)
        
        # 前 7 次调用失败，之后恢复
        if self.call_count <= 7:
            raise ConnectionError(f"服务错误 (调用 #{self.call_count})")
        
        return f"成功处理: {data} (调用 #{self.call_count})"

async def main():
    service = UnstableService()
    breaker = CircuitBreaker(
        failure_threshold=3,
        success_threshold=2,
        timeout=5.0
    )
    
    for i in range(15):
        try:
            print(f"\n--- 请求 {i + 1} (断路器状态: {breaker.get_state().value}) ---")
            result = await breaker.call(service.call, f"数据-{i}")
            print(f"✅ {result}")
        
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        await asyncio.sleep(1)  # 每次请求间隔 1 秒
        
        # 在第 10 次请求后等待超时
        if i == 9:
            print("\n⏰ 等待 6 秒让断路器超时...")
            await asyncio.sleep(6)

# asyncio.run(main())
```

---

## 7. 背压处理模式

### 背压控制

```python
import asyncio
from typing import Callable, Any

class BackpressureQueue:
    """带背压控制的队列"""
    
    def __init__(self, maxsize: int = 10, high_water: int = 8, low_water: int = 3):
        self.queue = asyncio.Queue(maxsize=maxsize)
        self.high_water = high_water
        self.low_water = low_water
        self.paused = False
        self.pause_event = asyncio.Event()
        self.pause_event.set()  # 初始不暂停
    
    async def put(self, item: Any):
        """生产者放入数据"""
        # 等待恢复信号
        await self.pause_event.wait()
        
        await self.queue.put(item)
        
        # 检查是否达到高水位
        if not self.paused and self.queue.qsize() >= self.high_water:
            self.paused = True
            self.pause_event.clear()
            print(f"⚠️ 背压触发：队列大小 {self.queue.qsize()} >= {self.high_water}")
    
    async def get(self) -> Any:
        """消费者获取数据"""
        item = await self.queue.get()
        
        # 检查是否降到低水位
        if self.paused and self.queue.qsize() <= self.low_water:
            self.paused = False
            self.pause_event.set()
            print(f"✅ 背压解除：队列大小 {self.queue.qsize()} <= {self.low_water}")
        
        return item
    
    def task_done(self):
        self.queue.task_done()
    
    async def join(self):
        await self.queue.join()

# 快速生产者
async def fast_producer(queue: BackpressureQueue, producer_id: int):
    """快速生产数据"""
    for i in range(20):
        item = f"P{producer_id}-{i}"
        print(f"📦 生产者 {producer_id} 准备生产: {item}")
        await queue.put(item)
        print(f"📦 生产者 {producer_id} 已生产: {item} (队列: {queue.queue.qsize()})")
        await asyncio.sleep(0.1)  # 快速生产

# 慢速消费者
async def slow_consumer(queue: BackpressureQueue, consumer_id: int):
    """慢速消费数据"""
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=5.0)
            print(f"🔨 消费者 {consumer_id} 处理: {item}")
            await asyncio.sleep(0.5)  # 慢速消费
            queue.task_done()
        except asyncio.TimeoutError:
            print(f"⏰ 消费者 {consumer_id} 超时退出")
            break

async def main():
    queue = BackpressureQueue(maxsize=10, high_water=8, low_water=3)
    
    # 2 个快速生产者
    producers = [
        asyncio.create_task(fast_producer(queue, i))
        for i in range(2)
    ]
    
    # 1 个慢速消费者
    consumers = [
        asyncio.create_task(slow_consumer(queue, 0))
    ]
    
    await asyncio.gather(*producers)
    await queue.join()
    
    for consumer in consumers:
        consumer.cancel()

# asyncio.run(main())
```

---

## 8. 优雅关闭模式

### Graceful Shutdown

```python
import asyncio
import signal
from typing import Set

class GracefulShutdown:
    """优雅关闭管理器"""
    
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.tasks: Set[asyncio.Task] = set()
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """设置信号处理器"""
        # 注意：这在 Windows 上可能有限制
        try:
            for sig in (signal.SIGTERM, signal.SIGINT):
                signal.signal(sig, self._signal_handler)
        except (ValueError, OSError):
            # Windows 或其他平台可能不支持某些信号
            pass
    
    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        print(f"\n🛑 收到信号 {signum}，开始优雅关闭...")
        self.shutdown_event.set()
    
    def create_task(self, coro):
        """创建并跟踪任务"""
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return task
    
    async def wait_for_shutdown(self):
        """等待关闭信号"""
        await self.shutdown_event.wait()
    
    async def shutdown(self, timeout: float = 5.0):
        """执行优雅关闭"""
        print(f"📝 取消 {len(self.tasks)} 个运行中的任务...")
        
        # 取消所有任务
        for task in self.tasks:
            task.cancel()
        
        # 等待所有任务完成或超时
        try:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True),
                timeout=timeout
            )
            print("✅ 所有任务已完成")
        except asyncio.TimeoutError:
            print(f"⚠️ 超时：部分任务未能在 {timeout} 秒内完成")

# 示例应用
class Application:
    def __init__(self):
        self.shutdown_manager = GracefulShutdown()
        self.running = True
    
    async def worker(self, worker_id: int):
        """工作任务"""
        try:
            while self.running:
                print(f"Worker {worker_id} 工作中...")
                await asyncio.sleep(2)
        except asyncio.CancelledError:
            print(f"Worker {worker_id} 收到取消信号，清理资源...")
            await asyncio.sleep(1)  # 模拟清理工作
            print(f"Worker {worker_id} 已清理完成")
            raise
    
    async def run(self):
        """运行应用"""
        print("🚀 应用启动")
        
        # 创建多个 worker
        for i in range(3):
            self.shutdown_manager.create_task(self.worker(i))
        
        # 等待关闭信号
        await self.shutdown_manager.wait_for_shutdown()
        
        # 标记停止
        self.running = False
        
        # 执行关闭
        await self.shutdown_manager.shutdown(timeout=5.0)
        
        print("👋 应用已关闭")

async def main():
    app = Application()
    try:
        await app.run()
    except KeyboardInterrupt:
        print("\n⌨️ 检测到键盘中断")

# asyncio.run(main())
# 运行后按 Ctrl+C 触发优雅关闭
```

### 上下文管理器版本

```python
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_service(name: str):
    """托管服务的上下文管理器"""
    print(f"🚀 启动服务: {name}")
    
    # 初始化资源
    tasks = []
    
    try:
        yield tasks
    finally:
        # 清理资源
        print(f"🛑 关闭服务: {name}")
        
        for task in tasks:
            task.cancel()
        
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"✅ 服务 {name} 已关闭")

async def service_worker(name: str):
    """服务工作任务"""
    try:
        while True:
            print(f"{name} 运行中...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print(f"{name} 被取消")
        raise

async def main():
    async with managed_service("MyService") as tasks:
        # 创建工作任务
        tasks.append(asyncio.create_task(service_worker("Worker-1")))
        tasks.append(asyncio.create_task(service_worker("Worker-2")))
        
        # 运行一段时间
        await asyncio.sleep(5)
        
        # 退出 context manager 会自动清理

# asyncio.run(main())
```

---

## 总结

这些设计模式涵盖了 asyncio 编程中最常见的场景：

1. **生产者-消费者**: 解耦数据生成和处理
2. **任务池**: 限制并发数量，资源管理
3. **管道**: 数据流式处理
4. **扇出-扇入**: 并行处理和结果聚合
5. **超时重试**: 处理不稳定的服务
6. **断路器**: 快速失败，保护系统
7. **背压控制**: 防止生产者压垮消费者
8. **优雅关闭**: 确保资源正确释放

掌握这些模式可以帮助你构建健壮、高效的异步应用！

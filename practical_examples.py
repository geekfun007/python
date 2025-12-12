"""
Asyncio 实战示例
================
包含真实场景的异步编程示例
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Any
import json


# ============================================================================
# 示例 1: 并发 HTTP 请求
# ============================================================================

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """异步获取 URL"""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            return {
                "url": url,
                "status": response.status,
                "data": await response.text()
            }
    except asyncio.TimeoutError:
        return {"url": url, "error": "Timeout"}
    except Exception as e:
        return {"url": url, "error": str(e)}


async def fetch_multiple_urls(urls: List[str]) -> List[Dict[str, Any]]:
    """并发获取多个 URL"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results


async def example_http_requests():
    """示例：并发 HTTP 请求"""
    print("=== 示例 1: 并发 HTTP 请求 ===\n")
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
    ]
    
    start = time.time()
    results = await fetch_multiple_urls(urls)
    elapsed = time.time() - start
    
    print(f"获取 {len(urls)} 个 URL 耗时: {elapsed:.2f} 秒")
    print(f"如果顺序执行需要约 {sum([1, 2, 1])} 秒")
    
    for result in results:
        if "error" in result:
            print(f"❌ {result['url']}: {result['error']}")
        else:
            print(f"✅ {result['url']}: {result['status']}")


# ============================================================================
# 示例 2: 数据库连接池模拟
# ============================================================================

class AsyncDatabasePool:
    """异步数据库连接池模拟"""
    
    def __init__(self, pool_size: int = 5):
        self.pool_size = pool_size
        self.semaphore = asyncio.Semaphore(pool_size)
        self.active_connections = 0
    
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """执行数据库查询"""
        async with self.semaphore:
            self.active_connections += 1
            conn_id = self.active_connections
            
            print(f"  🔗 连接 #{conn_id}: 执行查询: {query}")
            
            # 模拟查询时间
            await asyncio.sleep(1)
            
            result = {
                "query": query,
                "connection_id": conn_id,
                "rows": [{"id": i, "data": f"row-{i}"} for i in range(3)]
            }
            
            print(f"  ✅ 连接 #{conn_id}: 查询完成")
            self.active_connections -= 1
            
            return result


async def example_database_pool():
    """示例：数据库连接池"""
    print("\n=== 示例 2: 数据库连接池 ===\n")
    
    pool = AsyncDatabasePool(pool_size=3)
    
    # 创建 10 个查询，但只有 3 个连接
    queries = [f"SELECT * FROM table_{i}" for i in range(10)]
    
    start = time.time()
    tasks = [pool.execute_query(query) for query in queries]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start
    
    print(f"\n执行 {len(queries)} 个查询耗时: {elapsed:.2f} 秒")
    print(f"使用连接池大小: {pool.pool_size}")
    print(f"平均每个查询: {elapsed/len(queries):.2f} 秒")


# ============================================================================
# 示例 3: 实时数据流处理
# ============================================================================

class DataStreamProcessor:
    """实时数据流处理器"""
    
    def __init__(self, buffer_size: int = 10):
        self.buffer = asyncio.Queue(maxsize=buffer_size)
        self.processed_count = 0
    
    async def produce_data(self, source_id: int, num_items: int):
        """生产数据流"""
        for i in range(num_items):
            data = {
                "source_id": source_id,
                "sequence": i,
                "timestamp": time.time(),
                "value": i * 10
            }
            
            await self.buffer.put(data)
            print(f"📡 源 {source_id} 产生数据: seq={i}")
            await asyncio.sleep(0.3)
    
    async def process_data(self, processor_id: int):
        """处理数据流"""
        while True:
            try:
                data = await asyncio.wait_for(self.buffer.get(), timeout=2.0)
                
                # 模拟数据处理
                await asyncio.sleep(0.5)
                
                self.processed_count += 1
                print(f"  ⚙️ 处理器 {processor_id} 处理: 源={data['source_id']}, "
                      f"seq={data['sequence']}, value={data['value']}")
                
                self.buffer.task_done()
            
            except asyncio.TimeoutError:
                print(f"  ⏰ 处理器 {processor_id} 完成")
                break
    
    async def monitor(self):
        """监控数据流"""
        while True:
            await asyncio.sleep(1)
            print(f"📊 监控: 缓冲区={self.buffer.qsize()}, 已处理={self.processed_count}")
            
            if self.buffer.empty() and self.processed_count > 0:
                break


async def example_stream_processing():
    """示例：实时数据流处理"""
    print("\n=== 示例 3: 实时数据流处理 ===\n")
    
    processor = DataStreamProcessor(buffer_size=5)
    
    # 创建多个数据源和处理器
    sources = [
        asyncio.create_task(processor.produce_data(source_id=i, num_items=5))
        for i in range(2)
    ]
    
    processors = [
        asyncio.create_task(processor.process_data(processor_id=i))
        for i in range(3)
    ]
    
    monitor = asyncio.create_task(processor.monitor())
    
    # 等待所有数据源完成
    await asyncio.gather(*sources)
    
    # 等待缓冲区清空
    await processor.buffer.join()
    
    # 取消处理器和监控
    for p in processors:
        p.cancel()
    monitor.cancel()
    
    await asyncio.gather(*processors, monitor, return_exceptions=True)
    
    print(f"\n✅ 总共处理 {processor.processed_count} 条数据")


# ============================================================================
# 示例 4: 微服务调用编排
# ============================================================================

class MicroserviceOrchestrator:
    """微服务调用编排器"""
    
    async def call_user_service(self, user_id: int) -> Dict[str, Any]:
        """调用用户服务"""
        await asyncio.sleep(0.5)
        return {
            "user_id": user_id,
            "name": f"User-{user_id}",
            "email": f"user{user_id}@example.com"
        }
    
    async def call_order_service(self, user_id: int) -> List[Dict[str, Any]]:
        """调用订单服务"""
        await asyncio.sleep(0.7)
        return [
            {"order_id": i, "amount": 100 * i, "status": "completed"}
            for i in range(1, 4)
        ]
    
    async def call_recommendation_service(self, user_id: int) -> List[str]:
        """调用推荐服务"""
        await asyncio.sleep(0.3)
        return [f"Product-{i}" for i in range(5)]
    
    async def call_analytics_service(self, user_id: int) -> Dict[str, Any]:
        """调用分析服务"""
        await asyncio.sleep(0.4)
        return {
            "page_views": 150,
            "purchases": 5,
            "avg_session_duration": 300
        }
    
    async def get_user_dashboard(self, user_id: int) -> Dict[str, Any]:
        """获取用户仪表板（编排多个服务调用）"""
        print(f"🔄 开始获取用户 {user_id} 的仪表板数据...")
        
        start = time.time()
        
        # 并发调用多个微服务
        user_data, orders, recommendations, analytics = await asyncio.gather(
            self.call_user_service(user_id),
            self.call_order_service(user_id),
            self.call_recommendation_service(user_id),
            self.call_analytics_service(user_id)
        )
        
        elapsed = time.time() - start
        
        dashboard = {
            "user": user_data,
            "orders": orders,
            "recommendations": recommendations,
            "analytics": analytics,
            "fetch_time": f"{elapsed:.2f}s"
        }
        
        print(f"✅ 仪表板数据获取完成，耗时 {elapsed:.2f} 秒")
        
        return dashboard


async def example_microservice_orchestration():
    """示例：微服务编排"""
    print("\n=== 示例 4: 微服务调用编排 ===\n")
    
    orchestrator = MicroserviceOrchestrator()
    
    dashboard = await orchestrator.get_user_dashboard(user_id=123)
    
    print(f"\n用户: {dashboard['user']['name']}")
    print(f"订单数: {len(dashboard['orders'])}")
    print(f"推荐产品: {len(dashboard['recommendations'])} 个")
    print(f"页面浏览: {dashboard['analytics']['page_views']}")
    print(f"\n如果顺序调用这些服务需要: 0.5 + 0.7 + 0.3 + 0.4 = 1.9 秒")
    print(f"并发调用实际耗时: {dashboard['fetch_time']}")


# ============================================================================
# 示例 5: 批量任务处理器
# ============================================================================

class BatchProcessor:
    """批量任务处理器"""
    
    def __init__(self, batch_size: int = 5, max_concurrent: int = 3):
        self.batch_size = batch_size
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_item(self, item: Any) -> Any:
        """处理单个项目"""
        async with self.semaphore:
            await asyncio.sleep(0.5)  # 模拟处理
            return f"processed-{item}"
    
    async def process_batch(self, batch: List[Any]) -> List[Any]:
        """处理一批项目"""
        print(f"  📦 处理批次: {len(batch)} 个项目")
        tasks = [self.process_item(item) for item in batch]
        results = await asyncio.gather(*tasks)
        print(f"  ✅ 批次完成")
        return results
    
    async def process_all(self, items: List[Any]) -> List[Any]:
        """处理所有项目（分批）"""
        all_results = []
        
        # 分批处理
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            total_batches = (len(items) + self.batch_size - 1) // self.batch_size
            
            print(f"\n批次 {batch_num}/{total_batches}")
            results = await self.process_batch(batch)
            all_results.extend(results)
        
        return all_results


async def example_batch_processing():
    """示例：批量任务处理"""
    print("\n=== 示例 5: 批量任务处理 ===\n")
    
    processor = BatchProcessor(batch_size=5, max_concurrent=3)
    
    # 100 个项目
    items = list(range(100))
    
    start = time.time()
    results = await processor.process_all(items)
    elapsed = time.time() - start
    
    print(f"\n处理 {len(items)} 个项目耗时: {elapsed:.2f} 秒")
    print(f"每批 {processor.batch_size} 个，最多并发 {processor.semaphore._value} 个")
    print(f"结果数量: {len(results)}")


# ============================================================================
# 示例 6: 缓存系统
# ============================================================================

class AsyncCache:
    """异步缓存系统"""
    
    def __init__(self, ttl: float = 5.0):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.locks: Dict[str, asyncio.Lock] = {}
        self.ttl = ttl
    
    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """检查缓存是否过期"""
        return time.time() - entry["timestamp"] > self.ttl
    
    async def get_or_fetch(
        self, 
        key: str, 
        fetch_func: callable, 
        *args, 
        **kwargs
    ) -> Any:
        """获取缓存或从源获取"""
        
        # 检查缓存
        if key in self.cache and not self._is_expired(self.cache[key]):
            print(f"  💾 缓存命中: {key}")
            return self.cache[key]["value"]
        
        # 获取或创建锁
        if key not in self.locks:
            self.locks[key] = asyncio.Lock()
        
        # 使用锁防止并发获取相同数据
        async with self.locks[key]:
            # 再次检查（可能其他协程已经获取了）
            if key in self.cache and not self._is_expired(self.cache[key]):
                print(f"  💾 缓存命中（双重检查）: {key}")
                return self.cache[key]["value"]
            
            # 从源获取
            print(f"  🔍 缓存未命中，获取数据: {key}")
            value = await fetch_func(*args, **kwargs)
            
            # 存入缓存
            self.cache[key] = {
                "value": value,
                "timestamp": time.time()
            }
            
            return value
    
    def invalidate(self, key: str):
        """使缓存失效"""
        if key in self.cache:
            del self.cache[key]
            print(f"  🗑️ 缓存失效: {key}")


async def expensive_operation(item_id: int) -> Dict[str, Any]:
    """模拟昂贵的操作"""
    await asyncio.sleep(2)  # 模拟耗时操作
    return {
        "item_id": item_id,
        "data": f"expensive-data-{item_id}",
        "computed_at": time.time()
    }


async def example_caching():
    """示例：异步缓存系统"""
    print("\n=== 示例 6: 异步缓存系统 ===\n")
    
    cache = AsyncCache(ttl=5.0)
    
    # 第一次请求（缓存未命中）
    print("第一次请求 item-1:")
    start = time.time()
    result1 = await cache.get_or_fetch("item-1", expensive_operation, 1)
    elapsed1 = time.time() - start
    print(f"  耗时: {elapsed1:.2f} 秒\n")
    
    # 第二次请求相同数据（缓存命中）
    print("第二次请求 item-1:")
    start = time.time()
    result2 = await cache.get_or_fetch("item-1", expensive_operation, 1)
    elapsed2 = time.time() - start
    print(f"  耗时: {elapsed2:.2f} 秒\n")
    
    # 并发请求相同数据（只会获取一次）
    print("并发请求 item-2 (10 次):")
    start = time.time()
    tasks = [
        cache.get_or_fetch("item-2", expensive_operation, 2)
        for _ in range(10)
    ]
    results = await asyncio.gather(*tasks)
    elapsed3 = time.time() - start
    print(f"  10 次请求耗时: {elapsed3:.2f} 秒（锁确保只获取一次）\n")
    
    print(f"性能提升:")
    print(f"  缓存命中速度提升: {elapsed1 / elapsed2:.0f}x")
    print(f"  并发请求优化: 原本需要 {2.0 * 10:.0f} 秒，实际 {elapsed3:.0f} 秒")


# ============================================================================
# 示例 7: WebSocket 服务器
# ============================================================================

class WebSocketServer:
    """WebSocket 服务器模拟"""
    
    def __init__(self):
        self.clients: Dict[str, asyncio.Queue] = {}
        self.message_queue = asyncio.Queue()
    
    async def register_client(self, client_id: str):
        """注册客户端"""
        self.clients[client_id] = asyncio.Queue()
        print(f"  ✅ 客户端连接: {client_id}")
    
    async def unregister_client(self, client_id: str):
        """注销客户端"""
        if client_id in self.clients:
            del self.clients[client_id]
            print(f"  ❌ 客户端断开: {client_id}")
    
    async def broadcast(self, message: str):
        """广播消息到所有客户端"""
        print(f"  📢 广播: {message} 到 {len(self.clients)} 个客户端")
        
        for client_id, queue in self.clients.items():
            await queue.put(message)
    
    async def send_to_client(self, client_id: str, message: str):
        """发送消息到特定客户端"""
        if client_id in self.clients:
            await self.clients[client_id].put(message)
            print(f"  📤 发送到 {client_id}: {message}")
    
    async def client_handler(self, client_id: str):
        """客户端处理器"""
        await self.register_client(client_id)
        
        try:
            # 模拟接收消息
            while True:
                # 从客户端队列获取消息
                message = await asyncio.wait_for(
                    self.clients[client_id].get(),
                    timeout=10.0
                )
                print(f"  📥 {client_id} 收到: {message}")
                
        except asyncio.TimeoutError:
            print(f"  ⏰ {client_id} 超时")
        finally:
            await self.unregister_client(client_id)
    
    async def message_producer(self):
        """消息生产者（模拟服务器推送）"""
        for i in range(5):
            await asyncio.sleep(1)
            await self.broadcast(f"服务器消息 #{i}")


async def example_websocket_server():
    """示例：WebSocket 服务器"""
    print("\n=== 示例 7: WebSocket 服务器 ===\n")
    
    server = WebSocketServer()
    
    # 创建多个客户端
    clients = [
        asyncio.create_task(server.client_handler(f"Client-{i}"))
        for i in range(3)
    ]
    
    # 创建消息生产者
    producer = asyncio.create_task(server.message_producer())
    
    # 等待消息生产完成
    await producer
    
    # 等待一段时间让客户端接收消息
    await asyncio.sleep(2)
    
    # 取消所有客户端
    for client in clients:
        client.cancel()
    
    await asyncio.gather(*clients, return_exceptions=True)


# ============================================================================
# 示例 8: 定时任务调度器
# ============================================================================

class TaskScheduler:
    """定时任务调度器"""
    
    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []
        self.running = False
    
    def schedule(
        self, 
        func: callable, 
        interval: float, 
        name: str = None,
        *args,
        **kwargs
    ):
        """添加定时任务"""
        task_info = {
            "name": name or func.__name__,
            "func": func,
            "interval": interval,
            "args": args,
            "kwargs": kwargs,
            "last_run": 0,
            "run_count": 0
        }
        self.tasks.append(task_info)
        print(f"  📅 添加任务: {task_info['name']} (间隔: {interval}秒)")
    
    async def _run_task(self, task_info: Dict[str, Any]):
        """运行单个任务"""
        try:
            task_info["run_count"] += 1
            task_info["last_run"] = time.time()
            
            print(f"  ⚙️ 执行任务: {task_info['name']} "
                  f"(第 {task_info['run_count']} 次)")
            
            await task_info["func"](*task_info["args"], **task_info["kwargs"])
            
        except Exception as e:
            print(f"  ❌ 任务错误 {task_info['name']}: {e}")
    
    async def start(self, duration: float = None):
        """启动调度器"""
        self.running = True
        start_time = time.time()
        
        print(f"  🚀 调度器启动\n")
        
        while self.running:
            current_time = time.time()
            
            # 检查每个任务是否需要运行
            for task_info in self.tasks:
                time_since_last = current_time - task_info["last_run"]
                
                if time_since_last >= task_info["interval"]:
                    asyncio.create_task(self._run_task(task_info))
            
            # 检查是否达到持续时间
            if duration and (current_time - start_time) >= duration:
                self.running = False
                break
            
            # 短暂休眠避免 CPU 空转
            await asyncio.sleep(0.1)
        
        print(f"\n  🛑 调度器停止")
    
    def stop(self):
        """停止调度器"""
        self.running = False


# 定义定时任务
async def task_every_2_seconds():
    """每 2 秒执行的任务"""
    print(f"    ⏰ 任务 A 执行")
    await asyncio.sleep(0.5)

async def task_every_5_seconds():
    """每 5 秒执行的任务"""
    print(f"    ⏰ 任务 B 执行")
    await asyncio.sleep(0.5)

async def task_every_10_seconds():
    """每 10 秒执行的任务"""
    print(f"    ⏰ 任务 C 执行")
    await asyncio.sleep(0.5)


async def example_task_scheduler():
    """示例：定时任务调度器"""
    print("\n=== 示例 8: 定时任务调度器 ===\n")
    
    scheduler = TaskScheduler()
    
    # 添加定时任务
    scheduler.schedule(task_every_2_seconds, interval=2.0, name="Task-A")
    scheduler.schedule(task_every_5_seconds, interval=5.0, name="Task-B")
    scheduler.schedule(task_every_10_seconds, interval=10.0, name="Task-C")
    
    # 运行 15 秒
    await scheduler.start(duration=15.0)
    
    print("\n任务执行统计:")
    for task in scheduler.tasks:
        print(f"  {task['name']}: 执行 {task['run_count']} 次")


# ============================================================================
# 主函数
# ============================================================================

async def main():
    """运行所有示例"""
    examples = [
        ("HTTP 请求", example_http_requests),
        ("数据库连接池", example_database_pool),
        ("数据流处理", example_stream_processing),
        ("微服务编排", example_microservice_orchestration),
        ("批量处理", example_batch_processing),
        ("缓存系统", example_caching),
        ("WebSocket 服务器", example_websocket_server),
        ("任务调度器", example_task_scheduler),
    ]
    
    print("=" * 60)
    print("Asyncio 实战示例集")
    print("=" * 60)
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n\n{'=' * 60}")
        print(f"示例 {i}: {name}")
        print(f"{'=' * 60}\n")
        
        try:
            # 注意：示例 1 需要 aiohttp，如果未安装会跳过
            if func == example_http_requests:
                try:
                    await func()
                except NameError:
                    print("⚠️ 跳过（需要安装 aiohttp: pip install aiohttp）")
            else:
                await func()
        except Exception as e:
            print(f"❌ 示例执行错误: {e}")
        
        # 等待一下再运行下一个示例
        await asyncio.sleep(1)
    
    print(f"\n\n{'=' * 60}")
    print("所有示例完成！")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    # 运行所有示例
    asyncio.run(main())
    
    # 或者运行单个示例:
    # asyncio.run(example_http_requests())
    # asyncio.run(example_database_pool())
    # asyncio.run(example_stream_processing())
    # asyncio.run(example_microservice_orchestration())
    # asyncio.run(example_batch_processing())
    # asyncio.run(example_caching())
    # asyncio.run(example_websocket_server())
    # asyncio.run(example_task_scheduler())

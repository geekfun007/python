"""
实战项目 3: 性能监控装饰器

一个功能完整的性能监控工具，包括:
- 函数执行时间统计
- 内存使用监控
- 调用次数追踪
- 参数和返回值记录
- 性能报告生成
"""

import time
import functools
import tracemalloc
import threading
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import statistics

# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class CallRecord:
    """函数调用记录"""
    function_name: str
    args: tuple
    kwargs: dict
    start_time: float
    end_time: float
    duration: float
    memory_start: float
    memory_end: float
    memory_delta: float
    result: Any = None
    exception: Optional[Exception] = None
    
    @property
    def success(self) -> bool:
        return self.exception is None


@dataclass
class FunctionStats:
    """函数统计信息"""
    function_name: str
    call_count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    avg_time: float = 0.0
    times: List[float] = field(default_factory=list)
    total_memory: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    
    def update(self, record: CallRecord):
        """更新统计信息"""
        self.call_count += 1
        self.total_time += record.duration
        self.times.append(record.duration)
        
        self.min_time = min(self.min_time, record.duration)
        self.max_time = max(self.max_time, record.duration)
        self.avg_time = self.total_time / self.call_count
        
        self.total_memory += record.memory_delta
        
        if record.success:
            self.success_count += 1
        else:
            self.failure_count += 1


# ============================================================================
# 性能监控器
# ============================================================================

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.records: List[CallRecord] = []
        self.stats: Dict[str, FunctionStats] = defaultdict(
            lambda: FunctionStats(function_name="")
        )
        self.lock = threading.Lock()
        self._memory_tracking = False
    
    def start_memory_tracking(self):
        """开始内存追踪"""
        if not self._memory_tracking:
            tracemalloc.start()
            self._memory_tracking = True
    
    def stop_memory_tracking(self):
        """停止内存追踪"""
        if self._memory_tracking:
            tracemalloc.stop()
            self._memory_tracking = False
    
    def record_call(self, record: CallRecord):
        """记录调用"""
        with self.lock:
            self.records.append(record)
            
            if record.function_name not in self.stats:
                self.stats[record.function_name] = FunctionStats(
                    function_name=record.function_name
                )
            
            self.stats[record.function_name].update(record)
    
    def get_stats(self, function_name: Optional[str] = None) -> Dict:
        """获取统计信息"""
        with self.lock:
            if function_name:
                if function_name in self.stats:
                    return self._format_stats(self.stats[function_name])
                return {}
            
            # 返回所有函数的统计
            return {
                name: self._format_stats(stats)
                for name, stats in self.stats.items()
            }
    
    def _format_stats(self, stats: FunctionStats) -> Dict:
        """格式化统计信息"""
        median_time = statistics.median(stats.times) if stats.times else 0
        
        return {
            '调用次数': stats.call_count,
            '总耗时': f'{stats.total_time:.4f}秒',
            '平均耗时': f'{stats.avg_time:.4f}秒',
            '最小耗时': f'{stats.min_time:.4f}秒',
            '最大耗时': f'{stats.max_time:.4f}秒',
            '中位数耗时': f'{median_time:.4f}秒',
            '总内存': f'{stats.total_memory / 1024:.2f} KB',
            '成功': stats.success_count,
            '失败': stats.failure_count,
            '成功率': f'{stats.success_count / stats.call_count * 100:.1f}%'
                if stats.call_count > 0 else 'N/A'
        }
    
    def clear(self):
        """清除所有记录"""
        with self.lock:
            self.records.clear()
            self.stats.clear()
    
    def generate_report(self) -> str:
        """生成性能报告"""
        report = []
        report.append("=" * 70)
        report.append("性能监控报告")
        report.append("=" * 70)
        
        for func_name, stats in self.stats.items():
            report.append(f"\n函数: {func_name}")
            report.append("-" * 70)
            
            formatted = self._format_stats(stats)
            for key, value in formatted.items():
                report.append(f"  {key}: {value}")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)


# 全局监控器实例
_global_monitor = PerformanceMonitor()


# ============================================================================
# 装饰器
# ============================================================================

def monitor_performance(
    track_memory: bool = True,
    track_args: bool = False,
    track_result: bool = False
):
    """
    性能监控装饰器
    
    Args:
        track_memory: 是否追踪内存
        track_args: 是否记录参数
        track_result: 是否记录返回值
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 开始追踪
            start_time = time.time()
            
            memory_start = 0
            if track_memory:
                _global_monitor.start_memory_tracking()
                memory_start = tracemalloc.get_traced_memory()[0]
            
            # 执行函数
            exception = None
            result = None
            
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                exception = e
                raise
            finally:
                # 结束追踪
                end_time = time.time()
                
                memory_end = 0
                if track_memory:
                    memory_end = tracemalloc.get_traced_memory()[0]
                
                # 创建记录
                record = CallRecord(
                    function_name=func.__name__,
                    args=args if track_args else (),
                    kwargs=kwargs if track_args else {},
                    start_time=start_time,
                    end_time=end_time,
                    duration=end_time - start_time,
                    memory_start=memory_start,
                    memory_end=memory_end,
                    memory_delta=memory_end - memory_start,
                    result=result if track_result else None,
                    exception=exception
                )
                
                _global_monitor.record_call(record)
            
            return result
        
        # 添加监控方法
        wrapper.get_stats = lambda: _global_monitor.get_stats(func.__name__)
        wrapper.clear_stats = _global_monitor.clear
        
        return wrapper
    return decorator


def time_it(func: Callable) -> Callable:
    """简单的计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} 耗时: {elapsed:.4f}秒")
        return result
    return wrapper


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """失败重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    print(f"{func.__name__} 失败 (尝试 {attempt}/{max_retries}): {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


def memoize_performance(func: Callable) -> Callable:
    """带性能监控的缓存装饰器"""
    cache = {}
    hits = 0
    misses = 0
    
    @functools.wraps(func)
    def wrapper(*args):
        nonlocal hits, misses
        
        if args in cache:
            hits += 1
            return cache[args]
        
        misses += 1
        result = func(*args)
        cache[args] = result
        return result
    
    def cache_info():
        return {
            'hits': hits,
            'misses': misses,
            'size': len(cache),
            'hit_rate': f'{hits / (hits + misses) * 100:.1f}%'
                if (hits + misses) > 0 else 'N/A'
        }
    
    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache.clear
    
    return wrapper


# ============================================================================
# 演示函数
# ============================================================================

@monitor_performance(track_memory=True, track_args=False)
def fibonacci(n: int) -> int:
    """斐波那契数列 - 递归实现"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@monitor_performance(track_memory=True)
def process_large_list(size: int) -> int:
    """处理大列表 - 测试内存"""
    data = list(range(size))
    return sum(data)


@time_it
def slow_function():
    """慢速函数"""
    time.sleep(0.5)
    return "完成"


@retry_on_failure(max_retries=3, delay=0.1)
def unstable_function(success_rate: float = 0.5):
    """不稳定的函数"""
    import random
    if random.random() < success_rate:
        return "成功"
    raise ValueError("失败")


@memoize_performance
def expensive_calculation(n: int) -> int:
    """耗时计算"""
    time.sleep(0.1)
    return n ** 2


def demo_basic_monitoring():
    """演示基础监控"""
    print("=" * 60)
    print("基础性能监控")
    print("=" * 60)
    
    # 调用多次
    for i in range(5):
        fibonacci(10)
    
    print("\nfibonacci 统计:")
    stats = fibonacci.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()


def demo_memory_tracking():
    """演示内存追踪"""
    print("=" * 60)
    print("内存追踪")
    print("=" * 60)
    
    sizes = [10000, 50000, 100000]
    
    for size in sizes:
        process_large_list(size)
    
    print("\nprocess_large_list 统计:")
    stats = process_large_list.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()


def demo_time_decorator():
    """演示计时装饰器"""
    print("=" * 60)
    print("计时装饰器")
    print("=" * 60)
    
    slow_function()
    slow_function()
    print()


def demo_retry():
    """演示重试装饰器"""
    print("=" * 60)
    print("重试装饰器")
    print("=" * 60)
    
    try:
        result = unstable_function(success_rate=0.6)
        print(f"结果: {result}")
    except ValueError as e:
        print(f"最终失败: {e}")
    print()


def demo_memoize():
    """演示缓存装饰器"""
    print("=" * 60)
    print("缓存装饰器")
    print("=" * 60)
    
    print("第一次调用 (计算):")
    result1 = expensive_calculation(5)
    print(f"结果: {result1}")
    
    print("\n第二次调用 (缓存):")
    result2 = expensive_calculation(5)
    print(f"结果: {result2}")
    
    print(f"\n缓存信息: {expensive_calculation.cache_info()}")
    print()


def demo_full_report():
    """演示完整报告"""
    print("=" * 60)
    print("完整性能报告")
    print("=" * 60)
    
    # 执行一些函数
    fibonacci(8)
    fibonacci(10)
    process_large_list(50000)
    
    # 生成报告
    report = _global_monitor.generate_report()
    print(report)
    print()


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("实战项目: 性能监控装饰器")
    print("=" * 60 + "\n")
    
    demo_basic_monitoring()
    demo_memory_tracking()
    demo_time_decorator()
    demo_retry()
    demo_memoize()
    demo_full_report()
    
    print("=" * 60)
    print("性能监控演示完成!")
    print("=" * 60)

"""
实战项目 1: 高性能缓存系统

实现一个具有以下特性的缓存系统:
- LRU (最近最少使用) 淘汰策略
- TTL (生存时间) 支持
- 线程安全
- 装饰器模式使用
- 统计信息
"""

import time
import threading
from typing import Any, Optional, Callable, Dict
from collections import OrderedDict
from functools import wraps
import hashlib
import pickle

# ============================================================================
# 1. 基础 LRU 缓存
# ============================================================================

class LRUCache:
    """LRU 缓存实现"""
    
    def __init__(self, capacity: int = 100):
        """
        初始化 LRU 缓存
        
        Args:
            capacity: 缓存容量
        """
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()
        self.lock = threading.RLock()
        
        # 统计信息
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存的值，如果不存在返回 None
        """
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            # 移动到末尾(最近使用)
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
    
    def put(self, key: str, value: Any) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        with self.lock:
            if key in self.cache:
                # 更新现有键
                self.cache.move_to_end(key)
            else:
                # 添加新键
                if len(self.cache) >= self.capacity:
                    # 移除最旧的项
                    self.cache.popitem(last=False)
            
            self.cache[key] = value
    
    def delete(self, key: str) -> bool:
        """删除缓存项"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
    
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self.lock:
            total = self.hits + self.misses
            hit_rate = self.hits / total if total > 0 else 0
            
            return {
                'size': len(self.cache),
                'capacity': self.capacity,
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': f'{hit_rate:.2%}'
            }


# ============================================================================
# 2. TTL 缓存 (支持过期时间)
# ============================================================================

class TTLCache:
    """支持 TTL 的缓存"""
    
    def __init__(self, capacity: int = 100, default_ttl: float = 300):
        """
        初始化 TTL 缓存
        
        Args:
            capacity: 缓存容量
            default_ttl: 默认过期时间(秒)
        """
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache: OrderedDict = OrderedDict()
        self.lock = threading.RLock()
        self.hits = 0
        self.misses = 0
        self.expired = 0
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值 (检查过期)"""
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            value, expire_time = self.cache[key]
            
            # 检查是否过期
            if time.time() > expire_time:
                del self.cache[key]
                self.expired += 1
                self.misses += 1
                return None
            
            # 移动到末尾
            self.cache.move_to_end(key)
            self.hits += 1
            return value
    
    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """设置缓存值"""
        with self.lock:
            if ttl is None:
                ttl = self.default_ttl
            
            expire_time = time.time() + ttl
            
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                if len(self.cache) >= self.capacity:
                    self.cache.popitem(last=False)
            
            self.cache[key] = (value, expire_time)
    
    def cleanup_expired(self) -> int:
        """清理过期项"""
        with self.lock:
            current_time = time.time()
            expired_keys = []
            
            for key, (value, expire_time) in self.cache.items():
                if current_time > expire_time:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
            
            return len(expired_keys)
    
    def clear(self) -> None:
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
            self.expired = 0
    
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self.lock:
            total = self.hits + self.misses
            hit_rate = self.hits / total if total > 0 else 0
            
            return {
                'size': len(self.cache),
                'capacity': self.capacity,
                'hits': self.hits,
                'misses': self.misses,
                'expired': self.expired,
                'hit_rate': f'{hit_rate:.2%}'
            }


# ============================================================================
# 3. 缓存装饰器
# ============================================================================

def lru_cache_decorator(maxsize: int = 128):
    """LRU 缓存装饰器"""
    cache = LRUCache(capacity=maxsize)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = _make_key(func.__name__, args, kwargs)
            
            # 尝试从缓存获取
            result = cache.get(key)
            if result is not None:
                return result
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存入缓存
            cache.put(key, result)
            return result
        
        # 添加缓存管理方法
        wrapper.cache_info = cache.stats
        wrapper.cache_clear = cache.clear
        
        return wrapper
    return decorator


def ttl_cache_decorator(ttl: float = 60, maxsize: int = 128):
    """TTL 缓存装饰器"""
    cache = TTLCache(capacity=maxsize, default_ttl=ttl)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = _make_key(func.__name__, args, kwargs)
            
            result = cache.get(key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.put(key, result)
            return result
        
        wrapper.cache_info = cache.stats
        wrapper.cache_clear = cache.clear
        wrapper.cache_cleanup = cache.cleanup_expired
        
        return wrapper
    return decorator


def _make_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """生成缓存键"""
    try:
        # 尝试序列化参数
        key_data = pickle.dumps((func_name, args, tuple(sorted(kwargs.items()))))
        return hashlib.md5(key_data).hexdigest()
    except Exception:
        # 降级到字符串表示
        return f"{func_name}_{args}_{kwargs}"


# ============================================================================
# 4. 多级缓存
# ============================================================================

class MultiLevelCache:
    """多级缓存系统"""
    
    def __init__(self):
        self.l1_cache = LRUCache(capacity=10)  # 一级缓存 (小容量, 快速)
        self.l2_cache = LRUCache(capacity=100)  # 二级缓存 (大容量)
        self.lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """多级查找"""
        with self.lock:
            # 尝试 L1
            value = self.l1_cache.get(key)
            if value is not None:
                return value
            
            # 尝试 L2
            value = self.l2_cache.get(key)
            if value is not None:
                # 提升到 L1
                self.l1_cache.put(key, value)
                return value
            
            return None
    
    def put(self, key: str, value: Any) -> None:
        """写入缓存"""
        with self.lock:
            self.l1_cache.put(key, value)
            self.l2_cache.put(key, value)
    
    def stats(self) -> Dict[str, Any]:
        """统计信息"""
        return {
            'l1': self.l1_cache.stats(),
            'l2': self.l2_cache.stats()
        }


# ============================================================================
# 演示和测试
# ============================================================================

def demo_lru_cache():
    """演示 LRU 缓存"""
    print("=" * 60)
    print("LRU 缓存演示")
    print("=" * 60)
    
    cache = LRUCache(capacity=3)
    
    # 添加元素
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    print(f"缓存状态: {cache.stats()}")
    print(f"获取 'a': {cache.get('a')}")
    print(f"获取 'b': {cache.get('b')}")
    
    # 添加第4个元素，会淘汰 'c'
    cache.put("d", 4)
    print(f"\n添加 'd' 后:")
    print(f"获取 'c': {cache.get('c')}")  # None
    print(f"获取 'd': {cache.get('d')}")  # 4
    
    print(f"\n最终统计: {cache.stats()}")
    print()


def demo_ttl_cache():
    """演示 TTL 缓存"""
    print("=" * 60)
    print("TTL 缓存演示")
    print("=" * 60)
    
    cache = TTLCache(capacity=10, default_ttl=2)
    
    cache.put("short", "短期数据", ttl=1)
    cache.put("long", "长期数据", ttl=5)
    
    print(f"立即获取 'short': {cache.get('short')}")
    print(f"立即获取 'long': {cache.get('long')}")
    
    time.sleep(1.5)
    print(f"\n1.5秒后:")
    print(f"获取 'short': {cache.get('short')}")  # None (已过期)
    print(f"获取 'long': {cache.get('long')}")  # 仍有效
    
    print(f"\n统计: {cache.stats()}")
    print()


@lru_cache_decorator(maxsize=3)
def expensive_function(n: int) -> int:
    """模拟耗时计算"""
    print(f"计算 fibonacci({n})...")
    time.sleep(0.1)
    if n < 2:
        return n
    return expensive_function(n-1) + expensive_function(n-2)


@ttl_cache_decorator(ttl=2, maxsize=10)
def get_data(id: int) -> dict:
    """模拟数据获取"""
    print(f"从数据库获取数据 {id}...")
    time.sleep(0.1)
    return {"id": id, "data": f"数据-{id}"}


def demo_decorators():
    """演示缓存装饰器"""
    print("=" * 60)
    print("缓存装饰器演示")
    print("=" * 60)
    
    # LRU 装饰器
    print("第一次调用 fibonacci(5):")
    result1 = expensive_function(5)
    print(f"结果: {result1}")
    
    print("\n第二次调用 fibonacci(5):")
    result2 = expensive_function(5)
    print(f"结果: {result2}")
    
    print(f"\n缓存统计: {expensive_function.cache_info()}")
    
    # TTL 装饰器
    print("\n" + "=" * 40)
    print("第一次获取数据:")
    data1 = get_data(1)
    print(f"数据: {data1}")
    
    print("\n第二次获取数据 (从缓存):")
    data2 = get_data(1)
    print(f"数据: {data2}")
    
    print(f"\n缓存统计: {get_data.cache_info()}")
    print()


def demo_multilevel_cache():
    """演示多级缓存"""
    print("=" * 60)
    print("多级缓存演示")
    print("=" * 60)
    
    cache = MultiLevelCache()
    
    # 写入数据
    for i in range(15):
        cache.put(f"key{i}", f"value{i}")
    
    # 访问数据 (L1 和 L2)
    print("访问 key0 (从 L2 提升到 L1):")
    print(f"值: {cache.get('key0')}")
    
    print("\n再次访问 key0 (从 L1):")
    print(f"值: {cache.get('key0')}")
    
    print(f"\n统计信息:")
    stats = cache.stats()
    print(f"L1: {stats['l1']}")
    print(f"L2: {stats['l2']}")
    print()


def benchmark():
    """性能基准测试"""
    print("=" * 60)
    print("性能基准测试")
    print("=" * 60)
    
    cache = LRUCache(capacity=1000)
    
    # 写入测试
    start = time.time()
    for i in range(10000):
        cache.put(f"key{i}", f"value{i}")
    write_time = time.time() - start
    
    # 读取测试 (命中)
    start = time.time()
    for i in range(9000, 10000):
        cache.get(f"key{i}")
    read_time = time.time() - start
    
    print(f"写入 10000 项: {write_time:.4f} 秒")
    print(f"读取 1000 项: {read_time:.4f} 秒")
    print(f"缓存统计: {cache.stats()}")
    print()


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("实战项目: 高性能缓存系统")
    print("=" * 60 + "\n")
    
    demo_lru_cache()
    demo_ttl_cache()
    demo_decorators()
    demo_multilevel_cache()
    benchmark()
    
    print("=" * 60)
    print("缓存系统演示完成!")
    print("=" * 60)

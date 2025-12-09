"""
Python 高级教程 - 生成器与迭代器详解

生成器和迭代器是 Python 中实现惰性求值和内存高效数据处理的核心机制。
本模块涵盖:
1. 迭代器协议
2. 生成器函数和表达式
3. yield from 语句
4. 协程和生成器的关系
5. 实战应用
"""

from typing import Iterator, Iterable, Generator, Any
import itertools
import time

# ============================================================================
# 1. 迭代器协议
# ============================================================================

class CountDown:
    """倒计时迭代器"""
    
    def __init__(self, start: int):
        self.current = start
    
    def __iter__(self):
        """返回迭代器对象本身"""
        return self
    
    def __next__(self):
        """返回下一个值"""
        if self.current <= 0:
            raise StopIteration
        
        self.current -= 1
        return self.current + 1


class Range:
    """自定义 range 实现"""
    
    def __init__(self, start: int, end: int, step: int = 1):
        self.start = start
        self.end = end
        self.step = step
    
    def __iter__(self):
        """返回一个新的迭代器"""
        current = self.start
        while current < self.end:
            yield current
            current += self.step


# ============================================================================
# 2. 基础生成器函数
# ============================================================================

def fibonacci(n: int) -> Generator[int, None, None]:
    """斐波那契数列生成器"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def infinite_sequence() -> Generator[int, None, None]:
    """无限序列生成器"""
    num = 0
    while True:
        yield num
        num += 1


def read_large_file(filename: str) -> Generator[str, None, None]:
    """逐行读取大文件 - 内存高效"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()


# ============================================================================
# 3. 生成器表达式
# ============================================================================

def demo_generator_expressions():
    """演示生成器表达式"""
    print("=" * 60)
    print("生成器表达式")
    print("=" * 60)
    
    # 列表推导式 - 立即创建列表
    list_comp = [x ** 2 for x in range(10)]
    print(f"列表推导式: {list_comp}")
    
    # 生成器表达式 - 惰性求值
    gen_exp = (x ** 2 for x in range(10))
    print(f"生成器表达式: {gen_exp}")
    print(f"生成器值: {list(gen_exp)}")
    
    # 内存对比
    import sys
    list_mem = sys.getsizeof([x for x in range(10000)])
    gen_mem = sys.getsizeof((x for x in range(10000)))
    print(f"\n列表内存: {list_mem} 字节")
    print(f"生成器内存: {gen_mem} 字节")
    print()


# ============================================================================
# 4. yield from 语句
# ============================================================================

def chain(*iterables):
    """连接多个可迭代对象"""
    for iterable in iterables:
        yield from iterable


def flatten(nested_list):
    """扁平化嵌套列表"""
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def tree_traverse(tree):
    """树的深度优先遍历"""
    yield tree['value']
    for child in tree.get('children', []):
        yield from tree_traverse(child)


# ============================================================================
# 5. 生成器的双向通信 (send 和 throw)
# ============================================================================

def averager():
    """计算运行平均值的协程"""
    total = 0.0
    count = 0
    average = None
    
    while True:
        value = yield average
        if value is None:
            break
        total += value
        count += 1
        average = total / count


def echo_coroutine():
    """回显协程 - 演示 send 和 throw"""
    print("协程已启动")
    try:
        while True:
            value = yield
            print(f"收到: {value}")
    except GeneratorExit:
        print("协程正在关闭")
    except Exception as e:
        print(f"协程捕获异常: {e}")


# ============================================================================
# 6. 生成器的高级应用
# ============================================================================

def batched(iterable, batch_size: int):
    """将可迭代对象分批"""
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch


def sliding_window(iterable, window_size: int):
    """滑动窗口"""
    iterator = iter(iterable)
    window = list(itertools.islice(iterator, window_size))
    
    if len(window) == window_size:
        yield tuple(window)
    
    for item in iterator:
        window = window[1:] + [item]
        yield tuple(window)


def unique_generator(iterable):
    """去重生成器 - 保持顺序"""
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item


# ============================================================================
# 7. 数据流水线
# ============================================================================

def numbers_generator(start: int, end: int):
    """生成数字"""
    for num in range(start, end):
        yield num


def filter_even(numbers):
    """过滤偶数"""
    for num in numbers:
        if num % 2 == 0:
            yield num


def square(numbers):
    """平方"""
    for num in numbers:
        yield num ** 2


def sum_pipeline(numbers):
    """求和"""
    return sum(numbers)


# ============================================================================
# 8. 自定义可迭代对象
# ============================================================================

class CircularBuffer:
    """循环缓冲区 - 可迭代对象"""
    
    def __init__(self, size: int):
        self.size = size
        self.buffer = [None] * size
        self.index = 0
        self.filled = 0
    
    def append(self, item):
        """添加元素"""
        self.buffer[self.index] = item
        self.index = (self.index + 1) % self.size
        self.filled = min(self.filled + 1, self.size)
    
    def __iter__(self):
        """返回迭代器"""
        for i in range(self.filled):
            idx = (self.index - self.filled + i) % self.size
            yield self.buffer[idx]
    
    def __repr__(self):
        return f"CircularBuffer({list(self)})"


class LinkedList:
    """链表 - 可迭代对象"""
    
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    
    def append(self, value):
        """添加节点"""
        node = self.Node(value)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1
    
    def __iter__(self):
        """迭代器"""
        current = self.head
        while current:
            yield current.value
            current = current.next
    
    def __len__(self):
        return self.length
    
    def __repr__(self):
        return f"LinkedList({list(self)})"


# ============================================================================
# 9. itertools 模块常用函数
# ============================================================================

def demo_itertools():
    """演示 itertools 模块"""
    print("=" * 60)
    print("itertools 模块常用函数")
    print("=" * 60)
    
    # count - 无限计数器
    print("count(10, 2):", list(itertools.islice(itertools.count(10, 2), 5)))
    
    # cycle - 循环迭代
    print("cycle('ABC'):", list(itertools.islice(itertools.cycle('ABC'), 7)))
    
    # repeat - 重复元素
    print("repeat(10, 3):", list(itertools.repeat(10, 3)))
    
    # chain - 连接多个迭代器
    print("chain([1,2], [3,4]):", list(itertools.chain([1, 2], [3, 4])))
    
    # compress - 根据选择器过滤
    print("compress('ABCDEF', [1,0,1,0,1,1]):", 
          list(itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1])))
    
    # dropwhile - 删除开头满足条件的元素
    print("dropwhile(lambda x: x<5, [1,4,6,4,1]):",
          list(itertools.dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1])))
    
    # takewhile - 保留开头满足条件的元素
    print("takewhile(lambda x: x<5, [1,4,6,4,1]):",
          list(itertools.takewhile(lambda x: x < 5, [1, 4, 6, 4, 1])))
    
    # groupby - 分组
    data = [('A', 1), ('A', 2), ('B', 3), ('B', 4), ('C', 5)]
    print("groupby(data, key=lambda x: x[0]):")
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(f"  {key}: {list(group)}")
    
    # combinations - 组合
    print("combinations('ABC', 2):", list(itertools.combinations('ABC', 2)))
    
    # permutations - 排列
    print("permutations('ABC', 2):", list(itertools.permutations('ABC', 2)))
    
    # product - 笛卡尔积
    print("product('AB', '12'):", list(itertools.product('AB', '12')))
    print()


# ============================================================================
# 10. 协程式生成器 (生成器作为协程)
# ============================================================================

def running_statistics():
    """运行统计 - 协程示例"""
    count = 0
    total = 0
    minimum = float('inf')
    maximum = float('-inf')
    
    while True:
        value = yield {
            'count': count,
            'sum': total,
            'mean': total / count if count > 0 else 0,
            'min': minimum if count > 0 else None,
            'max': maximum if count > 0 else None
        }
        
        if value is None:
            break
        
        count += 1
        total += value
        minimum = min(minimum, value)
        maximum = max(maximum, value)


# ============================================================================
# 演示函数
# ============================================================================

def demo_iterator_protocol():
    """演示迭代器协议"""
    print("=" * 60)
    print("1. 迭代器协议")
    print("=" * 60)
    
    countdown = CountDown(5)
    print("倒计时:", list(countdown))
    
    custom_range = Range(0, 10, 2)
    print("自定义 range:", list(custom_range))
    print()


def demo_basic_generators():
    """演示基础生成器"""
    print("=" * 60)
    print("2. 基础生成器函数")
    print("=" * 60)
    
    print("斐波那契数列 (前 10 个):", list(fibonacci(10)))
    
    print("无限序列 (前 5 个):", list(itertools.islice(infinite_sequence(), 5)))
    print()


def demo_yield_from():
    """演示 yield from"""
    print("=" * 60)
    print("3. yield from 语句")
    print("=" * 60)
    
    print("连接多个序列:", list(chain([1, 2], [3, 4], [5, 6])))
    
    nested = [1, [2, 3], [4, [5, 6]], 7]
    print(f"扁平化 {nested}:", list(flatten(nested)))
    
    tree = {
        'value': 1,
        'children': [
            {'value': 2, 'children': [{'value': 4}, {'value': 5}]},
            {'value': 3, 'children': [{'value': 6}]}
        ]
    }
    print("树遍历:", list(tree_traverse(tree)))
    print()


def demo_coroutine():
    """演示协程"""
    print("=" * 60)
    print("4. 生成器协程 (send 和 throw)")
    print("=" * 60)
    
    # 平均值协程
    avg = averager()
    next(avg)  # 启动协程
    
    print("发送 10:", avg.send(10))
    print("发送 20:", avg.send(20))
    print("发送 30:", avg.send(30))
    
    # 回显协程
    echo = echo_coroutine()
    next(echo)
    echo.send("Hello")
    echo.send("World")
    
    try:
        echo.throw(ValueError, "测试异常")
    except StopIteration:
        pass
    
    print()


def demo_advanced_generators():
    """演示高级生成器应用"""
    print("=" * 60)
    print("5. 高级生成器应用")
    print("=" * 60)
    
    data = range(10)
    print("分批处理 (batch_size=3):")
    for batch in batched(data, 3):
        print(f"  {batch}")
    
    print("\n滑动窗口 (window_size=3):")
    for window in sliding_window(range(5), 3):
        print(f"  {window}")
    
    print("\n去重:", list(unique_generator([1, 2, 2, 3, 1, 4, 3, 5])))
    print()


def demo_pipeline():
    """演示数据流水线"""
    print("=" * 60)
    print("6. 数据流水线")
    print("=" * 60)
    
    # 构建流水线: 生成 -> 过滤偶数 -> 平方 -> 求和
    pipeline = sum_pipeline(square(filter_even(numbers_generator(1, 11))))
    print(f"流水线结果 (1-10 的偶数平方和): {pipeline}")
    print()


def demo_custom_iterables():
    """演示自定义可迭代对象"""
    print("=" * 60)
    print("7. 自定义可迭代对象")
    print("=" * 60)
    
    # 循环缓冲区
    buffer = CircularBuffer(3)
    for i in range(5):
        buffer.append(i)
    print(f"循环缓冲区: {buffer}")
    
    # 链表
    linked_list = LinkedList()
    for i in [1, 2, 3, 4, 5]:
        linked_list.append(i)
    print(f"链表: {linked_list}")
    print(f"链表长度: {len(linked_list)}")
    print()


def demo_running_stats():
    """演示运行统计协程"""
    print("=" * 60)
    print("8. 运行统计协程")
    print("=" * 60)
    
    stats = running_statistics()
    next(stats)  # 启动协程
    
    values = [10, 20, 15, 25, 30]
    for value in values:
        result = stats.send(value)
        print(f"发送 {value}: {result}")
    print()


# ============================================================================
# 重要注意事项
# ============================================================================

"""
生成器与迭代器最佳实践和注意事项:

1. 迭代器协议
   - __iter__: 返回迭代器对象 (通常是 self)
   - __next__: 返回下一个值，完成时抛出 StopIteration
   - 迭代器只能前进，不能后退或重置

2. 生成器优势
   ✓ 内存高效 (惰性求值)
   ✓ 代码简洁 (不需要维护状态)
   ✓ 支持无限序列
   ✓ 适合数据流处理

3. 生成器 vs 列表
   - 生成器: 一次产生一个值，内存占用小
   - 列表: 一次性创建所有值，可以多次遍历
   - 选择: 大数据集或无限序列用生成器

4. yield vs return
   - yield: 暂停函数执行，保存状态
   - return: 结束函数执行，抛出 StopIteration
   - 可以在生成器中使用 return 传递值

5. yield from
   - 委托给子生成器
   - 自动处理 StopIteration
   - 简化嵌套生成器代码

6. 生成器方法
   - send(value): 向生成器发送值
   - throw(exception): 向生成器抛出异常
   - close(): 关闭生成器

7. 协程 vs 生成器
   - 生成器: 生产数据 (yield value)
   - 协程: 消费数据 (value = yield)
   - Python 3.5+ 使用 async/await 替代协程

8. itertools 模块
   - 提供高效的迭代器工具
   - 组合使用可以构建复杂的数据处理流水线
   - 比纯 Python 循环更高效

9. 性能考虑
   - 生成器有函数调用开销
   - 简单操作可能不如列表推导式快
   - 大数据集时内存优势明显

10. 常见陷阱
    - 生成器只能遍历一次
    - 忘记调用 next() 或 send(None) 启动协程
    - 在需要多次遍历时使用生成器
    - 生成器表达式需要括号

11. 调试技巧
    - 使用 list() 查看生成器内容 (小数据集)
    - 添加 print 语句追踪执行
    - inspect.getgeneratorstate() 检查状态

12. 实际应用场景
    - 读取大文件 (逐行处理)
    - 数据流处理 (ETL 管道)
    - 无限序列 (传感器数据)
    - 树/图遍历 (深度/广度优先)
    - 协议解析 (状态机)
"""


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Python 高级教程 - 生成器与迭代器详解")
    print("=" * 60 + "\n")
    
    demo_iterator_protocol()
    demo_basic_generators()
    demo_generator_expressions()
    demo_yield_from()
    demo_coroutine()
    demo_advanced_generators()
    demo_pipeline()
    demo_custom_iterables()
    demo_itertools()
    demo_running_stats()
    
    print("=" * 60)
    print("生成器与迭代器教程完成!")
    print("=" * 60)

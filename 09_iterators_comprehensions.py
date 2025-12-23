"""
Python 迭代器与推导式详解
包含：迭代器、生成器、列表/字典/集合推导式等
"""

from itertools import *
from typing import Iterator, Generator
import sys


# ============================================
# 1. 迭代器基础
# ============================================

def iterator_basics():
    """迭代器基础"""
    print("\n=== 迭代器基础 ===")
    
    # 可迭代对象
    numbers = [1, 2, 3, 4, 5]
    
    # 获取迭代器
    iterator = iter(numbers)
    
    print("使用 next() 获取元素:")
    print(f"  {next(iterator)}")
    print(f"  {next(iterator)}")
    print(f"  {next(iterator)}")
    
    # 迭代器耗尽
    print("\n迭代器耗尽示例:")
    iterator = iter([1, 2, 3])
    for item in iterator:
        print(f"  {item}")
    
    # 尝试再次迭代
    print("再次迭代（为空）:")
    for item in iterator:
        print(f"  {item}")
    
    # for 循环的本质
    print("\nfor 循环的本质:")
    numbers = [1, 2, 3]
    iterator = iter(numbers)
    try:
        while True:
            item = next(iterator)
            print(f"  {item}")
    except StopIteration:
        pass


def custom_iterator():
    """自定义迭代器"""
    print("\n=== 自定义迭代器 ===")
    
    # 实现迭代器协议
    class Countdown:
        """倒计时迭代器"""
        def __init__(self, start):
            self.current = start
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.current <= 0:
                raise StopIteration
            self.current -= 1
            return self.current + 1
    
    print("倒计时:")
    for num in Countdown(5):
        print(f"  {num}")
    
    # 范围迭代器
    class Range:
        """自定义范围迭代器"""
        def __init__(self, start, end, step=1):
            self.current = start
            self.end = end
            self.step = step
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.current >= self.end:
                raise StopIteration
            value = self.current
            self.current += self.step
            return value
    
    print("\n自定义范围:")
    for num in Range(0, 10, 2):
        print(f"  {num}", end=" ")
    print()
    
    # 斐波那契数列迭代器
    class Fibonacci:
        """斐波那契数列迭代器"""
        def __init__(self, max_count):
            self.max_count = max_count
            self.count = 0
            self.a, self.b = 0, 1
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.count >= self.max_count:
                raise StopIteration
            self.count += 1
            self.a, self.b = self.b, self.a + self.b
            return self.a
    
    print("\n斐波那契数列（前10项）:")
    for num in Fibonacci(10):
        print(f"  {num}", end=" ")
    print()


# ============================================
# 2. 生成器
# ============================================

def generator_basics():
    """生成器基础"""
    print("\n=== 生成器基础 ===")
    
    # 生成器函数
    def countdown(n):
        """倒计时生成器"""
        while n > 0:
            yield n
            n -= 1
    
    print("生成器倒计时:")
    for num in countdown(5):
        print(f"  {num}")
    
    # 生成器表达式
    print("\n生成器表达式:")
    squares = (x ** 2 for x in range(10))
    print(f"生成器对象: {squares}")
    print(f"前5个平方数: {[next(squares) for _ in range(5)]}")
    
    # 无限生成器
    def infinite_sequence():
        """无限序列生成器"""
        num = 0
        while True:
            yield num
            num += 1
    
    print("\n无限序列（前10项）:")
    gen = infinite_sequence()
    for _ in range(10):
        print(f"  {next(gen)}", end=" ")
    print()


def generator_advanced():
    """生成器高级特性"""
    print("\n=== 生成器高级特性 ===")
    
    # 1. send() 方法
    print("1. send() 方法:")
    def echo_generator():
        """回显生成器"""
        while True:
            received = yield
            if received is not None:
                print(f"  接收到: {received}")
    
    gen = echo_generator()
    next(gen)  # 启动生成器
    gen.send("Hello")
    gen.send("World")
    gen.close()
    
    # 2. 双向通信
    print("\n2. 双向通信:")
    def accumulator():
        """累加器生成器"""
        total = 0
        while True:
            value = yield total
            if value is None:
                break
            total += value
    
    acc = accumulator()
    next(acc)  # 启动
    print(f"  累加5: {acc.send(5)}")
    print(f"  累加10: {acc.send(10)}")
    print(f"  累加3: {acc.send(3)}")
    
    # 3. throw() 方法
    print("\n3. throw() 方法:")
    def generator_with_exception():
        try:
            yield 1
            yield 2
            yield 3
        except ValueError:
            yield "捕获到 ValueError"
    
    gen = generator_with_exception()
    print(f"  {next(gen)}")
    print(f"  {gen.throw(ValueError)}")
    
    # 4. yield from
    print("\n4. yield from:")
    def inner_generator():
        yield 1
        yield 2
        yield 3
    
    def outer_generator():
        yield 'A'
        yield from inner_generator()
        yield 'B'
    
    print("  ", list(outer_generator()))


def generator_examples():
    """生成器实战示例"""
    print("\n=== 生成器实战 ===")
    
    # 1. 读取大文件
    print("1. 逐行读取文件生成器:")
    def read_large_file(filepath):
        """逐行读取大文件"""
        with open(filepath, 'r') as file:
            for line in file:
                yield line.strip()
    
    # 创建测试文件
    with open('/tmp/large_file.txt', 'w') as f:
        for i in range(5):
            f.write(f"Line {i+1}\n")
    
    for line in read_large_file('/tmp/large_file.txt'):
        print(f"  {line}")
    
    # 2. 分批处理
    print("\n2. 分批处理:")
    def batch_generator(data, batch_size):
        """分批生成数据"""
        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]
    
    data = list(range(20))
    for batch in batch_generator(data, 5):
        print(f"  批次: {batch}")
    
    # 3. 数据管道
    print("\n3. 数据管道:")
    def numbers_generator():
        """生成数字"""
        for i in range(1, 11):
            yield i
    
    def filter_even(numbers):
        """过滤偶数"""
        for num in numbers:
            if num % 2 == 0:
                yield num
    
    def square(numbers):
        """平方"""
        for num in numbers:
            yield num ** 2
    
    pipeline = square(filter_even(numbers_generator()))
    print("  ", list(pipeline))
    
    # 4. 斐波那契生成器
    print("\n4. 斐波那契生成器:")
    def fibonacci():
        """无限斐波那契数列"""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    fib = fibonacci()
    print("  前15项:", [next(fib) for _ in range(15)])


# ============================================
# 3. 列表推导式
# ============================================

def list_comprehensions():
    """列表推导式"""
    print("\n=== 列表推导式 ===")
    
    # 基本语法
    print("1. 基本语法:")
    squares = [x ** 2 for x in range(10)]
    print(f"  平方数: {squares}")
    
    # 带条件
    print("\n2. 带条件:")
    evens = [x for x in range(20) if x % 2 == 0]
    print(f"  偶数: {evens}")
    
    # 多重条件
    print("\n3. 多重条件:")
    numbers = [x for x in range(20) if x % 2 == 0 if x % 3 == 0]
    print(f"  能被2和3整除: {numbers}")
    
    # if-else
    print("\n4. if-else:")
    labels = ["偶数" if x % 2 == 0 else "奇数" for x in range(10)]
    print(f"  标签: {labels}")
    
    # 嵌套循环
    print("\n5. 嵌套循环:")
    pairs = [(x, y) for x in range(3) for y in range(3)]
    print(f"  坐标对: {pairs}")
    
    # 矩阵转置
    print("\n6. 矩阵转置:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transposed = [[row[i] for row in matrix] for i in range(3)]
    print(f"  原矩阵: {matrix}")
    print(f"  转置: {transposed}")
    
    # 扁平化
    print("\n7. 扁平化:")
    nested = [[1, 2], [3, 4], [5, 6]]
    flattened = [item for sublist in nested for item in sublist]
    print(f"  嵌套列表: {nested}")
    print(f"  扁平化: {flattened}")
    
    # 字符串处理
    print("\n8. 字符串处理:")
    words = ["Hello", "World", "Python"]
    lower = [word.lower() for word in words]
    first_chars = [word[0] for word in words]
    print(f"  小写: {lower}")
    print(f"  首字符: {first_chars}")


# ============================================
# 4. 字典推导式
# ============================================

def dict_comprehensions():
    """字典推导式"""
    print("\n=== 字典推导式 ===")
    
    # 基本语法
    print("1. 基本语法:")
    squares = {x: x ** 2 for x in range(6)}
    print(f"  平方数字典: {squares}")
    
    # 从两个列表创建
    print("\n2. 从列表创建:")
    keys = ['a', 'b', 'c']
    values = [1, 2, 3]
    d = {k: v for k, v in zip(keys, values)}
    print(f"  字典: {d}")
    
    # 带条件
    print("\n3. 带条件:")
    even_squares = {x: x ** 2 for x in range(10) if x % 2 == 0}
    print(f"  偶数平方: {even_squares}")
    
    # 反转字典
    print("\n4. 反转字典:")
    original = {'a': 1, 'b': 2, 'c': 3}
    reversed_dict = {v: k for k, v in original.items()}
    print(f"  原字典: {original}")
    print(f"  反转: {reversed_dict}")
    
    # 字符串转字典
    print("\n5. 字符串统计:")
    text = "hello world"
    char_count = {char: text.count(char) for char in set(text) if char != ' '}
    print(f"  字符统计: {char_count}")
    
    # 嵌套字典
    print("\n6. 嵌套处理:")
    students = {'Alice': [85, 90, 88], 'Bob': [78, 82, 80], 'Charlie': [92, 95, 94]}
    averages = {name: sum(scores) / len(scores) for name, scores in students.items()}
    print(f"  平均分: {averages}")


# ============================================
# 5. 集合推导式
# ============================================

def set_comprehensions():
    """集合推导式"""
    print("\n=== 集合推导式 ===")
    
    # 基本语法
    print("1. 基本语法:")
    squares = {x ** 2 for x in range(10)}
    print(f"  平方数集合: {squares}")
    
    # 去重
    print("\n2. 去重:")
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    unique = {x for x in numbers}
    print(f"  原列表: {numbers}")
    print(f"  去重: {unique}")
    
    # 带条件
    print("\n3. 带条件:")
    evens = {x for x in range(20) if x % 2 == 0}
    print(f"  偶数集合: {evens}")
    
    # 字符串处理
    print("\n4. 字符串处理:")
    text = "hello world"
    unique_chars = {char.lower() for char in text if char.isalpha()}
    print(f"  唯一字符: {unique_chars}")


# ============================================
# 6. 生成器表达式
# ============================================

def generator_expressions():
    """生成器表达式"""
    print("\n=== 生成器表达式 ===")
    
    # 基本语法（类似列表推导式，但使用圆括号）
    print("1. 基本语法:")
    squares_gen = (x ** 2 for x in range(10))
    print(f"  生成器: {squares_gen}")
    print(f"  转为列表: {list(squares_gen)}")
    
    # 内存效率
    print("\n2. 内存效率对比:")
    import sys
    list_comp = [x ** 2 for x in range(10000)]
    gen_exp = (x ** 2 for x in range(10000))
    print(f"  列表推导式大小: {sys.getsizeof(list_comp)} 字节")
    print(f"  生成器表达式大小: {sys.getsizeof(gen_exp)} 字节")
    
    # 链式操作
    print("\n3. 链式操作:")
    numbers = range(20)
    filtered = (x for x in numbers if x % 2 == 0)
    squared = (x ** 2 for x in filtered)
    print(f"  结果: {list(squared)}")
    
    # 在函数中使用
    print("\n4. 在函数中使用:")
    result = sum(x ** 2 for x in range(10))
    print(f"  平方和: {result}")
    
    max_value = max(x for x in range(10) if x % 2 == 0)
    print(f"  最大偶数: {max_value}")


# ============================================
# 7. itertools 模块
# ============================================

def itertools_demo():
    """itertools 模块"""
    print("\n=== itertools 模块 ===")
    
    # 1. count - 无限计数
    print("1. count():")
    counter = count(10, 2)  # 从10开始，步长2
    print(f"  前5项: {[next(counter) for _ in range(5)]}")
    
    # 2. cycle - 循环
    print("\n2. cycle():")
    cycler = cycle(['A', 'B', 'C'])
    print(f"  前8项: {[next(cycler) for _ in range(8)]}")
    
    # 3. repeat - 重复
    print("\n3. repeat():")
    repeater = repeat('X', 5)
    print(f"  重复5次: {list(repeater)}")
    
    # 4. chain - 连接
    print("\n4. chain():")
    chained = chain([1, 2, 3], ['a', 'b', 'c'])
    print(f"  连接: {list(chained)}")
    
    # 5. compress - 根据选择器过滤
    print("\n5. compress():")
    data = ['A', 'B', 'C', 'D', 'E']
    selectors = [1, 0, 1, 0, 1]
    filtered = compress(data, selectors)
    print(f"  过滤: {list(filtered)}")
    
    # 6. dropwhile - 丢弃开头
    print("\n6. dropwhile():")
    data = [1, 2, 3, 4, 5, 1, 2]
    result = dropwhile(lambda x: x < 4, data)
    print(f"  丢弃<4: {list(result)}")
    
    # 7. takewhile - 保留开头
    print("\n7. takewhile():")
    data = [1, 2, 3, 4, 5, 1, 2]
    result = takewhile(lambda x: x < 4, data)
    print(f"  保留<4: {list(result)}")
    
    # 8. groupby - 分组
    print("\n8. groupby():")
    data = [('A', 1), ('A', 2), ('B', 3), ('B', 4), ('C', 5)]
    for key, group in groupby(data, lambda x: x[0]):
        print(f"  {key}: {list(group)}")
    
    # 9. combinations - 组合
    print("\n9. combinations():")
    result = combinations([1, 2, 3, 4], 2)
    print(f"  2-组合: {list(result)}")
    
    # 10. permutations - 排列
    print("\n10. permutations():")
    result = permutations([1, 2, 3], 2)
    print(f"  2-排列: {list(result)}")
    
    # 11. product - 笛卡尔积
    print("\n11. product():")
    result = product([1, 2], ['a', 'b'])
    print(f"  笛卡尔积: {list(result)}")
    
    # 12. accumulate - 累积
    print("\n12. accumulate():")
    result = accumulate([1, 2, 3, 4, 5])
    print(f"  累加: {list(result)}")
    
    result = accumulate([1, 2, 3, 4, 5], lambda x, y: x * y)
    print(f"  累乘: {list(result)}")


# ============================================
# 8. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 数据处理管道
    print("1. 数据处理管道:")
    data = range(1, 21)
    
    # 过滤、转换、聚合
    result = sum(x ** 2 for x in data if x % 2 == 0)
    print(f"  偶数平方和: {result}")
    
    # 2. 文件处理
    print("\n2. 文件处理 - 统计单词:")
    text = """
    Python is a high-level programming language.
    Python is easy to learn and powerful.
    Many developers love Python.
    """
    
    words = (word.lower().strip('.,') for word in text.split())
    unique_words = {word for word in words if len(word) > 3}
    print(f"  长度>3的唯一单词: {unique_words}")
    
    # 3. 数据转换
    print("\n3. 数据转换:")
    students = [
        {'name': 'Alice', 'score': 85},
        {'name': 'Bob', 'score': 92},
        {'name': 'Charlie', 'score': 78},
        {'name': 'David', 'score': 95}
    ]
    
    # 转换为字典
    score_dict = {s['name']: s['score'] for s in students}
    print(f"  成绩字典: {score_dict}")
    
    # 过滤高分学生
    high_scorers = [s['name'] for s in students if s['score'] >= 90]
    print(f"  高分学生: {high_scorers}")
    
    # 4. 矩阵操作
    print("\n4. 矩阵操作:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    # 转置
    transposed = [[row[i] for row in matrix] for i in range(3)]
    print(f"  转置: {transposed}")
    
    # 每行求和
    row_sums = [sum(row) for row in matrix]
    print(f"  行和: {row_sums}")
    
    # 每列求和
    col_sums = [sum(row[i] for row in matrix) for i in range(3)]
    print(f"  列和: {col_sums}")
    
    # 5. 生成测试数据
    print("\n5. 生成测试数据:")
    
    def generate_test_users(count):
        """生成测试用户"""
        for i in range(count):
            yield {
                'id': i + 1,
                'name': f'User{i+1}',
                'email': f'user{i+1}@example.com'
            }
    
    users = list(generate_test_users(5))
    for user in users:
        print(f"  {user}")
    
    # 6. 滑动窗口
    print("\n6. 滑动窗口:")
    def sliding_window(data, window_size):
        """滑动窗口生成器"""
        for i in range(len(data) - window_size + 1):
            yield data[i:i + window_size]
    
    data = list(range(1, 11))
    for window in sliding_window(data, 3):
        print(f"  {window}")
    
    # 7. 分页生成器
    print("\n7. 分页生成器:")
    def paginate(data, page_size):
        """分页生成器"""
        for i in range(0, len(data), page_size):
            yield data[i:i + page_size]
    
    items = list(range(1, 26))
    for page_num, page in enumerate(paginate(items, 10), 1):
        print(f"  第{page_num}页: {page}")


# ============================================
# 9. 性能对比
# ============================================

def performance_comparison():
    """性能对比"""
    print("\n=== 性能对比 ===")
    
    import time
    
    n = 1000000
    
    # 1. 列表推导式 vs for循环
    print("1. 列表推导式 vs for循环:")
    
    start = time.time()
    result = [x ** 2 for x in range(n)]
    list_comp_time = time.time() - start
    print(f"  列表推导式: {list_comp_time:.4f} 秒")
    
    start = time.time()
    result = []
    for x in range(n):
        result.append(x ** 2)
    for_loop_time = time.time() - start
    print(f"  for循环: {for_loop_time:.4f} 秒")
    
    # 2. 生成器 vs 列表
    print("\n2. 内存使用 - 生成器 vs 列表:")
    print(f"  列表: {sys.getsizeof([x for x in range(1000)])} 字节")
    print(f"  生成器: {sys.getsizeof(x for x in range(1000))} 字节")


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 迭代器与推导式详解")
    print("=" * 60)
    
    iterator_basics()
    custom_iterator()
    
    generator_basics()
    generator_advanced()
    generator_examples()
    
    list_comprehensions()
    dict_comprehensions()
    set_comprehensions()
    generator_expressions()
    
    itertools_demo()
    practical_examples()
    performance_comparison()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Python 集合类型详解 (with Type Hints)
=====================================

本文件涵盖：
- tuple (元组)
- list (列表)
- set (集合)
- dict (字典)
- 其他集合类型
"""

from typing import Any, NamedTuple, TypedDict, Sequence, Mapping
from collections import defaultdict, Counter, OrderedDict, deque, ChainMap
from dataclasses import dataclass, field
import heapq

# ============================================================================
# 1. tuple 元组
# ============================================================================

class TupleDemo:
    """元组：不可变有序序列"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        # 创建元组
        t1: tuple[int, int, int] = (1, 2, 3)
        t2: tuple[str, ...] = ("a", "b", "c", "d")  # 可变长度元组
        t3: tuple[()] = ()                          # 空元组
        t4: tuple[int] = (42,)                      # 单元素元组（注意逗号）
        
        # 不加括号也可以
        t5: tuple[int, str, float] = 1, "hello", 3.14
        
        print(f"t1: {t1}")
        print(f"Single element tuple: {t4}")
        print(f"Mixed types: {t5}")
        
        # 索引和切片
        print(f"t1[0] = {t1[0]}")
        print(f"t1[-1] = {t1[-1]}")
        print(f"t1[1:] = {t1[1:]}")
        
        # 元组是不可变的
        # t1[0] = 10  # TypeError!
        
        # 但如果元组包含可变对象...
        t6: tuple[list[int], list[int]] = ([1, 2], [3, 4])
        t6[0].append(99)  # 这是允许的！
        print(f"Tuple with mutable: {t6}")
    
    @staticmethod
    def tuple_unpacking() -> None:
        """元组解包"""
        # 基本解包
        point: tuple[int, int] = (10, 20)
        x, y = point
        print(f"x={x}, y={y}")
        
        # 交换变量
        a, b = 1, 2
        a, b = b, a
        print(f"Swapped: a={a}, b={b}")
        
        # 星号解包
        first, *rest = (1, 2, 3, 4, 5)
        print(f"first={first}, rest={rest}")  # first=1, rest=[2, 3, 4, 5]
        
        first, *middle, last = (1, 2, 3, 4, 5)
        print(f"first={first}, middle={middle}, last={last}")
        
        # 嵌套解包
        data: tuple[str, tuple[int, int]] = ("point", (100, 200))
        name, (px, py) = data
        print(f"name={name}, px={px}, py={py}")
        
        # 函数返回多值
        def get_stats(numbers: list[int]) -> tuple[int, int, float]:
            return min(numbers), max(numbers), sum(numbers) / len(numbers)
        
        minimum, maximum, average = get_stats([1, 2, 3, 4, 5])
        print(f"min={minimum}, max={maximum}, avg={average}")
    
    @staticmethod
    def tuple_methods() -> None:
        """元组方法"""
        t: tuple[int, ...] = (1, 2, 3, 2, 1, 2)
        
        print(f"count(2): {t.count(2)}")   # 3
        print(f"index(3): {t.index(3)}")   # 2
        
        # 元组可以作为字典的键（因为不可变且可哈希）
        locations: dict[tuple[int, int], str] = {
            (0, 0): "origin",
            (1, 0): "east",
            (0, 1): "north",
        }
        print(f"Location at (0, 0): {locations[(0, 0)]}")


# ============================================================================
# 2. NamedTuple - 命名元组
# ============================================================================

# 方式 1: 类型化的命名元组（推荐）
class Point(NamedTuple):
    """二维点"""
    x: float
    y: float
    label: str = "default"  # 带默认值


class User(NamedTuple):
    """用户信息"""
    id: int
    name: str
    email: str
    is_active: bool = True


class NamedTupleDemo:
    """命名元组示例"""
    
    @staticmethod
    def basic_usage() -> None:
        """基本使用"""
        # 创建实例
        p1 = Point(3.0, 4.0, "A")
        p2 = Point(x=0.0, y=0.0)  # 使用默认 label
        
        # 通过名称访问
        print(f"p1.x = {p1.x}, p1.y = {p1.y}, p1.label = {p1.label}")
        
        # 也可以通过索引访问
        print(f"p1[0] = {p1[0]}")
        
        # 解包
        x, y, label = p1
        print(f"Unpacked: x={x}, y={y}, label={label}")
        
        # 转换为字典
        print(f"As dict: {p1._asdict()}")
        
        # 创建修改后的副本
        p3 = p1._replace(x=10.0)
        print(f"Replaced: {p3}")
        
        # 获取字段名
        print(f"Fields: {Point._fields}")
    
    @staticmethod
    def practical_example() -> None:
        """实际应用"""
        users: list[User] = [
            User(1, "Alice", "alice@example.com"),
            User(2, "Bob", "bob@example.com", False),
            User(3, "Charlie", "charlie@example.com"),
        ]
        
        # 筛选活跃用户
        active_users = [u for u in users if u.is_active]
        print(f"Active users: {[u.name for u in active_users]}")
        
        # 可以用于字典键
        user_scores: dict[User, int] = {
            users[0]: 100,
            users[1]: 85,
        }
        print(f"Alice's score: {user_scores[users[0]]}")


# ============================================================================
# 3. list 列表
# ============================================================================

class ListDemo:
    """列表：可变有序序列"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        # 创建列表
        nums: list[int] = [1, 2, 3, 4, 5]
        mixed: list[Any] = [1, "two", 3.0, [4, 5]]
        empty: list[str] = []
        
        # 从其他可迭代对象创建
        from_range: list[int] = list(range(5))
        from_str: list[str] = list("hello")
        
        print(f"nums: {nums}")
        print(f"from_range: {from_range}")
        print(f"from_str: {from_str}")
        
        # 索引
        print(f"nums[0] = {nums[0]}")      # 1
        print(f"nums[-1] = {nums[-1]}")    # 5
        
        # 切片 [start:stop:step]
        print(f"nums[1:4] = {nums[1:4]}")    # [2, 3, 4]
        print(f"nums[::2] = {nums[::2]}")    # [1, 3, 5]
        print(f"nums[::-1] = {nums[::-1]}")  # [5, 4, 3, 2, 1] (反转)
        
        # 修改
        nums[0] = 10
        nums[1:3] = [20, 30]
        print(f"After modification: {nums}")
    
    @staticmethod
    def list_methods() -> None:
        """列表方法"""
        nums: list[int] = [3, 1, 4, 1, 5, 9, 2, 6]
        
        # 添加元素
        nums.append(10)           # 末尾添加
        print(f"After append(10): {nums}")
        
        nums.insert(0, 0)         # 指定位置插入
        print(f"After insert(0, 0): {nums}")
        
        nums.extend([7, 8])       # 扩展多个元素
        print(f"After extend([7,8]): {nums}")
        
        # 删除元素
        removed = nums.pop()      # 删除并返回最后一个
        print(f"pop(): {removed}, list: {nums}")
        
        removed = nums.pop(0)     # 删除指定索引
        print(f"pop(0): {removed}, list: {nums}")
        
        nums.remove(1)            # 删除第一个匹配值
        print(f"After remove(1): {nums}")
        
        # 查找
        print(f"index(4): {nums.index(4)}")     # 找到返回索引
        print(f"count(1): {nums.count(1)}")     # 计数
        print(f"5 in nums: {5 in nums}")        # 成员检查
        
        # 排序
        nums.sort()               # 原地排序
        print(f"After sort(): {nums}")
        
        nums.sort(reverse=True)   # 降序
        print(f"After sort(reverse=True): {nums}")
        
        # 使用 key 函数排序
        words: list[str] = ["apple", "Banana", "cherry"]
        words.sort(key=str.lower)  # 忽略大小写排序
        print(f"Sorted words: {words}")
        
        # sorted() 返回新列表，不修改原列表
        original: list[int] = [3, 1, 2]
        new_sorted: list[int] = sorted(original)
        print(f"original: {original}, sorted: {new_sorted}")
        
        # 反转
        nums.reverse()
        print(f"After reverse(): {nums}")
        
        # 复制
        nums_copy: list[int] = nums.copy()  # 浅拷贝
        # 或者 nums_copy = nums[:]
        # 或者 nums_copy = list(nums)
        
        # 清空
        nums.clear()
        print(f"After clear(): {nums}")
    
    @staticmethod
    def list_comprehension() -> None:
        """列表推导式"""
        # 基本语法: [expression for item in iterable]
        squares: list[int] = [x**2 for x in range(10)]
        print(f"Squares: {squares}")
        
        # 带条件: [expression for item in iterable if condition]
        even_squares: list[int] = [x**2 for x in range(10) if x % 2 == 0]
        print(f"Even squares: {even_squares}")
        
        # 嵌套循环
        matrix: list[list[int]] = [[i*3 + j for j in range(3)] for i in range(3)]
        print(f"Matrix: {matrix}")
        
        # 扁平化
        flat: list[int] = [x for row in matrix for x in row]
        print(f"Flattened: {flat}")
        
        # 带 if-else
        labels: list[str] = ["even" if x % 2 == 0 else "odd" for x in range(5)]
        print(f"Labels: {labels}")
        
        # 嵌套 if
        filtered: list[int] = [x for x in range(20) if x % 2 == 0 if x % 3 == 0]
        print(f"Divisible by 2 and 3: {filtered}")
        
        # 字典推导
        word = "hello"
        char_index: dict[str, int] = {c: i for i, c in enumerate(word)}
        print(f"Char index: {char_index}")
        
        # 集合推导
        unique_lengths: set[int] = {len(w) for w in ["hi", "hello", "hey", "world"]}
        print(f"Unique lengths: {unique_lengths}")
    
    @staticmethod
    def list_as_stack_queue() -> None:
        """列表作为栈和队列"""
        # 作为栈 (LIFO) - append/pop 很高效
        stack: list[int] = []
        stack.append(1)
        stack.append(2)
        stack.append(3)
        print(f"Stack: {stack}")
        print(f"Pop: {stack.pop()}")  # 3
        
        # 作为队列 (FIFO) - 不推荐，pop(0) 是 O(n)
        # 应该使用 collections.deque
        queue: deque[int] = deque()
        queue.append(1)
        queue.append(2)
        queue.append(3)
        print(f"Queue: {queue}")
        print(f"Popleft: {queue.popleft()}")  # 1


# ============================================================================
# 4. set 集合
# ============================================================================

class SetDemo:
    """集合：无序不重复元素"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        # 创建集合
        s1: set[int] = {1, 2, 3, 4, 5}
        s2: set[int] = set([1, 2, 3])
        empty: set[int] = set()  # 注意：{} 创建的是空字典！
        
        # 自动去重
        numbers: set[int] = {1, 2, 2, 3, 3, 3}
        print(f"Set with duplicates: {numbers}")  # {1, 2, 3}
        
        # 集合元素必须可哈希
        # invalid = {[1, 2, 3]}  # TypeError! 列表不可哈希
        valid: set[tuple[int, ...]] = {(1, 2), (3, 4)}  # 元组可以
        
        print(f"s1: {s1}")
        print(f"Tuple set: {valid}")
    
    @staticmethod
    def set_methods() -> None:
        """集合方法"""
        s: set[int] = {1, 2, 3}
        
        # 添加元素
        s.add(4)
        print(f"After add(4): {s}")
        
        s.update([5, 6, 7])  # 添加多个
        print(f"After update([5,6,7]): {s}")
        
        # 删除元素
        s.remove(7)          # 删除指定元素（不存在会报错）
        print(f"After remove(7): {s}")
        
        s.discard(99)        # 安全删除（不存在不报错）
        print(f"After discard(99): {s}")
        
        popped = s.pop()     # 删除并返回任意元素
        print(f"Popped: {popped}")
        
        # 成员检查 - O(1) 平均时间
        print(f"3 in s: {3 in s}")
    
    @staticmethod
    def set_operations() -> None:
        """集合运算"""
        a: set[int] = {1, 2, 3, 4, 5}
        b: set[int] = {4, 5, 6, 7, 8}
        
        # 并集 (Union)
        print(f"a | b = {a | b}")              # {1, 2, 3, 4, 5, 6, 7, 8}
        print(f"a.union(b) = {a.union(b)}")
        
        # 交集 (Intersection)
        print(f"a & b = {a & b}")              # {4, 5}
        print(f"a.intersection(b) = {a.intersection(b)}")
        
        # 差集 (Difference)
        print(f"a - b = {a - b}")              # {1, 2, 3}
        print(f"a.difference(b) = {a.difference(b)}")
        
        # 对称差集 (Symmetric Difference)
        print(f"a ^ b = {a ^ b}")              # {1, 2, 3, 6, 7, 8}
        print(f"a.symmetric_difference(b) = {a.symmetric_difference(b)}")
        
        # 子集和超集检查
        c: set[int] = {1, 2}
        print(f"c <= a (subset): {c <= a}")           # True
        print(f"c.issubset(a): {c.issubset(a)}")      # True
        print(f"a >= c (superset): {a >= c}")         # True
        print(f"a.issuperset(c): {a.issuperset(c)}")  # True
        
        # 不相交检查
        d: set[int] = {10, 20}
        print(f"a.isdisjoint(d): {a.isdisjoint(d)}")  # True
    
    @staticmethod
    def frozenset_demo() -> None:
        """不可变集合"""
        # frozenset 是不可变的，可以作为字典的键或放入其他集合
        fs: frozenset[int] = frozenset([1, 2, 3])
        
        # fs.add(4)  # AttributeError!
        
        # 可以作为字典键
        data: dict[frozenset[int], str] = {
            frozenset([1, 2]): "pair_12",
            frozenset([3, 4]): "pair_34",
        }
        print(f"Data: {data}")
        
        # 集合的集合
        set_of_sets: set[frozenset[int]] = {
            frozenset([1, 2]),
            frozenset([3, 4]),
        }
        print(f"Set of sets: {set_of_sets}")
    
    @staticmethod
    def practical_examples() -> None:
        """实际应用"""
        # 去重
        items: list[int] = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
        unique: list[int] = list(set(items))
        print(f"Unique items: {unique}")
        
        # 保持顺序去重 (Python 3.7+)
        unique_ordered: list[int] = list(dict.fromkeys(items))
        print(f"Unique (ordered): {unique_ordered}")
        
        # 快速查找
        valid_users: set[str] = {"alice", "bob", "charlie"}
        user = "alice"
        if user in valid_users:  # O(1)
            print(f"{user} is valid")
        
        # 找出共同好友
        alice_friends: set[str] = {"bob", "charlie", "david"}
        bob_friends: set[str] = {"alice", "charlie", "eve"}
        common: set[str] = alice_friends & bob_friends
        print(f"Common friends: {common}")


# ============================================================================
# 5. dict 字典
# ============================================================================

class DictDemo:
    """字典：键值对映射"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        # 创建字典
        d1: dict[str, int] = {"a": 1, "b": 2, "c": 3}
        d2: dict[str, int] = dict(a=1, b=2, c=3)
        d3: dict[str, int] = dict([("a", 1), ("b", 2)])
        empty: dict[str, Any] = {}
        
        print(f"d1: {d1}")
        
        # 访问
        print(f"d1['a'] = {d1['a']}")
        # print(d1['z'])  # KeyError!
        
        # get() 安全访问
        print(f"d1.get('a') = {d1.get('a')}")      # 1
        print(f"d1.get('z') = {d1.get('z')}")      # None
        print(f"d1.get('z', 0) = {d1.get('z', 0)}")  # 0 (默认值)
        
        # 修改/添加
        d1['d'] = 4
        d1['a'] = 10
        print(f"After modification: {d1}")
        
        # 删除
        del d1['d']
        print(f"After del: {d1}")
        
        value = d1.pop('c')  # 删除并返回
        print(f"Popped: {value}, dict: {d1}")
        
        # 检查键
        print(f"'a' in d1: {'a' in d1}")
    
    @staticmethod
    def dict_methods() -> None:
        """字典方法"""
        d: dict[str, int] = {"a": 1, "b": 2, "c": 3}
        
        # 视图对象
        print(f"keys(): {list(d.keys())}")
        print(f"values(): {list(d.values())}")
        print(f"items(): {list(d.items())}")
        
        # 遍历
        for key in d:  # 默认遍历键
            print(f"Key: {key}")
        
        for key, value in d.items():
            print(f"{key}: {value}")
        
        # setdefault - 如果键不存在，设置默认值
        d.setdefault('d', 4)
        print(f"After setdefault('d', 4): {d}")
        
        d.setdefault('a', 999)  # 'a' 已存在，不会改变
        print(f"After setdefault('a', 999): {d}")
        
        # update - 批量更新
        d.update({'e': 5, 'f': 6})
        d.update(g=7)
        print(f"After update: {d}")
        
        # 合并字典 (Python 3.9+)
        d1: dict[str, int] = {'a': 1, 'b': 2}
        d2: dict[str, int] = {'c': 3, 'd': 4}
        merged = d1 | d2
        print(f"Merged (|): {merged}")
        
        # 就地合并
        d1 |= d2
        print(f"In-place merge (|=): {d1}")
        
        # popitem - 删除并返回最后插入的键值对 (Python 3.7+)
        item = d.popitem()
        print(f"Popped item: {item}")
    
    @staticmethod
    def dict_comprehension() -> None:
        """字典推导式"""
        # 基本语法
        squares: dict[int, int] = {x: x**2 for x in range(5)}
        print(f"Squares: {squares}")
        
        # 带条件
        even_squares: dict[int, int] = {x: x**2 for x in range(10) if x % 2 == 0}
        print(f"Even squares: {even_squares}")
        
        # 反转字典
        original: dict[str, int] = {'a': 1, 'b': 2, 'c': 3}
        reversed_dict: dict[int, str] = {v: k for k, v in original.items()}
        print(f"Reversed: {reversed_dict}")
        
        # 从两个列表创建
        keys: list[str] = ['name', 'age', 'city']
        values: list[Any] = ['Alice', 30, 'NYC']
        combined: dict[str, Any] = dict(zip(keys, values))
        print(f"Combined: {combined}")
    
    @staticmethod
    def special_dicts() -> None:
        """特殊字典类型"""
        # defaultdict - 自动创建缺失的键
        from collections import defaultdict
        
        # 默认值为 list
        groups: defaultdict[str, list[int]] = defaultdict(list)
        groups['even'].append(2)
        groups['odd'].append(1)
        groups['even'].append(4)
        print(f"Groups: {dict(groups)}")
        
        # 默认值为 int (计数器)
        counter: defaultdict[str, int] = defaultdict(int)
        for char in "hello world":
            counter[char] += 1
        print(f"Counter: {dict(counter)}")
        
        # Counter - 专门用于计数
        from collections import Counter
        
        text = "abracadabra"
        c = Counter(text)
        print(f"Counter: {c}")
        print(f"Most common: {c.most_common(3)}")
        
        # Counter 支持算术运算
        c1 = Counter(['a', 'b', 'a'])
        c2 = Counter(['b', 'c', 'c'])
        print(f"c1 + c2 = {c1 + c2}")
        print(f"c1 - c2 = {c1 - c2}")
        
        # OrderedDict (Python 3.7+ 普通 dict 已有序)
        # 但 OrderedDict 在比较时考虑顺序
        from collections import OrderedDict
        
        od1 = OrderedDict([('a', 1), ('b', 2)])
        od2 = OrderedDict([('b', 2), ('a', 1)])
        print(f"OrderedDict equal: {od1 == od2}")  # False
        
        d1 = {'a': 1, 'b': 2}
        d2 = {'b': 2, 'a': 1}
        print(f"Dict equal: {d1 == d2}")  # True
        
        # ChainMap - 链接多个字典
        defaults: dict[str, str] = {'color': 'red', 'size': 'medium'}
        user_settings: dict[str, str] = {'color': 'blue'}
        combined = ChainMap(user_settings, defaults)
        print(f"ChainMap color: {combined['color']}")  # 'blue'
        print(f"ChainMap size: {combined['size']}")    # 'medium'


# ============================================================================
# 6. TypedDict - 类型化字典
# ============================================================================

class UserDict(TypedDict):
    """类型化字典：指定每个键的类型"""
    name: str
    age: int
    email: str


class PartialUserDict(TypedDict, total=False):
    """total=False 表示所有键都是可选的"""
    name: str
    age: int
    nickname: str


class MixedUserDict(TypedDict):
    """混合必选和可选字段"""
    name: str  # 必选
    age: int   # 必选


class ExtendedUserDict(MixedUserDict, total=False):
    """继承并添加可选字段"""
    email: str   # 可选
    phone: str   # 可选


class TypedDictDemo:
    @staticmethod
    def basic_usage() -> None:
        """TypedDict 使用"""
        # 正确用法
        user: UserDict = {
            "name": "Alice",
            "age": 30,
            "email": "alice@example.com"
        }
        
        # 类型检查器会检查：
        # - 键是否正确
        # - 值的类型是否正确
        
        # 但运行时它就是普通字典
        print(f"User: {user}")
        print(f"Type: {type(user)}")  # <class 'dict'>
        
        # 可以像普通字典一样使用
        print(f"Name: {user['name']}")


# ============================================================================
# 7. deque 双端队列
# ============================================================================

class DequeDemo:
    """双端队列：两端高效操作"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        from collections import deque
        
        # 创建
        d: deque[int] = deque([1, 2, 3])
        d_limited: deque[int] = deque(maxlen=3)  # 固定大小
        
        # 右端操作
        d.append(4)
        print(f"After append(4): {d}")
        
        d.extend([5, 6])
        print(f"After extend([5,6]): {d}")
        
        right = d.pop()
        print(f"pop(): {right}, deque: {d}")
        
        # 左端操作 - O(1)，比 list 快
        d.appendleft(0)
        print(f"After appendleft(0): {d}")
        
        d.extendleft([-2, -1])  # 注意：顺序会反转
        print(f"After extendleft([-2,-1]): {d}")
        
        left = d.popleft()
        print(f"popleft(): {left}, deque: {d}")
        
        # 旋转
        d = deque([1, 2, 3, 4, 5])
        d.rotate(2)   # 右旋
        print(f"After rotate(2): {d}")
        
        d.rotate(-2)  # 左旋
        print(f"After rotate(-2): {d}")
    
    @staticmethod
    def practical_examples() -> None:
        """实际应用"""
        from collections import deque
        
        # 滑动窗口
        def sliding_window_max(nums: list[int], k: int) -> list[int]:
            """滑动窗口最大值"""
            result: list[int] = []
            window: deque[int] = deque()  # 存储索引
            
            for i, num in enumerate(nums):
                # 移除超出窗口的元素
                while window and window[0] <= i - k:
                    window.popleft()
                
                # 移除比当前元素小的元素
                while window and nums[window[-1]] < num:
                    window.pop()
                
                window.append(i)
                
                if i >= k - 1:
                    result.append(nums[window[0]])
            
            return result
        
        nums = [1, 3, -1, -3, 5, 3, 6, 7]
        print(f"Sliding window max (k=3): {sliding_window_max(nums, 3)}")
        
        # 最近 N 条记录
        recent_logs: deque[str] = deque(maxlen=5)
        for i in range(10):
            recent_logs.append(f"Log entry {i}")
        print(f"Recent logs: {list(recent_logs)}")


# ============================================================================
# 8. heapq 堆
# ============================================================================

class HeapDemo:
    """堆操作（最小堆）"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        # heapq 使用普通列表
        heap: list[int] = []
        
        # 添加元素
        heapq.heappush(heap, 3)
        heapq.heappush(heap, 1)
        heapq.heappush(heap, 4)
        heapq.heappush(heap, 1)
        heapq.heappush(heap, 5)
        
        print(f"Heap: {heap}")  # [1, 1, 4, 3, 5] (堆结构，不是排序)
        
        # 弹出最小元素
        print(f"heappop(): {heapq.heappop(heap)}")  # 1
        print(f"After pop: {heap}")
        
        # 查看最小元素但不删除
        print(f"Smallest: {heap[0]}")
        
        # 将列表转为堆
        nums: list[int] = [5, 2, 8, 1, 9]
        heapq.heapify(nums)
        print(f"Heapified: {nums}")
        
        # 最大的 n 个元素
        data = [1, 3, 5, 7, 9, 2, 4, 6, 8]
        print(f"3 largest: {heapq.nlargest(3, data)}")
        print(f"3 smallest: {heapq.nsmallest(3, data)}")
    
    @staticmethod
    def max_heap() -> None:
        """最大堆（通过取负实现）"""
        # Python 只有最小堆，要实现最大堆需要取负
        max_heap: list[int] = []
        
        for num in [3, 1, 4, 1, 5]:
            heapq.heappush(max_heap, -num)
        
        # 弹出时取负得到最大值
        print(f"Max: {-heapq.heappop(max_heap)}")  # 5
    
    @staticmethod
    def priority_queue() -> None:
        """优先队列示例"""
        from dataclasses import dataclass, field
        from typing import Any
        
        @dataclass(order=True)
        class Task:
            priority: int
            description: str = field(compare=False)
        
        tasks: list[Task] = []
        heapq.heappush(tasks, Task(3, "Low priority task"))
        heapq.heappush(tasks, Task(1, "High priority task"))
        heapq.heappush(tasks, Task(2, "Medium priority task"))
        
        while tasks:
            task = heapq.heappop(tasks)
            print(f"Processing: {task.description} (priority: {task.priority})")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    print("=" * 60)
    print("TUPLE DEMO")
    print("=" * 60)
    TupleDemo.basic_operations()
    print()
    TupleDemo.tuple_unpacking()
    
    print("\n" + "=" * 60)
    print("NAMEDTUPLE DEMO")
    print("=" * 60)
    NamedTupleDemo.basic_usage()
    print()
    NamedTupleDemo.practical_example()
    
    print("\n" + "=" * 60)
    print("LIST DEMO")
    print("=" * 60)
    ListDemo.basic_operations()
    print()
    ListDemo.list_methods()
    print()
    ListDemo.list_comprehension()
    
    print("\n" + "=" * 60)
    print("SET DEMO")
    print("=" * 60)
    SetDemo.basic_operations()
    print()
    SetDemo.set_operations()
    print()
    SetDemo.practical_examples()
    
    print("\n" + "=" * 60)
    print("DICT DEMO")
    print("=" * 60)
    DictDemo.basic_operations()
    print()
    DictDemo.dict_methods()
    print()
    DictDemo.dict_comprehension()
    print()
    DictDemo.special_dicts()
    
    print("\n" + "=" * 60)
    print("DEQUE DEMO")
    print("=" * 60)
    DequeDemo.basic_operations()
    
    print("\n" + "=" * 60)
    print("HEAP DEMO")
    print("=" * 60)
    HeapDemo.basic_operations()
    HeapDemo.priority_queue()


if __name__ == "__main__":
    main()

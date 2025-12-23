"""
Python 集合类型详解：tuple, list, set, dict
包含详细的方法说明和实战示例
"""

from collections import Counter, defaultdict, OrderedDict, deque
import copy


# ============================================
# 1. 元组 (tuple) - 不可变序列
# ============================================

def tuple_basics():
    """元组基础操作"""
    print("\n=== 元组 (tuple) 基础 ===")
    
    # 创建元组
    empty_tuple = ()
    single_tuple = (1,)          # 注意逗号
    my_tuple = (1, 2, 3, 4, 5)
    mixed_tuple = (1, "hello", 3.14, True)
    nested_tuple = (1, (2, 3), (4, 5, 6))
    
    # 不用括号也可以（但不推荐）
    tuple_no_parens = 1, 2, 3
    
    print(f"空元组: {empty_tuple}")
    print(f"单元素元组: {single_tuple}")
    print(f"普通元组: {my_tuple}")
    print(f"混合类型: {mixed_tuple}")
    print(f"嵌套元组: {nested_tuple}")
    
    # 索引和切片
    t = (10, 20, 30, 40, 50)
    print(f"\n索引和切片 (t={t}):")
    print(f"t[0] = {t[0]}")
    print(f"t[-1] = {t[-1]}")
    print(f"t[1:4] = {t[1:4]}")
    print(f"t[::2] = {t[::2]}")
    print(f"t[::-1] = {t[::-1]}")
    
    # 元组运算
    t1 = (1, 2, 3)
    t2 = (4, 5, 6)
    print(f"\n元组运算:")
    print(f"t1 + t2 = {t1 + t2}")
    print(f"t1 * 3 = {t1 * 3}")
    print(f"len(t1) = {len(t1)}")
    print(f"2 in t1 = {2 in t1}")
    print(f"max(t1) = {max(t1)}")
    print(f"min(t1) = {min(t1)}")
    print(f"sum(t1) = {sum(t1)}")


def tuple_methods():
    """元组的方法"""
    print("\n=== 元组方法 ===")
    
    t = (1, 2, 3, 2, 4, 2, 5)
    
    print(f"元组: {t}")
    print(f"t.count(2) = {t.count(2)}")      # 统计元素出现次数
    print(f"t.index(3) = {t.index(3)}")      # 查找元素首次出现的索引
    print(f"t.index(2, 2) = {t.index(2, 2)}")  # 从索引2开始查找
    
    # 元组解包
    print("\n元组解包:")
    coordinates = (10, 20, 30)
    x, y, z = coordinates
    print(f"x={x}, y={y}, z={z}")
    
    # 扩展解包 (Python 3.5+)
    numbers = (1, 2, 3, 4, 5)
    first, *middle, last = numbers
    print(f"first={first}, middle={middle}, last={last}")
    
    # 元组作为函数返回值
    def get_user_info():
        return "Alice", 25, "alice@example.com"
    
    name, age, email = get_user_info()
    print(f"\n函数返回: {name}, {age}, {email}")


def tuple_use_cases():
    """元组的使用场景"""
    print("\n=== 元组使用场景 ===")
    
    # 1. 作为字典的键（因为不可变）
    locations = {
        (0, 0): "原点",
        (1, 2): "点A",
        (3, 4): "点B"
    }
    print(f"坐标字典: {locations[(1, 2)]}")
    
    # 2. 函数多返回值
    def divide_with_remainder(a, b):
        return a // b, a % b
    
    quotient, remainder = divide_with_remainder(17, 5)
    print(f"17 ÷ 5 = {quotient} 余 {remainder}")
    
    # 3. 不可变性保护数据
    config = ("localhost", 8080, "admin")
    # config[0] = "127.0.0.1"  # 这会报错！
    print(f"配置（不可修改）: {config}")
    
    # 4. 命名元组（更具可读性）
    from collections import namedtuple
    
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)
    print(f"\n命名元组: {p}")
    print(f"p.x = {p.x}, p.y = {p.y}")
    
    Person = namedtuple('Person', ['name', 'age', 'city'])
    person = Person(name="Bob", age=30, city="Beijing")
    print(f"Person: {person.name}, {person.age}岁, 来自{person.city}")


# ============================================
# 2. 列表 (list) - 可变序列
# ============================================

def list_basics():
    """列表基础操作"""
    print("\n=== 列表 (list) 基础 ===")
    
    # 创建列表
    empty_list = []
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True, [1, 2]]
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    print(f"空列表: {empty_list}")
    print(f"数字列表: {numbers}")
    print(f"混合类型: {mixed}")
    print(f"二维列表: {matrix}")
    
    # 列表推导式创建
    squares = [x**2 for x in range(10)]
    print(f"平方数: {squares}")
    
    # 索引和切片
    lst = [10, 20, 30, 40, 50]
    print(f"\n索引和切片 (lst={lst}):")
    print(f"lst[0] = {lst[0]}")
    print(f"lst[-1] = {lst[-1]}")
    print(f"lst[1:4] = {lst[1:4]}")
    print(f"lst[::2] = {lst[::2]}")
    print(f"lst[::-1] = {lst[::-1]}")
    
    # 修改元素
    lst[0] = 100
    print(f"修改后: {lst}")
    
    # 列表运算
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    print(f"\n列表运算:")
    print(f"list1 + list2 = {list1 + list2}")
    print(f"list1 * 2 = {list1 * 2}")
    print(f"len(list1) = {len(list1)}")
    print(f"2 in list1 = {2 in list1}")


def list_methods():
    """列表的方法"""
    print("\n=== 列表方法 ===")
    
    # 添加元素
    lst = [1, 2, 3]
    print(f"初始列表: {lst}")
    
    lst.append(4)                    # 末尾添加
    print(f"append(4): {lst}")
    
    lst.insert(0, 0)                 # 指定位置插入
    print(f"insert(0, 0): {lst}")
    
    lst.extend([5, 6, 7])            # 扩展列表
    print(f"extend([5,6,7]): {lst}")
    
    # 删除元素
    print("\n删除元素:")
    lst = [1, 2, 3, 2, 4, 2, 5]
    print(f"初始列表: {lst}")
    
    lst.remove(2)                    # 删除第一个匹配项
    print(f"remove(2): {lst}")
    
    popped = lst.pop()               # 删除并返回最后一个元素
    print(f"pop(): {popped}, 列表: {lst}")
    
    popped = lst.pop(0)              # 删除并返回指定索引
    print(f"pop(0): {popped}, 列表: {lst}")
    
    del lst[0]                       # 使用 del 删除
    print(f"del lst[0]: {lst}")
    
    lst.clear()                      # 清空列表
    print(f"clear(): {lst}")
    
    # 查找和统计
    print("\n查找和统计:")
    lst = [1, 2, 3, 2, 4, 2, 5]
    print(f"列表: {lst}")
    print(f"lst.index(3) = {lst.index(3)}")
    print(f"lst.count(2) = {lst.count(2)}")
    
    # 排序和反转
    print("\n排序和反转:")
    lst = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"原列表: {lst}")
    
    lst.sort()                       # 原地排序
    print(f"sort(): {lst}")
    
    lst.sort(reverse=True)           # 降序排序
    print(f"sort(reverse=True): {lst}")
    
    lst.reverse()                    # 反转列表
    print(f"reverse(): {lst}")
    
    # sorted() 返回新列表
    lst = [3, 1, 4, 1, 5]
    sorted_lst = sorted(lst)
    print(f"\noriginal: {lst}")
    print(f"sorted(): {sorted_lst}")
    
    # 复制列表
    print("\n复制列表:")
    lst1 = [1, 2, 3]
    lst2 = lst1                      # 引用
    lst3 = lst1.copy()               # 浅复制
    lst4 = lst1[:]                   # 浅复制
    lst5 = list(lst1)                # 浅复制
    lst6 = copy.deepcopy(lst1)       # 深复制
    
    lst1[0] = 100
    print(f"lst1: {lst1}")
    print(f"lst2 (引用): {lst2}")
    print(f"lst3 (copy): {lst3}")


def list_advanced():
    """列表高级操作"""
    print("\n=== 列表高级操作 ===")
    
    # 列表推导式
    print("列表推导式:")
    squares = [x**2 for x in range(10)]
    print(f"平方数: {squares}")
    
    evens = [x for x in range(20) if x % 2 == 0]
    print(f"偶数: {evens}")
    
    matrix = [[i*3 + j + 1 for j in range(3)] for i in range(3)]
    print(f"矩阵: {matrix}")
    
    # 嵌套列表操作
    print("\n嵌套列表操作:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    # 转置矩阵
    transposed = [[row[i] for row in matrix] for i in range(3)]
    print(f"转置: {transposed}")
    
    # 使用 zip 转置
    transposed2 = list(zip(*matrix))
    print(f"zip转置: {transposed2}")
    
    # 扁平化列表
    nested = [[1, 2], [3, 4], [5, 6]]
    flattened = [item for sublist in nested for item in sublist]
    print(f"\n扁平化: {nested} -> {flattened}")
    
    # 列表的切片赋值
    print("\n切片赋值:")
    lst = [1, 2, 3, 4, 5]
    print(f"原列表: {lst}")
    
    lst[1:3] = [20, 30]
    print(f"lst[1:3] = [20, 30]: {lst}")
    
    lst[1:4] = [200]                 # 替换多个元素为一个
    print(f"lst[1:4] = [200]: {lst}")
    
    lst[1:1] = [100, 150]            # 插入元素
    print(f"lst[1:1] = [100, 150]: {lst}")


# ============================================
# 3. 集合 (set) - 无序不重复集合
# ============================================

def set_basics():
    """集合基础操作"""
    print("\n=== 集合 (set) 基础 ===")
    
    # 创建集合
    empty_set = set()                # 注意: {} 是空字典
    numbers = {1, 2, 3, 4, 5}
    from_list = set([1, 2, 2, 3, 3, 4])
    from_string = set("hello")
    
    print(f"空集合: {empty_set}")
    print(f"数字集合: {numbers}")
    print(f"从列表创建: {from_list}")
    print(f"从字符串创建: {from_string}")
    
    # 集合自动去重
    duplicates = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4}
    print(f"自动去重: {duplicates}")
    
    # 集合运算
    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7, 8}
    
    print(f"\n集合运算 (a={a}, b={b}):")
    print(f"并集 a | b: {a | b}")
    print(f"交集 a & b: {a & b}")
    print(f"差集 a - b: {a - b}")
    print(f"对称差 a ^ b: {a ^ b}")
    
    # 子集和超集
    c = {1, 2, 3}
    d = {1, 2, 3, 4, 5}
    print(f"\n子集和超集 (c={c}, d={d}):")
    print(f"c <= d (子集): {c <= d}")
    print(f"c < d (真子集): {c < d}")
    print(f"d >= c (超集): {d >= c}")
    print(f"d > c (真超集): {d > c}")


def set_methods():
    """集合的方法"""
    print("\n=== 集合方法 ===")
    
    # 添加元素
    s = {1, 2, 3}
    print(f"初始集合: {s}")
    
    s.add(4)
    print(f"add(4): {s}")
    
    s.update([5, 6, 7])
    print(f"update([5,6,7]): {s}")
    
    s.update([7, 8], {9, 10})
    print(f"update([7,8], {{9,10}}): {s}")
    
    # 删除元素
    print("\n删除元素:")
    s = {1, 2, 3, 4, 5}
    print(f"初始集合: {s}")
    
    s.remove(3)                      # 元素不存在会报错
    print(f"remove(3): {s}")
    
    s.discard(10)                    # 元素不存在不报错
    print(f"discard(10): {s}")
    
    popped = s.pop()                 # 随机删除并返回一个元素
    print(f"pop(): {popped}, 集合: {s}")
    
    s.clear()
    print(f"clear(): {s}")
    
    # 集合方法运算
    print("\n集合方法运算:")
    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7, 8}
    
    print(f"a.union(b): {a.union(b)}")
    print(f"a.intersection(b): {a.intersection(b)}")
    print(f"a.difference(b): {a.difference(b)}")
    print(f"a.symmetric_difference(b): {a.symmetric_difference(b)}")
    
    # 原地修改
    print("\n原地修改:")
    a = {1, 2, 3, 4, 5}
    print(f"初始 a: {a}")
    
    a.intersection_update({3, 4, 5, 6})
    print(f"intersection_update({{3,4,5,6}}): {a}")
    
    # 不可变集合 frozenset
    print("\n不可变集合 frozenset:")
    fs = frozenset([1, 2, 3, 4, 5])
    print(f"frozenset: {fs}")
    print(f"可以作为字典键或集合元素")
    
    nested_set = {frozenset([1, 2]), frozenset([3, 4])}
    print(f"嵌套集合: {nested_set}")


def set_use_cases():
    """集合的使用场景"""
    print("\n=== 集合使用场景 ===")
    
    # 1. 去重
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5]
    unique = list(set(numbers))
    print(f"列表去重: {numbers} -> {unique}")
    
    # 2. 成员测试（高效）
    valid_users = {"alice", "bob", "charlie"}
    print(f"\n成员测试:")
    print(f"'alice' in valid_users: {'alice' in valid_users}")
    print(f"'david' in valid_users: {'david' in valid_users}")
    
    # 3. 找出共同好友
    alice_friends = {"bob", "charlie", "david"}
    bob_friends = {"alice", "charlie", "eve"}
    common = alice_friends & bob_friends
    print(f"\n共同好友: {common}")
    
    # 4. 找出差异
    old_inventory = {"apple", "banana", "orange"}
    new_inventory = {"banana", "orange", "grape", "melon"}
    removed = old_inventory - new_inventory
    added = new_inventory - old_inventory
    print(f"\n库存变化:")
    print(f"移除: {removed}")
    print(f"新增: {added}")


# ============================================
# 4. 字典 (dict) - 键值对映射
# ============================================

def dict_basics():
    """字典基础操作"""
    print("\n=== 字典 (dict) 基础 ===")
    
    # 创建字典
    empty_dict = {}
    person = {"name": "Alice", "age": 25, "city": "Beijing"}
    mixed = {1: "one", "two": 2, (3, 4): "tuple_key"}
    from_tuples = dict([("a", 1), ("b", 2), ("c", 3)])
    from_kwargs = dict(name="Bob", age=30)
    
    print(f"空字典: {empty_dict}")
    print(f"基本字典: {person}")
    print(f"混合键类型: {mixed}")
    print(f"从元组创建: {from_tuples}")
    print(f"从关键字创建: {from_kwargs}")
    
    # 访问元素
    print(f"\n访问元素:")
    print(f"person['name'] = {person['name']}")
    print(f"person.get('age') = {person.get('age')}")
    print(f"person.get('email', '未提供') = {person.get('email', '未提供')}")
    
    # 修改和添加
    person["age"] = 26
    person["email"] = "alice@example.com"
    print(f"修改后: {person}")
    
    # 删除元素
    del person["email"]
    print(f"删除 email: {person}")


def dict_methods():
    """字典的方法"""
    print("\n=== 字典方法 ===")
    
    person = {"name": "Alice", "age": 25, "city": "Beijing"}
    
    # 获取键、值、项
    print("遍历字典:")
    print(f"keys(): {list(person.keys())}")
    print(f"values(): {list(person.values())}")
    print(f"items(): {list(person.items())}")
    
    # 遍历
    print("\nfor循环遍历:")
    for key in person:
        print(f"  {key}: {person[key]}")
    
    print("\n遍历键值对:")
    for key, value in person.items():
        print(f"  {key} = {value}")
    
    # 更新字典
    print("\n更新字典:")
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    print(f"d1: {d1}")
    print(f"d2: {d2}")
    d1.update(d2)
    print(f"d1.update(d2): {d1}")
    
    # pop 和 popitem
    print("\n删除并返回:")
    d = {"a": 1, "b": 2, "c": 3}
    print(f"原字典: {d}")
    
    value = d.pop("b")
    print(f"pop('b'): {value}, 字典: {d}")
    
    item = d.popitem()               # 删除最后插入的项 (Python 3.7+)
    print(f"popitem(): {item}, 字典: {d}")
    
    # setdefault
    print("\nsetdefault:")
    d = {"name": "Alice"}
    age = d.setdefault("age", 25)   # 如果键不存在，设置默认值
    print(f"setdefault('age', 25): {age}, 字典: {d}")
    
    name = d.setdefault("name", "Bob")  # 键存在，返回现有值
    print(f"setdefault('name', 'Bob'): {name}, 字典: {d}")
    
    # 字典推导式
    print("\n字典推导式:")
    squares = {x: x**2 for x in range(6)}
    print(f"平方数字典: {squares}")
    
    # 反转字典
    original = {"a": 1, "b": 2, "c": 3}
    reversed_dict = {v: k for k, v in original.items()}
    print(f"原字典: {original}")
    print(f"反转: {reversed_dict}")


def dict_advanced():
    """字典高级操作"""
    print("\n=== 字典高级操作 ===")
    
    # defaultdict - 自动创建默认值
    print("defaultdict:")
    from collections import defaultdict
    
    dd = defaultdict(int)            # 默认值为 0
    dd["a"] += 1
    dd["b"] += 2
    print(f"defaultdict(int): {dict(dd)}")
    
    dd_list = defaultdict(list)      # 默认值为空列表
    dd_list["fruits"].append("apple")
    dd_list["fruits"].append("banana")
    dd_list["vegetables"].append("carrot")
    print(f"defaultdict(list): {dict(dd_list)}")
    
    # Counter - 计数器
    print("\nCounter:")
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    counter = Counter(words)
    print(f"Counter: {counter}")
    print(f"most_common(2): {counter.most_common(2)}")
    
    # 字符统计
    text = "hello world"
    char_count = Counter(text)
    print(f"字符统计: {char_count}")
    
    # OrderedDict - 有序字典 (Python 3.7+ 普通dict也有序)
    print("\nOrderedDict:")
    od = OrderedDict()
    od["a"] = 1
    od["b"] = 2
    od["c"] = 3
    print(f"OrderedDict: {od}")
    
    # 嵌套字典
    print("\n嵌套字典:")
    students = {
        "Alice": {"age": 20, "grade": 85},
        "Bob": {"age": 21, "grade": 90},
        "Charlie": {"age": 19, "grade": 88}
    }
    
    print(f"Alice的成绩: {students['Alice']['grade']}")
    
    # 安全访问嵌套字典
    email = students.get("David", {}).get("email", "未找到")
    print(f"David的邮箱: {email}")
    
    # 合并字典 (Python 3.9+)
    print("\n合并字典:")
    d1 = {"a": 1, "b": 2}
    d2 = {"c": 3, "d": 4}
    merged = d1 | d2                 # Python 3.9+
    print(f"d1 | d2: {merged}")


def dict_use_cases():
    """字典的使用场景"""
    print("\n=== 字典使用场景 ===")
    
    # 1. 配置管理
    config = {
        "host": "localhost",
        "port": 8080,
        "debug": True,
        "database": {
            "host": "db.example.com",
            "port": 5432
        }
    }
    print(f"配置: {config['host']}:{config['port']}")
    
    # 2. 缓存 / 查找表
    fibonacci_cache = {0: 0, 1: 1}
    
    def fibonacci(n):
        if n not in fibonacci_cache:
            fibonacci_cache[n] = fibonacci(n-1) + fibonacci(n-2)
        return fibonacci_cache[n]
    
    print(f"\nFibonacci(10) = {fibonacci(10)}")
    print(f"缓存: {fibonacci_cache}")
    
    # 3. 分组数据
    students = [
        {"name": "Alice", "grade": "A"},
        {"name": "Bob", "grade": "B"},
        {"name": "Charlie", "grade": "A"},
        {"name": "David", "grade": "C"},
        {"name": "Eve", "grade": "B"},
    ]
    
    grade_groups = defaultdict(list)
    for student in students:
        grade_groups[student["grade"]].append(student["name"])
    
    print(f"\n按成绩分组:")
    for grade, names in sorted(grade_groups.items()):
        print(f"  {grade}: {names}")
    
    # 4. 词频统计
    text = "the quick brown fox jumps over the lazy dog the fox"
    word_count = Counter(text.split())
    print(f"\n词频统计:")
    for word, count in word_count.most_common():
        print(f"  {word}: {count}")


# ============================================
# 5. 集合类型比较与选择
# ============================================

def collection_comparison():
    """集合类型比较"""
    print("\n=== 集合类型比较 ===")
    
    print("""
    类型对比:
    
    tuple (元组):
    - 不可变
    - 有序
    - 可重复
    - 可作为字典键
    - 用于不可变数据、函数返回值
    
    list (列表):
    - 可变
    - 有序
    - 可重复
    - 不能作为字典键
    - 用于需要修改的序列数据
    
    set (集合):
    - 可变
    - 无序
    - 不可重复
    - 不能作为字典键
    - 用于去重、集合运算、成员测试
    
    dict (字典):
    - 可变
    - 有序 (Python 3.7+)
    - 键不重复，值可重复
    - 用于键值对映射、配置、缓存
    
    性能对比:
    - 访问: list O(1), dict O(1), set O(1), tuple O(1)
    - 查找: list O(n), dict O(1), set O(1), tuple O(n)
    - 插入: list O(1)末尾/O(n)中间, dict O(1), set O(1)
    - 删除: list O(n), dict O(1), set O(1)
    """)


# ============================================
# 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 购物车系统
    print("1. 购物车系统:")
    cart = {}
    
    def add_to_cart(item, price, quantity=1):
        if item in cart:
            cart[item]["quantity"] += quantity
        else:
            cart[item] = {"price": price, "quantity": quantity}
    
    def get_total():
        return sum(info["price"] * info["quantity"] for info in cart.values())
    
    add_to_cart("Apple", 5.0, 3)
    add_to_cart("Banana", 3.0, 2)
    add_to_cart("Apple", 5.0, 2)
    
    print(f"购物车: {cart}")
    print(f"总价: ${get_total():.2f}")
    
    # 2. 学生成绩管理
    print("\n2. 学生成绩管理:")
    grades = defaultdict(list)
    
    grades["Alice"].extend([85, 90, 88])
    grades["Bob"].extend([78, 82, 80])
    grades["Charlie"].extend([92, 95, 94])
    
    for student, scores in grades.items():
        average = sum(scores) / len(scores)
        print(f"{student}: 平均分 = {average:.1f}")
    
    # 3. 文本分析
    print("\n3. 文本分析:")
    text = """
    Python is a high-level programming language.
    Python is easy to learn and powerful.
    Many developers love Python.
    """
    
    words = text.lower().split()
    word_count = Counter(word.strip(".,") for word in words)
    
    print("出现最多的5个词:")
    for word, count in word_count.most_common(5):
        print(f"  {word}: {count}")
    
    # 4. 数据去重和统计
    print("\n4. 数据去重:")
    data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    unique_data = list(set(data))
    print(f"原数据: {data}")
    print(f"去重后: {unique_data}")
    print(f"统计: {Counter(data)}")


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 集合类型详解：tuple, list, set, dict")
    print("=" * 60)
    
    tuple_basics()
    tuple_methods()
    tuple_use_cases()
    
    list_basics()
    list_methods()
    list_advanced()
    
    set_basics()
    set_methods()
    set_use_cases()
    
    dict_basics()
    dict_methods()
    dict_advanced()
    dict_use_cases()
    
    collection_comparison()
    practical_examples()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

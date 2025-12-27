"""
Python 基本数据类型详解：int, float, bool, str
包含详细的方法说明和实战示例
"""

import math
import sys
import re
import unicodedata


# ============================================
# 1. 整数类型 (int)
# ============================================

def integer_basics():
    """整数基础操作"""
    print("\n=== 整数 (int) 基础 ===")
    
    # 不同进制的整数表示
    decimal = 100           # 十进制
    binary = 0b1100100      # 二进制 (0b 前缀)
    octal = 0o144           # 八进制 (0o 前缀)
    hexadecimal = 0x64      # 十六进制 (0x 前缀)
    
    print(f"十进制: {decimal}")
    print(f"二进制 0b1100100: {binary}")
    print(f"八进制 0o144: {octal}")
    print(f"十六进制 0x64: {hexadecimal}")
    
    # Python 3 中整数没有大小限制
    big_number = 10 ** 100
    print(f"\n大数运算: 10^100 = {big_number}")
    
    # 整数运算
    a, b = 17, 5
    print(f"\n整数运算 (a=17, b=5):")
    print(f"加法: {a} + {b} = {a + b}")
    print(f"减法: {a} - {b} = {a - b}")
    print(f"乘法: {a} * {b} = {a * b}")
    print(f"除法: {a} / {b} = {a / b}")          # 返回 float
    print(f"整除: {a} // {b} = {a // b}")        # 向下取整
    print(f"取模: {a} % {b} = {a % b}")
    print(f"幂运算: {a} ** {b} = {a ** b}")
    
    # 负数的整除和取模
    print(f"\n负数运算:")
    print(f"-17 // 5 = {-17 // 5}")    # -4 (向下取整)
    print(f"-17 % 5 = {-17 % 5}")      # 3
    print(f"17 // -5 = {17 // -5}")    # -4
    print(f"17 % -5 = {17 % -5}")      # -3


def integer_methods():
    """整数的方法和函数"""
    print("\n=== 整数方法 ===")
    
    num = 42
    
    # 类型转换
    print("类型转换:")
    print(f"int('42') = {int('42')}")
    print(f"int('101', 2) = {int('101', 2)}")    # 二进制转换
    print(f"int('FF', 16) = {int('FF', 16)}")    # 十六进制转换
    print(f"int(3.14) = {int(3.14)}")            # 截断小数部分
    print(f"int(True) = {int(True)}")            # bool 转 int
    
    # 进制转换
    print(f"\n进制转换 (num={num}):")
    print(f"bin({num}) = {bin(num)}")            # 转二进制字符串
    print(f"oct({num}) = {oct(num)}")            # 转八进制字符串
    print(f"hex({num}) = {hex(num)}")            # 转十六进制字符串
    
    # 数学函数
    print(f"\n数学函数:")
    print(f"abs(-42) = {abs(-42)}")              # 绝对值
    print(f"pow(2, 10) = {pow(2, 10)}")          # 幂运算
    print(f"pow(2, 10, 1000) = {pow(2, 10, 1000)}")  # 模幂运算: (2^10) % 1000
    print(f"divmod(17, 5) = {divmod(17, 5)}")    # 返回商和余数
    
    # 位操作
    a, b = 60, 13  # 60 = 0b111100, 13 = 0b1101
    print(f"\n位操作 (a={a}, b={b}):")
    print(f"a & b = {a & b} (按位与)")
    print(f"a | b = {a | b} (按位或)")
    print(f"a ^ b = {a ^ b} (按位异或)")
    print(f"~a = {~a} (按位取反)")
    print(f"a << 2 = {a << 2} (左移)")
    print(f"a >> 2 = {a >> 2} (右移)")
    
    # 整数属性
    print(f"\n整数属性:")
    print(f"(42).bit_length() = {(42).bit_length()}")  # 二进制位数
    print(f"(42).to_bytes(2, 'big') = {(42).to_bytes(2, 'big')}")  # 转字节
    
    # 系统相关
    print(f"\nsys.maxsize = {sys.maxsize}")      # 最大整数(指针大小)


# ============================================
# 2. 浮点数类型 (float)
# ============================================

def float_basics():
    """浮点数基础操作"""
    print("\n=== 浮点数 (float) 基础 ===")
    
    # 浮点数表示
    f1 = 3.14
    f2 = 3.14159265359
    f3 = .5         # 0.5
    f4 = 5.         # 5.0
    
    # 科学计数法
    scientific1 = 1.5e3     # 1.5 * 10^3 = 1500.0
    scientific2 = 1.5e-3    # 1.5 * 10^-3 = 0.0015
    
    print(f"基本浮点数: {f1}, {f2}")
    print(f"科学计数法: 1.5e3 = {scientific1}, 1.5e-3 = {scientific2}")
    
    # 浮点数运算
    a, b = 10.5, 3.2
    print(f"\n浮点数运算 (a={a}, b={b}):")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    print(f"a // b = {a // b}")
    print(f"a % b = {a % b}")
    print(f"a ** b = {a ** b}")
    
    # 浮点数精度问题
    print("\n浮点数精度问题:")
    print(f"0.1 + 0.2 = {0.1 + 0.2}")            # 不是精确的 0.3
    print(f"0.1 + 0.2 == 0.3: {0.1 + 0.2 == 0.3}")  # False
    
    # 解决方案：使用 round() 或 decimal 模块
    result = 0.1 + 0.2
    print(f"round(0.1 + 0.2, 1) = {round(result, 1)}")


def float_methods():
    """浮点数的方法和函数"""
    print("\n=== 浮点数方法 ===")
    
    # 类型转换
    print("类型转换:")
    print(f"float(42) = {float(42)}")
    print(f"float('3.14') = {float('3.14')}")
    print(f"float('inf') = {float('inf')}")      # 无穷大
    print(f"float('-inf') = {float('-inf')}")    # 负无穷大
    print(f"float('nan') = {float('nan')}")      # 非数字
    
    # 特殊值
    inf = float('inf')
    neg_inf = float('-inf')
    nan = float('nan')
    
    print(f"\n特殊值检测:")
    print(f"math.isinf(inf) = {math.isinf(inf)}")
    print(f"math.isnan(nan) = {math.isnan(nan)}")
    print(f"math.isfinite(3.14) = {math.isfinite(3.14)}")
    
    # 浮点数方法
    x = 3.14159
    print(f"\n浮点数方法 (x={x}):")
    print(f"x.as_integer_ratio() = {x.as_integer_ratio()}")  # 转为分数
    print(f"x.is_integer() = {x.is_integer()}")              # 是否为整数
    print(f"(3.0).is_integer() = {(3.0).is_integer()}")
    
    # 舍入函数
    num = 3.7
    print(f"\n舍入函数 (num={num}):")
    print(f"round(3.7) = {round(num)}")              # 四舍六入五取偶
    print(f"round(3.5) = {round(3.5)}")              # 4 (取偶数)
    print(f"round(4.5) = {round(4.5)}")              # 4 (取偶数)
    print(f"round(3.14159, 2) = {round(3.14159, 2)}")  # 保留2位小数
    print(f"math.floor(3.7) = {math.floor(num)}")    # 向下取整
    print(f"math.ceil(3.2) = {math.ceil(3.2)}")      # 向上取整
    print(f"math.trunc(3.7) = {math.trunc(num)}")    # 截断小数
    
    # 数学函数
    print(f"\n常用数学函数:")
    print(f"abs(-3.14) = {abs(-3.14)}")
    print(f"pow(2.0, 3.0) = {pow(2.0, 3.0)}")
    print(f"math.sqrt(16) = {math.sqrt(16)}")        # 平方根
    print(f"math.exp(1) = {math.exp(1)}")            # e^1
    print(f"math.log(10) = {math.log(10)}")          # 自然对数
    print(f"math.log10(100) = {math.log10(100)}")    # 以10为底的对数
    
    # 三角函数
    print(f"\n三角函数:")
    print(f"math.sin(math.pi/2) = {math.sin(math.pi/2)}")
    print(f"math.cos(0) = {math.cos(0)}")
    print(f"math.tan(math.pi/4) = {math.tan(math.pi/4)}")
    
    # 常量
    print(f"\n数学常量:")
    print(f"math.pi = {math.pi}")
    print(f"math.e = {math.e}")
    print(f"math.tau = {math.tau}")                  # 2π
    print(f"math.inf = {math.inf}")
    print(f"math.nan = {math.nan}")


def decimal_precision():
    """使用 decimal 模块进行精确计算"""
    print("\n=== 精确小数计算 (decimal) ===")
    
    from decimal import Decimal, getcontext
    
    # 设置精度
    getcontext().prec = 50
    
    # Decimal 类型
    d1 = Decimal('0.1')
    d2 = Decimal('0.2')
    
    print(f"使用 float: 0.1 + 0.2 = {0.1 + 0.2}")
    print(f"使用 Decimal: 0.1 + 0.2 = {d1 + d2}")
    
    # 金融计算示例
    price = Decimal('19.99')
    quantity = Decimal('3')
    tax_rate = Decimal('0.08')
    
    subtotal = price * quantity
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    print(f"\n金融计算示例:")
    print(f"单价: ${price}")
    print(f"数量: {quantity}")
    print(f"小计: ${subtotal}")
    print(f"税率: {tax_rate}")
    print(f"税额: ${tax.quantize(Decimal('0.01'))}")
    print(f"总计: ${total.quantize(Decimal('0.01'))}")


# ============================================
# 3. 布尔类型 (bool)
# ============================================

def boolean_basics():
    """布尔类型基础"""
    print("\n=== 布尔类型 (bool) 基础 ===")
    
    # 布尔值
    is_python_fun = True
    is_difficult = False
    
    print(f"type(True) = {type(True)}")
    print(f"True 是 int 的子类: {isinstance(True, int)}")
    print(f"True == 1: {True == 1}")
    print(f"False == 0: {False == 0}")
    
    # 布尔运算
    print("\n布尔运算:")
    print(f"True and True = {True and True}")
    print(f"True and False = {True and False}")
    print(f"True or False = {True or False}")
    print(f"False or False = {False or False}")
    print(f"not True = {not True}")
    print(f"not False = {not False}")
    
    # 短路求值
    print("\n短路求值:")
    print(f"True or (1/0): ", end="")
    print(True or (1/0))  # 不会执行 1/0，因为 True or 任何值都是 True
    
    print(f"False and (1/0): ", end="")
    print(False and print("不会执行"))  # 不会执行 print
    
    # 比较运算返回布尔值
    print("\n比较运算:")
    print(f"10 > 5 = {10 > 5}")
    print(f"10 == 10 = {10 == 10}")
    print(f"'abc' < 'xyz' = {'abc' < 'xyz'}")


def truthiness():
    """真值测试"""
    print("\n=== 真值测试 ===")
    
    # 假值 (Falsy values)
    print("以下值在布尔上下文中为 False:")
    falsy_values = [
        None,
        False,
        0,
        0.0,
        0j,
        '',
        [],
        {},
        (),
        set(),
        frozenset(),
    ]
    
    for value in falsy_values:
        print(f"bool({repr(value):20s}) = {bool(value)}")
    
    # 真值 (Truthy values)
    print("\n其他所有值都为 True:")
    truthy_values = [
        True,
        1,
        3.14,
        'hello',
        [1, 2],
        {'a': 1},
        (1,),
    ]
    
    for value in truthy_values:
        print(f"bool({repr(value):20s}) = {bool(value)}")
    
    # 实际应用
    print("\n实际应用:")
    my_list = [1, 2, 3]
    if my_list:
        print("列表非空")
    
    empty_string = ""
    if not empty_string:
        print("字符串为空")
    
    value = None
    result = value or "默认值"
    print(f"value or '默认值' = {result}")


def boolean_operators_advanced():
    """布尔运算符高级用法"""
    print("\n=== 布尔运算符高级用法 ===")
    
    # and 和 or 返回操作数，而不仅仅是 True/False
    print("and 和 or 返回操作数:")
    print(f"'hello' and 'world' = {('hello' and 'world')}")  # 'world'
    print(f"'' and 'world' = {('' and 'world')}")            # ''
    print(f"'hello' or 'world' = {('hello' or 'world')}")    # 'hello'
    print(f"'' or 'world' = {('' or 'world')}")              # 'world'
    
    # 链式比较
    print("\n链式比较:")
    x = 5
    print(f"1 < {x} < 10 = {1 < x < 10}")
    print(f"1 < {x} < 3 = {1 < x < 3}")
    print(f"1 == 1 == 1 = {1 == 1 == 1}")
    
    # 成员测试
    print("\n成员测试:")
    print(f"'a' in 'abc' = {'a' in 'abc'}")
    print(f"1 in [1, 2, 3] = {1 in [1, 2, 3]}")
    print(f"'x' not in 'abc' = {'x' not in 'abc'}")
    
    # 身份测试
    print("\n身份测试:")
    a = [1, 2, 3]
    b = a
    c = [1, 2, 3]
    print(f"b is a = {b is a}")
    print(f"c is a = {c is a}")
    print(f"c == a = {c == a}")
    print(f"None is None = {None is None}")


# ============================================
# 4. 字符串类型 (str)
# ============================================

def string_basics():
    """字符串基础"""
    print("\n=== 字符串 (str) 基础 ===")
    
    # 字符串创建方式
    print("字符串创建:")
    s1 = 'single quotes'           # 单引号
    s2 = "double quotes"           # 双引号
    s3 = '''triple single
    quotes'''                      # 三单引号（可跨行）
    s4 = """triple double
    quotes"""                      # 三双引号（可跨行）
    
    print(f"单引号: {s1}")
    print(f"双引号: {s2}")
    print(f"三引号: {repr(s3)}")
    
    # 转义字符
    print("\n转义字符:")
    escape_examples = [
        (r'\n', "换行", "Hello\nWorld"),
        (r'\t', "制表符", "Hello\tWorld"),
        (r'\\', "反斜杠", "C:\\Users"),
        (r'\'', "单引号", "It\'s"),
        (r'\"', "双引号", "Say \"Hi\""),
        (r'\r', "回车", "Line\rEnd"),
        (r'\0', "空字符", "Null\0Char"),
    ]
    for code, desc, example in escape_examples:
        print(f"  {code:6s} ({desc:6s}): {repr(example)}")
    
    # 原始字符串 (Raw String)
    print("\n原始字符串 (raw string):")
    normal = "C:\\Users\\name\\file.txt"
    raw = r"C:\Users\name\file.txt"
    print(f"普通字符串: {normal}")
    print(f"原始字符串: {raw}")
    print("  原始字符串中反斜杠不转义，常用于正则表达式和路径")
    
    # 字符串不可变性
    print("\n字符串不可变性:")
    s = "hello"
    print(f"s = '{s}', id(s) = {id(s)}")
    s = s + " world"  # 创建新字符串
    print(f"s = '{s}', id(s) = {id(s)} (新对象)")
    # s[0] = 'H'  # 错误！字符串不可变


def string_indexing_slicing():
    """字符串索引和切片"""
    print("\n=== 字符串索引和切片 ===")
    
    s = "Python"
    print(f"字符串: '{s}' (长度: {len(s)})")
    
    # 索引 (Index)
    print("\n索引 (正向从0开始, 反向从-1开始):")
    print("  字符:  P   y   t   h   o   n")
    print("  正向:  0   1   2   3   4   5")
    print("  反向: -6  -5  -4  -3  -2  -1")
    print(f"  s[0] = '{s[0]}'")
    print(f"  s[2] = '{s[2]}'")
    print(f"  s[-1] = '{s[-1]}'")
    print(f"  s[-3] = '{s[-3]}'")
    
    # 切片 (Slice) - [start:stop:step]
    print("\n切片 [start:stop:step]:")
    print(f"  s[0:3] = '{s[0:3]}'     # 索引 0,1,2")
    print(f"  s[:3] = '{s[:3]}'       # 从开始到索引2")
    print(f"  s[3:] = '{s[3:]}'       # 从索引3到结束")
    print(f"  s[1:5] = '{s[1:5]}'     # 索引 1,2,3,4")
    print(f"  s[-3:] = '{s[-3:]}'     # 最后3个字符")
    print(f"  s[:-2] = '{s[:-2]}'     # 除了最后2个")
    print(f"  s[::2] = '{s[::2]}'     # 每隔一个字符")
    print(f"  s[::-1] = '{s[::-1]}'   # 反转字符串")
    print(f"  s[1:5:2] = '{s[1:5:2]}' # 索引1到4，步长2")
    
    # 切片不会越界
    print("\n切片不会越界:")
    print(f"  s[0:100] = '{s[0:100]}'")
    print(f"  s[100:] = '{s[100:]}'")


def string_operators():
    """字符串运算符"""
    print("\n=== 字符串运算符 ===")
    
    s1 = "Hello"
    s2 = "World"
    
    # 连接 (+)
    print("连接 (+):")
    print(f"  '{s1}' + ' ' + '{s2}' = '{s1 + ' ' + s2}'")
    
    # 重复 (*)
    print("\n重复 (*):")
    print(f"  '{s1}' * 3 = '{s1 * 3}'")
    print(f"  '-' * 20 = '{'-' * 20}'")
    
    # 成员检测 (in, not in)
    print("\n成员检测 (in, not in):")
    text = "Hello World"
    print(f"  text = '{text}'")
    print(f"  'World' in text = {'World' in text}")
    print(f"  'world' in text = {'world' in text}")  # 区分大小写
    print(f"  'xyz' not in text = {'xyz' not in text}")
    
    # 比较运算符 (按字典序)
    print("\n比较运算符 (按Unicode码点):")
    print(f"  'abc' < 'abd' = {'abc' < 'abd'}")
    print(f"  'abc' < 'ABC' = {'abc' < 'ABC'}")  # 小写 > 大写
    print(f"  'abc' == 'abc' = {'abc' == 'abc'}")
    print(f"  ord('a') = {ord('a')}, ord('A') = {ord('A')}")


def string_methods_search():
    """字符串搜索方法"""
    print("\n=== 字符串搜索方法 ===")
    
    s = "Hello World, Hello Python"
    print(f"s = '{s}'")
    
    # find / rfind - 查找子串位置，未找到返回-1
    print("\nfind / rfind (未找到返回-1):")
    print(f"  s.find('Hello') = {s.find('Hello')}")
    print(f"  s.rfind('Hello') = {s.rfind('Hello')}")  # 从右边找
    print(f"  s.find('hello') = {s.find('hello')}")    # 区分大小写
    print(f"  s.find('o', 5) = {s.find('o', 5)}")      # 从索引5开始找
    print(f"  s.find('o', 5, 10) = {s.find('o', 5, 10)}")  # 在5-10范围找
    
    # index / rindex - 类似find，但未找到抛出异常
    print("\nindex / rindex (未找到抛出 ValueError):")
    print(f"  s.index('World') = {s.index('World')}")
    
    # count - 统计出现次数
    print("\ncount (统计出现次数):")
    print(f"  s.count('o') = {s.count('o')}")
    print(f"  s.count('Hello') = {s.count('Hello')}")
    print(f"  s.count('l', 0, 10) = {s.count('l', 0, 10)}")  # 指定范围
    
    # startswith / endswith
    print("\nstartswith / endswith:")
    print(f"  s.startswith('Hello') = {s.startswith('Hello')}")
    print(f"  s.endswith('Python') = {s.endswith('Python')}")
    print(f"  s.startswith(('Hi', 'Hello')) = {s.startswith(('Hi', 'Hello'))}")  # 元组


def string_methods_modify():
    """字符串修改方法 (返回新字符串)"""
    print("\n=== 字符串修改方法 ===")
    
    # 大小写转换
    s = "Hello World"
    print(f"原始: '{s}'")
    print("\n大小写转换:")
    print(f"  s.upper() = '{s.upper()}'")
    print(f"  s.lower() = '{s.lower()}'")
    print(f"  s.capitalize() = '{s.capitalize()}'")  # 首字母大写
    print(f"  s.title() = '{s.title()}'")            # 每个单词首字母大写
    print(f"  s.swapcase() = '{s.swapcase()}'")      # 大小写互换
    print(f"  'hello'.casefold() = {'HELLO'.casefold()}'")  # 更强力的小写转换
    
    # 去除空白
    s = "  Hello World  \n"
    print(f"\n去除空白 (s = {repr(s)}):")
    print(f"  s.strip() = {repr(s.strip())}")        # 两端
    print(f"  s.lstrip() = {repr(s.lstrip())}")      # 左边
    print(f"  s.rstrip() = {repr(s.rstrip())}")      # 右边
    print(f"  'xxxHelloxxx'.strip('x') = '{'xxxHelloxxx'.strip('x')}'")  # 指定字符
    
    # 替换
    s = "Hello World"
    print(f"\n替换 (s = '{s}'):")
    print(f"  s.replace('World', 'Python') = '{s.replace('World', 'Python')}'")
    print(f"  s.replace('l', 'L') = '{s.replace('l', 'L')}'")
    print(f"  s.replace('l', 'L', 1) = '{s.replace('l', 'L', 1)}'")  # 只替换1次
    
    # 填充与对齐
    s = "Python"
    print(f"\n填充与对齐 (s = '{s}'):")
    print(f"  s.center(20) = '{s.center(20)}'")
    print(f"  s.center(20, '*') = '{s.center(20, '*')}'")
    print(f"  s.ljust(20, '-') = '{s.ljust(20, '-')}'")
    print(f"  s.rjust(20, '-') = '{s.rjust(20, '-')}'")
    print(f"  '42'.zfill(5) = '{'42'.zfill(5)}'")       # 补零
    print(f"  '-42'.zfill(5) = '{'-42'.zfill(5)}'")
    
    # expandtabs
    s = "a\tb\tc"
    print(f"\nexpandtabs (s = {repr(s)}):")
    print(f"  s.expandtabs(4) = '{s.expandtabs(4)}'")


def string_methods_split_join():
    """字符串分割与连接方法"""
    print("\n=== 字符串分割与连接 ===")
    
    # split - 分割字符串
    s = "apple,banana,orange,grape"
    print(f"split (s = '{s}'):")
    print(f"  s.split(',') = {s.split(',')}")
    print(f"  s.split(',', 2) = {s.split(',', 2)}")  # 最多分割2次
    
    s2 = "  hello   world  python  "
    print(f"\nsplit (s2 = '{s2}'):")
    print(f"  s2.split() = {s2.split()}")  # 默认按空白分割，去除空串
    print(f"  s2.split(' ') = {s2.split(' ')}")  # 按单个空格，保留空串
    
    # rsplit - 从右边开始分割
    print(f"\nrsplit:")
    print(f"  s.rsplit(',', 2) = {s.rsplit(',', 2)}")
    
    # splitlines - 按行分割
    multi = "line1\nline2\rline3\r\nline4"
    print(f"\nsplitlines (multi = {repr(multi)}):")
    print(f"  multi.splitlines() = {multi.splitlines()}")
    print(f"  multi.splitlines(True) = {multi.splitlines(True)}")  # 保留换行符
    
    # partition / rpartition - 三元组分割
    s = "hello=world=python"
    print(f"\npartition (s = '{s}'):")
    print(f"  s.partition('=') = {s.partition('=')}")
    print(f"  s.rpartition('=') = {s.rpartition('=')}")
    print(f"  s.partition('x') = {s.partition('x')}")  # 未找到
    
    # join - 连接字符串列表
    print("\njoin:")
    words = ['apple', 'banana', 'orange']
    print(f"  words = {words}")
    print(f"  ','.join(words) = '{','.join(words)}'")
    print(f"  ' -> '.join(words) = '{' -> '.join(words)}'")
    print(f"  ''.join(words) = '{''.join(words)}'")
    
    # 连接数字需要先转字符串
    nums = [1, 2, 3, 4, 5]
    print(f"  '-'.join(map(str, nums)) = '{'-'.join(map(str, nums))}'")


def string_methods_check():
    """字符串检查方法"""
    print("\n=== 字符串检查方法 ===")
    
    print("isalpha() - 是否全是字母:")
    print(f"  'Hello'.isalpha() = {'Hello'.isalpha()}")
    print(f"  'Hello123'.isalpha() = {'Hello123'.isalpha()}")
    print(f"  '你好'.isalpha() = {'你好'.isalpha()}")  # 中文也是字母
    
    print("\nisdigit() - 是否全是数字:")
    print(f"  '12345'.isdigit() = {'12345'.isdigit()}")
    print(f"  '12.34'.isdigit() = {'12.34'.isdigit()}")
    print(f"  '①②③'.isdigit() = {'①②③'.isdigit()}")  # 特殊数字字符
    
    print("\nisnumeric() - 是否是数值字符:")
    print(f"  '12345'.isnumeric() = {'12345'.isnumeric()}")
    print(f"  '½'.isnumeric() = {'½'.isnumeric()}")     # 分数
    print(f"  '四'.isnumeric() = {'四'.isnumeric()}")   # 中文数字
    
    print("\nisalnum() - 是否是字母或数字:")
    print(f"  'Hello123'.isalnum() = {'Hello123'.isalnum()}")
    print(f"  'Hello 123'.isalnum() = {'Hello 123'.isalnum()}")  # 含空格
    
    print("\nisspace() - 是否全是空白字符:")
    print(f"  '   '.isspace() = {'   '.isspace()}")
    print(f"  '\\t\\n'.isspace() = {chr(9)+chr(10)!r}.isspace() = True")
    
    print("\nisupper() / islower():")
    print(f"  'HELLO'.isupper() = {'HELLO'.isupper()}")
    print(f"  'hello'.islower() = {'hello'.islower()}")
    print(f"  'Hello'.isupper() = {'Hello'.isupper()}")
    
    print("\nistitle() - 是否是标题格式:")
    print(f"  'Hello World'.istitle() = {'Hello World'.istitle()}")
    print(f"  'Hello world'.istitle() = {'Hello world'.istitle()}")
    
    print("\nisidentifier() - 是否是有效标识符:")
    print(f"  'my_var'.isidentifier() = {'my_var'.isidentifier()}")
    print(f"  '123abc'.isidentifier() = {'123abc'.isidentifier()}")
    print(f"  'class'.isidentifier() = {'class'.isidentifier()}")  # 关键字也是有效标识符
    
    print("\nisprintable() - 是否可打印:")
    print(f"  'Hello'.isprintable() = {'Hello'.isprintable()}")
    print(f"  'Hello\\n'.isprintable() = {'Hello\\n'.isprintable()}")
    
    print("\nisascii() - 是否全是ASCII字符:")
    print(f"  'Hello'.isascii() = {'Hello'.isascii()}")
    print(f"  '你好'.isascii() = {'你好'.isascii()}")


def string_formatting():
    """字符串格式化"""
    print("\n=== 字符串格式化 ===")
    
    name = "Alice"
    age = 25
    score = 95.5678
    
    # 方法1: % 格式化 (旧式)
    print("1. % 格式化 (旧式):")
    print(f"  '我是 %s, %d 岁' % (name, age) = '{'我是 %s, %d 岁' % (name, age)}'")
    print(f"  '分数: %.2f' % score = '{'分数: %.2f' % score}'")
    print("  常用格式符: %s(字符串), %d(整数), %f(浮点), %x(十六进制)")
    
    # 方法2: str.format()
    print("\n2. str.format() 方法:")
    print(f"  '我是 {{}}, {{}} 岁'.format(name, age) = '{'我是 {}, {} 岁'.format(name, age)}'")
    print(f"  '{{name}} - {{age}}'.format(name=name, age=age) = '{'{name} - {age}'.format(name=name, age=age)}'")
    print(f"  '{{0}} {{1}} {{0}}'.format('A', 'B') = '{'{0} {1} {0}'.format('A', 'B')}'")
    
    # 方法3: f-string (推荐，Python 3.6+)
    print("\n3. f-string (推荐, Python 3.6+):")
    print(f"  f'我是 {{name}}, {{age}} 岁' = '我是 {name}, {age} 岁'")
    print(f"  f'明年 {{age + 1}} 岁' = '明年 {age + 1} 岁'")
    print(f"  f'{{name.upper()}}' = '{name.upper()}'")
    
    # 格式规范
    print("\n格式规范 [[fill]align][sign][#][0][width][,][.precision][type]:")
    num = 42
    pi = 3.14159265
    
    # 宽度和对齐
    print("\n  宽度和对齐:")
    print(f"    f'{{num:10}}' = '{num:10}'      # 右对齐(默认)")
    print(f"    f'{{num:<10}}' = '{num:<10}'     # 左对齐")
    print(f"    f'{{num:^10}}' = '{num:^10}'     # 居中")
    print(f"    f'{{num:*^10}}' = '{num:*^10}'   # 填充字符")
    
    # 数字格式
    print("\n  数字格式:")
    print(f"    f'{{pi:.2f}}' = '{pi:.2f}'        # 2位小数")
    print(f"    f'{{pi:.4f}}' = '{pi:.4f}'      # 4位小数")
    print(f"    f'{{num:05d}}' = '{num:05d}'       # 补零")
    print(f"    f'{{num:+d}}' = '{num:+d}'         # 显示正号")
    big = 1234567890
    print(f"    f'{{big:,}}' = '{big:,}'      # 千位分隔符")
    print(f"    f'{{big:_}}' = '{big:_}'      # 下划线分隔符")
    
    # 进制转换
    print("\n  进制转换:")
    print(f"    f'{{num:b}}' = '{num:b}'       # 二进制")
    print(f"    f'{{num:o}}' = '{num:o}'        # 八进制")
    print(f"    f'{{num:x}}' = '{num:x}'        # 十六进制小写")
    print(f"    f'{{num:X}}' = '{num:X}'        # 十六进制大写")
    print(f"    f'{{num:#x}}' = '{num:#x}'      # 带前缀")
    
    # 百分比和科学计数法
    print("\n  百分比和科学计数法:")
    ratio = 0.25
    print(f"    f'{{ratio:.1%}}' = '{ratio:.1%}'    # 百分比")
    large = 12345678.9
    print(f"    f'{{large:.2e}}' = '{large:.2e}'  # 科学计数法")
    
    # 调试格式 (Python 3.8+)
    print("\n  调试格式 (Python 3.8+):")
    x = 10
    print(f"    f'{{x=}}' = '{x=}'")
    print(f"    f'{{x + 5=}}' = '{x + 5=}'")


def string_encoding():
    """字符串编码"""
    print("\n=== 字符串编码 ===")
    
    # Python 3 字符串是 Unicode
    print("Python 3 中 str 是 Unicode 字符串:")
    s = "Hello 你好 🐍"
    print(f"  s = '{s}'")
    print(f"  len(s) = {len(s)}")  # 字符数
    
    # 编码: str -> bytes
    print("\n编码 (str -> bytes):")
    s = "你好 Python"
    print(f"  s = '{s}'")
    print(f"  s.encode('utf-8') = {s.encode('utf-8')}")
    print(f"  s.encode('gbk') = {s.encode('gbk')}")
    print(f"  s.encode('ascii', errors='ignore') = {s.encode('ascii', errors='ignore')}")
    print(f"  s.encode('ascii', errors='replace') = {s.encode('ascii', errors='replace')}")
    
    # 解码: bytes -> str
    print("\n解码 (bytes -> str):")
    b = b'\xe4\xbd\xa0\xe5\xa5\xbd'
    print(f"  b = {b}")
    print(f"  b.decode('utf-8') = '{b.decode('utf-8')}'")
    
    # ord 和 chr
    print("\nord() 和 chr():")
    print(f"  ord('A') = {ord('A')}")
    print(f"  ord('中') = {ord('中')}")
    print(f"  chr(65) = '{chr(65)}'")
    print(f"  chr(20013) = '{chr(20013)}'")
    
    # Unicode 转义
    print("\nUnicode 表示:")
    print(f"  '\\u4e2d\\u6587' = '{'\\u4e2d\\u6587'}'")
    print(f"  '\\N{{SNAKE}}' = '{chr(0x1F40D)}'")
    
    # 字符信息
    print("\nunicodedata 模块:")
    import unicodedata
    char = '中'
    print(f"  char = '{char}'")
    print(f"  unicodedata.name(char) = '{unicodedata.name(char)}'")
    print(f"  unicodedata.category(char) = '{unicodedata.category(char)}'")


def string_regex_basics():
    """正则表达式基础"""
    print("\n=== 正则表达式基础 ===")
    
    import re
    
    text = "Hello, my email is test@example.com and phone is 123-456-7890"
    
    # 基本匹配
    print("基本匹配:")
    pattern = r"email"
    match = re.search(pattern, text)
    print(f"  re.search(r'email', text) = {match.group() if match else None}")
    
    # 常用模式
    print("\n常用正则模式:")
    patterns = [
        (r'\d+', "数字序列"),
        (r'\w+', "单词"),
        (r'[a-z]+', "小写字母"),
        (r'\S+@\S+', "简单邮箱"),
    ]
    for pattern, desc in patterns:
        matches = re.findall(pattern, text)
        print(f"  {pattern:15s} ({desc}): {matches}")
    
    # re 模块常用函数
    print("\nre 模块常用函数:")
    s = "apple banana apple cherry"
    
    print(f"  re.search(r'banana', s) = {re.search(r'banana', s)}")
    print(f"  re.match(r'apple', s) = {re.match(r'apple', s)}")  # 从开头匹配
    print(f"  re.findall(r'apple', s) = {re.findall(r'apple', s)}")
    print(f"  re.sub(r'apple', 'APPLE', s) = '{re.sub(r'apple', 'APPLE', s)}'")
    print(f"  re.split(r'\\s+', s) = {re.split(r'\s+', s)}")
    
    # 常用元字符
    print("\n常用正则元字符:")
    print("""
    .     匹配任意字符(除换行)    \\d    匹配数字 [0-9]
    ^     匹配开头               \\D    匹配非数字
    $     匹配结尾               \\w    匹配字母数字下划线
    *     0次或多次              \\W    匹配非字母数字下划线
    +     1次或多次              \\s    匹配空白字符
    ?     0次或1次               \\S    匹配非空白字符
    {n}   恰好n次                \\b    匹配单词边界
    {n,m} n到m次                 [...]  字符集
    """)


def string_practical():
    """字符串实战示例"""
    print("\n=== 字符串实战示例 ===")
    
    # 1. 回文检测
    print("1. 回文检测:")
    def is_palindrome(s):
        s = s.lower().replace(' ', '')
        return s == s[::-1]
    
    words = ["radar", "hello", "A man a plan a canal Panama"]
    for word in words:
        print(f"   '{word}' -> {is_palindrome(word)}")
    
    # 2. 统计单词频率
    print("\n2. 单词频率统计:")
    text = "apple banana apple cherry banana apple"
    words = text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    print(f"   '{text}'")
    print(f"   频率: {freq}")
    
    # 3. 字符串模板
    print("\n3. 字符串模板:")
    from string import Template
    template = Template("Hello, $name! You have $count messages.")
    result = template.substitute(name="Alice", count=5)
    print(f"   模板: 'Hello, $name! You have $count messages.'")
    print(f"   结果: '{result}'")
    
    # 4. 生成随机字符串
    print("\n4. 生成随机字符串:")
    import string
    import random
    chars = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(chars) for _ in range(10))
    print(f"   随机字符串: '{random_str}'")
    print(f"   string.ascii_letters = '{string.ascii_letters}'")
    print(f"   string.digits = '{string.digits}'")
    print(f"   string.punctuation = '{string.punctuation}'")
    
    # 5. 文本对齐表格
    print("\n5. 文本对齐表格:")
    data = [
        ("Name", "Age", "City"),
        ("Alice", "25", "New York"),
        ("Bob", "30", "San Francisco"),
        ("Charlie", "35", "Los Angeles"),
    ]
    for row in data:
        print(f"   {row[0]:<10} {row[1]:>5} {row[2]:<15}")
    
    # 6. URL 解析
    print("\n6. 简单的字符串处理:")
    url = "https://www.example.com/path/to/page?name=alice&age=25"
    protocol = url.split("://")[0]
    domain = url.split("://")[1].split("/")[0]
    path = "/" + "/".join(url.split("://")[1].split("?")[0].split("/")[1:])
    query = url.split("?")[1] if "?" in url else ""
    print(f"   URL: {url}")
    print(f"   协议: {protocol}")
    print(f"   域名: {domain}")
    print(f"   路径: {path}")
    print(f"   查询: {query}")


def string_methods_summary():
    """字符串方法总结"""
    print("\n=== 字符串方法速查表 ===")
    
    print("""
    搜索方法:
    ─────────────────────────────────────
    find(sub)       查找子串位置，未找到返回-1
    rfind(sub)      从右边查找
    index(sub)      查找子串位置，未找到抛异常
    rindex(sub)     从右边查找
    count(sub)      统计出现次数
    startswith(s)   是否以s开头
    endswith(s)     是否以s结尾
    
    修改方法 (返回新字符串):
    ─────────────────────────────────────
    upper()         转大写
    lower()         转小写
    capitalize()    首字母大写
    title()         每个单词首字母大写
    swapcase()      大小写互换
    strip()         去除两端空白
    lstrip()        去除左边空白
    rstrip()        去除右边空白
    replace(a, b)   替换
    center(w)       居中
    ljust(w)        左对齐
    rjust(w)        右对齐
    zfill(w)        补零
    
    分割与连接:
    ─────────────────────────────────────
    split(sep)      分割
    rsplit(sep)     从右分割
    splitlines()    按行分割
    partition(sep)  三元组分割
    join(list)      连接
    
    检查方法 (返回布尔值):
    ─────────────────────────────────────
    isalpha()       是否全是字母
    isdigit()       是否全是数字
    isalnum()       是否是字母或数字
    isspace()       是否全是空白
    isupper()       是否全大写
    islower()       是否全小写
    istitle()       是否标题格式
    isidentifier()  是否有效标识符
    isprintable()   是否可打印
    isascii()       是否全是ASCII
    
    编码方法:
    ─────────────────────────────────────
    encode(enc)     编码为bytes
    """)


# ============================================
# 5. 类型转换与检查
# ============================================

def type_conversion():
    """类型转换示例"""
    print("\n=== 类型转换 ===")
    
    # int, float, bool 之间转换
    print("基本类型转换:")
    print(f"int(3.14) = {int(3.14)}")
    print(f"int(True) = {int(True)}")
    print(f"int(False) = {int(False)}")
    
    print(f"float(42) = {float(42)}")
    print(f"float(True) = {float(True)}")
    
    print(f"bool(0) = {bool(0)}")
    print(f"bool(42) = {bool(42)}")
    print(f"bool(0.0) = {bool(0.0)}")
    print(f"bool(3.14) = {bool(3.14)}")
    
    # 字符串转换
    print("\n字符串转换:")
    print(f"str(42) = {str(42)}")
    print(f"str(3.14) = {str(3.14)}")
    print(f"str(True) = {str(True)}")
    
    print(f"int('42') = {int('42')}")
    print(f"float('3.14') = {float('3.14')}")
    
    # 类型检查
    print("\n类型检查:")
    x = 42
    print(f"type(x) = {type(x)}")
    print(f"type(x) == int = {type(x) == int}")
    print(f"isinstance(x, int) = {isinstance(x, int)}")
    print(f"isinstance(x, (int, float)) = {isinstance(x, (int, float))}")
    print(f"isinstance(True, bool) = {isinstance(True, bool)}")
    print(f"isinstance(True, int) = {isinstance(True, int)}")  # True!


# ============================================
# 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 温度转换
    def celsius_to_fahrenheit(celsius):
        """摄氏度转华氏度"""
        return celsius * 9/5 + 32
    
    def fahrenheit_to_celsius(fahrenheit):
        """华氏度转摄氏度"""
        return (fahrenheit - 32) * 5/9
    
    print("温度转换:")
    c = 25
    f = celsius_to_fahrenheit(c)
    print(f"{c}°C = {f:.1f}°F")
    print(f"{f:.1f}°F = {fahrenheit_to_celsius(f):.1f}°C")
    
    # 2. 判断闰年
    def is_leap_year(year):
        """判断是否为闰年"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    print("\n闰年判断:")
    years = [2000, 2020, 2021, 2024, 1900]
    for year in years:
        print(f"{year} 是闰年: {is_leap_year(year)}")
    
    # 3. 计算圆的面积和周长
    def circle_properties(radius):
        """计算圆的面积和周长"""
        area = math.pi * radius ** 2
        circumference = 2 * math.pi * radius
        return area, circumference
    
    print("\n圆的计算:")
    r = 5
    area, circ = circle_properties(r)
    print(f"半径 = {r}")
    print(f"面积 = {area:.2f}")
    print(f"周长 = {circ:.2f}")
    
    # 4. 复利计算
    def compound_interest(principal, rate, time, n=12):
        """
        计算复利
        principal: 本金
        rate: 年利率 (小数形式)
        time: 时间 (年)
        n: 每年复利次数
        """
        amount = principal * (1 + rate/n) ** (n * time)
        interest = amount - principal
        return amount, interest
    
    print("\n复利计算:")
    p, r, t = 10000, 0.05, 10
    amount, interest = compound_interest(p, r, t)
    print(f"本金: ${p:,.2f}")
    print(f"年利率: {r*100}%")
    print(f"时间: {t} 年")
    print(f"最终金额: ${amount:,.2f}")
    print(f"利息: ${interest:,.2f}")


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 基本数据类型详解：int, float, bool, str")
    print("=" * 60)
    
    integer_basics()
    integer_methods()
    
    float_basics()
    float_methods()
    decimal_precision()
    
    boolean_basics()
    truthiness()
    boolean_operators_advanced()
    
    string_basics()
    string_indexing_slicing()
    string_operators()
    string_methods_search()
    string_methods_modify()
    string_methods_split_join()
    string_methods_check()
    string_formatting()
    string_encoding()
    string_regex_basics()
    string_practical()
    string_methods_summary()
    
    type_conversion()
    practical_examples()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

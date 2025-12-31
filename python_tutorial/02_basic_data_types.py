"""
Python 基本数据类型详解 (with Type Hints)
=========================================

本文件涵盖：
- int (整数)
- float (浮点数)
- bool (布尔值)
- str (字符串)
- bytes (字节)
"""

from typing import Any, Literal
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import math
import struct

# ============================================================================
# 1. int 整数类型
# ============================================================================

class IntDemo:
    """整数类型详解"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        # Python 3 的 int 没有大小限制（只受内存限制）
        small: int = 42
        big: int = 10 ** 100  # 非常大的数
        negative: int = -999
        
        # 不同进制表示
        binary: int = 0b1010      # 二进制 = 10
        octal: int = 0o777        # 八进制 = 511
        hexadecimal: int = 0xFF   # 十六进制 = 255
        
        # 可读性：使用下划线分隔
        million: int = 1_000_000
        phone: int = 138_1234_5678
        
        print(f"Binary 0b1010 = {binary}")
        print(f"Octal 0o777 = {octal}")
        print(f"Hex 0xFF = {hexadecimal}")
        print(f"Million: {million}")
    
    @staticmethod
    def arithmetic_operations() -> None:
        """算术运算"""
        a: int = 17
        b: int = 5
        
        # 基本算术
        print(f"{a} + {b} = {a + b}")      # 加法: 22
        print(f"{a} - {b} = {a - b}")      # 减法: 12
        print(f"{a} * {b} = {a * b}")      # 乘法: 85
        print(f"{a} / {b} = {a / b}")      # 真除法: 3.4 (返回 float!)
        print(f"{a} // {b} = {a // b}")    # 整除: 3
        print(f"{a} % {b} = {a % b}")      # 取模: 2
        print(f"{a} ** {b} = {a ** b}")    # 幂运算: 1419857
        
        # divmod 同时获取商和余数
        quotient, remainder = divmod(a, b)
        print(f"divmod({a}, {b}) = ({quotient}, {remainder})")
        
        # 负数除法的行为（Python 向负无穷取整）
        print(f"-17 // 5 = {-17 // 5}")   # -4 (不是 -3)
        print(f"-17 % 5 = {-17 % 5}")     # 3 (保证 a = (a // b) * b + (a % b))
    
    @staticmethod
    def bit_operations() -> None:
        """位运算"""
        a: int = 0b1100  # 12
        b: int = 0b1010  # 10
        
        print(f"a = {bin(a)} ({a})")
        print(f"b = {bin(b)} ({b})")
        
        # 位运算
        print(f"a & b  (AND)  = {bin(a & b)} ({a & b})")    # 1000 = 8
        print(f"a | b  (OR)   = {bin(a | b)} ({a | b})")    # 1110 = 14
        print(f"a ^ b  (XOR)  = {bin(a ^ b)} ({a ^ b})")    # 0110 = 6
        print(f"~a     (NOT)  = {bin(~a)} ({~a})")          # -13 (补码)
        print(f"a << 2 (LEFT) = {bin(a << 2)} ({a << 2})")  # 110000 = 48
        print(f"a >> 2 (RIGHT)= {bin(a >> 2)} ({a >> 2})")  # 11 = 3
    
    @staticmethod
    def int_methods() -> dict[str, Any]:
        """int 对象方法"""
        num: int = 255
        
        return {
            # 转换为字节
            "to_bytes": num.to_bytes(2, byteorder='big'),  # b'\x00\xff'
            "from_bytes": int.from_bytes(b'\x00\xff', byteorder='big'),  # 255
            
            # 位数信息
            "bit_length": num.bit_length(),  # 8 (表示这个数需要的位数)
            "bit_count": num.bit_count(),    # 8 (Python 3.10+, popcount)
            
            # 数学函数
            "abs": abs(-42),
            "pow_with_mod": pow(2, 10, 1000),  # (2^10) % 1000 = 24
        }


# ============================================================================
# 2. float 浮点数类型
# ============================================================================

class FloatDemo:
    """浮点数类型详解"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        # 基本声明
        f1: float = 3.14
        f2: float = 2.0
        f3: float = .5       # 0.5
        f4: float = 1.       # 1.0
        
        # 科学计数法
        large: float = 1.5e10    # 1.5 × 10^10
        small: float = 1.5e-10   # 1.5 × 10^-10
        
        # 特殊值
        positive_inf: float = float('inf')
        negative_inf: float = float('-inf')
        not_a_number: float = float('nan')
        
        print(f"Infinity: {positive_inf}")
        print(f"Is infinite: {math.isinf(positive_inf)}")
        print(f"Is NaN: {math.isnan(not_a_number)}")
        print(f"Is finite: {math.isfinite(f1)}")
    
    @staticmethod
    def precision_issues() -> None:
        """精度问题演示"""
        # 经典精度问题
        result = 0.1 + 0.2
        print(f"0.1 + 0.2 = {result}")  # 0.30000000000000004
        print(f"0.1 + 0.2 == 0.3 ? {result == 0.3}")  # False!
        
        # 解决方案 1: 使用 math.isclose
        print(f"math.isclose(0.1 + 0.2, 0.3) ? {math.isclose(0.1 + 0.2, 0.3)}")  # True
        
        # 解决方案 2: 使用 Decimal（见后面）
        d1 = Decimal('0.1')
        d2 = Decimal('0.2')
        d3 = Decimal('0.3')
        print(f"Decimal: 0.1 + 0.2 == 0.3 ? {d1 + d2 == d3}")  # True
        
        # 解决方案 3: 使用 Fraction
        f1 = Fraction(1, 10)
        f2 = Fraction(2, 10)
        f3 = Fraction(3, 10)
        print(f"Fraction: 1/10 + 2/10 == 3/10 ? {f1 + f2 == f3}")  # True
    
    @staticmethod
    def float_methods() -> dict[str, Any]:
        """float 方法"""
        f: float = 3.14159
        
        return {
            # 转为整数比例
            "as_integer_ratio": f.as_integer_ratio(),  # (3537115888337719, 1125899906842624)
            
            # 判断是否为整数
            "is_integer": (3.0).is_integer(),  # True
            "is_integer_2": (3.14).is_integer(),  # False
            
            # 十六进制表示
            "hex": f.hex(),  # '0x1.921f9f01b866ep+1'
            "from_hex": float.fromhex('0x1.921f9f01b866ep+1'),
        }
    
    @staticmethod
    def math_functions() -> None:
        """数学函数"""
        x: float = 3.7
        
        print(f"x = {x}")
        print(f"math.floor({x}) = {math.floor(x)}")      # 3 (向下取整)
        print(f"math.ceil({x}) = {math.ceil(x)}")        # 4 (向上取整)
        print(f"math.trunc({x}) = {math.trunc(x)}")      # 3 (截断)
        print(f"round({x}) = {round(x)}")                # 4 (四舍五入)
        print(f"round({x}, 0) = {round(x, 0)}")          # 4.0
        
        # 银行家舍入法 (round half to even)
        print(f"round(0.5) = {round(0.5)}")   # 0
        print(f"round(1.5) = {round(1.5)}")   # 2
        print(f"round(2.5) = {round(2.5)}")   # 2
        
        # 三角函数
        print(f"math.sin(math.pi/2) = {math.sin(math.pi/2)}")  # 1.0
        print(f"math.cos(0) = {math.cos(0)}")                   # 1.0
        
        # 指数和对数
        print(f"math.exp(1) = {math.exp(1)}")                   # e ≈ 2.718
        print(f"math.log(math.e) = {math.log(math.e)}")        # 1.0
        print(f"math.log10(100) = {math.log10(100)}")          # 2.0
        print(f"math.log2(8) = {math.log2(8)}")                # 3.0
        
        # 平方根和幂
        print(f"math.sqrt(16) = {math.sqrt(16)}")              # 4.0
        print(f"math.pow(2, 10) = {math.pow(2, 10)}")          # 1024.0


# ============================================================================
# 3. Decimal 精确十进制
# ============================================================================

class DecimalDemo:
    """Decimal 精确计算"""
    
    @staticmethod
    def basic_usage() -> None:
        """基本使用"""
        # 从字符串创建（推荐）
        d1: Decimal = Decimal('0.1')
        d2: Decimal = Decimal('0.2')
        
        # 从浮点数创建（不推荐，会保留浮点误差）
        d_float: Decimal = Decimal(0.1)  # Decimal('0.1000000000000000055511151231257827021181583404541015625')
        
        print(f"Decimal('0.1') + Decimal('0.2') = {d1 + d2}")  # 0.3
        print(f"From float: {d_float}")
    
    @staticmethod
    def precision_control() -> None:
        """精度控制"""
        from decimal import getcontext, localcontext
        
        # 全局精度设置
        getcontext().prec = 50  # 设置精度为 50 位
        
        # 高精度计算
        result = Decimal('1') / Decimal('7')
        print(f"1/7 (50 digits) = {result}")
        
        # 使用局部上下文
        with localcontext() as ctx:
            ctx.prec = 10
            result = Decimal('1') / Decimal('7')
            print(f"1/7 (10 digits) = {result}")
    
    @staticmethod
    def rounding_modes() -> None:
        """舍入模式"""
        from decimal import ROUND_UP, ROUND_DOWN, ROUND_CEILING, ROUND_FLOOR
        
        d = Decimal('2.345')
        
        print(f"Original: {d}")
        print(f"ROUND_HALF_UP:   {d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")   # 2.35
        print(f"ROUND_UP:        {d.quantize(Decimal('0.01'), rounding=ROUND_UP)}")        # 2.35
        print(f"ROUND_DOWN:      {d.quantize(Decimal('0.01'), rounding=ROUND_DOWN)}")      # 2.34
        print(f"ROUND_CEILING:   {d.quantize(Decimal('0.01'), rounding=ROUND_CEILING)}")   # 2.35
        print(f"ROUND_FLOOR:     {d.quantize(Decimal('0.01'), rounding=ROUND_FLOOR)}")     # 2.34
    
    @staticmethod
    def financial_calculation() -> Decimal:
        """金融计算示例"""
        # 商品价格计算
        unit_price = Decimal('19.99')
        quantity = Decimal('3')
        tax_rate = Decimal('0.08')
        
        subtotal = unit_price * quantity
        tax = (subtotal * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total = subtotal + tax
        
        print(f"Subtotal: ${subtotal}")
        print(f"Tax (8%): ${tax}")
        print(f"Total: ${total}")
        
        return total


# ============================================================================
# 4. bool 布尔类型
# ============================================================================

class BoolDemo:
    """布尔类型详解"""
    
    @staticmethod
    def truthiness() -> None:
        """Python 中的真值判断"""
        # False 值（falsy）
        falsy_values: list[Any] = [
            False,      # 布尔 False
            None,       # None
            0,          # 整数零
            0.0,        # 浮点零
            0j,         # 复数零
            '',         # 空字符串
            [],         # 空列表
            {},         # 空字典
            set(),      # 空集合
            (),         # 空元组
            range(0),   # 空 range
        ]
        
        for value in falsy_values:
            print(f"bool({value!r:15}) = {bool(value)}")
        
        print("\n--- Truthy values ---")
        # True 值（truthy）- 基本上其他所有值
        truthy_values: list[Any] = [
            True,
            1, -1, 0.1,
            'hello', ' ',  # 非空字符串（包括空格）
            [0],           # 非空列表（即使元素是 0）
            {0: 0},        # 非空字典
        ]
        
        for value in truthy_values:
            print(f"bool({value!r:15}) = {bool(value)}")
    
    @staticmethod
    def boolean_operations() -> None:
        """布尔运算"""
        a: bool = True
        b: bool = False
        
        # 逻辑运算
        print(f"True and False = {a and b}")    # False
        print(f"True or False = {a or b}")      # True
        print(f"not True = {not a}")            # False
        
        # 短路求值
        def side_effect() -> bool:
            print("Function called!")
            return True
        
        # side_effect() 不会被调用，因为 False and ... 一定是 False
        print(f"False and side_effect() = {False and side_effect()}")
        
        # and 和 or 返回的是操作数，不一定是 bool
        print(f"'hello' and 'world' = {'hello' and 'world'}")  # 'world'
        print(f"'' or 'default' = {'' or 'default'}")          # 'default'
        print(f"None or [] or 'found' = {None or [] or 'found'}")  # 'found'
        
        # 实用模式：默认值
        name: str | None = None
        display_name: str = name or "Anonymous"
        print(f"Display name: {display_name}")
    
    @staticmethod
    def comparison_operators() -> None:
        """比较运算符"""
        # 比较运算
        print(f"5 == 5.0 = {5 == 5.0}")         # True (值相等)
        print(f"5 is 5.0 = {5 is 5.0}")         # False (不是同一对象)
        
        # 链式比较
        x: int = 5
        print(f"1 < x < 10 = {1 < x < 10}")     # True
        print(f"1 < x > 3 = {1 < x > 3}")       # True (1 < 5 and 5 > 3)
        
        # is vs ==
        a: list[int] = [1, 2, 3]
        b: list[int] = [1, 2, 3]
        c: list[int] = a
        
        print(f"a == b: {a == b}")  # True (值相等)
        print(f"a is b: {a is b}")  # False (不同对象)
        print(f"a is c: {a is c}")  # True (同一对象)
        
        # None 应该用 is 比较
        value: str | None = None
        print(f"value is None: {value is None}")    # 推荐
        print(f"value == None: {value == None}")    # 不推荐


# ============================================================================
# 5. str 字符串类型
# ============================================================================

class StrDemo:
    """字符串类型详解"""
    
    @staticmethod
    def string_creation() -> None:
        """字符串创建"""
        # 单引号和双引号等价
        s1: str = 'hello'
        s2: str = "hello"
        
        # 三引号：多行字符串
        s3: str = """This is
a multi-line
string"""
        
        # 原始字符串（不转义）
        path: str = r"C:\Users\name\Documents"
        regex: str = r"\d+\.\d+"
        
        # f-string 格式化（Python 3.6+）
        name: str = "Python"
        version: float = 3.12
        s4: str = f"{name} {version}"
        
        # f-string 表达式
        s5: str = f"2 + 2 = {2 + 2}"
        s6: str = f"Upper: {name.upper()}"
        
        # f-string 格式化
        pi: float = 3.14159265359
        s7: str = f"Pi = {pi:.2f}"           # Pi = 3.14
        s8: str = f"Padded: {42:05d}"        # Padded: 00042
        s9: str = f"Percent: {0.756:.1%}"    # Percent: 75.6%
        
        print(s3)
        print(f"Path: {path}")
        print(f"f-string: {s4}")
        print(s7, s8, s9)
    
    @staticmethod
    def string_methods() -> None:
        """字符串方法"""
        s: str = "  Hello, World!  "
        
        # 大小写转换
        print(f"upper(): {s.upper()}")           # "  HELLO, WORLD!  "
        print(f"lower(): {s.lower()}")           # "  hello, world!  "
        print(f"title(): {s.title()}")           # "  Hello, World!  "
        print(f"capitalize(): {s.capitalize()}") # "  hello, world!  "
        print(f"swapcase(): {s.swapcase()}")     # "  hELLO, wORLD!  "
        
        # 去除空白
        print(f"strip(): '{s.strip()}'")         # "Hello, World!"
        print(f"lstrip(): '{s.lstrip()}'")       # "Hello, World!  "
        print(f"rstrip(): '{s.rstrip()}'")       # "  Hello, World!"
        
        # 查找和替换
        text: str = "hello hello hello"
        print(f"find('hello'): {text.find('hello')}")       # 0
        print(f"rfind('hello'): {text.rfind('hello')}")     # 12
        print(f"index('hello'): {text.index('hello')}")     # 0 (找不到会抛异常)
        print(f"count('hello'): {text.count('hello')}")     # 3
        print(f"replace: {text.replace('hello', 'hi', 2)}") # "hi hi hello"
        
        # 判断方法
        print(f"'abc'.isalpha(): {'abc'.isalpha()}")       # True
        print(f"'123'.isdigit(): {'123'.isdigit()}")       # True
        print(f"'abc123'.isalnum(): {'abc123'.isalnum()}") # True
        print(f"'  '.isspace(): {'  '.isspace()}")         # True
        print(f"'Hello'.startswith('He'): {'Hello'.startswith('He')}")  # True
        print(f"'Hello'.endswith('lo'): {'Hello'.endswith('lo')}")      # True
        
        # 分割和连接
        csv: str = "a,b,c,d"
        parts: list[str] = csv.split(',')
        print(f"split(','): {parts}")                      # ['a', 'b', 'c', 'd']
        print(f"join: {'-'.join(parts)}")                  # "a-b-c-d"
        
        lines: str = "line1\nline2\nline3"
        print(f"splitlines(): {lines.splitlines()}")       # ['line1', 'line2', 'line3']
        
        # 对齐
        s = "hello"
        print(f"center(11, '-'): '{s.center(11, '-')}'")   # "---hello---"
        print(f"ljust(10, '-'): '{s.ljust(10, '-')}'")     # "hello-----"
        print(f"rjust(10, '-'): '{s.rjust(10, '-')}'")     # "-----hello"
        print(f"zfill(10): '{'42'.zfill(10)}'")            # "0000000042"
    
    @staticmethod
    def string_formatting() -> None:
        """字符串格式化方式对比"""
        name: str = "Alice"
        age: int = 30
        
        # 方式 1: % 格式化（老式，不推荐）
        s1: str = "Name: %s, Age: %d" % (name, age)
        
        # 方式 2: str.format()
        s2: str = "Name: {}, Age: {}".format(name, age)
        s3: str = "Name: {n}, Age: {a}".format(n=name, a=age)
        
        # 方式 3: f-string（推荐）
        s4: str = f"Name: {name}, Age: {age}"
        
        # f-string 高级格式化
        value: float = 12345.6789
        
        print(f"Fixed point:  {value:.2f}")        # 12345.68
        print(f"Exponential:  {value:.2e}")        # 1.23e+04
        print(f"Percentage:   {0.123:.1%}")        # 12.3%
        print(f"Binary:       {42:b}")             # 101010
        print(f"Hex:          {255:x}")            # ff
        print(f"Octal:        {64:o}")             # 100
        print(f"Width:        {42:10}")            # "        42"
        print(f"Left align:   {42:<10}")           # "42        "
        print(f"Center:       {42:^10}")           # "    42    "
        print(f"With sign:    {42:+}")             # +42
        print(f"Thousands:    {1234567:,}")        # 1,234,567
        
        # f-string 调试（Python 3.8+）
        x = 10
        y = 20
        print(f"{x=}, {y=}, {x+y=}")  # x=10, y=20, x+y=30
    
    @staticmethod
    def string_encoding() -> None:
        """字符串编码"""
        # 字符串是 Unicode
        chinese: str = "你好世界"
        emoji: str = "Hello 🌍!"
        
        print(f"Chinese: {chinese}")
        print(f"Emoji: {emoji}")
        print(f"Length of emoji string: {len(emoji)}")  # 9 (🌍 算一个字符)
        
        # 编码为 bytes
        encoded: bytes = chinese.encode('utf-8')
        print(f"UTF-8 bytes: {encoded}")
        print(f"UTF-8 length: {len(encoded)}")  # 12 (每个中文字符 3 字节)
        
        # 解码回 str
        decoded: str = encoded.decode('utf-8')
        print(f"Decoded: {decoded}")
        
        # 其他编码
        gbk_encoded: bytes = chinese.encode('gbk')
        print(f"GBK bytes: {gbk_encoded}")
        print(f"GBK length: {len(gbk_encoded)}")  # 8 (每个中文字符 2 字节)


# ============================================================================
# 6. bytes 字节类型
# ============================================================================

class BytesDemo:
    """字节类型详解"""
    
    @staticmethod
    def basic_operations() -> None:
        """基本操作"""
        # 创建 bytes
        b1: bytes = b"hello"                    # 字面量（仅 ASCII）
        b2: bytes = bytes([104, 101, 108, 108, 111])  # 从整数列表
        b3: bytes = bytes.fromhex("68656c6c6f")       # 从十六进制
        b4: bytes = "你好".encode("utf-8")             # 从字符串编码
        
        print(f"b1: {b1}")
        print(f"b2: {b2}")
        print(f"b3: {b3}")
        print(f"b4: {b4}")
        
        # bytes 是不可变的
        # b1[0] = 72  # TypeError!
        
        # 索引返回整数
        print(f"b1[0] = {b1[0]} (type: {type(b1[0]).__name__})")  # 104 (int)
        
        # 切片返回 bytes
        print(f"b1[0:2] = {b1[0:2]} (type: {type(b1[0:2]).__name__})")  # b'he'
        
        # 转换方法
        print(f"hex(): {b1.hex()}")           # '68656c6c6f'
        print(f"decode(): {b1.decode()}")     # 'hello'
    
    @staticmethod
    def bytearray_demo() -> None:
        """可变字节数组"""
        # bytearray 是可变的
        ba: bytearray = bytearray(b"hello")
        ba[0] = 72  # 'H'
        print(f"Modified: {ba}")  # bytearray(b'Hello')
        
        ba.append(33)  # '!'
        print(f"Appended: {ba}")  # bytearray(b'Hello!')
        
        ba.extend(b" World")
        print(f"Extended: {ba}")  # bytearray(b'Hello! World')
    
    @staticmethod
    def binary_data() -> None:
        """处理二进制数据"""
        # struct 模块：打包/解包二进制数据
        # 格式: '<' 小端, '>' 大端, 'i' int, 'f' float, 's' string
        
        # 打包
        packed: bytes = struct.pack('<if', 42, 3.14)
        print(f"Packed: {packed.hex()}")
        
        # 解包
        integer, floating = struct.unpack('<if', packed)
        print(f"Unpacked: int={integer}, float={floating}")
        
        # 更复杂的结构
        # 假设有一个包含: id(4字节), x(float), y(float), name(10字节)
        data = struct.pack('<Iff10s', 1, 1.5, 2.5, b'point_001')
        print(f"Struct data: {data.hex()}")
        
        id_, x, y, name = struct.unpack('<Iff10s', data)
        print(f"ID: {id_}, X: {x}, Y: {y}, Name: {name.decode().strip(chr(0))}")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    print("=" * 60)
    print("INT DEMO")
    print("=" * 60)
    IntDemo.basic_operations()
    print()
    IntDemo.arithmetic_operations()
    print()
    IntDemo.bit_operations()
    print(f"\nInt methods: {IntDemo.int_methods()}")
    
    print("\n" + "=" * 60)
    print("FLOAT DEMO")
    print("=" * 60)
    FloatDemo.basic_operations()
    print()
    FloatDemo.precision_issues()
    print()
    FloatDemo.math_functions()
    
    print("\n" + "=" * 60)
    print("DECIMAL DEMO")
    print("=" * 60)
    DecimalDemo.basic_usage()
    print()
    DecimalDemo.rounding_modes()
    print()
    DecimalDemo.financial_calculation()
    
    print("\n" + "=" * 60)
    print("BOOL DEMO")
    print("=" * 60)
    BoolDemo.truthiness()
    print()
    BoolDemo.boolean_operations()
    
    print("\n" + "=" * 60)
    print("STRING DEMO")
    print("=" * 60)
    StrDemo.string_creation()
    print()
    StrDemo.string_methods()
    print()
    StrDemo.string_formatting()
    print()
    StrDemo.string_encoding()
    
    print("\n" + "=" * 60)
    print("BYTES DEMO")
    print("=" * 60)
    BytesDemo.basic_operations()
    print()
    BytesDemo.bytearray_demo()
    print()
    BytesDemo.binary_data()


if __name__ == "__main__":
    main()

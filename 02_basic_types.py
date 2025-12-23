"""
Python 基本数据类型详解：int, float, bool
包含详细的方法说明和实战示例
"""

import math
import sys


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
# 4. 类型转换与检查
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
    print("Python 基本数据类型详解：int, float, bool")
    print("=" * 60)
    
    integer_basics()
    integer_methods()
    
    float_basics()
    float_methods()
    decimal_precision()
    
    boolean_basics()
    truthiness()
    boolean_operators_advanced()
    
    type_conversion()
    practical_examples()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Python 基础语法详解
包含：变量、注释、缩进、关键字、运算符等
"""

# ============================================
# 1. 注释 (Comments)
# ============================================

# 这是单行注释

"""
这是多行注释
可以跨越多行
通常用于文档字符串 (docstring)
"""

'''
这也是多行注释
可以使用单引号或双引号
'''


# ============================================
# 2. 变量与赋值 (Variables and Assignment)
# ============================================

def variables_demo():
    """变量定义与赋值"""
    print("\n=== 变量与赋值 ===")
    
    # 基本赋值
    x = 10
    name = "Python"
    is_valid = True
    
    print(f"x = {x}, name = {name}, is_valid = {is_valid}")
    
    # 多变量赋值
    a, b, c = 1, 2, 3
    print(f"a={a}, b={b}, c={c}")
    
    # 相同值赋值
    x = y = z = 100
    print(f"x={x}, y={y}, z={z}")
    
    # 变量交换
    a, b = b, a
    print(f"交换后: a={a}, b={b}")
    
    # 变量命名规则
    # 1. 只能包含字母、数字、下划线
    # 2. 不能以数字开头
    # 3. 区分大小写
    # 4. 不能使用关键字
    
    my_var = 1          # ✓ 推荐：使用下划线分隔
    myVar = 2           # ✓ 驼峰命名
    _private = 3        # ✓ 私有变量（约定）
    __special__ = 4     # ✓ 特殊变量
    CONSTANT = 5        # ✓ 常量（约定）


# ============================================
# 3. 数据类型 (Data Types) - 概览
# ============================================

def data_types_overview():
    """数据类型概览"""
    print("\n=== 数据类型概览 ===")
    
    # 数字类型
    integer = 42                    # int
    floating = 3.14                 # float
    complex_num = 1 + 2j           # complex
    
    # 字符串
    string = "Hello, World!"       # str
    
    # 布尔值
    boolean = True                 # bool
    
    # 序列类型
    my_list = [1, 2, 3]           # list (可变)
    my_tuple = (1, 2, 3)          # tuple (不可变)
    my_range = range(5)            # range
    
    # 集合类型
    my_set = {1, 2, 3}            # set (无序、不重复)
    my_frozenset = frozenset([1, 2, 3])  # frozenset (不可变集合)
    
    # 映射类型
    my_dict = {"name": "Alice", "age": 25}  # dict
    
    # None 类型
    nothing = None
    
    # 查看类型
    print(f"type(42) = {type(integer)}")
    print(f"type(3.14) = {type(floating)}")
    print(f"type('Hello') = {type(string)}")
    print(f"type([1,2,3]) = {type(my_list)}")


# ============================================
# 4. 运算符 (Operators)
# ============================================

def operators_demo():
    """运算符详解"""
    print("\n=== 运算符 ===")
    
    # 算术运算符
    print("算术运算符:")
    print(f"10 + 3 = {10 + 3}")      # 加法
    print(f"10 - 3 = {10 - 3}")      # 减法
    print(f"10 * 3 = {10 * 3}")      # 乘法
    print(f"10 / 3 = {10 / 3}")      # 除法（浮点）
    print(f"10 // 3 = {10 // 3}")    # 整除
    print(f"10 % 3 = {10 % 3}")      # 取模
    print(f"10 ** 3 = {10 ** 3}")    # 幂运算
    
    # 比较运算符
    print("\n比较运算符:")
    print(f"10 == 10: {10 == 10}")   # 等于
    print(f"10 != 5: {10 != 5}")     # 不等于
    print(f"10 > 5: {10 > 5}")       # 大于
    print(f"10 < 5: {10 < 5}")       # 小于
    print(f"10 >= 10: {10 >= 10}")   # 大于等于
    print(f"10 <= 5: {10 <= 5}")     # 小于等于
    
    # 逻辑运算符
    print("\n逻辑运算符:")
    print(f"True and False: {True and False}")
    print(f"True or False: {True or False}")
    print(f"not True: {not True}")
    
    # 位运算符
    print("\n位运算符:")
    print(f"5 & 3 = {5 & 3}")        # 按位与
    print(f"5 | 3 = {5 | 3}")        # 按位或
    print(f"5 ^ 3 = {5 ^ 3}")        # 按位异或
    print(f"~5 = {~5}")              # 按位取反
    print(f"5 << 1 = {5 << 1}")      # 左移
    print(f"5 >> 1 = {5 >> 1}")      # 右移
    
    # 赋值运算符
    print("\n赋值运算符:")
    x = 10
    x += 5   # x = x + 5
    print(f"x += 5: {x}")
    x -= 3   # x = x - 3
    print(f"x -= 3: {x}")
    x *= 2   # x = x * 2
    print(f"x *= 2: {x}")
    x //= 4  # x = x // 4
    print(f"x //= 4: {x}")
    
    # 成员运算符
    print("\n成员运算符:")
    my_list = [1, 2, 3, 4, 5]
    print(f"3 in [1,2,3,4,5]: {3 in my_list}")
    print(f"10 not in [1,2,3,4,5]: {10 not in my_list}")
    
    # 身份运算符
    print("\n身份运算符:")
    a = [1, 2, 3]
    b = a
    c = [1, 2, 3]
    print(f"b is a: {b is a}")       # True (同一对象)
    print(f"c is a: {c is a}")       # False (不同对象)
    print(f"c == a: {c == a}")       # True (值相等)
    print(f"c is not a: {c is not a}")


# ============================================
# 5. 字符串基础 (String Basics)
# ============================================

def string_basics():
    """字符串基础操作"""
    print("\n=== 字符串基础 ===")
    
    # 字符串创建
    single = 'single quotes'
    double = "double quotes"
    triple = """triple quotes
    can span multiple lines"""
    
    # 字符串拼接
    greeting = "Hello" + " " + "World"
    print(f"拼接: {greeting}")
    
    # 字符串重复
    repeated = "Ha" * 3
    print(f"重复: {repeated}")
    
    # 字符串索引和切片
    text = "Python"
    print(f"第一个字符: {text[0]}")
    print(f"最后一个字符: {text[-1]}")
    print(f"切片 [1:4]: {text[1:4]}")
    print(f"切片 [:3]: {text[:3]}")
    print(f"切片 [3:]: {text[3:]}")
    print(f"反转: {text[::-1]}")
    
    # 字符串格式化
    name = "Alice"
    age = 25
    
    # 方法1: % 格式化
    print("我是 %s, 今年 %d 岁" % (name, age))
    
    # 方法2: format()
    print("我是 {}, 今年 {} 岁".format(name, age))
    print("我是 {name}, 今年 {age} 岁".format(name=name, age=age))
    
    # 方法3: f-string (推荐，Python 3.6+)
    print(f"我是 {name}, 今年 {age} 岁")
    print(f"明年我 {age + 1} 岁")
    
    # 原始字符串 (raw string)
    path = r"C:\Users\name\files"  # 不转义反斜杠
    print(f"路径: {path}")


# ============================================
# 6. 输入输出 (Input/Output)
# ============================================

def io_basics():
    """基础输入输出"""
    print("\n=== 输入输出 ===")
    
    # 输出
    print("Hello, World!")
    print("多个", "参数", "输出", sep="-", end="!\n")
    
    # 格式化输出
    pi = 3.14159265359
    print(f"π ≈ {pi:.2f}")          # 保留2位小数
    print(f"π ≈ {pi:.4f}")          # 保留4位小数
    
    num = 42
    print(f"十进制: {num:d}")
    print(f"二进制: {num:b}")
    print(f"八进制: {num:o}")
    print(f"十六进制: {num:x}")
    
    # 输入 (注释掉以避免交互)
    # name = input("请输入你的名字: ")
    # print(f"你好, {name}!")
    # 
    # age = int(input("请输入你的年龄: "))
    # print(f"你今年 {age} 岁")


# ============================================
# 7. 缩进与代码块 (Indentation)
# ============================================

def indentation_demo():
    """缩进规则演示"""
    print("\n=== 缩进规则 ===")
    
    # Python 使用缩进来定义代码块
    # 推荐使用 4 个空格
    
    x = 10
    if x > 5:
        print("x 大于 5")
        print("这是同一个代码块")
    print("这是外层代码")
    
    # 多层缩进
    for i in range(3):
        print(f"外层循环: {i}")
        for j in range(2):
            print(f"  内层循环: {j}")


# ============================================
# 8. 关键字 (Keywords)
# ============================================

def keywords_demo():
    """Python 关键字"""
    print("\n=== Python 关键字 ===")
    
    import keyword
    print(f"Python 关键字总数: {len(keyword.kwlist)}")
    print(f"关键字列表:\n{keyword.kwlist}")
    
    # 常用关键字分类：
    # 控制流: if, elif, else, for, while, break, continue, pass
    # 函数相关: def, return, lambda, yield
    # 类相关: class
    # 异常处理: try, except, finally, raise
    # 逻辑运算: and, or, not, in, is
    # 导入: import, from, as
    # 其他: None, True, False, with, async, await


# ============================================
# 9. 命名空间与作用域 (Namespace and Scope)
# ============================================

# 全局变量
global_var = "我是全局变量"

def scope_demo():
    """作用域演示"""
    print("\n=== 命名空间与作用域 ===")
    
    # 局部变量
    local_var = "我是局部变量"
    
    def inner_function():
        # 嵌套函数中的变量
        inner_var = "我是嵌套函数的变量"
        print(f"访问全局变量: {global_var}")
        print(f"访问外层函数变量: {local_var}")
        print(f"访问本地变量: {inner_var}")
    
    inner_function()
    
    # 使用 global 关键字修改全局变量
    def modify_global():
        global global_var
        global_var = "全局变量被修改了"
    
    print(f"修改前: {global_var}")
    modify_global()
    print(f"修改后: {global_var}")
    
    # LEGB 规则: Local -> Enclosing -> Global -> Built-in
    x = "global"
    
    def outer():
        x = "enclosing"
        
        def inner():
            x = "local"
            print(f"local x: {x}")
        
        inner()
        print(f"enclosing x: {x}")
    
    outer()
    print(f"global x: {x}")


# ============================================
# 10. 代码风格 (Code Style - PEP 8)
# ============================================

def style_guide():
    """PEP 8 代码风格指南要点"""
    print("\n=== 代码风格指南 (PEP 8) ===")
    
    print("""
    重要规则:
    1. 使用 4 个空格进行缩进
    2. 每行最多 79 个字符
    3. 使用空行分隔函数和类
    4. 在操作符两侧加空格
    5. 函数和变量使用小写 + 下划线
    6. 类名使用驼峰命名法
    7. 常量使用全大写 + 下划线
    
    示例:
    """)
    
    # 好的风格
    def calculate_sum(a, b):
        """计算两个数的和"""
        result = a + b
        return result
    
    # 类命名
    class MyClass:
        """示例类"""
        CONSTANT_VALUE = 100
        
        def __init__(self):
            self.instance_var = 10
    
    print("参考 PEP 8 获取完整风格指南")


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 基础语法详解")
    print("=" * 60)
    
    variables_demo()
    data_types_overview()
    operators_demo()
    string_basics()
    io_basics()
    indentation_demo()
    keywords_demo()
    scope_demo()
    style_guide()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

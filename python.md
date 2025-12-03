# uv

### 项目初始化

```bash
# 创建新的 Python 项目
uv init my-project
cd my-project

# 创建带特定 Python 版本的项目
uv init --python 3.11 my-project

# 创建应用程序项目（非库）
uv init --app my-app

# 创建库项目
uv init --lib my-library
```

## 依赖管理命令

```bash
# 添加运行时依赖
uv add requests
uv add "django>=4.0,<5.0"
uv add numpy pandas matplotlib

# 添加开发依赖
uv add --dev pytest black mypy
uv add --dev "pytest>=6.0"

# 添加可选依赖组
uv add --optional web flask fastapi
uv add --optional data pandas numpy scipy

# 移除依赖
uv remove requests
uv remove pytest --dev
uv remove flask --optional web

# 更新所有依赖
uv lock --upgrade

# 更新特定依赖
uv lock --upgrade-package requests
uv lock --upgrade-package "django>=4.0"

# 同步到锁定文件状态
uv sync

# 同步并安装开发依赖
uv sync --dev

# 同步特定可选依赖组
uv sync --optional web
uv sync --optional "web,data"
```

## 运行

```bash
# 指定版本
uv venv --python 3.11

# uv 会自动激活环境，也可以手动激活
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate      # Windows

# 运行 Python 脚本
uv run python script.py

# 运行模块
uv run python -m my_module

# .env 文件示例
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your-api-key
DEBUG=true

# 运行并传递环境变量
uv run --env-file .env python script.py
```

# DataType

### 变量 (Variables)

#### 什么是变量

变量是用来存储数据的容器，可以在程序运行过程中改变其值。在 Python 中，变量不需要声明类型，Python 会根据赋值自动推断数据类型。

#### 变量的特点

- **动态类型**：Python 是动态类型语言，变量类型在运行时确定
- **可变性**：变量的值可以在程序执行过程中改变
- **无需声明**：使用前不需要显式声明变量类型

#### 变量命名规则

```python
## 正确的变量名
name = "张三"
age = 25
user_id = 12345
firstName = "李"  ## 驼峰命名法
_private_var = "私有变量"

## 错误的变量名示例
## 123name = "错误"     ## 不能以数字开头
## for = "错误"        ## 不能使用关键字
## user-name = "错误"  ## 不能包含连字符
```

#### 变量赋值

```python
## 基本赋值
x = 10
name = "Python"
is_valid = True

## 多重赋值
a, b, c = 1, 2, 3
x = y = z = 0

## 交换变量值
a, b = b, a

## 动态类型演示
var = 10        ## 整数
var = "hello"   ## 字符串
var = [1,2,3]   ## 列表
```

#### 变量作用域

```python
## 全局变量
global_var = "我是全局变量"

def function_example():
    ## 局部变量
    local_var = "我是局部变量"

    ## 访问全局变量
    print(global_var)

    ## 修改全局变量需要global关键字
    global global_var
    global_var = "修改后的全局变量"

    return local_var

## 内置函数查看变量
print(type(global_var))  ## <class 'str'>
print(id(global_var))    ## 查看内存地址
```

### 常量 (Constants)

#### 什么是常量

常量是在程序运行过程中不应该改变的值。虽然 Python 没有真正的常量机制，但通过约定俗成的方式来表示常量。

#### Python 中的常量约定

```python
## 使用全大写字母表示常量
PI = 3.14159
MAX_SIZE = 100
DATABASE_URL = "localhost:5432"
API_KEY = "your_api_key_here"

## 多单词常量用下划线分隔
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
```

#### 内置常量

```python
## Python内置常量
print(True)     ## 布尔值真
print(False)    ## 布尔值假
print(None)     ## 空值

## 其他内置常量
print(__name__)     ## 当前模块名 if __name__ == 'main':
print(__file__)     ## 当前文件路径
```

#### 使用枚举创建常量

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Status(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

## 使用枚举常量
current_color = Color.RED
print(current_color.name)   ## RED
print(current_color.value)  ## 1
```

### 数据类型与变量

#### 基本数据类型

```python
## 数字类型
integer_var = 42          ## 整数
float_var = 3.14          ## 浮点数
complex_var = 3 + 4j      ## 复数

## 字符串类型
string_var = "Hello, World!"
multiline_string = """
这是多行
字符串
"""

## 布尔类型
bool_var = True
is_empty = False

## 空值
none_var = None
```

#### 集合数据类型

```python
## 列表 (可变)
list_var = [1, 2, 3, "hello"]
list_var.append(4)  ## 可以修改

## 元组 (不可变)
tuple_var = (1, 2, 3, "hello")
## tuple_var[0] = 10  ## 这会报错

## 集合
set_var = {1, 2, 3, 4, 5}

## 字典
dict_var = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}
```

### 最佳实践

#### 变量命名建议

```python
## 使用有意义的变量名
user_count = 100        ## 好
x = 100                ## 不好

## 使用描述性名称
total_price = 299.99   ## 好
tp = 299.99           ## 不好

## 布尔变量使用is_、has_、can_等前缀
is_logged_in = True
has_permission = False
can_edit = True
```

#### 常量使用建议

```python
## 在文件顶部定义常量
MAX_CONNECTIONS = 100
DEFAULT_ENCODING = "utf-8"
API_VERSION = "v1"

def connect_to_database():
    ## 使用常量而不是硬编码
    if connection_count > MAX_CONNECTIONS:
        raise Exception("超过最大连接数")
```

#### 类型提示 (Type Hints)

```python
from typing import List, Dict, Optional

## 变量类型提示
name: str = "张三"
age: int = 25
height: float = 175.5
is_student: bool = True

## 函数参数和返回值类型提示
def calculate_area(length: float, width: float) -> float:
    return length * width

def get_user_info(user_id: int) -> Optional[Dict[str, str]]:
    ## 返回用户信息或None
    pass
```

### 内存管理

#### 变量的内存分配

```python
## 查看变量内存地址
a = 10
b = 10
print(id(a))  ## 内存地址
print(id(b))  ## 相同的内存地址（小整数缓存）

## 可变对象和不可变对象
list1 = [1, 2, 3]
list2 = list1        ## 指向同一个对象
list2.append(4)      ## 会影响list1

tuple1 = (1, 2, 3)
tuple2 = tuple1      ## 指向同一个对象
## tuple2[0] = 10     ## 不可变，会报错
```

#### 垃圾回收

```python
import gc

## 查看引用计数
import sys
a = [1, 2, 3]
print(sys.getrefcount(a))  ## 引用计数

## 手动垃圾回收
gc.collect()
```

## Python 基础数据类型与常用方法详解

### 1. Numeric（数值类型）

#### 1.1 整数（int）

```python
## 创建整数
x = 10
int(3.14)  ## 浮点数转整数（向下取整）
round(3.14)      ## 四舍五入: 3
round(3.14, 1)      ## 四舍五入: 3.1

y = int('20')  ## 字符串转整数
y = int('20', 2)  ## 字符串转整数
y = int('20', 8)  ## 字符串转整数
y = int('20', 16)  ## 字符串转整数

## 常用方法和操作
bin(10)         ## 二进制: '0b1010'
oct(10)         ## 八进制: '0o12'
hex(10)         ## 十六进制: '0xa'

min(1, 2, 3)
max(1, 2, 3)
sum([1, 2, 3])

## 位运算
a & b   ## 按位与
a | b   ## 按位或
a ^ b   ## 按位异或
~a      ## 按位取反
a << 2  ## 左移
a >> 2  ## 右移
```

#### 1.2 浮点数（float）

```python
## 创建浮点数
x = 3.14

y = float('3.14')

## 常用方法
import math

math.ceil(3.2)     ## 向上取整: 4
math.floor(3.8)    ## 向下取整: 3
math.trunc(3.9)    ## 截断小数: 3

math.inf
math.nan
math.isnan(x)      ## 检查是否为NaN
math.isinf(x)      ## 检查是否为无穷

## 浮点数方法
x.is_integer()     ## 检查是否为整数值
```

#### 1.3 复数（complex）

```python
## 创建复数
z = 3 + 4j
z = complex(3, 4)

## 复数属性和方法
z.real         ## 实部: 3.0
z.imag         ## 虚部: 4.0
z.conjugate()  ## 共轭复数: (3-4j)
abs(z)         ## 模: 5.0
```

### 2. Boolean（布尔类型）

```python
## 创建布尔值
a = True
b = False
c = bool(1)    ## True
d = bool("")   ## False

## 布尔运算
x and y   ## 逻辑与
x or y    ## 逻辑或
not x     ## 逻辑非

## 真值测试（以下为False）
bool(None)     ## None
bool(False)    ## False本身
bool(0)        ## 数值0
bool(0.0)      ## 浮点数0
bool(0j)       ## 复数0
bool('')       ## 空字符串
bool([])       ## 空列表
bool(())       ## 空元组
bool({})       ## 空字典
bool(set())    ## 空集合
```

### 3. String（字符串）

```python
## 创建字符串
s = 'hello'
s = "world"
s = '''多行
字符串'''
s = r'原始字符串\n'  ## 不转义
f = f'{variable} format'     ## f-string格式化
b = b'hello' # bytes 解码 b.decode('utf-8') 编码 s.encode('utf-8')

## 字符串方法
s.upper()          ## 转大写
s.lower()          ## 转小写
s.title()          ## 每个单词首字母大写
s.capitalize()     ## 首字母大写

s.replace('old', 'new', count=1)  ## 替换

## 判断方法
'sub' in s # 返回索引或-1 s.find('sub') s.rfind('sub') 不存在抛异常 s.index('sub') s.rindex('sub')
s.count('sub')     ## 统计子串出现次数

s.startswith('prefix')  ## 是否以指定字符串开头
s.endswith('suffix')    ## 是否以指定字符串结尾

s.isalpha()       ## 是否全是字母
s.isdigit()       ## 是否全是数字
s.isalnum()       ## 是否全是字母或数字
s.isspace()       ## 是否全是空白字符
s.isupper()       ## 是否全是大写
s.islower()       ## 是否全是小写
s.istitle()       ## 是否标题化

## 分割和连接
s.split(',', maxsplit=-1)      ## 分割字符串 s.rsplit(',', 1)
s.splitlines()    ## 按行分割

','.join(['a', 'b'])  ## 连接字符串

## 修剪和填充
s.strip()         ## 去除两端空白
s.lstrip()        ## 去除左侧空白
s.rstrip()        ## 去除右侧空白

s.ljust(10, fillchar="x")       ## 左对齐
s.rjust(10, fillchar="x")       ## 右对齐
s.center(10)      ## 居中，填充空格
```

### 4. Regular Expression（正则表达式）

```python
import re

## 编译正则表达式
pattern = re.compile(r'\d+')

### 常用正则表达式模式
r'\d'      ## 数字
r'\D'      ## 非数字
r'\w'      ## 字母数字下划线
r'\W'      ## 非字母数字下划线
r'\s'      ## 空白字符
r'\S'      ## 非空白字符
r'.'       ## 任意字符（除换行符）
r'^'       ## 字符串开头
r'$'       ## 字符串结尾
r'*'       ## 0或多个
r'+'       ## 1或多个
r'?'       ## 0或1个
r'{n}'     ## 恰好n个
r'{n,m}'   ## n到m个
r'[abc]'   ## 字符集合
r'[^abc]'  ## 反向字符集合
r'(pat)'   ## 分组
r'(?:pat)' ## 非捕获分组
r'(?=pat)' ## 正向预查
r'(?!pat)' ## 负向预查
r'(?<=pat)' ## 正向回顾
r'(?<!pat)' ## 负向回顾
r'(?P<name>pat)' ## 命名分组

### 标志 flags= |
re.IGNORECASE  ## 忽略大小写
re.MULTILINE   ## 多行模式
re.DOTALL      ## 点匹配所有字符
re.VERBOSE     ## 详细模式
re.ASCII       ## ASCII模式

## 匹配方法
re.search(r'pat', 'string')    ## 搜索第一个匹配
re.finditer(r'pat', 'string')  ## 返回迭代器 Match[string]
re.findall(r'pat', 'string')   ## 查找所有匹配分组 分组 [()] 不存在分组 [str]

re.match(r'pat', 'string')     ## 从开头匹配
re.fullmatch(r'pat', 'string') ## 完全匹配（头尾）

match = re.search(r'(\d+)', 'abc123')
if match:
    match.group()     ## 返回匹配的字符串
    match.group(1)    ## 返回第一个分组

    match.groups()    ## 返回所有分组
    match.groupdict()    ## 返回所有命名分组

    match.span()      ## 返回(start, end)
    match.start()     ## 匹配开始位置
    match.end()       ## 匹配结束位置

## 替换和分割
re.sub(r'pat', 'repl', 'string', count=-1)    ## 替换 \1 \2 分组引用 \g<name> 命名分组 def replace_match(match: Match[string] | None): -> string 函数

re.split(r'pat', 'string')          ## 分割
```

### 5. List（列表）

```python
## 创建列表
lst = [1, 2, 3]
lst = list(iterator)

lst = [x**2 for x in range(10)]  ## 列表推导式

lst[start] # 获取元素 start <= len - 1
lst[start:end]        ## 获取切片
lst[start:end:step]   ## 带步长的切片
lst[::-1]             ## 反转列表

## 添加元素
lst.append(item)       ## 末尾添加
lst.extend([4, 5])     ## 扩展列表
lst.insert(index, item)  ## 指定位置插入

## 删除元素
lst.pop()             ## 删除并返回最后一个元素
lst.pop(index)        ## 删除并返回指定位置元素
lst.remove(item)      ## item in lst
lst.clear()           ## 清空列表

del lst[index]        ## 删除指定位置元素
del lst[start:end]    ## 删除切片

## 查找和统计
item in lst           ## 检查元素是否存在 lst.index(item) lst.index(item, start, end)
lst.count(item)       ## 统计元素出现次数

## 排序和反转
lst.sort()            ## 原地排序
lst.sort(reverse=True)  ## 降序排序
lst.sort(key=len)     ## 按指定函数排序
lst.reverse()         ## 原地反转

sorted(lst)           ## 返回排序后的新列表
reversed(lst)         ## 返回反转迭代器

## 复制
lst.copy()            ## 浅复制
lst[:]                ## 切片复制

import copy
copy.deepcopy(lst)   ## 深复制

## 计数器
from collections import Counter

c = Counter(['a', 'b', 'a'])

c.most_common(2)      ## 最常见的n个元素 [('a', 2), ('b', 1)]

c.update(['b', 'c'])  ## 更新计数
c.subtract(['a'])     ## 减少计数
```

### 6. Tuple（元组）

```python
## 创建元组
t = (1, 2, 3) ## 单元素元组需要逗号 (1,)
t = tuple(iterator)

## 元组方法（不可变）
item in t ## 检查元素是否存在 t.index(item)

t.count(item)         ## 统计元素出现次数

## 元组解包
a, b, c = t           ## 解包
a, *rest = t          ## 扩展解包
a, *_, c = t          ## 忽略中间元素
```

### 7. Set（集合）

```python
## 创建集合
s = {1, 2, 3}
s = set(iterator)

s = {x**2 for x in range(10)}  ## 集合推导式

## 添加和删除
s.add(item)           ## 添加元素
s.update([4, 5])      ## 批量添加

s.pop()               ## 删除并返回任意元素
s.discard(item)       ## 删除元素（不存在不抛异常）s.remove(item) item in s
s.clear()             ## 清空集合

## 集合运算
s1 | s2               ## 并集 s1.union(s2)
s1 & s2               ## 交集 s1.intersection(s2)
s1 - s2               ## 差集 s1.difference(s2)
s1 ^ s2               ## 对称差集 s1.symmetric_difference(s2)

## 集合关系判断
s1 <= s2   ## 是否为子集 s1.issubset(s2)
s1 >= s2 ## 是否为超集 s1.issuperset(s2)
```

### 8. Dictionary（字典）

```python
## 创建字典
d = {'a': 1, 'b': 2}
d = dict(a=1, b=2)
d = dict([('a', 1), ('b', 2)])
d = dict.fromkeys(['a', 'b'], 0)

d = {x: x**2 for x in range(5)}  ## 字典推导式

## 访问和修改
d.get('key', default)          ## 获取值（不存在返回None）d['key'] 不存在抛异常 key in d
d['key'] = value      ## 设置值 d.setdefault('key', default)
del d['key']          ## 删除键值对 不存在抛异常 key in d
d.clear()             ## 清空字典

## 更新和复制
d.update({'c': 3})    ## 更新字典
d.update(c=3, d=4)    ## 关键字参数更新
d.update([('c'， 3), ('d', 4)])    ## 关键字参数更新

d.copy()              ## 浅复制

## 视图对象
d.keys()              ## 键视图
d.values()            ## 值视图
d.items()             ## 键值对视图

## 遍历
for key in d:
    print(key, d[key])
for key, value in d.items():
    print(key, value)

## 特殊字典类型
from collections import defaultdict

## defaultdict：带默认值的字典
dd = defaultdict(list)

dd['key'].append(1)
```

### 9. Class（类）

```python
## 定义类
from typing import Any, Iterator

class MyClass:
    ## 类变量
    class_var: int = 0

    ## 构造函数
    def __init__(self, name: str) -> None:
        self.name: str = name  ## 实例变量
        self._protected: int = 0  ## 受保护变量（约定）
        self.__private: int = 0   ## 私有变量（名称改写）

    ## 实例方法
    def method(self) -> str:
        return self.name

    ## 类方法
    @classmethod
    def class_method(cls) -> int:
        return cls.class_var

    ## 静态方法
    @staticmethod
    def static_method() -> str:
        return "static"

    ## 属性装饰器
    @property
    def prop(self) -> int:
        return self._protected

    @prop.setter
    def prop(self, value: int) -> None:
        self._protected = value

    @prop.deleter
    def prop(self) -> None:
        del self._protected

    ## 特殊方法（魔术方法）
    def __str__(self) -> str:
        # str(self)
        return f"MyClass({self.name})"

    def __repr__(self) -> str:
        # repr(self)
        return f"MyClass('{self.name}')"

    def __getitem__(self, key: int) -> str:
        # self[key]
        return self.name[key]

    def __setitem__(self, key: int, value: str) -> None:
        # self[key] = value
        pass

    def __delitem__(self, key: int) -> None:
        # del self[key]
        pass

    def __len__(self) -> int:
        # len(self)
        return len(self.name)

    def __contains__(self, item: str) -> bool:
        # item in self
        return item in self.name

    def __iter__(self) -> Iterator[str]:
        # iter(self)
        return iter(self.name)

    def __next__(self):
        pass

    def __eq__(self, other: Any) -> bool:
        # self == other
        return self.name == other.name

    def __lt__(self, other: Any) -> bool:
        # self < other
        return self.name < other.name

    def __add__(self, other: Any) -> str:
        # self + other
        return self.name + other.name

    def __enter__(self) -> "MyClass":
        # with 语句进入时调用
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # with 语句退出时调用
        pass

## 继承
class ChildClass(MyClass):
    def __init__(self, name: str, age: int) -> None:
        super().__init__(name)
        self.age: int = age

    def method(self) -> str:
        return super().method() + str(self.age)

## 多重继承
class A:
    def __init__(self, value: int) -> None:
        self.value = value

    def show(self) -> str:
        return f"A: {self.value}"

class B:
    def __init__(self, text: str) -> None:
        self.text = text

    def show(self) -> str:
        return f"B: {self.text}"

class C(A, B):
    def __init__(self, value: int, text: str) -> None:
        super().__init__(value)  # 在新式类中，super() 会遵循 MRO 调用A.__init__，即广度优先从左到右
        B.__init__(self, text)   # 必须显式调用B.__init__，否则B不会初始化

    def show(self) -> str:
        s1 = super().show()      # 默认按照MRO先调用A.show
        s2 = B.show(self)        # 也可手动调用B.show
        return s1 + "; " + s2

## 类型检查
isinstance(obj, MyClass)  ## 检查实例
issubclass(ChildClass, MyClass)  ## 检查子类
```

### 10. Datetime（日期时间）

```python
from datetime import datetime
import time

## datetime对象
dt = datetime(2024, 1, 1, 12, 0, 0)  ## 指定时间
dt = datetime.now()           ## 当前时间 datetime.today()
dt = datetime.fromtimestamp(timestamp)  ## 从时间戳创建
dt = datetime.strptime('2024-01-01', '%Y-%m-%d')  ## 解析字符串

### 格式化字符串
'%Y'    ## 4位年份
'%y'    ## 2位年份
'%m'    ## 月份（01-12）
'%d'    ## 日期（01-31）
'%H'    ## 小时（00-23）
'%I'    ## 小时（01-12）
'%M'    ## 分钟（00-59）
'%S'    ## 秒（00-59）
'%p'    ## AM/PM

### 常量
dt.year, dt.month, dt.day
dt.hour, dt.minute, dt.second, dt.milliseconds / 1000 second, dt.microsecond / 1000 * 1000 second


## 方法
dt.date()             ## 获取日期部分
dt.time()             ## 获取时间部分
dt.isoweekday()       ## 星期几（1-7） dt.weekday() (0-6) dt.isocalendar()

dt.timestamp()        ## 转时间戳 float
dt.strftime('%Y-%m-%d %H:%M:%S')  ## 格式化
dt.isoformat()        ## ISO格式字符串

dt.replace(year=2025)  ## 替换部分

## date对象
from datetime import date

d = date.today()      ## 今天
d = date(2024, 1, 1)  ## 指定日期

d.isoweekday()           ## 星期几（1-7） dt.weekday() (0-6)

d.strftime('%Y-%m-%d')  ## 格式化
d.isoformat()         ## ISO格式

## time对象
from datetime import time

t = time(12, 30, 45)  ## 指定时间

t.strftime('%H:%M:%S')  ## 格式化
t.isoformat()         ## ISO格式

## timedelta对象（时间差）
from datetime import timedelta

td = timedelta(days=7, hours=2, minutes=30, seconds=0, milliseconds=0)

dt2 = dt + timedelta(days=1)  ## 加一天
dt2 = dt - timedelta(hours=1)  ## 减一小时
diff = dt2 - dt       ## 时间差

td.days               ## 天数（只包含） 7
td.seconds            ## 秒数（不包含天数）int 2 hours * 60 * 60 + 30 minutes * 60
td.total_seconds()    ## 总秒数 float

## time模块
from time import time, sleep

time()           ## 当前时间戳 float
sleep(1)         ## 休眠1秒
```

### 11. json（JSON 模块详解）

#### 基本用法

```python
import json

# Python 字典/列表转 JSON 字符串
data = {'name': 'Alice', 'age': 25, 'hobbies': ['reading', 'music']}
json_str = json.dumps(data)
print(json_str)  # {"name": "Alice", "age": 25, "hobbies": ["reading", "music"]}

# JSON 字符串转 Python 对象
parsed = json.loads(json_str)
print(parsed['name'])  # Alice
```

#### 文件读写

```python
# 保存到 .json 文件
data = {'user': 'Alice', 'score': 99}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)  # ensure_ascii=False 支持中文，indent 格式化

# 从 .json 文件读取
with open('data.json', 'r', encoding='utf-8') as f:
    loaded = json.load(f)
    print(loaded['user'])
```

#### 异常处理

- `json.JSONDecodeError`: 解码错误
- `TypeError`: 非法类型无法序列化

```python
try:
    obj = json.loads('invalid json')
except json.JSONDecodeError as e:
    print("解析失败:", e)
```

#### Python 和 JSON 类型映射表

| Python      | JSON       |
| ----------- | ---------- |
| dict        | object     |
| list, tuple | array      |
| str         | string     |
| int, float  | number     |
| True/False  | true/false |
| None        | null       |

### 12. CSV 详解

#### 基本用法

```python
import csv

# 读取 CSV 文件
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # 每一行是一个列表

# 写入 CSV 文件
data = [
    ['姓名', '年龄', '城市'],
    ['张三', '25', '北京'],
    ['李四', '30', '上海']
]
with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

#### 字典方式读写 (`csv.DictReader` / `csv.DictWriter`)

```python
# 以字典方式读取
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['姓名'], row['年龄'])

# 以字典方式写入
data = [
    {'姓名': '王五', '年龄': 22, '城市': '广州'},
    {'姓名': '赵六', '年龄': 27, '城市': '深圳'}
]
with open('output2.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['姓名', '年龄', '城市']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

### 13. Error（错误和异常）

```python
## 异常层次结构
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- PermissionError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning

## 异常处理
try:
    ## 可能出错的代码
    result = 10 / 0
except ZeroDivisionError as e:
    ## 处理特定异常
    print(f"除零错误: {e}")
except (ValueError, TypeError) as e:
    ## 处理多个异常
    print(f"值或类型错误: {e}")
except Exception as e:
    ## 处理其他异常
    print(f"其他错误: {e}")
else:
    ## 没有异常时执行
    print("没有错误")
finally:
    ## 总是执行
    print("清理资源")

## 抛出异常
raise ValueError("错误信息")

## 自定义异常
class CustomError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

    def __str__(self):
        if self.code:
            return f"{self.args[0]} (Code: {self.code})"

        return str(self.args[0])

## 上下文管理
class MyContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"处理异常: {exc_val}")

        return False  ## 返回True会抑制异常

# 异步上下文管理器
class AsyncResource:
    async def __aenter__(self):
        print("获取资源")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("释放资源")
        await asyncio.sleep(0.1)

async def context_manager_example():
    """异步上下文管理器"""
    async with AsyncResource() as resource:
        print("使用资源")
        await asyncio.sleep(1)
```

### 12. Enum（枚举）

```python
from enum import Enum

## 基本枚举
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

## 访问枚举
Color.RED             ## 枚举成员
Color.RED.name        ## 'RED'
Color.RED.value       ## 1
```

### 13. Iterator & Generator（迭代器与生成器）

#### 迭代器（Iterators）

##### 迭代协议

```python
## 可迭代对象：实现了 __iter__() 方法
## 迭代器：实现了 __iter__() 和 __next__() 方法

class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

it = MyIterator([1, 2, 3]) ## 迭代器是一次性的

print(next(it)) ## 1
print(next(it)) ## 2
print(next(it)) ## 3
print(next(it)) ## StopIteration

## for-in
my_iter = MyIterator([1, 2, 3])

for item in my_iter:
    print(item)  ## 输出: 1, 2, 3

## 异步迭代器
class AsyncCounter:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count >= self.max_count:
            raise StopAsyncIteration

        await asyncio.sleep(0.1)
        self.count += 1
        return self.count

async def async_iterator_example():
    """异步迭代器示例"""
    async for value in AsyncCounter(5):
        print(f"异步迭代值: {value}")
```

##### 内置迭代器

```python
## 使用 iter() 函数创建迭代器
numbers = [1, 2, 3, 4, 5]
my_iter = iter(numbers)

for item in my_iter:
    print(item)  ## 输出: 1, 2, 3, 4, 5

## 迭代器是一次性的
for item in my_iter:
    print(item)  ## 无输出
```

#### 生成器（Generators）

##### yield 关键字

生成器是创建迭代器的简单方式，使用 `yield` 关键字可以轻松创建生成器函数。

```python
def simple_generator():
    yield 1
    yield 2
    yield 3

## for-in
for value in simple_generator():
    print(value)  ## 输出: 1, 2, 3
```

##### 生成器的优势

生成器采用惰性计算，节省内存：

```python
## 传统方式 - 占用大量内存
def get_squares_list(n):
    return [x**2 for x in range(n)]

## 生成器方式 - 按需计算，节省内存
def get_squares_generator(n):
    for x in range(n):
        yield x**2
```

##### 生成器表达式

```python
## 列表推导式使用方括号
squares_list = [x**2 for x in range(10)]

## 生成器表达式使用圆括号
squares_gen = (x**2 for x in range(10))

## 生成器表达式可以直接传递给函数
total = sum(x**2 for x in range(100))
```

##### 高级生成器特性

```python
## 1. send() 方法 - 向生成器发送值
def interactive_generator():
    value = 0
    while True:
        received = yield value
        if received is not None:
            value = received
        else:
            value += 1

gen = interactive_generator()

print(next(gen))        ## 0
print(gen.send(10))     ## 10
print(next(gen))        ## 11

## 2. yield from - 委托生成器
def sub_generator():
    yield 1
    yield 2

def main_generator():
    yield from sub_generator()
    yield from [3, 4]
    yield 5

for val in main_generator():
    print(val)  ## 输出: 1, 2, 3, 4, 5
```

#### 推导式（Comprehensions）

##### 列表推导式

```python
## 基本语法
squares = [x**2 for x in range(10)]

## 带条件的列表推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]

## 嵌套循环
matrix = [[i*j for j in range(3)] for i in range(3)]

## 条件表达式
result = [x if x > 0 else 0 for x in [-1, 2, -3, 4]]
```

##### 字典推导式

```python
## 基本语法
squares_dict = {x: x**2 for x in range(5)}
## {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

## 交换键值
original = {'a': 1, 'b': 2, 'c': 3}
swapped = {v: k for k, v in original.items()}
## {1: 'a', 2: 'b', 3: 'c'}

## 条件过滤
filtered = {k: v for k, v in original.items() if v > 1}
## {'b': 2, 'c': 3}
```

##### 集合推导式

```python
## 基本语法
unique_squares = {x**2 for x in [-2, -1, 0, 1, 2]}
## {0, 1, 4}

## 从字符串提取唯一字符
unique_chars = {char.lower() for char in "Hello World" if char.isalpha()}
## {'h', 'e', 'l', 'o', 'w', 'r', 'd'}
```

### 14. 常用内置函数汇总

```python
## 类型转换
int(), float(), str(), bool()
list(), tuple(), set(), dict()
bytes(), bytearray()
complex()

## 数学运算
abs()      ## 绝对值
round()    ## 四舍五入
min(), max()  ## 最小最大值
sum()      ## 求和
pow()      ## 幂运算
divmod()   ## 商和余数

## 序列操作
len()      ## 长度
sorted()   ## 排序
reversed() ## 反转
enumerate()  ## 枚举
zip()      ## 打包
filter()   ## 过滤
map()      ## 映射
all()      ## 全部为真
any()      ## 任意为真

## 对象操作
id()       ## 对象ID
type()     ## 类型
isinstance()  ## 实例判断
issubclass()  ## 子类判断
hasattr(), getattr(), setattr(), delattr()
dir()      ## 属性列表
vars()     ## 属性字典
help()     ## 帮助信息

## 迭代器
iter()     ## 创建迭代器
next()     ## 下一个元素
range()    ## 范围

## 输入输出
input()    ## 输入
print()    ## 输出
open()     ## 打开文件

## 其他
eval()     ## 执行表达式
exec()     ## 执行语句
compile()  ## 编译代码
globals()  ## 全局变量
locals()   ## 局部变量
__import__()  ## 动态导入
```

## Python 条件语句与循环详解

### 条件语句

#### 1. if-elif-else 语句

Python 中的 if-elif-else 语句用于根据条件执行不同的代码块。

##### 基本语法

```python
## 基本 if 语句
age = 18
if age >= 18:
    print("成年人")

## if-else 语句
score = 75
if score >= 60:
    print("及格")
else:
    print("不及格")

## if-elif-else 语句
grade = 85
if grade >= 90:
    print("优秀")
elif grade >= 80:
    print("良好")
elif grade >= 60:
    print("及格")
else:
    print("不及格")
```

##### 条件表达式（三元运算符）

```python
## 简化的条件表达式
age = 20
status = "成年" if age >= 18 else "未成年"
print(status)  ## 输出: 成年

## 等价于
if age >= 18:
    status = "成年"
else:
    status = "未成年"
```

##### 嵌套条件语句

```python
num = 15

if num > 0:
    if num % 2 == 0:
        print(f"{num} 是正偶数")
    else:
        print(f"{num} 是正奇数")
elif num < 0:
    print(f"{num} 是负数")
else:
    print("数字是零")
```

##### 多条件判断

```python
## 使用 and, or, not
username = "admin"
password = "123456"

if username == "admin" and password == "123456":
    print("登录成功")

## 使用 in 操作符
fruits = ['apple', 'banana', 'orange']
if 'apple' in fruits:
    print("找到苹果")

## 链式比较
x = 5
if 1 < x < 10:
    print("x 在 1 和 10 之间")
```

#### 2. match-case 语句（Python 3.10+）

match-case 是 Python 3.10 引入的模式匹配语句，类似于其他语言的 switch-case。

##### 基本用法

```python
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:  ## 默认情况，相当于 else
            return "Unknown status"

print(http_status(200))  ## OK
print(http_status(999))  ## Unknown status
```

##### 模式匹配进阶

```python
## 匹配多值
def get_day_type(day):
    match day:
        case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
            return "工作日"
        case "Saturday" | "Sunday":
            return "周末"
        case _:
            return "无效日期"

## 匹配元组
def process_point(point: (int, int)) -> str:
    match point:
        case (0, 0):
            return "原点"
        case (0, y):
            return f"Y轴上的点，y={y}"
        case (x, 0):
            return f"X轴上的点，x={x}"
        case (x, y):
            return f"坐标点 ({x}, {y})"

print(process_point((0, 0)))    ## 原点
print(process_point((5, 0)))    ## X轴上的点，x=5

## 匹配对象
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def describe_point(point: Point) -> str:
    match point:
        case Point(x=0, y=0):
            return "原点"
        case Point(x=0, y=y):
            return f"在Y轴上: y={y}"
        case Point(x=x, y=0):
            return f"在X轴上: x={x}"
        case Point():
            return f"点 ({point.x}, {point.y})"

## 匹配带条件的模式（guard）
def classify_number(num):
    match num:
        case n if n < 0:
            return "负数"
        case 0:
            return "零"
        case n if n > 0 and n < 10:
            return "一位正数"
        case n if n >= 10:
            return "多位正数"
```

### 循环语句

#### 1. for 循环

for 循环用于遍历序列（列表、元组、字符串等）或其他可迭代对象。

##### 基本用法

```python
## 遍历列表
fruits = ['apple', 'banana', 'orange']
for fruit in fruits:
    print(fruit)

## 遍历字符串
for char in "Python":
    print(char)

## 使用 range()
for i in range(5):  ## 0 到 4
    print(i)

for i in range(2, 8):  ## 2 到 7
    print(i)

for i in range(1, 10, 2):  ## 1, 3, 5, 7, 9（步长为2）
    print(i)
```

##### enumerate() 函数

```python
## 获取索引和值
fruits = ['apple', 'banana', 'orange']
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

## 指定起始索引
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
```

##### zip() 函数

```python
## 同时遍历多个序列
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['New York', 'London', 'Paris']

for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} years old and lives in {city}")
```

##### 字典遍历

```python
person = {'name': 'Alice', 'age': 30, 'city': 'New York'}

## 遍历键
for key in person:
    print(key)

## 遍历值
for value in person.values():
    print(value)

## 遍历键值对
for key, value in person.items():
    print(f"{key}: {value}")
```

##### 列表推导式

```python
## 基本列表推导式
squares = [x**2 for x in range(10)]
print(squares)  ## [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

## 带条件的列表推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  ## [0, 4, 16, 36, 64]

## 嵌套列表推导式
matrix = [[i*j for j in range(3)] for i in range(3)]
print(matrix)  ## [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

#### 2. while 循环

while 循环在条件为真时重复执行代码块。

##### 基本用法

```python
## 基本 while 循环
count = 0
while count < 5:
    print(count)
    count += 1

## 无限循环（需要 break 退出）
while True:
    user_input = input("输入 'quit' 退出: ")
    if user_input == 'quit':
        break
    print(f"你输入了: {user_input}")
```

##### while-else 语句

```python
count = 0
while count < 3:
    print(count)
    count += 1
else:
    print("循环正常结束")  ## 当循环正常结束时执行

## 如果使用 break，else 不会执行
count = 0
while count < 5:
    if count == 3:
        break
    print(count)
    count += 1
else:
    print("这不会被打印")  ## 因为使用了 break
```

#### break 语句

```python
## 在 for 循环中使用 break
for i in range(10):
    if i == 5:
        break
    print(i)  ## 输出 0, 1, 2, 3, 4

## 在 while 循环中使用 break
count = 0
while True:
    if count >= 5:
        break
    print(count)
    count += 1
```

#### continue 语句

```python
## 跳过偶数
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  ## 输出 1, 3, 5, 7, 9

## 在 while 循环中使用 continue
count = 0
while count < 10:
    count += 1
    if count % 2 == 0:
        continue
    print(count)  ## 输出 1, 3, 5, 7, 9
```

#### pass 语句

```python
## 作为占位符
for i in range(5):
    if i == 3:
        pass  ## 暂时不做任何事
    else:
        print(i)

## 在定义空函数或类时使用
def placeholder_function():
    pass

class EmptyClass:
    pass
```

## Python 语言函数详解

### 函数基础

#### 1. 函数定义与调用

Python 中使用`def`关键字定义函数（增加类型注解示例）：

```python
def greet(name: str) -> str:
    """这是一个文档字符串"""
    return f"Hello, {name}!"

## 调用函数
message: str = greet("Alice")
print(message)  ## 输出: Hello, Alice!
```

#### 2. 参数类型

Python 函数支持多种参数类型，并可加类型注解：

**位置参数**：最基本的参数形式，按顺序传递。

```python
def add(x: int, y: int) -> int:
    return x + y

result: int = add(3, 5)  ## x=3, y=5
```

**默认参数**：可以设置默认值，调用时可选。

```python
def power(base: int, exponent: int = 2) -> int:
    return base ** exponent

print(power(3))     ## 9 (使用默认值2)
print(power(3, 3))  ## 27
```

**可变参数**：接受任意数量的参数。

```python
from typing import Any

## *args: 接收任意数量的位置参数
def sum_all(*args: int) -> int:
    return sum(args)

print(sum_all(1, 2, 3, 4))  ## 10

## **kwargs: 接收任意数量的关键字参数
def print_info(**kwargs: Any) -> None:
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Bob", age=25, city="Beijing")
```

**仅限关键字参数**：必须使用关键字传递的参数。

```python
def greet(name: str, *, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

## greet("Alice", "Hi")  ## 错误！
greet("Alice", greeting="Hi")  ## 正确
```

#### 3. 返回值

函数可以返回单个值或多个值：

```python
## 返回单个值
def square(x: int) -> int:
    return x ** 2

## 返回多个值（实际返回元组）
from typing import Sequence, Tuple

def get_min_max(numbers: Sequence[int]) -> Tuple[int, int]:
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([1, 5, 3, 9, 2])
print(minimum, maximum)  ## 1 9

## 没有return语句时返回None
def print_message(msg: str) -> None:
    print(msg)
    ## 隐式返回 None
```

#### 4. 作用域与闭包

Python 使用 LEGB 规则查找变量：Local → Enclosing → Global → Built-in

```python
global_var: str = "全局变量"

def outer_function(x: int) -> callable:
    ## Enclosing scope
    def inner_function(y: int) -> int:
        ## Local scope
        return x + y  ## x来自外层函数
    return inner_function

## 闭包示例
closure = outer_function(10)
print(closure(5))  ## 15

## global和nonlocal关键字
count: int = 0
def increment() -> None:
    global count
    count += 1

def make_counter() -> callable:
    count: int = 0
    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter
```

#### 5. 高级特性

**装饰器**：用于修改函数行为的特殊函数。

```python
from typing import Callable, Any
import time

def timer(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 用时: {time.time() - start:.4f}秒")
        return result
    return wrapper

@timer
def slow_function() -> str:
    time.sleep(1)
    return "完成"

slow_function()  ## 输出执行时间
```

**lambda 函数**：创建简单的匿名函数。

```python
## 基本语法
square = lambda x: x ** 2
print(square(5))  ## 25

## 常用于高阶函数
numbers: list[int] = [1, 2, 3, 4, 5]
squared: list[int] = list(map(lambda x: x ** 2, numbers))
evens: list[int] = list(filter(lambda x: x % 2 == 0, numbers))
```

**生成器函数**：使用 yield 返回迭代器。

```python
from typing import Iterator

def fibonacci(n: int) -> Iterator[int]:
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

## 使用生成器
for num in fibonacci(10):
    print(num, end=" ")  ## 0 1 1 2 3 5 8 13 21 34
```

#### 6. 类型提示

Python 3.5+支持类型注解（强烈推荐）：

```python
from typing import List, Optional, Union, Dict

def process_items(
    items: List[str],
    max_count: int = 10,
    prefix: Optional[str] = None
) -> List[str]:
    """处理字符串列表"""
    result = items[:max_count]
    if prefix:
        result = [prefix + item for item in result]
    return result

## 更复杂的类型
def parse_data(data: Union[str, bytes]) -> Dict[str, str]:
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    return {"content": data}
```

#### 7. 函数式编程工具

Python 提供了一些函数式编程的内置函数：

```python
from functools import reduce, partial
from operator import add, mul
from typing import Callable

## map: 对序列每个元素应用函数
numbers: list[int] = [1, 2, 3, 4]
squared: list[int] = list(map(lambda x: x**2, numbers))

## filter: 筛选满足条件的元素
evens: list[int] = list(filter(lambda x: x % 2 == 0, numbers))

## reduce: 累积操作
total: int = reduce(add, numbers)  ## 1+2+3+4 = 10
product: int = reduce(mul, numbers)  ## 1*2*3*4 = 24

## partial: 部分应用函数
def multiply(x: int, y: int) -> int:
    return x * y

double: Callable[[int], int] = partial(multiply, 2)
print(double(5))  ## 10
```

#### 8. 异步函数

Python 3.5+支持异步编程：

```python
import asyncio

async def fetch_data(url: str) -> str:
    print(f"开始获取 {url}")
    await asyncio.sleep(1)  ## 模拟网络请求
    return f"数据来自 {url}"

async def main() -> list[str]:
    ## 并发执行多个异步任务
    tasks = [
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3")
    ]
    results = await asyncio.gather(*tasks)
    return results

## 运行异步函数
## asyncio.run(main())
```

# I/O

## 文件打开与关闭

### 基本语法

```python
# 打开文件
file = open('filename.txt', 'mode', encoding='utf-8')

# 使用文件
# ...

# 关闭文件
file.close()
```

### 推荐的上下文管理器方式

```python
with open('filename.txt', 'mode', encoding='utf-8') as file:
    # 文件操作
    pass
# 文件自动关闭
```

## 文件打开模式

| 模式   | 说明                 | 文件不存在时           |
| ------ | -------------------- | ---------------------- |
| `'r'`  | 只读模式（默认）     | 抛出异常               |
| `'w'`  | 写入模式，覆盖原内容 | 创建新文件             |
| `'a'`  | 追加模式             | 创建新文件             |
| `'x'`  | 独占创建模式         | 创建新文件，存在则异常 |
| `'r+'` | 读写模式             | 抛出异常               |
| `'w+'` | 读写模式，覆盖原内容 | 创建新文件             |
| `'a+'` | 读写模式，追加写入   | 创建新文件             |

### 二进制模式

在任何模式后加 `'b'`，如 `'rb'`、`'wb'`、`'ab'` 等

## 文件读取操作

### 读取全部内容

```python
# 读取整个文件为字符串
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 读取所有行到列表
with open('file.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(lines)
```

### 逐行读取

```python
# 方法1：使用readline()
with open('file.txt', 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line:
            break
        print(line.strip())  # strip()去除换行符

# 方法2：直接遍历文件对象（推荐）
with open('file.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())

# 方法3：enumerate获取行号
with open('file.txt', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        print(f"第{i}行: {line.strip()}")
```

### 分块读取大文件

```python
def read_chunks(file_path, chunk_size=1024):
    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# 使用
for chunk in read_chunks('large_file.txt'):
    process_chunk(chunk)
```

## 文件写入操作

### 基本写入

```python
# 写入字符串
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, World!\n')
    f.write('第二行内容\n')

# 写入多行
lines = ['第一行\n', '第二行\n', '第三行\n']
with open('output.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)
```

### 追加写入

```python
with open('output.txt', 'a', encoding='utf-8') as f:
    f.write('追加的内容\n')
```

### 格式化写入

```python
data = [
    {'name': '张三', 'age': 25},
    {'name': '李四', 'age': 30}
]

with open('data.txt', 'w', encoding='utf-8') as f:
    for item in data:
        f.write(f"姓名: {item['name']}, 年龄: {item['age']}\n")
```

## 二进制文件操作

### 读取二进制文件

```python
# 读取图片文件
with open('image.jpg', 'rb') as f:
    data = f.read()
    print(f"文件大小: {len(data)} 字节")

# 复制二进制文件
def copy_file(src, dest):
    with open(src, 'rb') as src_file:
        with open(dest, 'wb') as dest_file:
            # 分块复制
            while True:
                chunk = src_file.read(1024)
                if not chunk:
                    break
                dest_file.write(chunk)
```

## 文件指针操作

```python
with open('file.txt', 'r+', encoding='utf-8') as f:
    # 获取当前位置
    pos = f.tell()
    print(f"当前位置: {pos}")

    # 移动到文件开头
    f.seek(0)

    # 移动到文件末尾
    f.seek(0, 2)  # 2表示从文件末尾开始

    # 移动到指定位置
    f.seek(10)    # 移动到第10个字节
```

## 文件和目录操作

### os 模块

```python
import os

# 检查文件/目录是否存在
if os.path.exists('file.txt'):
    print("文件存在")

if os.path.isfile('file.txt'):
    print("是文件")

if os.path.isdir('directory'):
    print("是目录")

# 获取文件信息
stat_info = os.stat('file.txt')
print(f"文件大小: {stat_info.st_size} 字节")
print(f"修改时间: {stat_info.st_mtime}")

# 删除文件
os.remove('file.txt')

# 重命名文件
os.rename('old_name.txt', 'new_name.txt')
```

### pathlib 模块（Python 3.4+，推荐）

#### 基本属性

```python
p = Path('/home/user/documents/file.txt')

print(p.name)           # 'file.txt' - 文件名
print(p.stem)           # 'file' - 文件名（不含扩展名）
print(p.suffix)         # '.txt' - 文件扩展名
print(p.suffixes)       # ['.txt'] - 所有扩展名列表
print(p.parent)         # Path('/home/user/documents') - 父目录
print(p.root)           # '/' - 根部分

# 多重扩展名示例
p2 = Path('archive.tar.gz')
print(p2.stem)          # 'archive'
print(p2.suffix)        # '.gz'
print(p2.suffixes)      # ['.tar', '.gz']
```

#### 路径拼接

```python
# 使用 / 操作符（推荐）
base = Path('/home/user')
file_path = base / 'documents' / 'file.txt'
print(file_path)        # /home/user/documents/file.txt

# 使用 joinpath 方法
path = Path('/home').joinpath('user', 'documents', 'file.txt')
print(path)             # /home/user/documents/file.txt

# 动态拼接
parts = ['documents', 'photos', 'vacation']
photo_dir = Path.home()
for part in parts:
    photo_dir = photo_dir / part
print(photo_dir)        # /home/username/documents/photos/vacation
```

#### 路径修改

```python
p = Path('documents/report.txt')

# 修改文件名
new_name = p.with_name('summary.txt')
print(new_name)         # documents/summary.txt

# 修改扩展名
new_ext = p.with_suffix('.pdf')
print(new_ext)          # documents/report.pdf

backup = p.with_suffix(p.suffix + '.bak')
print(backup)           # documents/report.txt.bak

# 修改stem（文件名不含扩展名）
new_stem = p.with_stem('final_report')
print(new_stem)         # documents/final_report.txt
```

#### 存在性检查

```python
p = Path('file.txt')

print(p.exists())       # 文件或目录是否存在
print(p.is_file())      # 是否为文件
print(p.is_dir())       # 是否为目录
print(p.is_symlink())   # 是否为符号链接
print(p.is_socket())    # 是否为socket
print(p.is_fifo())      # 是否为FIFO
print(p.is_block_device())  # 是否为块设备
print(p.is_char_device())   # 是否为字符设备
```

#### 文件属性

```python
p = Path('file.txt')

if p.exists():
    stat = p.stat()
    print(f"文件大小: {stat.st_size} 字节")
    print(f"修改时间: {stat.st_mtime}")
    print(f"创建时间: {stat.st_ctime}")

    # 文件权限
    print(f"权限: {oct(stat.st_mode)}", stat.st_mode & 0o400)

    # 所有者信息
    print(f"用户ID: {stat.st_uid}")
    print(f"组ID: {stat.st_gid}")
```

#### 列举目录内容

```python
directory = Path('.')

# 列举直接子项
for item in directory.iterdir():
    if item.is_file():
        print(f"文件: {item}")
    elif item.is_dir():
        print(f"目录: {item}")

# 使用glob模式匹配
for txt_file in directory.glob('*.txt'): # 匹配所有.txt文件
    print(txt_file)

for item in directory.glob('**/test_*.py'):
    print(item)
```

#### 创建目录

```python
# 创建单个目录
new_dir = Path('new_directory')
new_dir.mkdir()

# 创建多层目录
deep_dir = Path('level1/level2/level3')
deep_dir.mkdir(parents=True)

# 如果存在则不报错
safe_dir = Path('maybe_exists')
safe_dir.mkdir(exist_ok=True)

# 设置权限（Unix/Linux）
secure_dir = Path('secure')
secure_dir.mkdir(mode=0o700)  # 只有所有者可读写执行
```

#### 读取文件

```python
p = Path('data.txt')

# 读取文本文件
if p.exists():
    # 读取整个文件
    content = p.read_text(encoding='utf-8')
    print(content)

    # 读取为行列表
    lines = content.splitlines()

# 读取二进制文件
binary_data = p.read_bytes()

# 安全读取（处理异常）
def safe_read_text(file_path):
    try:
        return file_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在")
        return None
    except UnicodeDecodeError:
        print(f"文件 {file_path} 编码错误")
        return None
```

#### 写入文件

```python
p = Path('output.txt')

# 写入文本
content = "Hello, World!\n第二行内容"
p.write_text(content, encoding='utf-8')

# 写入二进制数据
binary_data = b'\x00\x01\x02\x03'
p.write_bytes(binary_data)

# 追加内容（需要使用传统方法）
with p.open('a', encoding='utf-8') as f:
    f.write('追加的内容\n')
```

### 文件操作

```python
source = Path('source.txt')
target = Path('target.txt')

# 重命名/移动文件
source.rename(target)

# 删除文件
if target.exists():
    target.unlink()

# 删除目录（仅空目录）
if target.exists() and target.is_dir():
    target.rmdir()

# 删除目录树（需要shutil）
import shutil

if target.exists():
    shutil.rmtree('directory_tree')
```

# Network

## HTTP 客户端库

### 1. requests 库（最常用）

**安装**: `pip install requests`

**常用方法**:

```python
import requests

# GET 请求
response = requests.get('https://api.github.com/users/octocat')
response = requests.get('https://httpbin.org/get', params={'key': 'value'})

# POST 请求
data = {'username': 'test', 'password': '123'}
response = requests.post('https://httpbin.org/post', data=data)
response = requests.post('https://httpbin.org/post', json=data)  # JSON格式

# 其他HTTP方法
response = requests.put('https://httpbin.org/put', data=data)
response = requests.delete('https://httpbin.org/delete', params={'key': 'value'})
response = requests.patch('https://httpbin.org/patch', data=data)

# 设置请求头
headers = {'User-Agent': 'My App 1.0'}
response = requests.get('https://httpbin.org/headers', headers=headers)


# 会话管理
session = requests.Session()
session.headers.update({'Authorization': 'Bearer token'})
response = session.get('https://api.example.com/data')

# 发送 Cookie
cookies = {'session_id': '12345', 'user': 'admin'}
response = requests.get('https://httpbin.org/cookies', cookies=cookies)

# 文件上传
files = {'file': open('report.txt', 'rb')}
response = requests.post('https://httpbin.org/post', files=files)

# 超时设置
response = requests.get('https://httpbin.org/delay/5', timeout=3)

# 响应处理
 # 状态码检查
if response.status == 200:
    print("请求成功")
response.ok
response.raise_for_status()  # 如果状态码不是 2xx 会抛出异常

# 获取不同格式的响应数据
print(response.text)         # 文本
print(response.json())       # JSON


# 流式读取大文件
print(response.content)       # 字节

for chunk in response.iter_content(chunk_size=8192):
    # 处理每个chunk
    pass

 # 响应头信息
print(f"Headers: {dict(response.headers)}")

# Cookie信息
print(f"Cookies: {response.cookies}")
```

### 2. aiohttp（纯异步）

**安装**: `pip install aiohttp`

```python
import aiohttp
import asyncio

async def fetch():
    async with aiohttp.ClientSession() as session:
        # GET 请求
        params = {'param1': 'value1', 'param2': 'value2'}
        async with session.get('https://httpbin.org/get', params=params) as response:
            text = await response.text()
            json_data = await response.json()

            print(f"Status: {response.status}")
            print(f"Headers: {response.headers}")

        # POST 请求
        data = {'key': 'value'}
        async with session.post('https://httpbin.org/post', data=data) as response:
            result = await response.json()

        # JSON POST
        async with session.post('https://httpbin.org/post', json=data) as response:
            result = await response.json()

        # 其他HTTP方法
        async with session.put('https://httpbin.org/put', data=data) as response:
            pass
        async with session.delete('https://httpbin.org/delete') as response:
            pass
        async with session.patch('https://httpbin.org/patch', data=data) as response:
            pass
        async with session.head('https://httpbin.org/get') as response:
            pass

        # 自定义请求头
        headers = {'Custom-Header': 'custom-value'}
        async with session.get('https://httpbin.org/headers', headers=headers) as response:
            data = await response.json()

        # Cookie处理
        cookies = {'session_id': '12345'}
        async with session.get('https://httpbin.org/cookies', cookies=cookies) as response:
            data = await response.json()

        # 响应处理
        async with session.get('https://httpbin.org/json') as response:
            # 状态码检查
            if response.status == 200:
                print("请求成功")

            # 获取不同格式的响应数据
            text_data = await response.text()          # 文本
            json_data = await response.json()          # JSON


            # 流式读取大文件
            bytes_data = await response.content.read()         # 字节

            async for chunk in response.content.iter_chunked(1024):
                # 处理每个chunk
                pass

            # 响应头信息
            print(f"Headers: {dict(response.headers)}")

            # Cookie信息
            print(f"Cookies: {response.cookies}")

data = asyncio.run(fetch())
```

## HTTP 服务端实现

### 1. Flask（轻量级 Web 框架）

**安装**: `pip install flask`

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify([{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    # 处理数据
    return jsonify({'message': 'User created', 'data': data}), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({'id': user_id, 'name': f'User {user_id}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### 2. FastAPI（现代高性能框架）

**安装**: `pip install fastapi uvicorn`

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}

@app.post("/users/")
async def create_user(user: User):
    return {"message": "User created", "user": user}

# 运行: uvicorn main:app --reload
```

### 3. http.server（标准库简单服务器）

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {'message': 'Hello from Python server'}
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {'received': post_data.decode()}
        self.wfile.write(json.dumps(response).encode())

server = HTTPServer(('localhost', 8000), MyHandler)
server.serve_forever()
```

### 4. Django REST Framework

**安装**: `pip install django djangorestframework`

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserListView(APIView):
    def get(self, request):
        users = [{'id': 1, 'name': 'Alice'}]
        return Response(users)

    def post(self, request):
        data = request.data
        # 处理数据
        return Response(data, status=status.HTTP_201_CREATED)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/users/', views.UserListView.as_view()),
]
```

# Process

## 1. 核心概念对比

### 1.1 基本特性对比

| 特性         | asyncio        | threading             | multiprocessing    |
| ------------ | -------------- | --------------------- | ------------------ |
| **执行模型** | 单线程事件循环 | 多线程（受 GIL 限制） | 多进程（真正并行） |
| **内存共享** | 共享内存       | 共享内存              | 独立内存空间       |
| **通信方式** | 直接变量访问   | 直接变量访问          | 需要 IPC 机制      |
| **适用场景** | I/O 密集型     | I/O 密集型            | CPU 密集型         |
| **启动开销** | 最小           | 中等                  | 最大               |
| **调试难度** | 中等           | 困难                  | 最困难             |

### 1.2 GIL 影响

```python
# GIL对并发的影响
import threading
import time
import multiprocessing

# 受GIL影响的CPU密集型任务
def cpu_task():
    result = 0
    for i in range(10000000):
        result += i * i
    return result

# 多线程版本（受GIL限制）
def threading_version():
    start = time.time()
    threads = []
    for _ in range(4):
        t = threading.Thread(target=cpu_task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"多线程耗时: {time.time() - start:.2f}秒")

# 多进程版本（真正并行）
def multiprocessing_version():
    start = time.time()
    with multiprocessing.Pool(4) as pool:
        pool.map(cpu_task, range(4))

    print(f"多进程耗时: {time.time() - start:.2f}秒")
```

## 2. asyncio 常用 API 详解

### 2.1 直接使用协程 vs create_task

```python
async def fetch_data(url: str) -> str:
    await asyncio.sleep(0.1)

    return f"数据来自 {url}"

async def example():
    # 方式1: 直接使用协程对象
    task = fetch_data(f"url{i}")
    # 问题：协程对象不会自动执行！
    # 需要显式 await 或调度

    result = await task

    # 方式2: create_task (Python 3.7+, 推荐)
    task = asyncio.create_task(fetch_data(f"url{i}"))
    # ✅ 协程立即被调度执行
    # ✅ 返回 Task 对象
    # ✅ 可以取消、检查状态

    # - task.done()    # 是否已完成
    # - task.cancel()  # 取消任务
    # - task.result()  # 获取结果（未完成会抛异常）
    # - task.exception() # 获取异常(如果有)
    # - task.cancelled() # 是否被取消

    result = await task

async def exec():
    # 1. 创建事件循环
    loop = asyncio.get_event_loop()

    # 2. 创建协程对象（不会立即执行）
    coro = fetch_data("url")

    # 3. 创建任务（调度到事件循环）
    task = asyncio.create_task(coro)  # 或 loop.create_task(coro)

    # 4. 事件循环驱动执行
    # - 遇到 await → 挂起，等待 Future 完成
    # - Future 完成 → 回调唤醒协程继续执行
    # - 直到协程返回或抛出异常

    # 5. 获取结果
    result = await task
```

### 2. asyncio vs TypeScript 异步对比详解

#### 1. 基础异步函数定义

```python
async def fetch_data(url: str) -> str:
    await asyncio.sleep(1)  # 模拟异步操作
    return f"数据来自 {url}"
```

```typescript
async function fetchData(url: string): Promise<string> {
  await new Promise((resolve) => setTimeout(resolve, 1000)); // 模拟异步操作
  return `数据来自 ${url}`;
}
```

#### 2. 执行异步函数

```python
async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())  # 运行异步函数
```

```typescript
async function main(): Promise<void> {
  const result = await fetchData("https://api.example.com");
  console.log(result);
}

main(); // 直接调用，浏览器/Node.js 会自动处理
```

#### 3. 并发执行多个异步任务

> **是否需要 `asyncio.create_task`？**
>
> - 如果只用 `asyncio.gather()` 或直接 await 协程，大多数场景下可以直接用协程对象（如 `[fetch_data(x) for x in ...]`），不需要手动包装成 Task；`gather` 会自动帮你包装成 Task。
> - 但**如需手动取消、跟踪状态或任务要提前启动**，则建议用 `asyncio.create_task`。
> - `asyncio.as_completed` 推荐传 Task（用 create_task），否则只有执行到 await 时协程才真的开始执行，易踩坑。
> - 只有 `asyncio.wait` 明确要求 Future/Task 类型，不能用普通协程对象。

##### Promise.all

- Python

  ```python
  # 等待所有完成（无需 create_task）
  async def python_gather():
      tasks = [fetch_data(f"url{i}") for i in range(3)]  # 直接协程对象即可
      results = await asyncio.gather(*tasks)  # gather 自动包装为 Task
      return results
  ```

- TypeScript

  ```typescript
  // 等待所有完成
  async function tsPromiseAll(): Promise<string[]> {
    const promises = [fetchData("url1"), fetchData("url2"), fetchData("url3")];

    return await Promise.all(promises);
  }

  // 兼容性 Polyfill（简化版，结果只要有失败就 reject，与 Promise.all 语义等价）
  function promiseAllPolyfill<T>(promises: Promise<T>[]): Promise<T[]> {
    return new Promise((resolve, reject) => {
      let results: T[] = [];
      let count = 0;
      promises.forEach((p, i) => {
        p.then((res) => {
          results[i] = res;
          count++;
          if (count === promises.length) resolve(results);
        }).catch((err) => reject(err));
      });
    });
  }
  ```

##### Promise.allSettled

> 与 `asyncio.gather` 的区别：gather 等待全部完成才返回所有结果（结果顺序和输入顺序一致），而 as_completed 是**边结束边处理，顺序与任务实际完成先后有关**。

- Python

  ```python
    # 捕获所有异常，返回所有任务的结果或异常(顺序与输入一致，通常不需 create_task)
    async def python_all_settled():
        tasks = [fetch_data(f"url{i}") for i in range(2)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # results 可能包含返回值或 Exception 实例
        for result in results:
            if isinstance(result, Exception):
                print(f"失败: {result}")
            else:
                print(f"完成: {result}")

    # 按完成顺序依次处理多个任务（建议传 Task/确保立即调度）
    async def python_as_completed():
        tasks = [asyncio.create_task(fetch_data(f"url{i}")) for i in range(5)]

        for task in asyncio.as_completed(tasks):   # 推荐传 Task
            try:
                result = await task
                print(f"完成: {result}")
            except Exception as e:
                print(f"失败: {e}")
  ```

- TypeScript

  ```typescript
  // 包括失败（allSettled）
  async function tsPromiseAllSettled(): Promise<string[]> {
    const promises = [fetchData("url1"), fetchData("url2")];
    const results = await Promise.allSettled(promises);

    return results.map((r) => (r.status === "fulfilled" ? r.value : r.reason));
  }

  // 兼容性 Polyfill
  function promiseAllSettledPolyfill<T>(
    promises: Promise<T>[]
  ): Promise<{ status: string; value?: T; reason?: any }[]> {
    return Promise.all(
      promises.map((p) =>
        p.then(
          (value) => ({ status: "fulfilled", value }),
          (reason) => ({ status: "rejected", reason })
        )
      )
    );
  }
  ```

##### Promise.race

- Python

  ```python
  # 第一个完成（无论成功/失败），与 Promise.race 语义相同
  async def python_race():
      # 一定要传 Future/Task（如 create_task），不能直接传协程对象
      tasks = [asyncio.create_task(fetch_data(f"url{i}")) for i in range(3)]
      done, pending = await asyncio.wait(
          tasks,
          return_when=asyncio.FIRST_COMPLETED
      )
      first_done = next(iter(done))

      try:
          return await first_done
      finally:
          for task in pending:
              task.cancel()
  ```

- TypeScript

  ```typescript
  // 第一个完成
  async function tsPromiseRace(): Promise<string> {
    const promises = [fetchData("url1"), fetchData("url2"), fetchData("url3")];

    return await Promise.race(promises);
  }

  // 兼容性 Polyfill（无论成功或失败，第一个 settle 就返回）
  function promiseRacePolyfill<T>(promises: Promise<T>[]): Promise<T> {
    return new Promise((resolve, reject) => {
      promises.forEach((p) => {
        p.then(resolve, reject);
      });
    });
  }
  ```

##### Promise.any

- Python

  ```python
  # 更严格实现：等待所有，返回第一个成功，否则抛异常
  async def python_any_strict():
      tasks = [asyncio.create_task(fetch_data(f"url{i}")) for i in range(3)]
      excs = []
      for task in asyncio.as_completed(tasks):
          try:
              result = await task
              for other in tasks:
                  if other != task and not other.done():
                      other.cancel()
              return result
          except Exception as e:
              excs.append(e)

      raise Exception("All Promises rejected", excs)
  ```

- TypeScript

  ```typescript
  // 返回第一个成功，全部失败则抛异常
  async function tsPromiseAny(): Promise<string> {
    const promises = [fetchData("url1"), fetchData("url2"), fetchData("url3")];

    return await Promise.any(promises); // ES2021
  }

  // 若需兼容性 polyfill:
  async function tsPromiseAnyPolyfill<T>(promises: Promise<T>[]): Promise<T> {
    return new Promise((resolve, reject) => {
      let rejections: any[] = [];
      let count = 0;
      promises.forEach((p) =>
        p.then(resolve, (err) => {
          rejections.push(err);
          count++;
          if (count === promises.length) reject(rejections);
        })
      );
    });
  }
  ```

#### 4. 超时控制

```python
# Python
async def python_timeout():
    try:
        result = await asyncio.wait_for(
            fetch_data("slow-url"),
            timeout=2.0  # 2秒超时
        )
        return result
    except asyncio.TimeoutError:
        return "请求超时"
```

```typescript
// TypeScript
async function tsTimeout(): Promise<string> {
  const timeoutPromise = new Promise<string>((_, reject) => {
    setTimeout(() => reject(new Error("超时")), 2000);
  });

  try {
    return await Promise.race([fetchData("slow-url"), timeoutPromise]);
  } catch (error) {
    return "请求超时";
  }
}
```

#### 5. 异常处理

```python
async def python_exception_handling():
    async def may_fail(url: str) -> str:
        if "error" in url:
            raise ValueError(f"错误: {url}")
        return f"成功: {url}"

    try:
        await asyncio.gather(
            may_fail("url1"),
            may_fail("error-url")
        )
    except ValueError as e:
        print(f"捕获异常: {e}")
```

```typescript
async function tsExceptionHandling(): Promise<string[]> {
  async function mayFail(url: string): Promise<string> {
    if (url.includes("error")) {
      throw new Error(`错误: ${url}`);
    }
    return `成功: ${url}`;
  }

  try {
    return await Promise.all([mayFail("url1"), mayFail("error-url")]);
  } catch (error) {
    console.log(`捕获异常: ${error}`);
    return [];
  }
}
```

#### 6. 并发限制（信号量）

```python
# Python - Semaphore
async def python_semaphore():
    semaphore = asyncio.Semaphore(2)  # 最多2个并发

    async def limited_fetch(url: str):
        async with semaphore:
            return await fetch_data(url)

    tasks = [limited_fetch(f"url{i}") for i in range(10)]
    results = await asyncio.gather(*tasks)
```

```typescript
// TypeScript - 手动实现 Semaphore
class Semaphore {
  private permits: number;
  private waiters: Array<() => void> = [];

  constructor(permits: number) {
    this.permits = permits;
  }

  async acquire(): Promise<void> {
    if (this.permits > 0) {
      this.permits--;
      return;
    }
    return new Promise((resolve) => {
      this.waiters.push(resolve);
    });
  }

  release(): void {
    if (this.waiters.length > 0) {
      const resolve = this.waiters.shift();
      resolve();
    } else {
      this.permits++;
    }
  }
}

async function tsSemaphore(): Promise<string[]> {
  const semaphore = new Semaphore(2);

  async function limitedFetch(url: string): Promise<string> {
    await semaphore.acquire();
    try {
      return await fetchData(url);
    } finally {
      semaphore.release();
    }
  }

  const urls = Array.from({ length: 10 }, (_, i) => `url${i}`);
  return Promise.all(urls.map((url) => limitedFetch(url)));
}
```

#### 7. 任务取消

```python
# Python
async def python_task_cancel():
    async def long_task():
        try:
            await asyncio.sleep(10)
            return "完成"
        except asyncio.CancelledError:
            print("任务被取消")
            raise

    task = asyncio.create_task(long_task())
    await asyncio.sleep(1)  # 等待1秒
    task.cancel()  # 取消任务

    try:
        await task
    except asyncio.CancelledError:
        print("任务已取消")
```

```typescript
async function tsTaskCancel(): Promise<void> {
  const controller = new AbortController();

  async function longTask(signal: AbortSignal): Promise<string> {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => resolve("完成"), 10000);

      signal.addEventListener("abort", () => {
        clearTimeout(timeout);
        reject(new Error("任务被取消"));
      });
    });
  }

  const task = longTask(controller.signal);

  setTimeout(() => {
    controller.abort(); // 取消任务
  }, 1000);

  try {
    await task;
  } catch (error) {
    console.log("任务已取消");
  }
}
```

## 3. threading 常用 API 详解

### 3.1 基础线程 API

```python
import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. 基础线程操作
def basic_threading():
    """基础线程操作"""

    def worker(name, delay):
        print(f"线程 {name} 开始")
        time.sleep(delay)
        print(f"线程 {name} 完成")
        return f"结果 {name}"

    # 创建线程
    thread = threading.Thread(target=worker, args=("A", 1))

    # 检查状态
    print(f"线程是否存活: {thread.is_alive()}")

    # 启动线程
    thread.start()
    print(f"线程启动后是否存活: {thread.is_alive()}")

    # 等待完成
    thread.join()
    print(f"线程启动后是否存活: {thread.is_alive()}")

# 2. 同步
def sync_primitives():
    """同步"""

    # 锁
    lock = threading.Lock()
    counter = 0

    def increment():
        nonlocal counter
        for _ in range(100000):
            with lock:
                counter += 1

    # 信号量
    semaphore = threading.Semaphore(2)

    def limited_worker(worker_id):
        with semaphore:
            print(f"工作者 {worker_id} 获取资源")
            time.sleep(1)
            print(f"工作者 {worker_id} 释放资源")

    # 事件
    event = threading.Event()

    def waiter(name):
        print(f"{name} 等待事件...")
        event.wait()
        print(f"{name} 收到事件!")

    def setter():
        time.sleep(2)
        print("设置事件")
        event.set()

    # 条件变量
    condition = threading.Condition()
    shared_data = []

    def producer():
        with condition:
            time.sleep(1)
            shared_data.append("数据")
            print("生产者生产数据")
            condition.notify_all()

    def consumer():
        with condition:
            while not shared_data:
                condition.wait()
            data = shared_data.pop(0)
            print(f"消费者消费: {data}")

# 3. 线程池
def thread_pool_example():
    """线程池示例"""

    def fetch_url(url):
        import requests
        try:
            response = requests.get(url, timeout=5)
            return f"{url}: {response.status_code}"
        except Exception as e:
            return f"{url}: 错误 - {e}"

    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/3"
    ]

    # 使用ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 方式1: submit
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}

        for future in as_completed(future_to_url):
            result = future.result()
            print(result)

        # 方式2: map
        results = list(executor.map(fetch_url, urls))
        for result in results:
            print(result)

# 4. 线程间通信
def thread_communication():
    """线程间通信"""

    # 使用Queue进行通信
    message_queue = queue.Queue()

    def producer():
        for i in range(5):
            message = f"消息 {i}"
            message_queue.put(message)
            print(f"生产: {message}")
            time.sleep(0.5)
        message_queue.put(None)  # 结束信号

    def consumer():
        while True:
            message = message_queue.get()
            if message is None:
                break
            print(f"消费: {message}")
            message_queue.task_done()
            time.sleep(0.3)

    # 启动生产者和消费者
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
```

## 4. multiprocessing 常用 API 详解

### 4.1 基础进程 API

```python
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor

# 1. 基础进程操作
def basic_multiprocessing():
    """基础进程操作"""

    def worker(name, delay):
        print(f"进程 {name} (PID: {os.getpid()}) 开始")
        time.sleep(delay)
        print(f"进程 {name} 完成")
        return f"结果 {name}"

    if __name__ == '__main__':
        # 创建进程
        process = multiprocessing.Process(
            target=worker,
            args=("Worker1", 2),
            name="WorkerProcess"
        )

        # 检查状态
        print(f"进程是否存活: {process.is_alive()}")

        # 启动进程
        process.start()
        print(f"进程启动后是否存活: {process.is_alive()}")

        # 等待完成
        process.join()
        print(f"进程启动后是否存活: {process.is_alive()}")


# 2. 同步
def process_synchronization():
    """进程同步"""

    # 锁
    def worker(lock, shared_value):
        with lock:
            shared_value.value += 1
            print(f"进程 {os.getpid()}: 值 = {shared_value.value}")
            time.sleep(0.1)

    if __name__ == '__main__':
        # 锁
        lock = multiprocessing.Lock()
        shared_value = multiprocessing.Value('i', 0)

        processes = []
        for i in range(5):
            p = multiprocessing.Process(
                target=worker,
                args=(lock, shared_value)
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        print(f"最终值: {shared_value.value}")

    # 事件
    def waiter(event, name):
        print(f"{name} 等待事件...")
        event.wait()
        print(f"{name} 收到事件!")

    def setter(event):
        time.sleep(2)
        print("设置事件")
        event.set()

    if __name__ == '__main__':
        # 事件
        event = multiprocessing.Event()

        # 创建等待进程
        waiters = []
        for i in range(3):
            p = multiprocessing.Process(target=waiter, args=(event, f"进程{i}"))
            waiters.append(p)
            p.start()

        # 创建设置事件的进程
        setter_process = multiprocessing.Process(target=setter, args=(event,))
        setter_process.start()

        # 等待所有进程完成
        for p in waiters:
            p.join()
        setter_process.join()

    # 条件变量
    def waiter(condition, name):
        print(f"{name} 等待事件...")
        condition.wait()
        print(f"{name} 收到事件!")

    def setter(condition):
        time.sleep(2)
        print("设置事件")
        condition.set()

    if __name__ == '__main__':
        # 事件
        condition = multiprocessing.Condition()

        # 创建等待进程
        waiters = []
        for i in range(3):
            p = multiprocessing.Process(target=waiter, args=(condition, f"进程{i}"))
            waiters.append(p)
            p.start()

        # 创建设置事件的进程
        setter_process = multiprocessing.Process(target=setter, args=(condition,))
        setter_process.start()

        # 等待所有进程完成
        for p in waiters:
            p.join()
        setter_process.join()

# 3. 进程池
def process_pool_example():
    """进程池示例"""

    def cpu_intensive_task(n):
        """CPU密集型任务"""
        result = 0
        for i in range(n):
            result += i * i
        return result

    def io_intensive_task(url):
        """I/O密集型任务"""
        import requests
        try:
            response = requests.get(url, timeout=5)
            return f"{url}: {response.status_code}"
        except Exception as e:
            return f"{url}: 错误 - {e}"

    if __name__ == '__main__':
        # CPU密集型任务 - 使用进程池
        numbers = [1000000, 2000000, 3000000, 4000000]

        with ProcessPoolExecutor(max_workers=4) as executor:
            # 使用map
            results = list(executor.map(cpu_intensive_task, numbers))

            # 使用submit
            futures = [executor.submit(cpu_intensive_task, n) for n in numbers]
            results2 = [f.result() for f in futures]

        print("CPU密集型任务结果:", results)

        # I/O密集型任务 - 也可以使用进程池
        urls = [
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2",
            "https://httpbin.org/delay/3"
        ]

        with ProcessPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(io_intensive_task, urls))

        print("I/O密集型任务结果:", results)


# 4. 进程间通信
def process_communication():
    """进程间通信"""

    # Queue - 队列通信（适合复杂的多进程通信）
    def queue_communication():
        def producer(queue):
            for i in range(5):
                item = f"item_{i}"
                queue.put(item)
                print(f"生产: {item}")
                time.sleep(0.5)

        def consumer(queue):
            while True:
                try:
                    item = queue.get(timeout=2)
                    print(f"消费: {item}")
                    time.sleep(0.3)
                except:
                    break

        if __name__ == '__main__':
            queue = multiprocessing.Queue()

            p1 = multiprocessing.Process(target=producer, args=(queue,))
            p2 = multiprocessing.Process(target=consumer, args=(queue,))

            p1.start()
            p2.start()

            p1.join()
            p2.join()

    # Pipe - 管道通信（适合简单的点对点通信）
    def pipe_communication():
        def sender(conn):
            conn.send("Hello from sender!")
            conn.send([1, 2, 3, 4, 5])
            conn.close()

        def receiver(conn):
            while True:
                try:
                    data = conn.recv()
                    print(f"接收: {data}")
                except EOFError:
                    break
            conn.close()

        if __name__ == '__main__':
            parent_conn, child_conn = multiprocessing.Pipe()

            p1 = multiprocessing.Process(target=sender, args=(child_conn,))
            p2 = multiprocessing.Process(target=receiver, args=(parent_conn,))

            p1.start()
            p2.start()

            p1.join()
            p2.join()

    # 共享内存
    def shared_memory():
        def worker(shared_list, shared_value, lock):
            with lock:
                shared_list[0] += 1
                shared_value.value += 1
                print(f"进程 {os.getpid()}: "
                      f"list={shared_list[0]}, value={shared_value.value}")

        if __name__ == '__main__':
            # 使用Manager创建共享对象
            manager = multiprocessing.Manager()
            shared_list = manager.list([0])
            shared_value = multiprocessing.Value('i', 0)
            lock = multiprocessing.Lock()

            processes = []
            for i in range(4):
                p = multiprocessing.Process(
                    target=worker,
                    args=(shared_list, shared_value, lock)
                )
                processes.append(p)
                p.start()

            for p in processes:
                p.join()

```

## 5. 性能对比与选择指南

### 5.1 性能测试代码

```python
import time
import asyncio
import aiohttp
import requests
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def performance_comparison():
    """性能对比测试"""

    # 测试URL
    urls = ["https://httpbin.org/delay/1"] * 10

    # 1. 同步方式
    def sync_requests():
        start = time.time()
        for url in urls:
            response = requests.get(url)
        return time.time() - start

    # 2. 异步方式
    async def async_requests():
        start = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [session.get(url) for url in urls]
            await asyncio.gather(*tasks)
        return time.time() - start

    # 3. 多线程方式
    def thread_requests():
        def fetch_url(url):
            return requests.get(url)

        start = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(fetch_url, urls))
        return time.time() - start

    # 4. 多进程方式
    def process_requests():
        def fetch_url(url):
            return requests.get(url)

        start = time.time()
        with ProcessPoolExecutor(max_workers=10) as executor:
            list(executor.map(fetch_url, urls))
        return time.time() - start

    # 运行测试
    print("性能测试结果:")
    print(f"同步方式: {sync_requests():.2f}秒")
    print(f"异步方式: {asyncio.run(async_requests()):.2f}秒")
    print(f"多线程: {thread_requests():.2f}秒")
    print(f"多进程: {process_requests():.2f}秒")

# CPU密集型任务对比
def cpu_intensive_comparison():
    """CPU密集型任务对比"""

    def cpu_task(n):
        result = 0
        for i in range(n):
            result += i * i
        return result

    numbers = [1000000] * 4

    # 同步方式
    start = time.time()
    for n in numbers:
        cpu_task(n)
    sync_time = time.time() - start

    # 多线程方式（受GIL限制）
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_task, numbers))
    thread_time = time.time() - start

    # 多进程方式
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_task, numbers))
    process_time = time.time() - start

    print("CPU密集型任务对比:")
    print(f"同步方式: {sync_time:.2f}秒")
    print(f"多线程: {thread_time:.2f}秒")
    print(f"多进程: {process_time:.2f}秒")
```

### 5.2 选择指南

| 场景           | 推荐方案                  | 原因                                 |
| -------------- | ------------------------- | ------------------------------------ |
| **网络请求**   | asyncio                   | 单线程事件循环，资源占用少，性能最佳 |
| **文件 I/O**   | asyncio                   | 异步 I/O，不阻塞事件循环             |
| **数据库操作** | asyncio + 异步驱动        | 高并发，低资源占用                   |
| **CPU 密集型** | multiprocessing           | 绕过 GIL，真正并行                   |
| **混合任务**   | asyncio + multiprocessing | 异步处理 I/O，进程处理 CPU           |
| **简单并发**   | threading                 | 代码简单，适合少量并发               |
| **大量并发**   | asyncio                   | 资源占用少，性能好                   |

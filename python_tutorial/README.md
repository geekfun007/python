# Python 详解与实战（带类型提示）

这是一个全面的 Python 教程，涵盖从基础语法到高级特性的完整内容，所有示例代码都包含类型提示（Type Hints）。

## 📚 目录

| 文件 | 内容 | 关键概念 |
|------|------|----------|
| `01_syntax_and_type_hints.py` | 基础语法与类型提示 | 变量注解、函数注解、泛型、Protocol |
| `02_basic_data_types.py` | 基本数据类型 | int、float、bool、str、bytes、Decimal |
| `03_collections.py` | 集合类型 | tuple、list、set、dict、deque、heap |
| `04_class_and_oop.py` | 类与面向对象 | 类、继承、魔术方法、dataclass、ABC |
| `05_enum_datetime_regex.py` | 枚举、日期、正则 | Enum、datetime、re |
| `06_error_handling_iterator.py` | 错误处理与迭代器 | 异常处理、自定义异常、迭代器、生成器 |
| `07_logic_and_functions.py` | 逻辑与函数 | 条件、循环、函数、闭包、装饰器、函数式编程 |
| `08_concurrency_async.py` | 并发与异步 | 多进程、多线程、asyncio、concurrent.futures |
| `09_io_operations.py` | IO 操作 | 文件读写、pathlib、JSON、CSV、压缩 |
| `10_http_client.py` | HTTP 客户端 | urllib、requests、httpx、aiohttp |
| `11_fastapi_server.py` | HTTP 服务器与 FastAPI | FastAPI、路由、依赖注入、中间件 |

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd python_tutorial
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 或使用 conda
conda create -n python-tutorial python=3.11
conda activate python-tutorial
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行示例

```bash
# 运行任意教程文件
python 01_syntax_and_type_hints.py
python 02_basic_data_types.py
# ...

# 启动 FastAPI 服务器
uvicorn 11_fastapi_server:app --reload
# 访问 http://localhost:8000/docs 查看 API 文档
```

## 📖 详细内容

### 1. 基础语法与类型提示 (`01_syntax_and_type_hints.py`)

```python
from typing import Optional, Union, TypeVar, Generic

# 变量类型注解
name: str = "Python"
age: int = 30
maybe_value: Optional[str] = None

# 函数类型注解
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 泛型
T = TypeVar('T')

class Stack(Generic[T]):
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...
```

### 2. 数据类型 (`02_basic_data_types.py`, `03_collections.py`)

```python
# 基本类型
x: int = 42
pi: float = 3.14
active: bool = True
text: str = "Hello"

# 集合类型
numbers: list[int] = [1, 2, 3]
point: tuple[int, int] = (10, 20)
unique: set[str] = {"a", "b", "c"}
data: dict[str, int] = {"a": 1, "b": 2}
```

### 3. 类与面向对象 (`04_class_and_oop.py`)

```python
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Point:
    x: float
    y: float

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
```

### 4. 异步编程 (`08_concurrency_async.py`)

```python
import asyncio

async def fetch_data(url: str) -> dict:
    await asyncio.sleep(1)  # 模拟 IO
    return {"url": url, "data": "..."}

async def main() -> None:
    # 并发执行多个任务
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )
    print(results)

asyncio.run(main())
```

### 5. FastAPI 服务器 (`11_fastapi_server.py`)

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/{item_id}")
async def get_item(item_id: int) -> dict:
    return {"item_id": item_id}
```

## 🔧 类型检查

使用 mypy 进行静态类型检查：

```bash
# 检查单个文件
mypy 01_syntax_and_type_hints.py

# 检查整个项目
mypy .

# 严格模式
mypy --strict 01_syntax_and_type_hints.py
```

## 📝 代码风格

项目遵循以下规范：
- **类型提示**: 所有函数和方法都有完整的类型注解
- **文档字符串**: 使用 Google 风格的 docstring
- **PEP 8**: 遵循 Python 代码风格指南
- **Black**: 代码格式化

```bash
# 格式化代码
black .

# 检查代码风格
ruff check .
```

## 🎯 学习路径

### 初学者
1. `01_syntax_and_type_hints.py` - 了解基本语法
2. `02_basic_data_types.py` - 掌握基本数据类型
3. `03_collections.py` - 学习集合操作
4. `07_logic_and_functions.py` - 理解控制流和函数

### 进阶
1. `04_class_and_oop.py` - 面向对象编程
2. `05_enum_datetime_regex.py` - 常用工具类
3. `06_error_handling_iterator.py` - 异常和迭代器
4. `09_io_operations.py` - 文件操作

### 高级
1. `08_concurrency_async.py` - 并发和异步编程
2. `10_http_client.py` - HTTP 客户端
3. `11_fastapi_server.py` - Web 开发

## 📚 推荐资源

- [Python 官方文档](https://docs.python.org/3/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)
- [Real Python](https://realpython.com/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

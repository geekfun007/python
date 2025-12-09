# Python 高级教程

一个全面的 Python 高级编程教程，涵盖核心设计原则、重要注意事项和实战详解。

## 📚 教程结构

### 核心概念教程

1. **[01_decorators_advanced.py](01_decorators_advanced.py)** - 装饰器详解
   - 基础装饰器、带参数装饰器、类装饰器
   - 缓存、权限验证、重试、类型检查
   - 单例模式、装饰器叠加

2. **[02_metaclasses.py](02_metaclasses.py)** - 元类详解
   - 元类基础、type 与元类
   - 单例元类、属性验证元类
   - ORM 元类、插件注册元类

3. **[03_descriptors.py](03_descriptors.py)** - 描述符详解
   - 描述符协议、数据描述符 vs 非数据描述符
   - 类型检查、范围验证、延迟计算
   - 自定义 property、单位转换

4. **[04_context_managers.py](04_context_managers.py)** - 上下文管理器详解
   - 上下文管理器协议
   - 文件操作、数据库连接、锁管理
   - 异步上下文管理器

5. **[05_generators_iterators.py](05_generators_iterators.py)** - 生成器与迭代器详解
   - 迭代器协议、生成器函数
   - yield from、数据流水线
   - itertools 模块应用

6. **[06_async_programming.py](06_async_programming.py)** - 异步编程详解
   - async/await 语法、asyncio 事件循环
   - 并发控制、信号量、锁、队列
   - 异步 HTTP 请求

7. **[07_type_hints.py](07_type_hints.py)** - 类型提示详解
   - 基础类型提示、泛型类型
   - Protocol 协议类型、TypeVar
   - dataclass、函数重载

8. **[08_magic_methods.py](08_magic_methods.py)** - 魔法方法详解
   - 对象创建、字符串表示
   - 运算符重载、容器协议
   - 属性访问、可调用对象

### 实战项目

**[examples/](examples/)** 目录包含完整的实战项目:

1. **[01_cache_system.py](examples/01_cache_system.py)** - 高性能缓存系统
   - LRU 缓存、TTL 缓存
   - 线程安全、装饰器模式
   - 多级缓存

2. **[02_async_web_crawler.py](examples/02_async_web_crawler.py)** - 异步网页爬虫
   - 并发请求控制、请求限流
   - URL 去重、错误处理
   - 进度追踪

3. **[03_performance_monitor.py](examples/03_performance_monitor.py)** - 性能监控装饰器
   - 执行时间统计、内存监控
   - 调用次数追踪、性能报告

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 可选依赖: `aiohttp` (用于异步示例)

### 安装依赖

```bash
# 基础教程不需要额外依赖
python --version  # 确认 Python 3.8+

# 如需运行异步爬虫示例
pip install aiohttp
```

### 运行教程

每个文件都可以独立运行:

```bash
# 运行装饰器教程
python 01_decorators_advanced.py

# 运行元类教程
python 02_metaclasses.py

# 运行实战项目
python examples/01_cache_system.py
```

## 📖 学习路径

### 初级 → 中级

1. 先学习 **装饰器** (01) - Python 最常用的高级特性
2. 掌握 **生成器与迭代器** (05) - 理解惰性求值
3. 学习 **上下文管理器** (04) - 资源管理
4. 了解 **类型提示** (07) - 提高代码质量

### 中级 → 高级

5. 深入 **描述符** (03) - 理解 Python 属性系统
6. 研究 **元类** (02) - 框架设计基础
7. 掌握 **异步编程** (06) - 高并发处理
8. 全面学习 **魔法方法** (08) - Python 对象模型

### 实战应用

9. 实现 **缓存系统** - 综合应用装饰器、线程安全
10. 开发 **异步爬虫** - 应用异步编程技术
11. 构建 **性能监控** - 综合多种高级特性

## 💡 核心设计原则

### 1. 装饰器模式
- 在不修改原函数的情况下增强功能
- 使用 `@functools.wraps` 保留元信息
- 支持参数化和叠加使用

### 2. 元类设计
- 控制类的创建过程
- 实现单例、ORM、插件系统
- 谨慎使用，优先考虑装饰器和 `__init_subclass__`

### 3. 描述符协议
- 自定义属性访问逻辑
- 实现验证、延迟计算、类型检查
- 理解数据描述符优先级

### 4. 上下文管理
- 确保资源正确释放
- 使用 `with` 语句简化代码
- 支持异步上下文

### 5. 惰性求值
- 使用生成器处理大数据
- 内存高效的数据流处理
- 支持无限序列

## ⚠️ 重要注意事项

### 性能考虑

- 装饰器有函数调用开销
- 生成器比列表更节省内存
- 异步适合 I/O 密集型，不适合 CPU 密集型
- 使用 `__slots__` 减少内存占用

### 线程安全

- GIL 限制多线程性能
- 使用 `threading.Lock` 保护共享资源
- `queue.Queue` 是线程安全的
- 考虑使用 `multiprocessing`

### 代码质量

- 遵循 PEP 8 代码规范
- 编写文档字符串
- 添加类型提示
- 编写单元测试

### 常见陷阱

- 忘记使用 `@functools.wraps`
- 在 `__setattr__` 中造成无限递归
- 生成器只能遍历一次
- 元类过度使用导致代码难懂

## 🔧 工具推荐

### 代码质量

- **pylint** - 代码静态分析
- **mypy** - 类型检查
- **black** - 代码格式化
- **pytest** - 单元测试

### 性能分析

- **cProfile** - 性能分析
- **memory_profiler** - 内存分析
- **line_profiler** - 逐行分析

### 异步开发

- **aiohttp** - 异步 HTTP
- **asyncpg** - 异步 PostgreSQL
- **aioredis** - 异步 Redis

## 📚 参考资源

### 官方文档
- [Python 官方文档](https://docs.python.org/3/)
- [PEP 8 风格指南](https://pep8.org/)
- [PEP 484 类型提示](https://www.python.org/dev/peps/pep-0484/)

### 推荐书籍
- 《Fluent Python》 by Luciano Ramalho
- 《Effective Python》 by Brett Slatkin
- 《Python Cookbook》 by David Beazley

### 在线资源
- [Real Python](https://realpython.com/)
- [Python Weekly](https://www.pythonweekly.com/)

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

本项目采用 MIT 许可证。

---

**开始学习:** 从 `01_decorators_advanced.py` 开始你的 Python 高级编程之旅！ 🚀

**实战演练:** 尝试完成 `examples/` 目录下的实战项目！ 💪

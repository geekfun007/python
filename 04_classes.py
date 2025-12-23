"""
Python 类与面向对象编程详解
包含：类定义、继承、多态、封装、特殊方法等
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, ClassVar
import json


# ============================================
# 1. 类的基础
# ============================================

def class_basics():
    """类的基础定义和使用"""
    print("\n=== 类的基础 ===")
    
    # 定义一个简单的类
    class Person:
        """人类"""
        
        def __init__(self, name, age):
            """构造函数"""
            self.name = name
            self.age = age
        
        def greet(self):
            """问候方法"""
            return f"你好，我是{self.name}，今年{self.age}岁"
        
        def have_birthday(self):
            """过生日，年龄+1"""
            self.age += 1
    
    # 创建实例
    person1 = Person("Alice", 25)
    person2 = Person("Bob", 30)
    
    print(person1.greet())
    print(person2.greet())
    
    # 修改属性
    person1.have_birthday()
    print(f"{person1.name} 过完生日后: {person1.age}岁")
    
    # 访问属性
    print(f"\n访问属性:")
    print(f"person1.name = {person1.name}")
    print(f"person1.age = {person1.age}")


def class_attributes():
    """类属性与实例属性"""
    print("\n=== 类属性与实例属性 ===")
    
    class Dog:
        # 类属性（所有实例共享）
        species = "Canis familiaris"
        count = 0
        
        def __init__(self, name, age):
            # 实例属性（每个实例独有）
            self.name = name
            self.age = age
            Dog.count += 1  # 增加计数
        
        def description(self):
            return f"{self.name} 是 {self.age} 岁"
    
    dog1 = Dog("Buddy", 3)
    dog2 = Dog("Lucy", 5)
    
    print(f"物种: {Dog.species}")
    print(f"创建的狗数量: {Dog.count}")
    print(f"dog1: {dog1.description()}")
    print(f"dog2: {dog2.description()}")
    
    # 修改类属性
    Dog.species = "狗"
    print(f"\n修改后物种: {dog1.species}")  # 影响所有实例


def methods_types():
    """方法类型：实例方法、类方法、静态方法"""
    print("\n=== 方法类型 ===")
    
    class MyClass:
        class_var = "类变量"
        
        def __init__(self, value):
            self.instance_var = value
        
        # 实例方法（需要 self）
        def instance_method(self):
            return f"实例方法访问: {self.instance_var}"
        
        # 类方法（需要 cls）
        @classmethod
        def class_method(cls):
            return f"类方法访问: {cls.class_var}"
        
        # 静态方法（不需要 self 或 cls）
        @staticmethod
        def static_method(x, y):
            return f"静态方法计算: {x + y}"
        
        # 另一个类方法用例：替代构造函数
        @classmethod
        def from_string(cls, string):
            value = string.upper()
            return cls(value)
    
    obj = MyClass("实例值")
    
    # 调用不同类型的方法
    print(obj.instance_method())
    print(MyClass.class_method())
    print(MyClass.static_method(10, 20))
    
    # 使用替代构造函数
    obj2 = MyClass.from_string("hello")
    print(f"从字符串创建: {obj2.instance_var}")


# ============================================
# 2. 封装与私有属性
# ============================================

def encapsulation_demo():
    """封装示例"""
    print("\n=== 封装 ===")
    
    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner           # 公开属性
            self._balance = balance      # 受保护属性（约定）
            self.__pin = "1234"          # 私有属性（名称改写）
        
        # Getter
        def get_balance(self):
            return self._balance
        
        # Setter
        def deposit(self, amount):
            if amount > 0:
                self._balance += amount
                return True
            return False
        
        def withdraw(self, amount):
            if 0 < amount <= self._balance:
                self._balance -= amount
                return True
            return False
        
        # 私有方法
        def __verify_pin(self, pin):
            return pin == self.__pin
        
        def change_pin(self, old_pin, new_pin):
            if self.__verify_pin(old_pin):
                self.__pin = new_pin
                return True
            return False
    
    account = BankAccount("Alice", 1000)
    
    print(f"所有者: {account.owner}")
    print(f"余额: {account.get_balance()}")
    
    account.deposit(500)
    print(f"存款后: {account.get_balance()}")
    
    account.withdraw(200)
    print(f"取款后: {account.get_balance()}")
    
    # 尝试访问私有属性（不推荐）
    print(f"\n名称改写后的私有属性: {account._BankAccount__pin}")


def properties_demo():
    """属性装饰器 @property"""
    print("\n=== @property 装饰器 ===")
    
    class Temperature:
        def __init__(self, celsius=0):
            self._celsius = celsius
        
        @property
        def celsius(self):
            """获取摄氏温度"""
            return self._celsius
        
        @celsius.setter
        def celsius(self, value):
            """设置摄氏温度"""
            if value < -273.15:
                raise ValueError("温度不能低于绝对零度")
            self._celsius = value
        
        @property
        def fahrenheit(self):
            """获取华氏温度"""
            return self._celsius * 9/5 + 32
        
        @fahrenheit.setter
        def fahrenheit(self, value):
            """设置华氏温度"""
            self.celsius = (value - 32) * 5/9
    
    temp = Temperature(25)
    print(f"摄氏: {temp.celsius}°C")
    print(f"华氏: {temp.fahrenheit}°F")
    
    temp.celsius = 0
    print(f"\n设置为 0°C")
    print(f"摄氏: {temp.celsius}°C")
    print(f"华氏: {temp.fahrenheit}°F")
    
    temp.fahrenheit = 212
    print(f"\n设置为 212°F")
    print(f"摄氏: {temp.celsius}°C")
    print(f"华氏: {temp.fahrenheit}°F")


# ============================================
# 3. 继承
# ============================================

def inheritance_basics():
    """继承基础"""
    print("\n=== 继承基础 ===")
    
    # 父类
    class Animal:
        def __init__(self, name):
            self.name = name
        
        def speak(self):
            return "动物发出声音"
        
        def info(self):
            return f"我是 {self.name}"
    
    # 子类
    class Dog(Animal):
        def speak(self):
            """重写父类方法"""
            return "汪汪汪!"
        
        def fetch(self):
            """新增方法"""
            return f"{self.name} 正在捡球"
    
    class Cat(Animal):
        def speak(self):
            return "喵喵喵!"
        
        def scratch(self):
            return f"{self.name} 正在抓沙发"
    
    dog = Dog("旺财")
    cat = Cat("小咪")
    
    print(dog.info())
    print(dog.speak())
    print(dog.fetch())
    
    print(f"\n{cat.info()}")
    print(cat.speak())
    print(cat.scratch())


def super_usage():
    """super() 的使用"""
    print("\n=== super() 的使用 ===")
    
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        
        def introduce(self):
            return f"我是 {self.name}，{self.age}岁"
    
    class Student(Person):
        def __init__(self, name, age, student_id):
            super().__init__(name, age)  # 调用父类构造函数
            self.student_id = student_id
        
        def introduce(self):
            parent_intro = super().introduce()  # 调用父类方法
            return f"{parent_intro}，学号: {self.student_id}"
    
    class GraduateStudent(Student):
        def __init__(self, name, age, student_id, research_area):
            super().__init__(name, age, student_id)
            self.research_area = research_area
        
        def introduce(self):
            parent_intro = super().introduce()
            return f"{parent_intro}，研究方向: {self.research_area}"
    
    person = Person("张三", 30)
    student = Student("李四", 20, "2021001")
    grad = GraduateStudent("王五", 25, "2019001", "人工智能")
    
    print(person.introduce())
    print(student.introduce())
    print(grad.introduce())


def multiple_inheritance():
    """多重继承"""
    print("\n=== 多重继承 ===")
    
    class Flyer:
        def fly(self):
            return "我会飞"
    
    class Swimmer:
        def swim(self):
            return "我会游泳"
    
    class Duck(Flyer, Swimmer):
        def quack(self):
            return "嘎嘎嘎"
    
    duck = Duck()
    print(duck.fly())
    print(duck.swim())
    print(duck.quack())
    
    # 方法解析顺序 (MRO)
    print(f"\nDuck 的 MRO: {Duck.__mro__}")
    print(f"或使用: {Duck.mro()}")


# ============================================
# 4. 多态
# ============================================

def polymorphism_demo():
    """多态示例"""
    print("\n=== 多态 ===")
    
    class Shape:
        def area(self):
            pass
        
        def perimeter(self):
            pass
    
    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height
        
        def area(self):
            return self.width * self.height
        
        def perimeter(self):
            return 2 * (self.width + self.height)
    
    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius
        
        def area(self):
            import math
            return math.pi * self.radius ** 2
        
        def perimeter(self):
            import math
            return 2 * math.pi * self.radius
    
    # 多态：不同对象调用相同方法，表现不同行为
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Rectangle(2, 8),
    ]
    
    for i, shape in enumerate(shapes, 1):
        print(f"形状 {i}:")
        print(f"  面积: {shape.area():.2f}")
        print(f"  周长: {shape.perimeter():.2f}")


# ============================================
# 5. 抽象基类
# ============================================

def abstract_base_class():
    """抽象基类示例"""
    print("\n=== 抽象基类 ===")
    
    class Animal(ABC):
        """抽象基类"""
        
        def __init__(self, name):
            self.name = name
        
        @abstractmethod
        def speak(self):
            """抽象方法，子类必须实现"""
            pass
        
        @abstractmethod
        def move(self):
            """抽象方法"""
            pass
        
        def sleep(self):
            """具体方法"""
            return f"{self.name} 正在睡觉"
    
    class Dog(Animal):
        def speak(self):
            return f"{self.name}: 汪汪汪!"
        
        def move(self):
            return f"{self.name} 正在跑"
    
    class Bird(Animal):
        def speak(self):
            return f"{self.name}: 叽叽喳喳!"
        
        def move(self):
            return f"{self.name} 正在飞"
    
    # animal = Animal("测试")  # 错误！不能实例化抽象类
    
    dog = Dog("旺财")
    bird = Bird("小鸟")
    
    for animal in [dog, bird]:
        print(animal.speak())
        print(animal.move())
        print(animal.sleep())
        print()


# ============================================
# 6. 特殊方法（魔术方法）
# ============================================

def magic_methods():
    """特殊方法示例"""
    print("\n=== 特殊方法 ===")
    
    class Vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        
        def __repr__(self):
            """开发者友好的字符串表示"""
            return f"Vector({self.x}, {self.y})"
        
        def __str__(self):
            """用户友好的字符串表示"""
            return f"({self.x}, {self.y})"
        
        def __add__(self, other):
            """向量加法"""
            return Vector(self.x + other.x, self.y + other.y)
        
        def __sub__(self, other):
            """向量减法"""
            return Vector(self.x - other.x, self.y - other.y)
        
        def __mul__(self, scalar):
            """标量乘法"""
            return Vector(self.x * scalar, self.y * scalar)
        
        def __eq__(self, other):
            """相等比较"""
            return self.x == other.x and self.y == other.y
        
        def __abs__(self):
            """向量长度"""
            return (self.x ** 2 + self.y ** 2) ** 0.5
        
        def __len__(self):
            """长度（维度）"""
            return 2
        
        def __getitem__(self, index):
            """索引访问"""
            if index == 0:
                return self.x
            elif index == 1:
                return self.y
            else:
                raise IndexError("索引超出范围")
        
        def __bool__(self):
            """布尔值"""
            return self.x != 0 or self.y != 0
    
    v1 = Vector(2, 3)
    v2 = Vector(1, 4)
    
    print(f"v1 = {v1}")
    print(f"repr(v1) = {repr(v1)}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"v1 == v2: {v1 == v2}")
    print(f"abs(v1) = {abs(v1):.2f}")
    print(f"len(v1) = {len(v1)}")
    print(f"v1[0] = {v1[0]}, v1[1] = {v1[1]}")
    print(f"bool(v1) = {bool(v1)}")
    print(f"bool(Vector(0, 0)) = {bool(Vector(0, 0))}")


def context_manager():
    """上下文管理器"""
    print("\n=== 上下文管理器 ===")
    
    class FileManager:
        def __init__(self, filename, mode):
            self.filename = filename
            self.mode = mode
            self.file = None
        
        def __enter__(self):
            """进入上下文"""
            print(f"打开文件: {self.filename}")
            self.file = open(self.filename, self.mode)
            return self.file
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            """退出上下文"""
            if self.file:
                print(f"关闭文件: {self.filename}")
                self.file.close()
            # 返回 False 表示不抑制异常
            return False
    
    # 使用上下文管理器
    with FileManager("/tmp/test.txt", "w") as f:
        f.write("Hello, World!")
    
    print("文件已自动关闭")


# ============================================
# 7. 数据类 (dataclass)
# ============================================

def dataclass_demo():
    """数据类示例"""
    print("\n=== 数据类 (dataclass) ===")
    
    @dataclass
    class Point:
        """坐标点"""
        x: float
        y: float
        z: float = 0.0  # 默认值
    
    @dataclass
    class Person:
        """人员信息"""
        name: str
        age: int
        email: str = ""
        hobbies: List[str] = field(default_factory=list)
    
    @dataclass
    class Config:
        """配置类"""
        host: str = "localhost"
        port: int = 8080
        debug: bool = False
        # 类变量
        version: ClassVar[str] = "1.0.0"
    
    # 创建实例
    p1 = Point(1.0, 2.0)
    p2 = Point(1.0, 2.0, 3.0)
    
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p1 == p2: {p1 == p2}")
    
    person = Person(name="Alice", age=25)
    person.hobbies.append("reading")
    print(f"\n{person}")
    
    config = Config()
    print(f"\n{config}")
    print(f"版本: {Config.version}")


# ============================================
# 8. 类的高级特性
# ============================================

def advanced_features():
    """类的高级特性"""
    print("\n=== 类的高级特性 ===")
    
    # 1. __slots__ - 限制实例属性，节省内存
    class Point:
        __slots__ = ('x', 'y')
        
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    p = Point(1, 2)
    print(f"Point: ({p.x}, {p.y})")
    # p.z = 3  # 错误！不能添加新属性
    
    # 2. __call__ - 使实例可调用
    class Multiplier:
        def __init__(self, factor):
            self.factor = factor
        
        def __call__(self, x):
            return x * self.factor
    
    double = Multiplier(2)
    triple = Multiplier(3)
    
    print(f"\ndouble(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")
    
    # 3. 描述符
    class Validator:
        def __init__(self, min_value=None, max_value=None):
            self.min_value = min_value
            self.max_value = max_value
        
        def __set_name__(self, owner, name):
            self.name = name
        
        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            return obj.__dict__.get(self.name)
        
        def __set__(self, obj, value):
            if self.min_value is not None and value < self.min_value:
                raise ValueError(f"{self.name} 不能小于 {self.min_value}")
            if self.max_value is not None and value > self.max_value:
                raise ValueError(f"{self.name} 不能大于 {self.max_value}")
            obj.__dict__[self.name] = value
    
    class Person:
        age = Validator(min_value=0, max_value=150)
        
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
    person = Person("Alice", 25)
    print(f"\n{person.name}, {person.age}岁")
    
    try:
        person.age = 200
    except ValueError as e:
        print(f"错误: {e}")


# ============================================
# 9. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 购物车系统
    print("1. 购物车系统:")
    
    class Product:
        def __init__(self, name, price):
            self.name = name
            self.price = price
        
        def __repr__(self):
            return f"Product('{self.name}', ${self.price:.2f})"
    
    class CartItem:
        def __init__(self, product, quantity=1):
            self.product = product
            self.quantity = quantity
        
        def subtotal(self):
            return self.product.price * self.quantity
        
        def __repr__(self):
            return f"{self.product.name} x{self.quantity} = ${self.subtotal():.2f}"
    
    class ShoppingCart:
        def __init__(self):
            self.items = []
        
        def add_item(self, product, quantity=1):
            for item in self.items:
                if item.product.name == product.name:
                    item.quantity += quantity
                    return
            self.items.append(CartItem(product, quantity))
        
        def remove_item(self, product_name):
            self.items = [item for item in self.items 
                         if item.product.name != product_name]
        
        def total(self):
            return sum(item.subtotal() for item in self.items)
        
        def __str__(self):
            if not self.items:
                return "购物车是空的"
            result = "购物车内容:\n"
            for item in self.items:
                result += f"  {item}\n"
            result += f"总计: ${self.total():.2f}"
            return result
    
    cart = ShoppingCart()
    cart.add_item(Product("Apple", 1.50), 3)
    cart.add_item(Product("Banana", 0.80), 5)
    cart.add_item(Product("Apple", 1.50), 2)
    
    print(cart)
    
    # 2. 银行账户系统
    print("\n2. 银行账户系统:")
    
    class BankAccount:
        account_count = 0
        
        def __init__(self, owner, balance=0):
            self.owner = owner
            self._balance = balance
            self.transactions = []
            BankAccount.account_count += 1
            self.account_number = f"ACC{BankAccount.account_count:06d}"
        
        @property
        def balance(self):
            return self._balance
        
        def deposit(self, amount):
            if amount > 0:
                self._balance += amount
                self.transactions.append(f"+${amount:.2f}")
                return True
            return False
        
        def withdraw(self, amount):
            if 0 < amount <= self._balance:
                self._balance -= amount
                self.transactions.append(f"-${amount:.2f}")
                return True
            return False
        
        def transfer(self, other, amount):
            if self.withdraw(amount):
                other.deposit(amount)
                return True
            return False
        
        def __str__(self):
            return f"账户 {self.account_number} ({self.owner}): ${self._balance:.2f}"
    
    acc1 = BankAccount("Alice", 1000)
    acc2 = BankAccount("Bob", 500)
    
    print(acc1)
    print(acc2)
    
    acc1.deposit(200)
    acc1.withdraw(150)
    acc1.transfer(acc2, 300)
    
    print(f"\n转账后:")
    print(acc1)
    print(acc2)
    print(f"Alice 交易记录: {acc1.transactions}")


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 类与面向对象编程详解")
    print("=" * 60)
    
    class_basics()
    class_attributes()
    methods_types()
    
    encapsulation_demo()
    properties_demo()
    
    inheritance_basics()
    super_usage()
    multiple_inheritance()
    
    polymorphism_demo()
    abstract_base_class()
    
    magic_methods()
    context_manager()
    
    dataclass_demo()
    advanced_features()
    
    practical_examples()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Python 枚举类型 (Enum) 详解
包含：基本枚举、自动值、标志位枚举等
"""

from enum import Enum, IntEnum, Flag, IntFlag, auto, unique
from typing import List


# ============================================
# 1. 基本枚举
# ============================================

def basic_enum():
    """基本枚举使用"""
    print("\n=== 基本枚举 ===")
    
    # 定义枚举
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
    
    # 访问枚举成员
    print(f"Color.RED = {Color.RED}")
    print(f"Color.RED.name = {Color.RED.name}")
    print(f"Color.RED.value = {Color.RED.value}")
    
    # 通过值访问
    color = Color(1)
    print(f"\nColor(1) = {color}")
    
    # 通过名称访问
    color = Color['GREEN']
    print(f"Color['GREEN'] = {color}")
    
    # 比较
    print(f"\nColor.RED == Color.RED: {Color.RED == Color.RED}")
    print(f"Color.RED is Color.RED: {Color.RED is Color.RED}")
    print(f"Color.RED == 1: {Color.RED == 1}")  # False
    
    # 遍历枚举
    print("\n遍历枚举:")
    for color in Color:
        print(f"  {color.name} = {color.value}")


def enum_with_methods():
    """带方法的枚举"""
    print("\n=== 带方法的枚举 ===")
    
    class Planet(Enum):
        MERCURY = (3.303e+23, 2.4397e6)
        VENUS   = (4.869e+24, 6.0518e6)
        EARTH   = (5.976e+24, 6.37814e6)
        MARS    = (6.421e+23, 3.3972e6)
        
        def __init__(self, mass, radius):
            self.mass = mass       # kg
            self.radius = radius   # meters
        
        @property
        def surface_gravity(self):
            """计算表面重力"""
            G = 6.67430e-11  # 万有引力常数
            return G * self.mass / (self.radius ** 2)
    
    earth = Planet.EARTH
    print(f"地球:")
    print(f"  质量: {earth.mass:.3e} kg")
    print(f"  半径: {earth.radius:.3e} m")
    print(f"  表面重力: {earth.surface_gravity:.2f} m/s²")
    
    print("\n所有行星的表面重力:")
    for planet in Planet:
        print(f"  {planet.name}: {planet.surface_gravity:.2f} m/s²")


# ============================================
# 2. 自动值 (auto)
# ============================================

def auto_values():
    """自动赋值"""
    print("\n=== 自动赋值 ===")
    
    class Status(Enum):
        PENDING = auto()    # 1
        APPROVED = auto()   # 2
        REJECTED = auto()   # 3
    
    print("Status 枚举:")
    for status in Status:
        print(f"  {status.name} = {status.value}")
    
    # 自定义 auto() 行为
    class AutoName(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name.lower()
    
    class Language(AutoName):
        PYTHON = auto()     # 'python'
        JAVA = auto()       # 'java'
        CPP = auto()        # 'cpp'
    
    print("\nLanguage 枚举（自定义auto）:")
    for lang in Language:
        print(f"  {lang.name} = {lang.value}")


# ============================================
# 3. 唯一性约束 (@unique)
# ============================================

def unique_constraint():
    """唯一性约束"""
    print("\n=== 唯一性约束 ===")
    
    # 不使用 @unique - 允许别名
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
        CRIMSON = 1  # 别名，指向 RED
    
    print("允许别名:")
    print(f"  Color.RED: {Color.RED}")
    print(f"  Color.CRIMSON: {Color.CRIMSON}")
    print(f"  Color.RED is Color.CRIMSON: {Color.RED is Color.CRIMSON}")
    
    # 使用 @unique - 不允许别名
    try:
        @unique
        class UniqueColor(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3
            # CRIMSON = 1  # 这会引发 ValueError
    except ValueError as e:
        print(f"\n使用 @unique 时不允许别名: {e}")
    
    @unique
    class UniqueColor(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
    
    print("\n@unique 枚举:")
    for color in UniqueColor:
        print(f"  {color.name} = {color.value}")


# ============================================
# 4. IntEnum - 整数枚举
# ============================================

def int_enum_demo():
    """整数枚举"""
    print("\n=== IntEnum ===")
    
    class Priority(IntEnum):
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4
    
    # IntEnum 可以与整数比较
    print(f"Priority.HIGH = {Priority.HIGH}")
    print(f"Priority.HIGH == 3: {Priority.HIGH == 3}")  # True
    print(f"Priority.HIGH > Priority.LOW: {Priority.HIGH > Priority.LOW}")  # True
    
    # 可以进行数学运算
    print(f"Priority.HIGH + 1 = {Priority.HIGH + 1}")
    
    # 可以作为列表索引
    items = ['a', 'b', 'c', 'd', 'e']
    print(f"items[Priority.HIGH] = {items[Priority.HIGH]}")


# ============================================
# 5. Flag 和 IntFlag - 位标志
# ============================================

def flag_demo():
    """位标志枚举"""
    print("\n=== Flag 和 IntFlag ===")
    
    class Permission(Flag):
        READ = auto()      # 1
        WRITE = auto()     # 2
        EXECUTE = auto()   # 4
        DELETE = auto()    # 8
    
    # 组合标志
    rw = Permission.READ | Permission.WRITE
    print(f"READ | WRITE = {rw}")
    print(f"值: {rw.value}")
    
    # 检查标志
    print(f"\nREAD in rw: {Permission.READ in rw}")
    print(f"EXECUTE in rw: {Permission.EXECUTE in rw}")
    
    # 所有权限
    all_perms = Permission.READ | Permission.WRITE | Permission.EXECUTE | Permission.DELETE
    print(f"\n所有权限: {all_perms}")
    print(f"值: {all_perms.value}")
    
    # IntFlag 示例
    class FileMode(IntFlag):
        R = 4  # 读
        W = 2  # 写
        X = 1  # 执行
    
    mode = FileMode.R | FileMode.W
    print(f"\nFileMode.R | FileMode.W = {mode}")
    print(f"值: {mode.value}")  # 6
    print(f"等于整数 6: {mode == 6}")  # True


# ============================================
# 6. 枚举的高级用法
# ============================================

def advanced_enum():
    """枚举的高级用法"""
    print("\n=== 枚举的高级用法 ===")
    
    # 1. 枚举作为字典键
    class Fruit(Enum):
        APPLE = 1
        BANANA = 2
        ORANGE = 3
    
    prices = {
        Fruit.APPLE: 1.20,
        Fruit.BANANA: 0.80,
        Fruit.ORANGE: 1.50
    }
    
    print("水果价格:")
    for fruit, price in prices.items():
        print(f"  {fruit.name}: ${price:.2f}")
    
    # 2. 枚举继承
    class ExtendedColor(Enum):
        # 不能继承有成员的枚举
        # 但可以创建基类
        pass
    
    # 3. 函数式 API 创建枚举
    Animal = Enum('Animal', ['DOG', 'CAT', 'BIRD'])
    
    print("\n使用函数式 API 创建的枚举:")
    for animal in Animal:
        print(f"  {animal.name} = {animal.value}")
    
    # 指定起始值
    Size = Enum('Size', ['SMALL', 'MEDIUM', 'LARGE'], start=0)
    print("\nSize 枚举（从0开始）:")
    for size in Size:
        print(f"  {size.name} = {size.value}")
    
    # 4. 从值列表创建
    Status = Enum('Status', ['PENDING', 'APPROVED', 'REJECTED'])
    print("\nStatus 枚举:")
    for status in Status:
        print(f"  {status.name} = {status.value}")


# ============================================
# 7. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. HTTP 状态码
    print("1. HTTP 状态码:")
    
    class HTTPStatus(IntEnum):
        # 2xx 成功
        OK = 200
        CREATED = 201
        NO_CONTENT = 204
        
        # 3xx 重定向
        MOVED_PERMANENTLY = 301
        FOUND = 302
        
        # 4xx 客户端错误
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        FORBIDDEN = 403
        NOT_FOUND = 404
        
        # 5xx 服务器错误
        INTERNAL_SERVER_ERROR = 500
        BAD_GATEWAY = 502
        SERVICE_UNAVAILABLE = 503
        
        def is_success(self):
            return 200 <= self.value < 300
        
        def is_redirect(self):
            return 300 <= self.value < 400
        
        def is_client_error(self):
            return 400 <= self.value < 500
        
        def is_server_error(self):
            return 500 <= self.value < 600
    
    status = HTTPStatus.OK
    print(f"状态: {status.name} ({status.value})")
    print(f"是否成功: {status.is_success()}")
    
    status = HTTPStatus.NOT_FOUND
    print(f"\n状态: {status.name} ({status.value})")
    print(f"是否客户端错误: {status.is_client_error()}")
    
    # 2. 订单状态机
    print("\n2. 订单状态机:")
    
    class OrderStatus(Enum):
        PENDING = "待处理"
        PAID = "已支付"
        SHIPPED = "已发货"
        DELIVERED = "已送达"
        CANCELLED = "已取消"
        
        def can_transition_to(self, new_status):
            """检查是否可以转换到新状态"""
            transitions = {
                OrderStatus.PENDING: [OrderStatus.PAID, OrderStatus.CANCELLED],
                OrderStatus.PAID: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
                OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
                OrderStatus.DELIVERED: [],
                OrderStatus.CANCELLED: []
            }
            return new_status in transitions.get(self, [])
    
    class Order:
        def __init__(self, order_id):
            self.order_id = order_id
            self.status = OrderStatus.PENDING
        
        def change_status(self, new_status):
            if self.status.can_transition_to(new_status):
                print(f"订单 {self.order_id}: {self.status.value} -> {new_status.value}")
                self.status = new_status
                return True
            else:
                print(f"订单 {self.order_id}: 不能从 {self.status.value} 转换到 {new_status.value}")
                return False
    
    order = Order("ORD001")
    order.change_status(OrderStatus.PAID)
    order.change_status(OrderStatus.SHIPPED)
    order.change_status(OrderStatus.DELIVERED)
    order.change_status(OrderStatus.CANCELLED)  # 失败
    
    # 3. 游戏方向
    print("\n3. 游戏方向:")
    
    class Direction(Enum):
        NORTH = (0, 1)
        SOUTH = (0, -1)
        EAST = (1, 0)
        WEST = (-1, 0)
        
        def __init__(self, dx, dy):
            self.dx = dx
            self.dy = dy
        
        def move(self, x, y):
            """从当前位置移动"""
            return (x + self.dx, y + self.dy)
        
        def opposite(self):
            """返回相反方向"""
            opposites = {
                Direction.NORTH: Direction.SOUTH,
                Direction.SOUTH: Direction.NORTH,
                Direction.EAST: Direction.WEST,
                Direction.WEST: Direction.EAST
            }
            return opposites[self]
    
    x, y = 5, 5
    print(f"起始位置: ({x}, {y})")
    
    for direction in [Direction.NORTH, Direction.EAST, Direction.SOUTH]:
        x, y = direction.move(x, y)
        print(f"向 {direction.name} 移动到: ({x}, {y})")
    
    print(f"NORTH 的相反方向: {Direction.NORTH.opposite().name}")
    
    # 4. 日志级别
    print("\n4. 日志级别:")
    
    class LogLevel(IntEnum):
        DEBUG = 10
        INFO = 20
        WARNING = 30
        ERROR = 40
        CRITICAL = 50
    
    class Logger:
        def __init__(self, min_level=LogLevel.INFO):
            self.min_level = min_level
        
        def log(self, level, message):
            if level >= self.min_level:
                print(f"[{level.name}] {message}")
    
    logger = Logger(LogLevel.WARNING)
    logger.log(LogLevel.DEBUG, "调试信息")      # 不显示
    logger.log(LogLevel.INFO, "普通信息")       # 不显示
    logger.log(LogLevel.WARNING, "警告信息")    # 显示
    logger.log(LogLevel.ERROR, "错误信息")      # 显示
    
    # 5. 文件权限
    print("\n5. 文件权限:")
    
    class Permission(IntFlag):
        NONE = 0
        EXECUTE = 1
        WRITE = 2
        READ = 4
        
        # 组合权限
        RW = READ | WRITE
        RX = READ | EXECUTE
        RWX = READ | WRITE | EXECUTE
    
    def check_permission(user_perm, required_perm):
        """检查用户是否有所需权限"""
        return (user_perm & required_perm) == required_perm
    
    user_perm = Permission.READ | Permission.WRITE
    print(f"用户权限: {user_perm}")
    
    print(f"可以读取: {check_permission(user_perm, Permission.READ)}")
    print(f"可以写入: {check_permission(user_perm, Permission.WRITE)}")
    print(f"可以执行: {check_permission(user_perm, Permission.EXECUTE)}")
    print(f"可以读写: {check_permission(user_perm, Permission.RW)}")


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 枚举类型 (Enum) 详解")
    print("=" * 60)
    
    basic_enum()
    enum_with_methods()
    auto_values()
    unique_constraint()
    int_enum_demo()
    flag_demo()
    advanced_enum()
    practical_examples()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

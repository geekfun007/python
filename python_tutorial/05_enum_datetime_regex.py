"""
Python Enum、DateTime、正则表达式详解 (with Type Hints)
=======================================================

本文件涵盖：
- Enum 枚举
- datetime 日期时间
- re 正则表达式
"""

from typing import Any, Pattern, Match
from enum import Enum, IntEnum, Flag, IntFlag, auto, unique
from datetime import datetime, date, time, timedelta, timezone
from zoneinfo import ZoneInfo  # Python 3.9+
import re
import calendar

# ============================================================================
# 1. Enum 枚举
# ============================================================================

class Color(Enum):
    """基本枚举"""
    RED = 1
    GREEN = 2
    BLUE = 3


class Status(Enum):
    """字符串值的枚举"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(IntEnum):
    """整数枚举（可以与 int 比较）"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AutoColor(Enum):
    """使用 auto() 自动生成值"""
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()


@unique  # 确保值唯一
class UniqueStatus(Enum):
    """唯一值枚举"""
    ACTIVE = 1
    INACTIVE = 2
    # DISABLED = 1  # 这会报错，因为值重复


class Permission(Flag):
    """标志枚举（支持位运算）"""
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    DELETE = auto()
    
    # 组合权限
    READ_WRITE = READ | WRITE
    ALL = READ | WRITE | EXECUTE | DELETE


class EnumDemo:
    """枚举演示"""
    
    @staticmethod
    def basic_usage() -> None:
        """基本使用"""
        # 访问枚举成员
        print(f"Color.RED: {Color.RED}")
        print(f"Color.RED.name: {Color.RED.name}")
        print(f"Color.RED.value: {Color.RED.value}")
        
        # 通过值访问
        print(f"Color(1): {Color(1)}")
        
        # 通过名称访问
        print(f"Color['RED']: {Color['RED']}")
        
        # 比较
        print(f"Color.RED == Color.RED: {Color.RED == Color.RED}")
        print(f"Color.RED is Color.RED: {Color.RED is Color.RED}")
        print(f"Color.RED == 1: {Color.RED == 1}")  # False (Enum)
        
        # IntEnum 可以与 int 比较
        print(f"Priority.HIGH == 3: {Priority.HIGH == 3}")  # True (IntEnum)
        print(f"Priority.HIGH > Priority.LOW: {Priority.HIGH > Priority.LOW}")
        
        # 遍历
        print("\nAll colors:")
        for color in Color:
            print(f"  {color.name} = {color.value}")
    
    @staticmethod
    def flag_enum_demo() -> None:
        """Flag 枚举演示"""
        # 组合权限
        user_perms = Permission.READ | Permission.WRITE
        print(f"User permissions: {user_perms}")
        
        # 检查权限
        print(f"Has READ: {Permission.READ in user_perms}")
        print(f"Has DELETE: {Permission.DELETE in user_perms}")
        
        # 添加权限
        user_perms |= Permission.EXECUTE
        print(f"After adding EXECUTE: {user_perms}")
        
        # 移除权限
        user_perms &= ~Permission.WRITE
        print(f"After removing WRITE: {user_perms}")
    
    @staticmethod
    def practical_example() -> None:
        """实际应用"""
        class HttpMethod(Enum):
            GET = "GET"
            POST = "POST"
            PUT = "PUT"
            DELETE = "DELETE"
            PATCH = "PATCH"
        
        class HttpStatus(IntEnum):
            OK = 200
            CREATED = 201
            BAD_REQUEST = 400
            UNAUTHORIZED = 401
            NOT_FOUND = 404
            INTERNAL_ERROR = 500
            
            @classmethod
            def is_success(cls, code: int) -> bool:
                return 200 <= code < 300
            
            @classmethod
            def is_error(cls, code: int) -> bool:
                return code >= 400
        
        # 使用
        method = HttpMethod.POST
        status = HttpStatus.CREATED
        
        print(f"Method: {method.value}")
        print(f"Status: {status} ({status.value})")
        print(f"Is success: {HttpStatus.is_success(status)}")


# ============================================================================
# 2. DateTime 日期时间
# ============================================================================

class DateTimeDemo:
    """日期时间演示"""
    
    @staticmethod
    def date_basics() -> None:
        """date 基础"""
        # 创建日期
        today: date = date.today()
        specific: date = date(2024, 12, 25)
        from_string: date = date.fromisoformat("2024-06-15")
        
        print(f"Today: {today}")
        print(f"Specific date: {specific}")
        print(f"From string: {from_string}")
        
        # 属性
        print(f"Year: {today.year}, Month: {today.month}, Day: {today.day}")
        print(f"Weekday (0=Mon): {today.weekday()}")
        print(f"ISO weekday (1=Mon): {today.isoweekday()}")
        
        # 格式化
        print(f"ISO format: {today.isoformat()}")
        print(f"Custom format: {today.strftime('%Y年%m月%d日')}")
        
        # 日期运算
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(weeks=1)
        print(f"Tomorrow: {tomorrow}")
        print(f"Next week: {next_week}")
        
        # 日期差
        delta = specific - today
        print(f"Days until Christmas: {delta.days}")
    
    @staticmethod
    def time_basics() -> None:
        """time 基础"""
        # 创建时间
        t1: time = time(14, 30, 45)  # 14:30:45
        t2: time = time(14, 30, 45, 123456)  # 带微秒
        from_string: time = time.fromisoformat("09:30:00")
        
        print(f"t1: {t1}")
        print(f"t2 (with microseconds): {t2}")
        
        # 属性
        print(f"Hour: {t1.hour}, Minute: {t1.minute}, Second: {t1.second}")
        
        # 格式化
        print(f"12-hour format: {t1.strftime('%I:%M %p')}")
    
    @staticmethod
    def datetime_basics() -> None:
        """datetime 基础"""
        # 创建
        now: datetime = datetime.now()
        utc_now: datetime = datetime.now(timezone.utc)
        specific: datetime = datetime(2024, 12, 25, 10, 30, 0)
        from_string: datetime = datetime.fromisoformat("2024-06-15T14:30:00")
        
        print(f"Now: {now}")
        print(f"UTC now: {utc_now}")
        print(f"Specific: {specific}")
        
        # 从 date 和 time 组合
        d = date(2024, 6, 15)
        t = time(14, 30)
        combined = datetime.combine(d, t)
        print(f"Combined: {combined}")
        
        # 提取 date 和 time
        print(f"Date part: {now.date()}")
        print(f"Time part: {now.time()}")
        
        # 时间戳
        timestamp: float = now.timestamp()
        from_timestamp: datetime = datetime.fromtimestamp(timestamp)
        print(f"Timestamp: {timestamp}")
        print(f"From timestamp: {from_timestamp}")
    
    @staticmethod
    def datetime_formatting() -> None:
        """日期时间格式化"""
        dt = datetime(2024, 6, 15, 14, 30, 45)
        
        # strftime 格式化符号
        formats: dict[str, str] = {
            "%Y-%m-%d": "年-月-日",
            "%H:%M:%S": "时:分:秒",
            "%Y-%m-%d %H:%M:%S": "完整日期时间",
            "%Y/%m/%d": "斜线分隔",
            "%d %b %Y": "日 月缩写 年",
            "%A, %B %d, %Y": "星期, 月份 日, 年",
            "%I:%M %p": "12小时制",
            "%Y年%m月%d日": "中文格式",
        }
        
        print("格式化示例:")
        for fmt, desc in formats.items():
            print(f"  {desc}: {dt.strftime(fmt)}")
        
        # strptime 解析
        parsed = datetime.strptime("2024-06-15 14:30:00", "%Y-%m-%d %H:%M:%S")
        print(f"\nParsed: {parsed}")
    
    @staticmethod
    def timedelta_demo() -> None:
        """时间差演示"""
        # 创建 timedelta
        delta1 = timedelta(days=7)
        delta2 = timedelta(hours=5, minutes=30)
        delta3 = timedelta(weeks=2, days=3, hours=4)
        
        print(f"delta1: {delta1}")
        print(f"delta2: {delta2}")
        print(f"delta3: {delta3}")
        
        # 属性（只有 days, seconds, microseconds）
        print(f"delta3.days: {delta3.days}")
        print(f"delta3.seconds: {delta3.seconds}")
        print(f"Total seconds: {delta3.total_seconds()}")
        
        # 运算
        now = datetime.now()
        print(f"Now: {now}")
        print(f"+ 7 days: {now + delta1}")
        print(f"- 5.5 hours: {now - delta2}")
        
        # timedelta 之间运算
        print(f"delta1 + delta2: {delta1 + delta2}")
        print(f"delta1 * 2: {delta1 * 2}")
        print(f"delta1 / 2: {delta1 / 2}")
        
        # 两个 datetime 相减得到 timedelta
        dt1 = datetime(2024, 12, 31)
        dt2 = datetime(2024, 1, 1)
        diff = dt1 - dt2
        print(f"Days in 2024: {diff.days}")
    
    @staticmethod
    def timezone_demo() -> None:
        """时区演示"""
        # UTC 时间
        utc_now = datetime.now(timezone.utc)
        print(f"UTC now: {utc_now}")
        
        # 使用 ZoneInfo (Python 3.9+)
        shanghai_tz = ZoneInfo("Asia/Shanghai")
        tokyo_tz = ZoneInfo("Asia/Tokyo")
        ny_tz = ZoneInfo("America/New_York")
        
        # 创建带时区的 datetime
        shanghai_now = datetime.now(shanghai_tz)
        print(f"Shanghai: {shanghai_now}")
        
        # 时区转换
        tokyo_time = shanghai_now.astimezone(tokyo_tz)
        ny_time = shanghai_now.astimezone(ny_tz)
        print(f"Tokyo: {tokyo_time}")
        print(f"New York: {ny_time}")
        
        # 手动设置偏移
        custom_tz = timezone(timedelta(hours=8))
        dt_with_tz = datetime(2024, 6, 15, 14, 30, tzinfo=custom_tz)
        print(f"Custom timezone: {dt_with_tz}")
    
    @staticmethod
    def calendar_demo() -> None:
        """日历功能"""
        # 打印月历
        print("June 2024:")
        print(calendar.month(2024, 6))
        
        # 判断闰年
        print(f"2024 is leap year: {calendar.isleap(2024)}")
        print(f"2023 is leap year: {calendar.isleap(2023)}")
        
        # 某月的天数
        _, days = calendar.monthrange(2024, 2)  # 闰年2月
        print(f"Days in Feb 2024: {days}")


# ============================================================================
# 3. 正则表达式 (re)
# ============================================================================

class RegexDemo:
    """正则表达式演示"""
    
    @staticmethod
    def basic_patterns() -> None:
        """基本模式"""
        text = "The quick brown fox jumps over 2 lazy dogs in 2024."
        
        # 查找第一个匹配
        match: Match[str] | None = re.search(r'\d+', text)
        if match:
            print(f"First number: {match.group()} at {match.start()}-{match.end()}")
        
        # 查找所有匹配
        numbers: list[str] = re.findall(r'\d+', text)
        print(f"All numbers: {numbers}")
        
        # 带位置信息的所有匹配
        for m in re.finditer(r'\d+', text):
            print(f"  Found '{m.group()}' at {m.span()}")
        
        # 匹配开头
        if re.match(r'The', text):
            print("Text starts with 'The'")
        
        # fullmatch 完全匹配
        if re.fullmatch(r'\d{4}', "2024"):
            print("'2024' is a 4-digit year")
    
    @staticmethod
    def pattern_syntax() -> None:
        """模式语法"""
        patterns: dict[str, tuple[str, str]] = {
            # 字符匹配
            r'.': ('a', "任意字符"),
            r'\d': ('5', "数字 [0-9]"),
            r'\D': ('a', "非数字"),
            r'\w': ('a', "单词字符 [a-zA-Z0-9_]"),
            r'\W': ('!', "非单词字符"),
            r'\s': (' ', "空白字符"),
            r'\S': ('a', "非空白字符"),
            
            # 量词
            r'a*': ('aaa', "0个或多个"),
            r'a+': ('aaa', "1个或多个"),
            r'a?': ('a', "0个或1个"),
            r'a{3}': ('aaa', "精确3个"),
            r'a{2,4}': ('aaa', "2到4个"),
            r'a{2,}': ('aaaa', "至少2个"),
            
            # 锚点
            r'^The': ('The cat', "开头匹配"),
            r'cat$': ('the cat', "结尾匹配"),
            r'\bcat\b': ('the cat sat', "单词边界"),
        }
        
        print("Pattern examples:")
        for pattern, (text, desc) in patterns.items():
            match = re.search(pattern, text)
            result = match.group() if match else "No match"
            print(f"  {pattern:12} on '{text}': {result:10} ({desc})")
    
    @staticmethod
    def groups_demo() -> None:
        """分组"""
        # 基本分组
        text = "John Smith: john@example.com"
        pattern = r'(\w+) (\w+): (\w+@\w+\.\w+)'
        
        match = re.search(pattern, text)
        if match:
            print(f"Full match: {match.group(0)}")
            print(f"First name: {match.group(1)}")
            print(f"Last name: {match.group(2)}")
            print(f"Email: {match.group(3)}")
            print(f"All groups: {match.groups()}")
        
        # 命名分组
        pattern_named = r'(?P<first>\w+) (?P<last>\w+): (?P<email>\w+@\w+\.\w+)'
        match = re.search(pattern_named, text)
        if match:
            print(f"\nNamed groups:")
            print(f"  first: {match.group('first')}")
            print(f"  last: {match.group('last')}")
            print(f"  groupdict: {match.groupdict()}")
        
        # 非捕获组 (?:...)
        text2 = "cat cats category"
        # (?:s)? 匹配可选的 's' 但不捕获
        pattern = r'cat(?:s)?'
        matches = re.findall(pattern, text2)
        print(f"\nNon-capturing group: {matches}")
    
    @staticmethod
    def substitution() -> None:
        """替换"""
        text = "Hello World! Hello Python!"
        
        # 基本替换
        result = re.sub(r'Hello', 'Hi', text)
        print(f"Basic sub: {result}")
        
        # 限制替换次数
        result = re.sub(r'Hello', 'Hi', text, count=1)
        print(f"Sub count=1: {result}")
        
        # 使用分组引用
        text2 = "John Smith, Jane Doe, Bob Wilson"
        # 交换姓名顺序
        result = re.sub(r'(\w+) (\w+)', r'\2, \1', text2)
        print(f"Swap names: {result}")
        
        # 使用函数替换
        def upper_first(match: Match[str]) -> str:
            return match.group(0).upper()
        
        text3 = "hello world"
        result = re.sub(r'\b\w', upper_first, text3)
        print(f"Uppercase first letters: {result}")
        
        # subn 返回替换次数
        result, count = re.subn(r'\d', 'X', "a1b2c3")
        print(f"subn result: {result}, count: {count}")
    
    @staticmethod
    def split_demo() -> None:
        """分割"""
        text = "one, two;  three   four"
        
        # 使用正则分割
        parts = re.split(r'[,;\s]+', text)
        print(f"Split: {parts}")
        
        # 保留分隔符（使用捕获组）
        parts = re.split(r'([,;])', "a,b;c")
        print(f"Split with separators: {parts}")
        
        # 限制分割次数
        parts = re.split(r'\s+', "one two three four", maxsplit=2)
        print(f"Split maxsplit=2: {parts}")
    
    @staticmethod
    def compiled_patterns() -> None:
        """编译模式（提高性能）"""
        # 编译模式
        email_pattern: Pattern[str] = re.compile(
            r'''
            (?P<username>[\w.+-]+)    # 用户名
            @                          # @ 符号
            (?P<domain>[\w.-]+)        # 域名
            \.                         # 点
            (?P<tld>\w{2,})            # 顶级域名
            ''',
            re.VERBOSE  # 允许注释和空白
        )
        
        emails = [
            "user@example.com",
            "john.doe@company.co.uk",
            "invalid-email",
        ]
        
        for email in emails:
            match = email_pattern.match(email)
            if match:
                print(f"Valid: {email}")
                print(f"  Username: {match.group('username')}")
                print(f"  Domain: {match.group('domain')}")
                print(f"  TLD: {match.group('tld')}")
            else:
                print(f"Invalid: {email}")
    
    @staticmethod
    def flags_demo() -> None:
        """正则标志"""
        text = "Hello\nWORLD\nhello"
        
        # IGNORECASE 忽略大小写
        matches = re.findall(r'hello', text, re.IGNORECASE)
        print(f"IGNORECASE: {matches}")
        
        # MULTILINE ^ 和 $ 匹配每行
        matches = re.findall(r'^\w+', text, re.MULTILINE)
        print(f"MULTILINE ^: {matches}")
        
        # DOTALL . 匹配换行符
        match = re.search(r'Hello.+hello', text, re.DOTALL | re.IGNORECASE)
        if match:
            print(f"DOTALL: {match.group()!r}")
        
        # 组合标志
        pattern = re.compile(r'hello', re.IGNORECASE | re.MULTILINE)
        matches = pattern.findall(text)
        print(f"Combined flags: {matches}")
    
    @staticmethod
    def practical_examples() -> None:
        """实际应用"""
        # 验证邮箱
        def is_valid_email(email: str) -> bool:
            pattern = r'^[\w.+-]+@[\w.-]+\.\w{2,}$'
            return bool(re.match(pattern, email))
        
        # 验证手机号（中国）
        def is_valid_phone(phone: str) -> bool:
            pattern = r'^1[3-9]\d{9}$'
            return bool(re.match(pattern, phone))
        
        # 提取 URL
        def extract_urls(text: str) -> list[str]:
            pattern = r'https?://[\w./%-]+'
            return re.findall(pattern, text)
        
        # 密码强度检查
        def check_password(password: str) -> dict[str, bool]:
            return {
                "has_lowercase": bool(re.search(r'[a-z]', password)),
                "has_uppercase": bool(re.search(r'[A-Z]', password)),
                "has_digit": bool(re.search(r'\d', password)),
                "has_special": bool(re.search(r'[!@#$%^&*]', password)),
                "min_length": len(password) >= 8,
            }
        
        # 测试
        print(f"Valid email 'test@example.com': {is_valid_email('test@example.com')}")
        print(f"Valid phone '13812345678': {is_valid_phone('13812345678')}")
        
        text = "Visit https://example.com and http://test.org/path"
        print(f"URLs found: {extract_urls(text)}")
        
        print(f"Password check 'Abc123!@': {check_password('Abc123!@')}")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    print("=" * 60)
    print("ENUM DEMO")
    print("=" * 60)
    EnumDemo.basic_usage()
    print()
    EnumDemo.flag_enum_demo()
    print()
    EnumDemo.practical_example()
    
    print("\n" + "=" * 60)
    print("DATETIME DEMO")
    print("=" * 60)
    DateTimeDemo.date_basics()
    print()
    DateTimeDemo.time_basics()
    print()
    DateTimeDemo.datetime_basics()
    print()
    DateTimeDemo.datetime_formatting()
    print()
    DateTimeDemo.timedelta_demo()
    print()
    DateTimeDemo.timezone_demo()
    print()
    DateTimeDemo.calendar_demo()
    
    print("\n" + "=" * 60)
    print("REGEX DEMO")
    print("=" * 60)
    RegexDemo.basic_patterns()
    print()
    RegexDemo.pattern_syntax()
    print()
    RegexDemo.groups_demo()
    print()
    RegexDemo.substitution()
    print()
    RegexDemo.split_demo()
    print()
    RegexDemo.compiled_patterns()
    print()
    RegexDemo.flags_demo()
    print()
    RegexDemo.practical_examples()


if __name__ == "__main__":
    main()

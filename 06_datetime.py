"""
Python 日期时间处理详解
包含：datetime, date, time, timedelta, timezone 等
"""

from datetime import datetime, date, time, timedelta, timezone
from datetime import tzinfo
import time as time_module
import calendar


# ============================================
# 1. date - 日期
# ============================================

def date_basics():
    """日期基础操作"""
    print("\n=== date (日期) ===")
    
    # 创建日期
    today = date.today()
    birthday = date(1990, 5, 15)
    
    print(f"今天: {today}")
    print(f"生日: {birthday}")
    
    # 访问日期组件
    print(f"\n日期组件:")
    print(f"年: {today.year}")
    print(f"月: {today.month}")
    print(f"日: {today.day}")
    print(f"星期几: {today.weekday()}")  # 0=Monday, 6=Sunday
    print(f"ISO星期几: {today.isoweekday()}")  # 1=Monday, 7=Sunday
    
    # 日期格式化
    print(f"\n日期格式化:")
    print(f"ISO格式: {today.isoformat()}")
    print(f"strftime: {today.strftime('%Y年%m月%d日')}")
    print(f"strftime: {today.strftime('%Y-%m-%d')}")
    
    # 日期解析
    date_str = "2024-12-25"
    parsed_date = date.fromisoformat(date_str)
    print(f"\n解析日期: {date_str} -> {parsed_date}")
    
    # 时间戳转换
    timestamp = time_module.time()
    from_timestamp = date.fromtimestamp(timestamp)
    print(f"从时间戳创建: {from_timestamp}")


def date_operations():
    """日期运算"""
    print("\n=== 日期运算 ===")
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(weeks=1)
    
    print(f"今天: {today}")
    print(f"昨天: {yesterday}")
    print(f"明天: {tomorrow}")
    print(f"下周: {next_week}")
    
    # 日期差值
    date1 = date(2024, 1, 1)
    date2 = date(2024, 12, 31)
    diff = date2 - date1
    
    print(f"\n日期差值:")
    print(f"{date2} - {date1} = {diff.days} 天")
    
    # 比较日期
    print(f"\n日期比较:")
    print(f"today > yesterday: {today > yesterday}")
    print(f"today == today: {today == today}")


# ============================================
# 2. time - 时间
# ============================================

def time_basics():
    """时间基础操作"""
    print("\n=== time (时间) ===")
    
    # 创建时间
    now_time = time(14, 30, 45)  # 14:30:45
    precise_time = time(14, 30, 45, 123456)  # 包含微秒
    
    print(f"时间: {now_time}")
    print(f"精确时间: {precise_time}")
    
    # 访问时间组件
    print(f"\n时间组件:")
    print(f"时: {now_time.hour}")
    print(f"分: {now_time.minute}")
    print(f"秒: {now_time.second}")
    print(f"微秒: {precise_time.microsecond}")
    
    # 时间格式化
    print(f"\n时间格式化:")
    print(f"ISO格式: {now_time.isoformat()}")
    print(f"strftime: {now_time.strftime('%H:%M:%S')}")
    print(f"strftime: {now_time.strftime('%I:%M:%S %p')}")  # 12小时制
    
    # 时间解析
    time_str = "14:30:45"
    parsed_time = time.fromisoformat(time_str)
    print(f"\n解析时间: {time_str} -> {parsed_time}")


# ============================================
# 3. datetime - 日期时间
# ============================================

def datetime_basics():
    """日期时间基础操作"""
    print("\n=== datetime (日期时间) ===")
    
    # 创建日期时间
    now = datetime.now()
    utc_now = datetime.utcnow()
    specific = datetime(2024, 12, 25, 18, 30, 0)
    
    print(f"当前时间: {now}")
    print(f"UTC时间: {utc_now}")
    print(f"指定时间: {specific}")
    
    # 访问组件
    print(f"\n日期时间组件:")
    print(f"年: {now.year}")
    print(f"月: {now.month}")
    print(f"日: {now.day}")
    print(f"时: {now.hour}")
    print(f"分: {now.minute}")
    print(f"秒: {now.second}")
    print(f"微秒: {now.microsecond}")
    
    # 提取日期和时间
    print(f"\n提取:")
    print(f"日期部分: {now.date()}")
    print(f"时间部分: {now.time()}")


def datetime_formatting():
    """日期时间格式化"""
    print("\n=== 日期时间格式化 ===")
    
    now = datetime.now()
    
    # strftime - 格式化为字符串
    print("strftime 格式化:")
    print(f"ISO格式: {now.isoformat()}")
    print(f"标准格式: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"中文格式: {now.strftime('%Y年%m月%d日 %H时%M分%S秒')}")
    print(f"12小时制: {now.strftime('%Y-%m-%d %I:%M:%S %p')}")
    print(f"星期: {now.strftime('%A, %B %d, %Y')}")
    
    # 常用格式代码
    print(f"\n常用格式代码:")
    print(f"%Y (年): {now.strftime('%Y')}")
    print(f"%m (月): {now.strftime('%m')}")
    print(f"%d (日): {now.strftime('%d')}")
    print(f"%H (时24): {now.strftime('%H')}")
    print(f"%I (时12): {now.strftime('%I')}")
    print(f"%M (分): {now.strftime('%M')}")
    print(f"%S (秒): {now.strftime('%S')}")
    print(f"%A (星期): {now.strftime('%A')}")
    print(f"%B (月份): {now.strftime('%B')}")


def datetime_parsing():
    """日期时间解析"""
    print("\n=== 日期时间解析 ===")
    
    # strptime - 从字符串解析
    date_strings = [
        ("2024-12-25", "%Y-%m-%d"),
        ("2024-12-25 18:30:00", "%Y-%m-%d %H:%M:%S"),
        ("25/12/2024", "%d/%m/%Y"),
        ("December 25, 2024", "%B %d, %Y"),
    ]
    
    print("strptime 解析:")
    for date_str, fmt in date_strings:
        parsed = datetime.strptime(date_str, fmt)
        print(f"{date_str:25s} -> {parsed}")
    
    # fromisoformat - 从 ISO 格式解析
    iso_str = "2024-12-25T18:30:00"
    parsed = datetime.fromisoformat(iso_str)
    print(f"\nISO格式解析: {iso_str} -> {parsed}")
    
    # 从时间戳创建
    timestamp = time_module.time()
    from_ts = datetime.fromtimestamp(timestamp)
    print(f"\n从时间戳: {timestamp:.0f} -> {from_ts}")
    
    # 时间戳
    dt = datetime(2024, 12, 25, 18, 30, 0)
    ts = dt.timestamp()
    print(f"\n转为时间戳: {dt} -> {ts}")


def datetime_operations():
    """日期时间运算"""
    print("\n=== 日期时间运算 ===")
    
    now = datetime.now()
    
    # 使用 timedelta
    print("使用 timedelta:")
    print(f"现在: {now}")
    print(f"1小时后: {now + timedelta(hours=1)}")
    print(f"30分钟前: {now - timedelta(minutes=30)}")
    print(f"7天后: {now + timedelta(days=7)}")
    print(f"1周2天3小时: {now + timedelta(weeks=1, days=2, hours=3)}")
    
    # 日期时间差值
    dt1 = datetime(2024, 1, 1, 0, 0, 0)
    dt2 = datetime(2024, 12, 31, 23, 59, 59)
    diff = dt2 - dt1
    
    print(f"\n时间差值:")
    print(f"{dt2} - {dt1}")
    print(f"总天数: {diff.days}")
    print(f"总秒数: {diff.total_seconds()}")
    print(f"总小时数: {diff.total_seconds() / 3600:.2f}")
    
    # 替换组件
    print(f"\n替换组件:")
    dt = datetime(2024, 12, 25, 18, 30, 45)
    print(f"原始: {dt}")
    print(f"替换年: {dt.replace(year=2025)}")
    print(f"替换时间: {dt.replace(hour=12, minute=0, second=0)}")


# ============================================
# 4. timedelta - 时间间隔
# ============================================

def timedelta_demo():
    """时间间隔"""
    print("\n=== timedelta (时间间隔) ===")
    
    # 创建时间间隔
    delta1 = timedelta(days=7)
    delta2 = timedelta(hours=12, minutes=30)
    delta3 = timedelta(weeks=2, days=3, hours=4, minutes=30, seconds=15)
    
    print(f"7天: {delta1}")
    print(f"12.5小时: {delta2}")
    print(f"复杂间隔: {delta3}")
    
    # timedelta 属性
    print(f"\ntimedelta 属性:")
    print(f"天数: {delta3.days}")
    print(f"秒数: {delta3.seconds}")
    print(f"微秒: {delta3.microseconds}")
    print(f"总秒数: {delta3.total_seconds()}")
    
    # timedelta 运算
    print(f"\ntimedelta 运算:")
    d1 = timedelta(days=7)
    d2 = timedelta(days=3)
    print(f"7天 + 3天 = {d1 + d2}")
    print(f"7天 - 3天 = {d1 - d2}")
    print(f"7天 * 2 = {d1 * 2}")
    print(f"7天 / 2 = {d1 / 2}")
    print(f"7天 // 2 = {d1 // 2}")
    
    # 负时间间隔
    print(f"\n负时间间隔:")
    negative = timedelta(days=-7)
    print(f"-7天: {negative}")
    print(f"绝对值: {abs(negative)}")


# ============================================
# 5. 时区处理
# ============================================

def timezone_demo():
    """时区处理"""
    print("\n=== 时区处理 ===")
    
    # UTC 时区
    utc_tz = timezone.utc
    now_utc = datetime.now(utc_tz)
    print(f"UTC时间: {now_utc}")
    
    # 自定义时区
    # 东八区 (北京时间)
    beijing_tz = timezone(timedelta(hours=8))
    now_beijing = datetime.now(beijing_tz)
    print(f"北京时间: {now_beijing}")
    
    # 时区转换
    print(f"\n时区转换:")
    utc_time = datetime(2024, 12, 25, 12, 0, 0, tzinfo=timezone.utc)
    print(f"UTC: {utc_time}")
    
    # 转换为北京时间
    beijing_time = utc_time.astimezone(beijing_tz)
    print(f"北京: {beijing_time}")
    
    # 转换为东京时间 (UTC+9)
    tokyo_tz = timezone(timedelta(hours=9))
    tokyo_time = utc_time.astimezone(tokyo_tz)
    print(f"东京: {tokyo_time}")
    
    # 移除时区信息
    naive = now_utc.replace(tzinfo=None)
    print(f"\n移除时区: {naive}")
    
    # 添加时区信息
    naive_dt = datetime(2024, 12, 25, 12, 0, 0)
    aware_dt = naive_dt.replace(tzinfo=beijing_tz)
    print(f"添加时区: {aware_dt}")


# ============================================
# 6. calendar 模块
# ============================================

def calendar_demo():
    """日历功能"""
    print("\n=== calendar 模块 ===")
    
    # 打印月历
    print("2024年12月日历:")
    print(calendar.month(2024, 12))
    
    # 判断闰年
    print(f"\n闰年判断:")
    for year in [2020, 2021, 2024, 2100]:
        is_leap = calendar.isleap(year)
        print(f"{year}: {'是' if is_leap else '否'}")
    
    # 某月天数
    print(f"\n每月天数:")
    for month in range(1, 13):
        days = calendar.monthrange(2024, month)[1]
        print(f"2024年{month}月: {days}天")
    
    # 星期几
    weekday = calendar.weekday(2024, 12, 25)
    weekday_name = calendar.day_name[weekday]
    print(f"\n2024-12-25 是: {weekday_name}")
    
    # 某月第一天是星期几，以及该月总天数
    first_weekday, num_days = calendar.monthrange(2024, 12)
    print(f"\n2024年12月:")
    print(f"第一天是: {calendar.day_name[first_weekday]}")
    print(f"总共: {num_days}天")


# ============================================
# 7. 性能和时间测量
# ============================================

def time_measurement():
    """时间测量"""
    print("\n=== 时间测量 ===")
    
    # time.time() - Unix 时间戳
    start = time_module.time()
    time_module.sleep(0.1)  # 休眠 0.1 秒
    end = time_module.time()
    print(f"time.time() 测量: {(end - start)*1000:.2f} 毫秒")
    
    # time.perf_counter() - 高精度计时器
    start = time_module.perf_counter()
    sum(range(1000000))
    end = time_module.perf_counter()
    print(f"perf_counter() 测量: {(end - start)*1000:.2f} 毫秒")
    
    # time.monotonic() - 单调时钟
    start = time_module.monotonic()
    time_module.sleep(0.1)
    end = time_module.monotonic()
    print(f"monotonic() 测量: {(end - start)*1000:.2f} 毫秒")


# ============================================
# 8. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 计算年龄
    print("1. 计算年龄:")
    def calculate_age(birthday):
        today = date.today()
        age = today.year - birthday.year
        if (today.month, today.day) < (birthday.month, birthday.day):
            age -= 1
        return age
    
    birthday = date(1990, 5, 15)
    age = calculate_age(birthday)
    print(f"生日: {birthday}")
    print(f"年龄: {age}岁")
    
    # 2. 倒计时
    print("\n2. 倒计时到新年:")
    now = datetime.now()
    new_year = datetime(now.year + 1, 1, 1, 0, 0, 0)
    countdown = new_year - now
    
    days = countdown.days
    hours, remainder = divmod(countdown.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"距离新年还有: {days}天 {hours}小时 {minutes}分钟 {seconds}秒")
    
    # 3. 工作日计算
    print("\n3. 工作日计算:")
    def count_weekdays(start_date, end_date):
        """计算两个日期之间的工作日数量"""
        weekdays = 0
        current = start_date
        while current <= end_date:
            if current.weekday() < 5:  # Monday=0, Friday=4
                weekdays += 1
            current += timedelta(days=1)
        return weekdays
    
    start = date(2024, 12, 1)
    end = date(2024, 12, 31)
    workdays = count_weekdays(start, end)
    print(f"{start} 到 {end}")
    print(f"工作日: {workdays}天")
    
    # 4. 日期范围生成
    print("\n4. 生成日期范围:")
    def date_range(start, end, step=1):
        """生成日期范围"""
        current = start
        while current <= end:
            yield current
            current += timedelta(days=step)
    
    start = date(2024, 12, 20)
    end = date(2024, 12, 25)
    print(f"{start} 到 {end} 的所有日期:")
    for d in date_range(start, end):
        print(f"  {d.strftime('%Y-%m-%d %A')}")
    
    # 5. 时间格式标准化
    print("\n5. 时间格式标准化:")
    date_strings = [
        "2024-12-25",
        "25/12/2024",
        "December 25, 2024",
        "2024/12/25"
    ]
    
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%Y/%m/%d"
    ]
    
    print("标准化为 ISO 格式:")
    for date_str, fmt in zip(date_strings, formats):
        try:
            dt = datetime.strptime(date_str, fmt)
            iso = dt.strftime("%Y-%m-%d")
            print(f"{date_str:25s} -> {iso}")
        except ValueError as e:
            print(f"{date_str:25s} -> 解析失败: {e}")
    
    # 6. 会议提醒
    print("\n6. 会议提醒系统:")
    class Meeting:
        def __init__(self, title, meeting_time):
            self.title = title
            self.meeting_time = meeting_time
        
        def time_until_meeting(self):
            """距离会议的时间"""
            now = datetime.now()
            if self.meeting_time > now:
                delta = self.meeting_time - now
                return delta
            return None
        
        def reminder(self):
            """生成提醒信息"""
            delta = self.time_until_meeting()
            if delta is None:
                return f"{self.title} 已经结束"
            
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            if delta.days > 0:
                return f"{self.title} 将在 {delta.days}天{hours}小时后开始"
            elif hours > 0:
                return f"{self.title} 将在 {hours}小时{minutes}分钟后开始"
            else:
                return f"{self.title} 将在 {minutes}分钟后开始"
    
    meeting = Meeting("项目评审", datetime.now() + timedelta(hours=2, minutes=30))
    print(meeting.reminder())
    
    # 7. 时区会议安排
    print("\n7. 跨时区会议:")
    utc_meeting = datetime(2024, 12, 25, 14, 0, 0, tzinfo=timezone.utc)
    
    timezones = {
        "北京": timezone(timedelta(hours=8)),
        "东京": timezone(timedelta(hours=9)),
        "伦敦": timezone(timedelta(hours=0)),
        "纽约": timezone(timedelta(hours=-5)),
    }
    
    print(f"UTC会议时间: {utc_meeting.strftime('%Y-%m-%d %H:%M %Z')}")
    print("\n各地时间:")
    for city, tz in timezones.items():
        local_time = utc_meeting.astimezone(tz)
        print(f"  {city}: {local_time.strftime('%Y-%m-%d %H:%M')}")


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 日期时间处理详解")
    print("=" * 60)
    
    date_basics()
    date_operations()
    
    time_basics()
    
    datetime_basics()
    datetime_formatting()
    datetime_parsing()
    datetime_operations()
    
    timedelta_demo()
    timezone_demo()
    calendar_demo()
    time_measurement()
    
    practical_examples()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

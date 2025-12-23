"""
Python 正则表达式详解
包含：re 模块、匹配、搜索、替换、分组等
"""

import re
from typing import List, Optional


# ============================================
# 1. 正则表达式基础
# ============================================

def regex_basics():
    """正则表达式基础"""
    print("\n=== 正则表达式基础 ===")
    
    text = "Hello, my phone number is 138-1234-5678"
    
    # re.search - 搜索第一个匹配
    match = re.search(r'\d{3}-\d{4}-\d{4}', text)
    if match:
        print(f"找到电话号码: {match.group()}")
        print(f"位置: {match.start()} 到 {match.end()}")
    
    # re.match - 从字符串开头匹配
    text2 = "138-1234-5678 is my phone"
    match = re.match(r'\d{3}-\d{4}-\d{4}', text2)
    if match:
        print(f"\n从开头匹配: {match.group()}")
    
    # re.fullmatch - 完全匹配整个字符串
    text3 = "138-1234-5678"
    match = re.fullmatch(r'\d{3}-\d{4}-\d{4}', text3)
    if match:
        print(f"完全匹配: {match.group()}")
    
    # re.findall - 找到所有匹配
    text4 = "Phone: 138-1234-5678, 139-8765-4321"
    phones = re.findall(r'\d{3}-\d{4}-\d{4}', text4)
    print(f"\n所有电话: {phones}")
    
    # re.finditer - 返回匹配对象迭代器
    print(f"\nfinditer 详细信息:")
    for match in re.finditer(r'\d{3}-\d{4}-\d{4}', text4):
        print(f"  {match.group()} at {match.start()}-{match.end()}")


def regex_patterns():
    """正则表达式模式"""
    print("\n=== 正则表达式模式 ===")
    
    # 基本字符
    print("1. 基本字符匹配:")
    print(f"  'hello' in 'hello world': {bool(re.search('hello', 'hello world'))}")
    
    # 元字符
    print("\n2. 元字符:")
    print(f"  . (任意字符): {re.findall(r'h.llo', 'hello hallo hullo')}")
    print(f"  ^ (开头): {bool(re.match(r'^Hello', 'Hello World'))}")
    print(f"  $ (结尾): {bool(re.search(r'World$', 'Hello World'))}")
    print(f"  * (0次或多次): {re.findall(r'ab*', 'a ab abb abbb')}")
    print(f"  + (1次或多次): {re.findall(r'ab+', 'a ab abb abbb')}")
    print(f"  ? (0次或1次): {re.findall(r'ab?', 'a ab abb')}")
    
    # 量词
    print("\n3. 量词:")
    print(f"  {{3}} (恰好3次): {re.findall(r'a{{3}}', 'aa aaa aaaa')}")
    print(f"  {{2,4}} (2到4次): {re.findall(r'a{{2,4}}', 'a aa aaa aaaa aaaaa')}")
    print(f"  {{2,}} (至少2次): {re.findall(r'a{{2,}}', 'a aa aaa aaaa')}")
    
    # 字符类
    print("\n4. 字符类:")
    print(f"  [abc] (a或b或c): {re.findall(r'[abc]', 'a b c d e')}")
    print(f"  [a-z] (a到z): {re.findall(r'[a-z]+', 'Hello World 123')}")
    print(f"  [^abc] (非abc): {re.findall(r'[^abc]', 'abcde')}")
    
    # 预定义字符类
    print("\n5. 预定义字符类:")
    text = "Hello 123, World 456!"
    print(f"  \\d (数字): {re.findall(r'\\d+', text)}")
    print(f"  \\D (非数字): {re.findall(r'\\D+', text)}")
    print(f"  \\w (单词字符): {re.findall(r'\\w+', text)}")
    print(f"  \\W (非单词字符): {re.findall(r'\\W+', text)}")
    print(f"  \\s (空白字符): {re.findall(r'\\s+', text)}")


def regex_groups():
    """正则表达式分组"""
    print("\n=== 正则表达式分组 ===")
    
    # 捕获分组
    text = "John Doe, age 30, email: john@example.com"
    pattern = r'(\w+) (\w+), age (\d+), email: ([\w.]+@[\w.]+)'
    match = re.search(pattern, text)
    
    if match:
        print("捕获分组:")
        print(f"  完整匹配: {match.group(0)}")
        print(f"  名: {match.group(1)}")
        print(f"  姓: {match.group(2)}")
        print(f"  年龄: {match.group(3)}")
        print(f"  邮箱: {match.group(4)}")
        print(f"  所有分组: {match.groups()}")
    
    # 命名分组
    pattern = r'(?P<first>\w+) (?P<last>\w+), age (?P<age>\d+)'
    match = re.search(pattern, text)
    
    if match:
        print("\n命名分组:")
        print(f"  名: {match.group('first')}")
        print(f"  姓: {match.group('last')}")
        print(f"  年龄: {match.group('age')}")
        print(f"  字典: {match.groupdict()}")
    
    # 非捕获分组
    text2 = "http://www.example.com https://example.org"
    pattern = r'(?:http|https)://[\w.]+'
    urls = re.findall(pattern, text2)
    print(f"\n非捕获分组: {urls}")
    
    # 反向引用
    text3 = "hello hello world world"
    pattern = r'\b(\w+)\s+\1\b'  # 匹配重复的单词
    matches = re.findall(pattern, text3)
    print(f"\n反向引用（重复单词）: {matches}")


def regex_flags():
    """正则表达式标志"""
    print("\n=== 正则表达式标志 ===")
    
    text = "Hello\nWorld\nPython"
    
    # re.IGNORECASE (re.I) - 忽略大小写
    print("1. IGNORECASE:")
    print(f"  不忽略: {re.findall(r'hello', text)}")
    print(f"  忽略: {re.findall(r'hello', text, re.IGNORECASE)}")
    
    # re.MULTILINE (re.M) - 多行模式
    print("\n2. MULTILINE:")
    print(f"  单行: {re.findall(r'^\\w+', text)}")
    print(f"  多行: {re.findall(r'^\\w+', text, re.MULTILINE)}")
    
    # re.DOTALL (re.S) - . 匹配包括换行符
    print("\n3. DOTALL:")
    print(f"  默认: {re.findall(r'Hello.*Python', text)}")
    print(f"  DOTALL: {re.findall(r'Hello.*Python', text, re.DOTALL)}")
    
    # re.VERBOSE (re.X) - 详细模式，可以添加注释
    pattern = r'''
        (\d{3})    # 区号
        -          # 分隔符
        (\d{4})    # 前四位
        -          # 分隔符
        (\d{4})    # 后四位
    '''
    phone = "138-1234-5678"
    match = re.search(pattern, phone, re.VERBOSE)
    if match:
        print(f"\n4. VERBOSE 模式匹配: {match.groups()}")


# ============================================
# 2. 字符串操作
# ============================================

def regex_split():
    """使用正则分割字符串"""
    print("\n=== 正则分割 ===")
    
    # 基本分割
    text = "apple,banana;orange:grape"
    parts = re.split(r'[,;:]', text)
    print(f"分割: {parts}")
    
    # 保留分隔符
    text2 = "Hello123World456Python"
    parts = re.split(r'(\d+)', text2)
    print(f"保留分隔符: {parts}")
    
    # 限制分割次数
    text3 = "a,b,c,d,e"
    parts = re.split(r',', text3, maxsplit=2)
    print(f"限制分割: {parts}")
    
    # 多个空白字符分割
    text4 = "one  two   three\tfour\nfive"
    parts = re.split(r'\s+', text4)
    print(f"空白分割: {parts}")


def regex_replace():
    """使用正则替换字符串"""
    print("\n=== 正则替换 ===")
    
    # 基本替换
    text = "I love cats and cats love me"
    result = re.sub(r'cats', 'dogs', text)
    print(f"替换: {result}")
    
    # 限制替换次数
    result = re.sub(r'cats', 'dogs', text, count=1)
    print(f"替换1次: {result}")
    
    # 使用分组替换
    text2 = "John Doe (30), Jane Smith (25)"
    result = re.sub(r'(\w+) (\w+) \((\d+)\)', r'\1 \2 is \3 years old', text2)
    print(f"\n分组替换: {result}")
    
    # 使用命名分组替换
    pattern = r'(?P<first>\w+) (?P<last>\w+)'
    result = re.sub(pattern, r'\g<last>, \g<first>', "John Doe")
    print(f"命名分组: {result}")
    
    # 使用函数替换
    def double(match):
        return str(int(match.group(0)) * 2)
    
    text3 = "10 + 20 = 30"
    result = re.sub(r'\d+', double, text3)
    print(f"\n函数替换: {result}")
    
    # subn - 返回替换次数
    text4 = "cat cat cat"
    result, count = re.subn(r'cat', 'dog', text4)
    print(f"\nsubn: {result}, 替换了 {count} 次")


# ============================================
# 3. 编译正则表达式
# ============================================

def regex_compile():
    """编译正则表达式"""
    print("\n=== 编译正则表达式 ===")
    
    # 编译正则表达式（提高性能）
    pattern = re.compile(r'\d{3}-\d{4}-\d{4}')
    
    text1 = "Phone: 138-1234-5678"
    text2 = "Contact: 139-8765-4321"
    
    print(f"匹配1: {pattern.search(text1).group()}")
    print(f"匹配2: {pattern.search(text2).group()}")
    
    # 编译时指定标志
    pattern = re.compile(r'hello', re.IGNORECASE | re.MULTILINE)
    text = "HELLO\nHello\nhello"
    matches = pattern.findall(text)
    print(f"\n编译标志: {matches}")
    
    # 查看模式信息
    print(f"\n模式: {pattern.pattern}")
    print(f"标志: {pattern.flags}")


# ============================================
# 4. 常用正则表达式模式
# ============================================

def common_patterns():
    """常用正则表达式"""
    print("\n=== 常用正则表达式 ===")
    
    patterns = {
        "邮箱": r'^[\w.+-]+@[\w-]+\.[\w.-]+$',
        "手机号": r'^1[3-9]\d{9}$',
        "身份证": r'^\d{17}[\dXx]$',
        "URL": r'https?://[\w\-.]+(:\d+)?(/[\w\-./?%&=]*)?',
        "IPv4": r'^(\d{1,3}\.){3}\d{1,3}$',
        "日期YYYY-MM-DD": r'^\d{4}-\d{2}-\d{2}$',
        "时间HH:MM:SS": r'^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$',
        "中文字符": r'[\u4e00-\u9fa5]+',
        "用户名": r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$',
        "密码": r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',
    }
    
    test_data = {
        "邮箱": ["test@example.com", "invalid.email"],
        "手机号": ["13812345678", "12345678901"],
        "URL": ["https://www.example.com", "not-a-url"],
        "IPv4": ["192.168.1.1", "999.999.999.999"],
        "日期YYYY-MM-DD": ["2024-12-25", "2024-13-32"],
    }
    
    for name, pattern in patterns.items():
        if name in test_data:
            print(f"\n{name} ({pattern}):")
            for text in test_data[name]:
                match = re.match(pattern, text)
                status = "✓" if match else "✗"
                print(f"  {status} {text}")


# ============================================
# 5. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 验证邮箱
    print("1. 邮箱验证:")
    def validate_email(email):
        pattern = r'^[\w.+-]+@[\w-]+\.[\w.-]+$'
        return bool(re.match(pattern, email))
    
    emails = [
        "test@example.com",
        "user.name+tag@example.co.uk",
        "invalid.email",
        "@example.com",
    ]
    
    for email in emails:
        valid = validate_email(email)
        print(f"  {email:35s} {'✓' if valid else '✗'}")
    
    # 2. 提取所有URL
    print("\n2. 提取URL:")
    text = """
    Visit https://www.python.org for documentation.
    Also check http://github.com/python
    """
    
    pattern = r'https?://[\w\-.]+(:\d+)?(/[\w\-./?%&=]*)?'
    urls = re.findall(pattern, text)
    for url in urls:
        print(f"  {url}")
    
    # 3. 手机号脱敏
    print("\n3. 手机号脱敏:")
    def mask_phone(text):
        pattern = r'(\d{3})\d{4}(\d{4})'
        return re.sub(pattern, r'\1****\2', text)
    
    text = "联系方式：13812345678, 13987654321"
    masked = mask_phone(text)
    print(f"  原文: {text}")
    print(f"  脱敏: {masked}")
    
    # 4. 提取HTML标签内容
    print("\n4. 提取HTML标签:")
    html = '<div>Hello</div><p>World</p><span>Python</span>'
    pattern = r'<(\w+)>(.*?)</\1>'
    matches = re.findall(pattern, html)
    for tag, content in matches:
        print(f"  <{tag}>: {content}")
    
    # 5. 解析日志
    print("\n5. 解析日志:")
    log = """
    [2024-12-25 10:30:45] INFO: Application started
    [2024-12-25 10:31:20] ERROR: Connection failed
    [2024-12-25 10:32:15] WARNING: Retry attempt 1
    """
    
    pattern = r'\[(?P<time>[\d\-: ]+)\] (?P<level>\w+): (?P<message>.*)'
    for line in log.strip().split('\n'):
        match = re.search(pattern, line)
        if match:
            print(f"  {match.group('level'):7s} | {match.group('message')}")
    
    # 6. 驼峰转下划线
    print("\n6. 驼峰转下划线:")
    def camel_to_snake(name):
        pattern = r'([a-z0-9])([A-Z])'
        return re.sub(pattern, r'\1_\2', name).lower()
    
    names = ["camelCase", "PascalCase", "someVariableName"]
    for name in names:
        snake = camel_to_snake(name)
        print(f"  {name:20s} -> {snake}")
    
    # 7. 提取中文
    print("\n7. 提取中文:")
    text = "Hello 世界！Python 很有趣。"
    chinese = re.findall(r'[\u4e00-\u9fa5]+', text)
    print(f"  原文: {text}")
    print(f"  中文: {chinese}")
    
    # 8. 密码强度检查
    print("\n8. 密码强度检查:")
    def check_password_strength(password):
        """
        密码要求:
        - 至少8个字符
        - 至少一个大写字母
        - 至少一个小写字母
        - 至少一个数字
        """
        if len(password) < 8:
            return False, "密码至少8个字符"
        if not re.search(r'[A-Z]', password):
            return False, "密码需要至少一个大写字母"
        if not re.search(r'[a-z]', password):
            return False, "密码需要至少一个小写字母"
        if not re.search(r'\d', password):
            return False, "密码需要至少一个数字"
        return True, "密码强度合格"
    
    passwords = ["weak", "Strong1", "VeryStrong123", "NoDigits"]
    for pwd in passwords:
        valid, msg = check_password_strength(pwd)
        status = "✓" if valid else "✗"
        print(f"  {status} {pwd:15s}: {msg}")
    
    # 9. 清理文本
    print("\n9. 清理文本:")
    def clean_text(text):
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', text)
        return text.strip()
    
    dirty = "  Hello   <b>World</b>!!!  \n\n Python  "
    clean = clean_text(dirty)
    print(f"  原文: '{dirty}'")
    print(f"  清理: '{clean}'")
    
    # 10. 提取代码注释
    print("\n10. 提取Python注释:")
    code = '''
def hello():
    # 这是单行注释
    print("Hello")  # 行尾注释
    """
    这是多行注释
    """
    return True
'''
    
    # 单行注释
    single_line = re.findall(r'#.*', code)
    print("  单行注释:")
    for comment in single_line:
        print(f"    {comment}")
    
    # 多行注释
    multi_line = re.findall(r'"""[\s\S]*?"""', code)
    print("  多行注释:")
    for comment in multi_line:
        print(f"    {comment.strip()}")


# ============================================
# 6. 性能优化
# ============================================

def performance_tips():
    """正则表达式性能优化"""
    print("\n=== 性能优化建议 ===")
    
    print("""
    1. 编译正则表达式
       - 对于重复使用的模式，使用 re.compile()
    
    2. 避免贪婪匹配
       - 使用非贪婪匹配 *? +? ??
       - 示例: r'<.*?>' 而不是 r'<.*>'
    
    3. 使用具体的字符类
       - 用 [0-9] 而不是 \d (如果只需要ASCII数字)
       - 用 [a-zA-Z] 而不是 \w
    
    4. 避免回溯
       - 使用原子分组 (?>...)
       - 避免嵌套量词
    
    5. 锚点优化
       - 使用 ^ 和 $ 限制匹配范围
       - 使用 \A 和 \Z 而不是 ^ 和 $（多行文本）
    
    6. 简化模式
       - 合并相似模式
       - 使用字符类而不是多个选择
    
    7. 选择正确的方法
       - search() vs match() vs fullmatch()
       - findall() vs finditer()
    """)


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python 正则表达式详解")
    print("=" * 60)
    
    regex_basics()
    regex_patterns()
    regex_groups()
    regex_flags()
    
    regex_split()
    regex_replace()
    regex_compile()
    
    common_patterns()
    practical_examples()
    performance_tips()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

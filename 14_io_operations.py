"""
Python IO 操作详解
包含：文件读写、路径操作、JSON、CSV、pickle等
"""

import os
import json
import csv
import pickle
import shutil
from pathlib import Path
import tempfile


# ============================================
# 1. 文件读写基础
# ============================================

def file_basics():
    """文件读写基础"""
    print("\n=== 文件读写基础 ===")
    
    # 写入文件
    print("1. 写入文件:")
    with open('/tmp/test.txt', 'w', encoding='utf-8') as f:
        f.write("Hello, World!\n")
        f.write("第二行\n")
        f.writelines(["第三行\n", "第四行\n"])
    print("  文件已写入")
    
    # 读取文件
    print("\n2. 读取文件:")
    with open('/tmp/test.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"  内容: {repr(content)}")
    
    # 按行读取
    print("\n3. 按行读取:")
    with open('/tmp/test.txt', 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            print(f"  {line_num}: {line.strip()}")
    
    # readlines()
    print("\n4. readlines():")
    with open('/tmp/test.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"  总行数: {len(lines)}")
    
    # 追加模式
    print("\n5. 追加模式:")
    with open('/tmp/test.txt', 'a', encoding='utf-8') as f:
        f.write("追加的内容\n")
    
    # 读写模式
    print("\n6. 读写模式 (r+):")
    with open('/tmp/test.txt', 'r+', encoding='utf-8') as f:
        content = f.read()
        f.write("额外内容\n")


def file_modes():
    """文件打开模式"""
    print("\n=== 文件打开模式 ===")
    
    print("""
    文件模式:
    
    读取模式:
    - 'r'  : 只读（默认）
    - 'rb' : 二进制只读
    - 'r+' : 读写
    
    写入模式:
    - 'w'  : 写入（覆盖）
    - 'wb' : 二进制写入
    - 'w+' : 读写（覆盖）
    
    追加模式:
    - 'a'  : 追加
    - 'ab' : 二进制追加
    - 'a+' : 读写追加
    
    独占模式:
    - 'x'  : 独占创建（文件存在则失败）
    
    编码:
    - encoding='utf-8'
    - encoding='gbk'
    - encoding='ascii'
    """)


# ============================================
# 2. 二进制文件
# ============================================

def binary_files():
    """二进制文件"""
    print("\n=== 二进制文件 ===")
    
    # 写入二进制
    print("1. 写入二进制:")
    data = b'Binary data \x00\x01\x02'
    with open('/tmp/binary.dat', 'wb') as f:
        f.write(data)
    print(f"  写入 {len(data)} 字节")
    
    # 读取二进制
    print("\n2. 读取二进制:")
    with open('/tmp/binary.dat', 'rb') as f:
        content = f.read()
        print(f"  读取: {content}")
    
    # 图片复制示例
    print("\n3. 复制二进制文件:")
    # 创建测试文件
    with open('/tmp/source.bin', 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' * 100)
    
    # 复制
    with open('/tmp/source.bin', 'rb') as src:
        with open('/tmp/dest.bin', 'wb') as dst:
            dst.write(src.read())
    
    print("  文件已复制")


# ============================================
# 3. 文件位置与seek
# ============================================

def file_position():
    """文件位置操作"""
    print("\n=== 文件位置操作 ===")
    
    # 创建测试文件
    with open('/tmp/position.txt', 'w') as f:
        f.write("0123456789ABCDEFGHIJ")
    
    with open('/tmp/position.txt', 'r') as f:
        # tell() - 当前位置
        print(f"1. 当前位置: {f.tell()}")
        
        # read(5)
        data = f.read(5)
        print(f"2. 读取5字节: {data}, 位置: {f.tell()}")
        
        # seek() - 移动位置
        f.seek(0)  # 移到开头
        print(f"3. seek(0), 位置: {f.tell()}")
        
        f.seek(10)  # 移到第10个字节
        data = f.read(5)
        print(f"4. seek(10), 读取: {data}")
        
        # 从末尾seek
        f.seek(-5, 2)  # 从末尾往前5字节
        data = f.read()
        print(f"5. 从末尾-5: {data}")


# ============================================
# 4. pathlib - 现代路径操作
# ============================================

def pathlib_demo():
    """pathlib 路径操作"""
    print("\n=== pathlib 路径操作 ===")
    
    # 创建路径
    print("1. 创建路径:")
    p = Path('/tmp/test_dir')
    print(f"  路径: {p}")
    print(f"  绝对路径: {p.absolute()}")
    
    # 路径拼接
    print("\n2. 路径拼接:")
    file_path = p / 'subdir' / 'file.txt'
    print(f"  拼接: {file_path}")
    
    # 路径属性
    print("\n3. 路径属性:")
    path = Path('/tmp/example.txt')
    print(f"  名称: {path.name}")
    print(f"  后缀: {path.suffix}")
    print(f"  stem: {path.stem}")
    print(f"  父目录: {path.parent}")
    print(f"  部分: {path.parts}")
    
    # 路径操作
    print("\n4. 路径检查:")
    path = Path('/tmp')
    print(f"  存在: {path.exists()}")
    print(f"  是文件: {path.is_file()}")
    print(f"  是目录: {path.is_dir()}")
    
    # 创建目录
    print("\n5. 创建目录:")
    test_dir = Path('/tmp/test_pathlib')
    test_dir.mkdir(parents=True, exist_ok=True)
    print(f"  创建: {test_dir}")
    
    # 写入文件
    file = test_dir / 'test.txt'
    file.write_text("Hello from pathlib!", encoding='utf-8')
    print(f"  写入: {file}")
    
    # 读取文件
    content = file.read_text(encoding='utf-8')
    print(f"  读取: {content}")
    
    # 遍历目录
    print("\n6. 遍历目录:")
    Path('/tmp/test_pathlib/file1.txt').touch()
    Path('/tmp/test_pathlib/file2.txt').touch()
    
    for item in Path('/tmp/test_pathlib').iterdir():
        print(f"  {item.name}")
    
    # glob 模式
    print("\n7. glob 模式:")
    for txt_file in Path('/tmp/test_pathlib').glob('*.txt'):
        print(f"  {txt_file.name}")


# ============================================
# 5. os 和 os.path
# ============================================

def os_operations():
    """os 模块操作"""
    print("\n=== os 模块操作 ===")
    
    # 当前目录
    print("1. 当前目录:")
    print(f"  {os.getcwd()}")
    
    # 列出目录
    print("\n2. 列出目录:")
    files = os.listdir('/tmp')
    print(f"  /tmp 下文件数: {len(files)}")
    print(f"  前5个: {files[:5]}")
    
    # 创建目录
    print("\n3. 创建目录:")
    os.makedirs('/tmp/test_os/sub', exist_ok=True)
    print("  目录已创建")
    
    # 路径操作
    print("\n4. os.path 操作:")
    path = '/tmp/test_os/file.txt'
    print(f"  dirname: {os.path.dirname(path)}")
    print(f"  basename: {os.path.basename(path)}")
    print(f"  split: {os.path.split(path)}")
    print(f"  join: {os.path.join('/tmp', 'test', 'file.txt')}")
    
    # 路径检查
    print("\n5. 路径检查:")
    print(f"  exists: {os.path.exists('/tmp')}")
    print(f"  isfile: {os.path.isfile('/tmp')}")
    print(f"  isdir: {os.path.isdir('/tmp')}")
    
    # 文件信息
    print("\n6. 文件信息:")
    with open('/tmp/test_info.txt', 'w') as f:
        f.write("test")
    
    stat = os.stat('/tmp/test_info.txt')
    print(f"  大小: {stat.st_size} 字节")
    print(f"  修改时间: {stat.st_mtime}")
    
    # 环境变量
    print("\n7. 环境变量:")
    print(f"  PATH: {os.environ.get('PATH', 'N/A')[:50]}...")


# ============================================
# 6. JSON 文件
# ============================================

def json_operations():
    """JSON 操作"""
    print("\n=== JSON 操作 ===")
    
    # Python 对象
    data = {
        "name": "Alice",
        "age": 25,
        "city": "Beijing",
        "hobbies": ["reading", "coding"],
        "is_active": True
    }
    
    # 写入 JSON
    print("1. 写入 JSON:")
    with open('/tmp/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("  JSON 已写入")
    
    # 读取 JSON
    print("\n2. 读取 JSON:")
    with open('/tmp/data.json', 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
        print(f"  {loaded_data}")
    
    # 字符串转换
    print("\n3. 字符串转换:")
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print(f"  JSON字符串:\n{json_str}")
    
    parsed = json.loads(json_str)
    print(f"  解析: {parsed['name']}")
    
    # 自定义序列化
    print("\n4. 自定义序列化:")
    from datetime import datetime
    
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return super().default(obj)
    
    data_with_date = {
        "event": "Meeting",
        "time": datetime.now()
    }
    
    json_str = json.dumps(data_with_date, cls=DateTimeEncoder)
    print(f"  {json_str}")


# ============================================
# 7. CSV 文件
# ============================================

def csv_operations():
    """CSV 操作"""
    print("\n=== CSV 操作 ===")
    
    # 写入 CSV
    print("1. 写入 CSV:")
    with open('/tmp/data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Age', 'City'])
        writer.writerow(['Alice', 25, 'Beijing'])
        writer.writerow(['Bob', 30, 'Shanghai'])
        writer.writerow(['Charlie', 35, 'Guangzhou'])
    print("  CSV 已写入")
    
    # 读取 CSV
    print("\n2. 读取 CSV:")
    with open('/tmp/data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(f"  {row}")
    
    # 字典写入
    print("\n3. 字典写入 CSV:")
    with open('/tmp/dict_data.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'age', 'city']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow({'name': 'Alice', 'age': 25, 'city': 'Beijing'})
        writer.writerow({'name': 'Bob', 'age': 30, 'city': 'Shanghai'})
    print("  字典CSV已写入")
    
    # 字典读取
    print("\n4. 字典读取 CSV:")
    with open('/tmp/dict_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"  {row}")


# ============================================
# 8. pickle - 序列化
# ============================================

def pickle_operations():
    """pickle 序列化"""
    print("\n=== pickle 序列化 ===")
    
    # Python 对象
    data = {
        "numbers": [1, 2, 3, 4, 5],
        "tuple": (10, 20, 30),
        "set": {1, 2, 3},
        "nested": {"a": 1, "b": [2, 3]}
    }
    
    # 序列化
    print("1. 序列化:")
    with open('/tmp/data.pickle', 'wb') as f:
        pickle.dump(data, f)
    print("  对象已序列化")
    
    # 反序列化
    print("\n2. 反序列化:")
    with open('/tmp/data.pickle', 'rb') as f:
        loaded_data = pickle.load(f)
        print(f"  {loaded_data}")
    
    # 序列化自定义类
    print("\n3. 序列化自定义类:")
    
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        
        def __repr__(self):
            return f"Person('{self.name}', {self.age})"
    
    person = Person("Alice", 25)
    
    # 保存
    with open('/tmp/person.pickle', 'wb') as f:
        pickle.dump(person, f)
    
    # 加载
    with open('/tmp/person.pickle', 'rb') as f:
        loaded_person = pickle.load(f)
        print(f"  {loaded_person}")


# ============================================
# 9. 临时文件
# ============================================

def temp_files():
    """临时文件"""
    print("\n=== 临时文件 ===")
    
    # 临时文件
    print("1. 临时文件:")
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("临时内容")
        temp_path = f.name
        print(f"  临时文件: {temp_path}")
    
    # 读取临时文件
    with open(temp_path, 'r') as f:
        print(f"  内容: {f.read()}")
    
    # 清理
    os.unlink(temp_path)
    
    # 临时目录
    print("\n2. 临时目录:")
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"  临时目录: {tmpdir}")
        
        # 在临时目录中创建文件
        file_path = Path(tmpdir) / 'test.txt'
        file_path.write_text("测试")
        print(f"  创建文件: {file_path}")
    
    print("  临时目录已自动清理")


# ============================================
# 10. 文件操作
# ============================================

def file_operations():
    """文件操作"""
    print("\n=== 文件操作 ===")
    
    # 复制文件
    print("1. 复制文件:")
    with open('/tmp/source.txt', 'w') as f:
        f.write("源文件内容")
    
    shutil.copy('/tmp/source.txt', '/tmp/dest.txt')
    print("  文件已复制")
    
    # 移动文件
    print("\n2. 移动/重命名:")
    shutil.move('/tmp/dest.txt', '/tmp/renamed.txt')
    print("  文件已移动")
    
    # 删除文件
    print("\n3. 删除文件:")
    os.remove('/tmp/renamed.txt')
    print("  文件已删除")
    
    # 复制目录树
    print("\n4. 复制目录:")
    os.makedirs('/tmp/source_dir/sub', exist_ok=True)
    Path('/tmp/source_dir/file.txt').write_text("test")
    
    if os.path.exists('/tmp/dest_dir'):
        shutil.rmtree('/tmp/dest_dir')
    
    shutil.copytree('/tmp/source_dir', '/tmp/dest_dir')
    print("  目录已复制")
    
    # 删除目录
    print("\n5. 删除目录:")
    shutil.rmtree('/tmp/dest_dir')
    print("  目录已删除")


# ============================================
# 11. 实战示例
# ============================================

def practical_examples():
    """实战示例"""
    print("\n=== 实战示例 ===")
    
    # 1. 读取配置文件
    print("1. 读取配置文件:")
    config = {
        "server": {
            "host": "localhost",
            "port": 8080
        },
        "database": {
            "url": "postgresql://localhost/db"
        }
    }
    
    with open('/tmp/config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    with open('/tmp/config.json', 'r') as f:
        loaded_config = json.load(f)
        print(f"  服务器: {loaded_config['server']['host']}:{loaded_config['server']['port']}")
    
    # 2. 处理 CSV 数据
    print("\n2. 处理 CSV 数据:")
    
    # 写入测试数据
    with open('/tmp/sales.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['product', 'quantity', 'price'])
        writer.writeheader()
        writer.writerows([
            {'product': 'A', 'quantity': 10, 'price': 100},
            {'product': 'B', 'quantity': 5, 'price': 200},
            {'product': 'C', 'quantity': 8, 'price': 150},
        ])
    
    # 读取并计算
    total = 0
    with open('/tmp/sales.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            subtotal = int(row['quantity']) * float(row['price'])
            total += subtotal
            print(f"  {row['product']}: {subtotal}")
    
    print(f"  总计: {total}")
    
    # 3. 日志文件
    print("\n3. 追加日志:")
    
    def log_message(message):
        """记录日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/app.log', 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    log_message("应用启动")
    log_message("处理请求")
    log_message("应用关闭")
    
    # 读取日志
    with open('/tmp/app.log', 'r') as f:
        print(f"  日志内容:")
        for line in f:
            print(f"    {line.strip()}")
    
    # 4. 文件搜索
    print("\n4. 搜索文件:")
    
    def find_files(directory, pattern):
        """查找文件"""
        results = []
        for path in Path(directory).rglob(pattern):
            results.append(path)
        return results
    
    txt_files = find_files('/tmp', '*.txt')
    print(f"  找到 {len(txt_files)} 个 .txt 文件")
    for f in txt_files[:5]:
        print(f"    {f}")


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""
    print("=" * 60)
    print("Python IO 操作详解")
    print("=" * 60)
    
    file_basics()
    file_modes()
    binary_files()
    file_position()
    
    pathlib_demo()
    os_operations()
    
    json_operations()
    csv_operations()
    pickle_operations()
    
    temp_files()
    file_operations()
    practical_examples()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

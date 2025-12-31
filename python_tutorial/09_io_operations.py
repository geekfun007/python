"""
Python IO 操作详解 (with Type Hints)
====================================

本文件涵盖：
- 文件读写
- 文本与二进制
- 路径操作 (pathlib)
- JSON/CSV/YAML 处理
- pickle 序列化
- 临时文件
- 压缩文件
"""

from typing import Any, Iterator, BinaryIO, TextIO
from pathlib import Path
from io import StringIO, BytesIO
import os
import shutil
import json
import csv
import pickle
import tempfile
import gzip
import zipfile
import tarfile
from contextlib import contextmanager
from dataclasses import dataclass, asdict

# ============================================================================
# 1. 基本文件操作
# ============================================================================

class BasicFileDemo:
    """基本文件操作"""
    
    @staticmethod
    def write_text_file(path: Path) -> None:
        """写入文本文件"""
        # 方式 1: 使用 with 语句（推荐）
        with open(path, 'w', encoding='utf-8') as f:
            f.write("Hello, World!\n")
            f.write("你好，世界！\n")
            
            # 写入多行
            lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
            f.writelines(lines)
        
        print(f"Written to {path}")
    
    @staticmethod
    def read_text_file(path: Path) -> str:
        """读取文本文件"""
        # 一次读取全部
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Content ({len(content)} chars):")
        print(content)
        return content
    
    @staticmethod
    def read_file_lines(path: Path) -> list[str]:
        """逐行读取"""
        # 方式 1: readlines()
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()  # 包含换行符
        
        print(f"Lines (with newlines): {lines}")
        
        # 方式 2: 迭代（内存友好）
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                print(f"Line {i}: {line.rstrip()}")
        
        # 方式 3: 去除换行符
        with open(path, 'r', encoding='utf-8') as f:
            clean_lines = [line.rstrip('\n') for line in f]
        
        return clean_lines
    
    @staticmethod
    def append_to_file(path: Path, text: str) -> None:
        """追加内容"""
        with open(path, 'a', encoding='utf-8') as f:
            f.write(text)
        print(f"Appended to {path}")
    
    @staticmethod
    def binary_file_operations(path: Path) -> None:
        """二进制文件操作"""
        # 写入二进制数据
        data = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])  # "Hello"
        with open(path, 'wb') as f:
            f.write(data)
        
        # 读取二进制数据
        with open(path, 'rb') as f:
            content = f.read()
        
        print(f"Binary content: {content}")
        print(f"As string: {content.decode('utf-8')}")
    
    @staticmethod
    def file_modes() -> None:
        """文件打开模式"""
        modes = {
            'r':  '只读（默认）',
            'w':  '写入（覆盖）',
            'a':  '追加',
            'x':  '排他创建（文件存在则失败）',
            'r+': '读写',
            'w+': '读写（覆盖）',
            'a+': '读写（追加）',
            'rb': '二进制读',
            'wb': '二进制写',
        }
        
        print("File open modes:")
        for mode, desc in modes.items():
            print(f"  '{mode}': {desc}")


# ============================================================================
# 2. pathlib 路径操作
# ============================================================================

class PathlibDemo:
    """pathlib 路径操作"""
    
    @staticmethod
    def path_creation() -> None:
        """创建路径"""
        # 创建 Path 对象
        p1 = Path("/home/user/documents")
        p2 = Path("relative/path/file.txt")
        
        # 当前目录和主目录
        cwd = Path.cwd()
        home = Path.home()
        
        print(f"Current directory: {cwd}")
        print(f"Home directory: {home}")
        
        # 路径拼接
        p3 = Path("/home/user") / "documents" / "file.txt"
        print(f"Joined path: {p3}")
        
        # 从字符串创建
        p4 = Path("/path/to/file.txt")
        print(f"Path from string: {p4}")
    
    @staticmethod
    def path_parts() -> None:
        """路径组成部分"""
        p = Path("/home/user/documents/report.pdf")
        
        print(f"Path: {p}")
        print(f"  parent: {p.parent}")
        print(f"  parents: {list(p.parents)}")
        print(f"  name: {p.name}")
        print(f"  stem: {p.stem}")
        print(f"  suffix: {p.suffix}")
        print(f"  suffixes: {p.suffixes}")
        print(f"  parts: {p.parts}")
        print(f"  anchor: {p.anchor}")
        
        # 多后缀
        p2 = Path("archive.tar.gz")
        print(f"\nPath: {p2}")
        print(f"  stem: {p2.stem}")
        print(f"  suffixes: {p2.suffixes}")
    
    @staticmethod
    def path_methods() -> None:
        """路径方法"""
        p = Path(".")
        
        # 解析为绝对路径
        print(f"resolve(): {p.resolve()}")
        
        # 检查
        print(f"exists(): {p.exists()}")
        print(f"is_file(): {p.is_file()}")
        print(f"is_dir(): {p.is_dir()}")
        print(f"is_absolute(): {p.is_absolute()}")
        
        # 修改路径
        p2 = Path("document.txt")
        print(f"\nOriginal: {p2}")
        print(f"  with_name('new.txt'): {p2.with_name('new.txt')}")
        print(f"  with_stem('report'): {p2.with_stem('report')}")
        print(f"  with_suffix('.md'): {p2.with_suffix('.md')}")
    
    @staticmethod
    def directory_operations(base: Path) -> None:
        """目录操作"""
        # 创建目录
        new_dir = base / "new_directory"
        new_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {new_dir}")
        
        # 列出内容
        print(f"\nContents of {base}:")
        for item in base.iterdir():
            item_type = "dir" if item.is_dir() else "file"
            print(f"  [{item_type}] {item.name}")
        
        # 递归查找
        print(f"\nAll Python files in {base}:")
        for py_file in base.rglob("*.py"):
            print(f"  {py_file}")
        
        # 使用 glob 模式
        print(f"\nFiles matching pattern '*.txt':")
        for txt_file in base.glob("*.txt"):
            print(f"  {txt_file}")
    
    @staticmethod
    def file_operations_with_path(path: Path) -> None:
        """使用 Path 进行文件操作"""
        # 写入
        path.write_text("Hello from pathlib!\n你好！\n", encoding='utf-8')
        
        # 读取
        content = path.read_text(encoding='utf-8')
        print(f"Content: {content}")
        
        # 二进制
        binary_path = path.with_suffix('.bin')
        binary_path.write_bytes(b'\x00\x01\x02\x03')
        data = binary_path.read_bytes()
        print(f"Binary data: {data}")
        
        # 文件信息
        stat = path.stat()
        print(f"\nFile stats for {path}:")
        print(f"  Size: {stat.st_size} bytes")
        print(f"  Modified: {stat.st_mtime}")
        
        # 清理
        binary_path.unlink()


# ============================================================================
# 3. JSON 处理
# ============================================================================

class JSONDemo:
    """JSON 处理"""
    
    @staticmethod
    def basic_json() -> None:
        """基本 JSON 操作"""
        # Python 对象 -> JSON 字符串
        data = {
            "name": "Alice",
            "age": 30,
            "emails": ["alice@example.com", "alice@work.com"],
            "address": {
                "city": "New York",
                "zip": "10001"
            },
            "active": True,
            "balance": None
        }
        
        # 序列化
        json_str = json.dumps(data)
        print(f"JSON string: {json_str}")
        
        # 格式化输出
        json_pretty = json.dumps(data, indent=2, ensure_ascii=False)
        print(f"\nPretty JSON:\n{json_pretty}")
        
        # 反序列化
        parsed = json.loads(json_str)
        print(f"\nParsed data: {parsed}")
        print(f"Type: {type(parsed)}")
    
    @staticmethod
    def json_file_operations(path: Path) -> None:
        """JSON 文件操作"""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
            ]
        }
        
        # 写入 JSON 文件
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Written JSON to {path}")
        
        # 读取 JSON 文件
        with open(path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        print(f"Loaded from file: {loaded}")
    
    @staticmethod
    def custom_json_encoder() -> None:
        """自定义 JSON 编码器"""
        from datetime import datetime, date
        from dataclasses import dataclass, asdict
        
        @dataclass
        class User:
            id: int
            name: str
            created_at: datetime
        
        class CustomEncoder(json.JSONEncoder):
            def default(self, obj: Any) -> Any:
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, date):
                    return obj.isoformat()
                if hasattr(obj, '__dict__'):
                    return obj.__dict__
                return super().default(obj)
        
        user = User(1, "Alice", datetime.now())
        
        # 使用自定义编码器
        json_str = json.dumps(user, cls=CustomEncoder, indent=2)
        print(f"Custom encoded JSON:\n{json_str}")
        
        # 使用 default 函数
        def encode_special(obj: Any) -> Any:
            if isinstance(obj, datetime):
                return {"__datetime__": obj.isoformat()}
            if isinstance(obj, set):
                return {"__set__": list(obj)}
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        data = {
            "timestamp": datetime.now(),
            "tags": {"python", "json", "tutorial"}
        }
        
        json_str = json.dumps(data, default=encode_special, indent=2)
        print(f"\nWith special encoding:\n{json_str}")


# ============================================================================
# 4. CSV 处理
# ============================================================================

class CSVDemo:
    """CSV 处理"""
    
    @staticmethod
    def write_csv(path: Path) -> None:
        """写入 CSV"""
        # 使用 writer
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入标题
            writer.writerow(['Name', 'Age', 'City'])
            
            # 写入数据
            writer.writerow(['Alice', 30, 'New York'])
            writer.writerow(['Bob', 25, 'Los Angeles'])
            
            # 写入多行
            writer.writerows([
                ['Charlie', 35, 'Chicago'],
                ['Diana', 28, 'Houston'],
            ])
        
        print(f"Written CSV to {path}")
    
    @staticmethod
    def read_csv(path: Path) -> list[list[str]]:
        """读取 CSV"""
        with open(path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # 跳过标题
            header = next(reader)
            print(f"Header: {header}")
            
            rows = list(reader)
            for row in rows:
                print(f"Row: {row}")
        
        return rows
    
    @staticmethod
    def dict_csv(path: Path) -> None:
        """使用字典操作 CSV"""
        # 写入
        fieldnames = ['name', 'age', 'city']
        
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerow({'name': 'Alice', 'age': 30, 'city': 'NYC'})
            writer.writerow({'name': 'Bob', 'age': 25, 'city': 'LA'})
        
        # 读取
        print("\nReading with DictReader:")
        with open(path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                print(f"  {row['name']}, {row['age']}, {row['city']}")
    
    @staticmethod
    def csv_dialects() -> None:
        """CSV 方言"""
        # 查看内置方言
        print("Built-in dialects:")
        for name in csv.list_dialects():
            print(f"  {name}")
        
        # 自定义方言
        csv.register_dialect(
            'custom',
            delimiter='|',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )
        
        # 使用 Sniffer 检测方言
        sample = 'Name|Age|City\nAlice|30|NYC\n'
        dialect = csv.Sniffer().sniff(sample)
        print(f"\nDetected delimiter: {dialect.delimiter!r}")


# ============================================================================
# 5. Pickle 序列化
# ============================================================================

class PickleDemo:
    """Pickle 序列化"""
    
    @staticmethod
    def basic_pickle(path: Path) -> None:
        """基本 pickle 操作"""
        # 复杂 Python 对象
        data = {
            "numbers": [1, 2, 3, 4, 5],
            "nested": {"a": [1, 2], "b": {"c": 3}},
            "tuple": (1, "two", 3.0),
            "set": {1, 2, 3},
        }
        
        # 序列化到文件
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        print(f"Pickled to {path}")
        
        # 从文件反序列化
        with open(path, 'rb') as f:
            loaded = pickle.load(f)
        print(f"Loaded: {loaded}")
        
        # 序列化到字节
        pickled_bytes = pickle.dumps(data)
        print(f"Pickled bytes length: {len(pickled_bytes)}")
        
        # 从字节反序列化
        unpickled = pickle.loads(pickled_bytes)
        print(f"Unpickled: {unpickled}")
    
    @staticmethod
    def pickle_custom_class() -> None:
        """序列化自定义类"""
        @dataclass
        class Person:
            name: str
            age: int
            friends: list[str]
        
        person = Person("Alice", 30, ["Bob", "Charlie"])
        
        # 序列化
        pickled = pickle.dumps(person)
        
        # 反序列化
        restored: Person = pickle.loads(pickled)
        print(f"Restored person: {restored}")
        print(f"Same type: {type(restored) == Person}")


# ============================================================================
# 6. 临时文件
# ============================================================================

class TempFileDemo:
    """临时文件操作"""
    
    @staticmethod
    def temp_file() -> None:
        """临时文件"""
        # 命名临时文件
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            prefix='mytemp_',
            delete=False  # 保留文件用于演示
        ) as f:
            f.write("Temporary content\n")
            print(f"Temp file: {f.name}")
            temp_path = f.name
        
        # 文件在 with 块外仍然存在
        print(f"File exists: {os.path.exists(temp_path)}")
        
        # 手动删除
        os.unlink(temp_path)
    
    @staticmethod
    def temp_directory() -> None:
        """临时目录"""
        with tempfile.TemporaryDirectory(prefix='mydir_') as tmpdir:
            print(f"Temp directory: {tmpdir}")
            
            # 在临时目录中创建文件
            temp_file = Path(tmpdir) / "test.txt"
            temp_file.write_text("Test content")
            
            print(f"Created: {temp_file}")
            print(f"Content: {temp_file.read_text()}")
        
        # 目录和内容自动删除
        print(f"Directory exists: {os.path.exists(tmpdir)}")  # False
    
    @staticmethod
    def spooled_temp_file() -> None:
        """内存中的临时文件"""
        # 小于 max_size 时在内存中，超过后写入磁盘
        with tempfile.SpooledTemporaryFile(
            max_size=1024,
            mode='w+t'
        ) as f:
            f.write("This is in memory\n")
            f.seek(0)
            print(f"Content: {f.read()}")


# ============================================================================
# 7. 压缩文件
# ============================================================================

class CompressionDemo:
    """压缩文件操作"""
    
    @staticmethod
    def gzip_operations(base_path: Path) -> None:
        """Gzip 操作"""
        gz_path = base_path / "test.txt.gz"
        
        # 压缩写入
        with gzip.open(gz_path, 'wt', encoding='utf-8') as f:
            f.write("This is compressed content.\n")
            f.write("Line 2\n")
        
        print(f"Written gzip file: {gz_path}")
        
        # 解压读取
        with gzip.open(gz_path, 'rt', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Content: {content}")
        
        # 压缩字节
        original = b"Hello, World! " * 100
        compressed = gzip.compress(original)
        decompressed = gzip.decompress(compressed)
        
        print(f"Original size: {len(original)}")
        print(f"Compressed size: {len(compressed)}")
        print(f"Compression ratio: {len(compressed)/len(original):.2%}")
        print(f"Decompressed matches: {original == decompressed}")
        
        # 清理
        gz_path.unlink()
    
    @staticmethod
    def zip_operations(base_path: Path) -> None:
        """Zip 操作"""
        zip_path = base_path / "archive.zip"
        
        # 创建 zip 文件
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 添加文件
            zf.writestr('file1.txt', 'Content of file 1')
            zf.writestr('file2.txt', 'Content of file 2')
            zf.writestr('subdir/file3.txt', 'Content in subdirectory')
        
        print(f"Created zip: {zip_path}")
        
        # 读取 zip 文件
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # 列出内容
            print("\nZip contents:")
            for info in zf.infolist():
                print(f"  {info.filename}: {info.file_size} bytes")
            
            # 读取特定文件
            content = zf.read('file1.txt').decode('utf-8')
            print(f"\nfile1.txt content: {content}")
            
            # 解压全部
            extract_dir = base_path / "extracted"
            zf.extractall(extract_dir)
            print(f"Extracted to: {extract_dir}")
        
        # 清理
        zip_path.unlink()
        shutil.rmtree(extract_dir)
    
    @staticmethod
    def tar_operations(base_path: Path) -> None:
        """Tar 操作"""
        tar_path = base_path / "archive.tar.gz"
        
        # 创建 tar.gz 文件
        with tarfile.open(tar_path, 'w:gz') as tf:
            # 添加字符串内容
            import io
            
            data = b"Content of the file"
            tarinfo = tarfile.TarInfo(name='file.txt')
            tarinfo.size = len(data)
            tf.addfile(tarinfo, io.BytesIO(data))
        
        print(f"Created tar.gz: {tar_path}")
        
        # 读取 tar 文件
        with tarfile.open(tar_path, 'r:gz') as tf:
            print("\nTar contents:")
            for member in tf.getmembers():
                print(f"  {member.name}: {member.size} bytes")
            
            # 读取文件内容
            f = tf.extractfile('file.txt')
            if f:
                content = f.read().decode('utf-8')
                print(f"\nfile.txt content: {content}")
        
        # 清理
        tar_path.unlink()


# ============================================================================
# 8. StringIO 和 BytesIO
# ============================================================================

class MemoryIODemo:
    """内存 IO 操作"""
    
    @staticmethod
    def string_io() -> None:
        """StringIO - 内存中的文本文件"""
        # 写入
        buffer = StringIO()
        buffer.write("Hello, ")
        buffer.write("World!\n")
        buffer.writelines(["Line 1\n", "Line 2\n"])
        
        # 获取全部内容
        content = buffer.getvalue()
        print(f"StringIO content: {content}")
        
        # 读取
        buffer.seek(0)  # 回到开始
        first_line = buffer.readline()
        print(f"First line: {first_line}")
        
        # 用于需要文件对象的函数
        buffer = StringIO("Name,Age\nAlice,30\nBob,25\n")
        reader = csv.reader(buffer)
        for row in reader:
            print(f"CSV row: {row}")
    
    @staticmethod
    def bytes_io() -> None:
        """BytesIO - 内存中的二进制文件"""
        # 写入
        buffer = BytesIO()
        buffer.write(b"Binary data: ")
        buffer.write(bytes([0x00, 0x01, 0x02, 0x03]))
        
        # 获取内容
        content = buffer.getvalue()
        print(f"BytesIO content: {content}")
        
        # 用于图像处理等场景
        from io import BytesIO
        
        # 模拟：创建一个简单的二进制结构
        buffer = BytesIO()
        buffer.write(b'\x89PNG')  # PNG 魔数开始
        buffer.write(b'\r\n\x1a\n')  # PNG 魔数结束
        
        # 读取验证
        buffer.seek(0)
        header = buffer.read(8)
        print(f"PNG-like header: {header}")


# ============================================================================
# 主函数
# ============================================================================

def main() -> None:
    """主函数"""
    # 创建工作目录
    work_dir = Path("./io_demo_temp")
    work_dir.mkdir(exist_ok=True)
    
    try:
        print("=" * 60)
        print("BASIC FILE OPERATIONS")
        print("=" * 60)
        
        text_file = work_dir / "test.txt"
        BasicFileDemo.write_text_file(text_file)
        BasicFileDemo.read_text_file(text_file)
        BasicFileDemo.read_file_lines(text_file)
        BasicFileDemo.append_to_file(text_file, "Appended line\n")
        BasicFileDemo.file_modes()
        
        print("\n" + "=" * 60)
        print("PATHLIB DEMO")
        print("=" * 60)
        
        PathlibDemo.path_creation()
        print()
        PathlibDemo.path_parts()
        print()
        PathlibDemo.path_methods()
        print()
        PathlibDemo.directory_operations(work_dir)
        print()
        
        path_file = work_dir / "pathlib_test.txt"
        PathlibDemo.file_operations_with_path(path_file)
        
        print("\n" + "=" * 60)
        print("JSON DEMO")
        print("=" * 60)
        
        JSONDemo.basic_json()
        print()
        json_file = work_dir / "data.json"
        JSONDemo.json_file_operations(json_file)
        print()
        JSONDemo.custom_json_encoder()
        
        print("\n" + "=" * 60)
        print("CSV DEMO")
        print("=" * 60)
        
        csv_file = work_dir / "data.csv"
        CSVDemo.write_csv(csv_file)
        print()
        CSVDemo.read_csv(csv_file)
        print()
        CSVDemo.dict_csv(csv_file)
        print()
        CSVDemo.csv_dialects()
        
        print("\n" + "=" * 60)
        print("PICKLE DEMO")
        print("=" * 60)
        
        pickle_file = work_dir / "data.pkl"
        PickleDemo.basic_pickle(pickle_file)
        print()
        PickleDemo.pickle_custom_class()
        
        print("\n" + "=" * 60)
        print("TEMP FILE DEMO")
        print("=" * 60)
        
        TempFileDemo.temp_file()
        print()
        TempFileDemo.temp_directory()
        
        print("\n" + "=" * 60)
        print("COMPRESSION DEMO")
        print("=" * 60)
        
        CompressionDemo.gzip_operations(work_dir)
        print()
        CompressionDemo.zip_operations(work_dir)
        print()
        CompressionDemo.tar_operations(work_dir)
        
        print("\n" + "=" * 60)
        print("MEMORY IO DEMO")
        print("=" * 60)
        
        MemoryIODemo.string_io()
        print()
        MemoryIODemo.bytes_io()
        
    finally:
        # 清理工作目录
        shutil.rmtree(work_dir, ignore_errors=True)
        print(f"\nCleaned up {work_dir}")


if __name__ == "__main__":
    main()

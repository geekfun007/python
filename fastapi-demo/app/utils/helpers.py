"""
Helper Functions
通用工具函数
"""

import re
import string
import secrets
from datetime import datetime
from typing import List, TypeVar, Generic
from unicodedata import normalize


T = TypeVar("T")


def generate_random_string(length: int = 32) -> str:
    """
    生成随机字符串
    
    Args:
        length: 字符串长度
    
    Returns:
        随机字符串
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def slugify(text: str, max_length: int = 50) -> str:
    """
    将文本转换为 URL 友好的 slug
    
    Args:
        text: 原始文本
        max_length: 最大长度
    
    Returns:
        slug 字符串
    
    Example:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("你好，世界")
        'ni-hao-shi-jie'
    """
    # 转小写
    text = text.lower()
    
    # 规范化 Unicode
    text = normalize('NFKD', text)
    
    # 只保留字母数字和空格
    text = re.sub(r'[^\w\s-]', '', text)
    
    # 空格替换为连字符
    text = re.sub(r'[-\s]+', '-', text)
    
    # 去除首尾连字符
    text = text.strip('-')
    
    # 限制长度
    return text[:max_length]


def paginate(
    items: List[T],
    page: int,
    page_size: int
) -> tuple[List[T], int]:
    """
    对列表进行分页
    
    Args:
        items: 完整列表
        page: 页码（从1开始）
        page_size: 每页数量
    
    Returns:
        (分页后的列表, 总数)
    """
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    
    return items[start:end], total


def format_datetime(
    dt: datetime,
    format_str: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    格式化日期时间
    
    Args:
        dt: datetime 对象
        format_str: 格式字符串
    
    Returns:
        格式化后的字符串
    """
    if dt is None:
        return ""
    return dt.strftime(format_str)


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断字符串
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀
    
    Returns:
        截断后的字符串
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def mask_email(email: str) -> str:
    """
    隐藏邮箱部分字符
    
    Args:
        email: 邮箱地址
    
    Returns:
        隐藏后的邮箱
    
    Example:
        >>> mask_email("john@example.com")
        'j***@example.com'
    """
    if not email or "@" not in email:
        return email
    
    local, domain = email.split("@")
    
    if len(local) <= 1:
        return f"*@{domain}"
    
    return f"{local[0]}{'*' * (len(local) - 1)}@{domain}"


def mask_phone(phone: str) -> str:
    """
    隐藏手机号中间几位
    
    Args:
        phone: 手机号
    
    Returns:
        隐藏后的手机号
    
    Example:
        >>> mask_phone("13812345678")
        '138****5678'
    """
    if not phone or len(phone) < 7:
        return phone
    
    return f"{phone[:3]}****{phone[-4:]}"

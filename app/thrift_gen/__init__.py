"""
Thrift IDL 生成模块
使用 thriftpy2 动态加载 .thrift 文件
"""
import os
from pathlib import Path

import thriftpy2

# IDL 文件目录
IDL_DIR = Path(__file__).parent.parent.parent / "idl"

# 动态加载 Thrift 模块
common_thrift = thriftpy2.load(
    str(IDL_DIR / "common.thrift"),
    module_name="common_thrift",
)

user_thrift = thriftpy2.load(
    str(IDL_DIR / "user.thrift"),
    module_name="user_thrift",
    include_dirs=[str(IDL_DIR)],
)

item_thrift = thriftpy2.load(
    str(IDL_DIR / "item.thrift"),
    module_name="item_thrift",
    include_dirs=[str(IDL_DIR)],
)

# 导出常用类型
__all__ = [
    "common_thrift",
    "user_thrift",
    "item_thrift",
    # Common types
    "ErrorCode",
    "BaseResponse",
    "PaginationRequest",
    "PaginationInfo",
    # User types
    "UserStatus",
    "UserRole",
    "UserInfo",
    "TokenInfo",
    # Item types
    "ItemStatus",
    "ItemCategory",
    "ItemInfo",
    "PriceInfo",
    "StockInfo",
]

# Common types
ErrorCode = common_thrift.ErrorCode
BaseResponse = common_thrift.BaseResponse
PaginationRequest = common_thrift.PaginationRequest
PaginationInfo = common_thrift.PaginationInfo
TimeRange = common_thrift.TimeRange

# User types
UserStatus = user_thrift.UserStatus
UserRole = user_thrift.UserRole
UserInfo = user_thrift.UserInfo
UserDetail = user_thrift.UserDetail
TokenInfo = user_thrift.TokenInfo
RegisterRequest = user_thrift.RegisterRequest
RegisterResponse = user_thrift.RegisterResponse
LoginRequest = user_thrift.LoginRequest
LoginResponse = user_thrift.LoginResponse

# Item types
ItemStatus = item_thrift.ItemStatus
ItemCategory = item_thrift.ItemCategory
ItemInfo = item_thrift.ItemInfo
ItemDetail = item_thrift.ItemDetail
PriceInfo = item_thrift.PriceInfo
StockInfo = item_thrift.StockInfo

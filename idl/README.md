# Thrift IDL 定义

本目录包含项目的 Thrift 接口定义语言 (IDL) 文件。

## 📁 文件结构

```
idl/
├── common.thrift    # 通用数据类型（响应、分页、错误码等）
├── user.thrift      # 用户服务接口定义
├── item.thrift      # 物品服务接口定义
└── README.md        # 本文档
```

## 📖 IDL 文件说明

### common.thrift

通用数据类型定义，包括：

- `ErrorCode` - 错误码枚举
- `BaseResponse` - 统一响应结构
- `PaginationRequest` - 分页请求参数
- `PaginationInfo` - 分页响应信息
- `TimeRange` - 时间范围查询

### user.thrift

用户服务接口定义，包括：

**枚举类型:**
- `UserStatus` - 用户状态（未激活、已激活、已封禁、已删除）
- `UserRole` - 用户角色（普通用户、管理员、超级管理员）

**数据结构:**
- `UserInfo` - 用户基础信息
- `UserDetail` - 用户详细信息
- `TokenInfo` - 登录令牌信息

**服务接口:**
- `Register` - 用户注册
- `Login` - 用户登录
- `RefreshToken` - 刷新令牌
- `GetUser` - 获取用户信息
- `ListUsers` - 获取用户列表
- `UpdateUser` - 更新用户信息
- `ChangePassword` - 修改密码
- `DeleteUser` - 删除用户

### item.thrift

物品服务接口定义，包括：

**枚举类型:**
- `ItemStatus` - 物品状态（草稿、待审核、已上架、已下架、已售罄、已删除）
- `ItemCategory` - 物品分类（电子产品、服装、食品、图书等）

**数据结构:**
- `PriceInfo` - 价格信息
- `StockInfo` - 库存信息
- `ItemInfo` - 物品基础信息
- `ItemDetail` - 物品详细信息

**服务接口:**
- `CreateItem` - 创建物品
- `GetItem` - 获取物品详情
- `ListItems` - 获取物品列表
- `UpdateItem` - 更新物品
- `DeleteItem` - 删除物品
- `UpdateItemStatus` - 更新物品状态
- `UpdateStock` - 更新库存
- `BatchGetItems` - 批量获取物品

## 🔧 使用方式

### 方式一：动态加载（推荐）

项目使用 `thriftpy2` 动态加载 IDL 文件，无需预编译：

```python
from app.thrift_gen import (
    UserInfo,
    ItemInfo,
    ErrorCode,
    BaseResponse,
)

# 创建 Thrift 对象
user = UserInfo(
    id=1,
    email="test@example.com",
    username="testuser",
    status=UserStatus.ACTIVE,
    role=UserRole.USER,
    created_at=int(time.time() * 1000),
    updated_at=int(time.time() * 1000),
)
```

### 方式二：预编译生成

如果需要生成静态 Python 代码：

```bash
# 安装 Apache Thrift 编译器
# macOS
brew install thrift

# Ubuntu
apt-get install thrift-compiler

# 运行生成脚本
./scripts/gen_thrift.sh
```

## 📝 IDL 编写规范

### 命名规范

- **文件名**: 小写，使用下划线分隔（如 `user_service.thrift`）
- **枚举**: 大驼峰命名（如 `UserStatus`）
- **枚举值**: 全大写，下划线分隔（如 `NOT_FOUND`）
- **结构体**: 大驼峰命名（如 `UserInfo`）
- **字段**: 小写，下划线分隔（如 `user_id`）
- **服务**: 大驼峰命名，以 Service 结尾（如 `UserService`）
- **方法**: 大驼峰命名（如 `GetUser`）

### 字段编号规范

- 字段编号从 1 开始
- 删除字段后不复用其编号
- 新增字段使用最大编号 + 1
- `required` 字段用于必填项
- `optional` 字段用于可选项

### 注释规范

```thrift
/**
 * 多行注释用于类、接口说明
 */
struct UserInfo {
    1: required i64 id,           // 单行注释用于字段说明
}
```

## 🔄 版本管理

- 向后兼容：只添加 optional 字段
- 重大变更：修改 namespace 版本号
- 废弃字段：添加 `@deprecated` 注释，但保留字段编号

## 📚 参考资料

- [Apache Thrift 官方文档](https://thrift.apache.org/docs/)
- [Thrift IDL 语法规范](https://thrift.apache.org/docs/idl)
- [thriftpy2 文档](https://thriftpy2.readthedocs.io/)

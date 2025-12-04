#!/bin/bash
# Thrift IDL 编译脚本
# 将 .thrift 文件编译成 Python 代码

set -e

echo "开始编译 Thrift IDL 文件..."

# 检查 thrift 命令是否存在
if ! command -v thrift &> /dev/null; then
    echo "警告: thrift 命令未找到，将使用 thriftpy2 动态加载"
    echo "如需编译，请安装: apt-get install thrift-compiler"
    exit 0
fi

# 编译目录
GEN_DIR="../app/thrift_services/gen-py"
mkdir -p "$GEN_DIR"

# 编译 user.thrift
echo "编译 user.thrift..."
thrift --gen py -out "$GEN_DIR" user.thrift

# 编译 product.thrift
echo "编译 product.thrift..."
thrift --gen py -out "$GEN_DIR" product.thrift

echo "✅ Thrift IDL 编译完成！"
echo "生成的代码位于: $GEN_DIR"

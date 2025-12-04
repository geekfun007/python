#!/bin/bash
# Thrift IDL 编译脚本
# 将 .thrift 文件编译为 Python 代码

echo "==================================="
echo "编译 Thrift IDL 文件..."
echo "==================================="

# 创建输出目录
mkdir -p generated

# 编译用户服务
echo "📝 编译 user.thrift..."
thrift --gen py -out generated idl/user.thrift
if [ $? -eq 0 ]; then
    echo "✅ user.thrift 编译成功"
else
    echo "❌ user.thrift 编译失败"
    exit 1
fi

# 编译产品服务
echo "📝 编译 product.thrift..."
thrift --gen py -out generated idl/product.thrift
if [ $? -eq 0 ]; then
    echo "✅ product.thrift 编译成功"
else
    echo "❌ product.thrift 编译失败"
    exit 1
fi

echo ""
echo "==================================="
echo "✅ 所有 Thrift IDL 文件编译完成！"
echo "==================================="
echo ""
echo "生成的文件位于: generated/"
ls -la generated/

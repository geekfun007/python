#!/bin/bash
# Thrift IDL 编译脚本
# Compile Thrift IDL to Python code

set -e

echo "================================================"
echo "Compiling Thrift IDL files..."
echo "================================================"

# 创建生成目录
mkdir -p generated

# 编译所有 thrift 文件
echo "Compiling common.thrift..."
thrift --gen py -out generated thrift_idl/common.thrift

echo "Compiling user.thrift..."
thrift --gen py -out generated thrift_idl/user.thrift

echo "Compiling product.thrift..."
thrift --gen py -out generated thrift_idl/product.thrift

echo ""
echo "================================================"
echo "✅ Thrift compilation completed!"
echo "================================================"
echo ""
echo "Generated files in: generated/"
ls -lh generated/

echo ""
echo "Next steps:"
echo "  1. Check generated Python files"
echo "  2. Implement Thrift service handlers"
echo "  3. Start Thrift server"

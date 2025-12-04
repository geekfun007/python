#!/bin/bash
# Thrift IDL 编译脚本
# Generate Python code from Thrift IDL files

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IDL_DIR="$SCRIPT_DIR/idl"
GEN_DIR="$SCRIPT_DIR/gen"

echo "🔧 Generating Thrift code..."

# 清理旧的生成文件
rm -rf "$GEN_DIR"
mkdir -p "$GEN_DIR"

# 编译 Thrift IDL
echo "📝 Compiling user.thrift..."
thrift --gen py -out "$GEN_DIR" "$IDL_DIR/user.thrift"

echo "📝 Compiling product.thrift..."
thrift --gen py -out "$GEN_DIR" "$IDL_DIR/product.thrift"

# 创建 __init__.py
touch "$GEN_DIR/__init__.py"

echo "✅ Thrift code generation complete!"
echo "📁 Generated files in: $GEN_DIR"

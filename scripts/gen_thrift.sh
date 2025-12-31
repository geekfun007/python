#!/bin/bash
# ============================================
# Thrift 代码生成脚本
# 从 .thrift 文件生成 Python 代码
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 目录定义
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
IDL_DIR="$PROJECT_ROOT/idl"
OUTPUT_DIR="$PROJECT_ROOT/app/thrift_gen/generated"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Thrift 代码生成器${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查 thrift 是否安装
if ! command -v thrift &> /dev/null; then
    echo -e "${YELLOW}警告: thrift 命令未找到${NC}"
    echo -e "${YELLOW}本项目使用 thriftpy2 动态加载 IDL，无需预编译${NC}"
    echo -e "${YELLOW}如需生成静态代码，请安装 Apache Thrift:${NC}"
    echo -e "  - macOS: brew install thrift"
    echo -e "  - Ubuntu: apt-get install thrift-compiler"
    echo -e "  - 或从源码编译: https://thrift.apache.org/"
    exit 0
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 清理旧文件
echo -e "${YELLOW}清理旧的生成文件...${NC}"
rm -rf "$OUTPUT_DIR"/*

# 生成 Python 代码
echo -e "${GREEN}生成 Python 代码...${NC}"

for thrift_file in "$IDL_DIR"/*.thrift; do
    if [ -f "$thrift_file" ]; then
        filename=$(basename "$thrift_file")
        echo -e "  处理: ${filename}"
        thrift -r --gen py:slots,utf8strings -out "$OUTPUT_DIR" -I "$IDL_DIR" "$thrift_file"
    fi
done

# 创建 __init__.py
echo -e "${GREEN}创建 __init__.py...${NC}"
cat > "$OUTPUT_DIR/__init__.py" << 'EOF'
"""
Thrift 生成的 Python 代码
由 scripts/gen_thrift.sh 自动生成
"""
from .common import ttypes as common_types
from .user import ttypes as user_types
from .item import ttypes as item_types

__all__ = [
    "common_types",
    "user_types", 
    "item_types",
]
EOF

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}代码生成完成!${NC}"
echo -e "${GREEN}输出目录: $OUTPUT_DIR${NC}"
echo -e "${GREEN}========================================${NC}"

# 列出生成的文件
echo -e "\n${YELLOW}生成的文件:${NC}"
find "$OUTPUT_DIR" -type f -name "*.py" | head -20

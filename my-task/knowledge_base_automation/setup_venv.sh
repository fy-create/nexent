#!/bin/bash

# 知识库自动化虚拟环境设置脚本

echo "🚀 开始设置知识库自动化虚拟环境..."

# 检查是否已存在虚拟环境
if [ -d "venv" ]; then
    echo "⚠️  虚拟环境已存在，是否要重新创建？(y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "🗑️  删除现有虚拟环境..."
        rm -rf venv
    else
        echo "✅ 使用现有虚拟环境"
        exit 0
    fi
fi

# 创建虚拟环境
echo "📦 创建Python虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "⬆️  升级pip..."
pip install --upgrade pip

# 安装依赖包
echo "📚 安装依赖包..."
pip install requests pathlib argparse

echo "✅ 虚拟环境设置完成！"
echo ""
echo "使用方法："
echo "  激活虚拟环境: source venv/bin/activate"
echo "  运行脚本: python auto_create_kb.py --config kb_config.json"
echo "  退出虚拟环境: deactivate"
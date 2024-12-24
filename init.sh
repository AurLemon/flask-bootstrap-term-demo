#!/bin/bash

# 检查 Python 装了没
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 未安装，请安装后继续操作。"
    exit 1
fi

# 检查 pip 装了没
if ! command -v pip &> /dev/null; then
    echo "Error: pip 未安装，请安装后继续操作。"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "虚拟环境未创建，正在创建..."
    python3 -m venv .venv
fi

source .venv/bin/activate 

# 安装依赖
if [ -f "requirements.txt" ]; then
    echo "根据项目依赖描述文件安装依赖包..."
    pip install -r requirements.txt 
else
    echo "依赖描述文件读取有误，请检查项目是否完整。"
fi

# 激活虚拟环境
echo "=========="
echo ""
echo "输入 source .venv/bin/activate 来激活虚拟环境；deactivate 退出虚拟环境。"
echo ""
echo "=========="

echo ""
echo "初始化完成 √"

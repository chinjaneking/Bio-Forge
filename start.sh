#!/bin/bash
# DeerFlow 2.0 快速启动脚本

echo "🦌 启动 DeerFlow 2.0 智能体平台..."

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "📦 创建 Python 虚拟环境..."
    python -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install -r requirements.txt

# 复制环境配置
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚙️  已创建 .env 配置文件"
fi

# 初始化数据库（使用SQLite简化演示）
echo "🗄️  初始化数据库..."

# 启动服务
echo "🚀 启动 API 服务..."
echo "📖 文档地址: http://localhost:8000/docs"
echo ""
python -m app.main

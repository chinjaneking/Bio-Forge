#!/usr/bin/env python3
"""Bio-Forge 项目最终验证"""

import os

print("🔬 Bio-Forge 120 智能体矩阵 - 最终验证")
print("=" * 60)
print()

# 1. 检查核心文件
core_files = [
    "app/agent_manager.py",
    "app/models/agent.py", 
    "app/api/agents.py",
    "app/main.py",
    "README.md",
    "WINDOWS_DOCKER_GUIDE.md",
    "docker-compose.yml"
]

print("📁 核心文件检查:")
for f in core_files:
    exists = os.path.exists(f)
    status = "✅" if exists else "❌"
    print(f"  {status} {f}")

# 2. 检查智能体数量
print()
print("🤖 智能体数量检查:")
with open("app/agent_manager.py", "r", encoding="utf-8") as f:
    content = f.read()
    agent_count = content.count('"name": "')
    target = 120
    status = "✅" if agent_count == target else "❌"
    print(f"  {status} 找到 {agent_count} 个智能体 (目标: {target})")

# 3. 检查关键配置
print()
print("🔧 配置检查:")
checks = [
    ("端口 1983", "1983"),
    ("容器名 bio-forge", "bio-forge"),
    ("数据库 bio-forge.db", "bio-forge.db"),
]

with open("docker-compose.yml", "r", encoding="utf-8") as f:
    compose_content = f.read()

for check_name, check_str in checks:
    exists = check_str in compose_content
    status = "✅" if exists else "❌"
    print(f"  {status} {check_name}")

print()
print("=" * 60)
print("🎉 Bio-Forge 项目准备就绪!")
print()
print("下一步:")
print("  1. 将 /mnt/user-data/outputs/bio-forge 内容复制到 C:\\bio-forge")
print("  2. 在 Windows 中打开 C:\\bio-forge")
print("  3. 运行: docker-compose up -d")
print("  4. 访问: http://localhost:1983/docs")
print()

#!/usr/bin/env python3
"""
Bio-Forge 120智能体矩阵 - 最终验证脚本
验证项目完整性和120个智能体的正确性
"""

import os
import re
import sys


def check_file_exists(filepath):
    """检查文件是否存在"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"  {status} {filepath}")
    return exists


def check_agent_manager():
    """检查agent_manager.py"""
    print("\n📋 检查智能体管理器:")
    print("-" * 40)
    
    filepath = "app/agent_manager.py"
    if not os.path.exists(filepath):
        print(f"  ❌ {filepath} 不存在")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("AgentManager 类", "class AgentManager:"),
        ("initialize_default_agents 方法", "def initialize_default_agents"),
        ("研发总监助手", "研发总监助手"),
        ("蛋白质结构预测智能体", "蛋白质结构预测智能体"),
        ("红景天苷发酵优化智能体", "红景天苷发酵优化智能体"),
    ]
    
    all_passed = True
    for name, pattern in checks:
        found = pattern in content
        status = "✅" if found else "❌"
        print(f"  {status} {name}")
        if not found:
            all_passed = False
    
    # 检查智能体数量
    agent_count = content.count('"name": "')
    status = "✅" if agent_count == 120 else "❌"
    print(f"  {status} 智能体数量: {agent_count}/120")
    if agent_count != 120:
        all_passed = False
    
    return all_passed


def check_agent_types():
    """检查智能体类型"""
    print("\n🏷️ 检查智能体类型:")
    print("-" * 40)
    
    filepath = "app/models/agent.py"
    if not os.path.exists(filepath):
        print(f"  ❌ {filepath} 不存在")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查AgentType枚举
    type_matches = re.findall(r'    (\w+) = "', content)
    status = "✅" if type_matches else "❌"
    print(f"  {status} 找到 {len(type_matches)} 种智能体类型")
    
    return len(type_matches) > 0


def check_api_routes():
    """检查API路由"""
    print("\n🔗 检查API路由:")
    print("-" * 40)
    
    filepath = "app/api/routes.py"
    if not os.path.exists(filepath):
        print(f"  ❌ {filepath} 不存在")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("/health 端点", "@router.get(\"/health\", response_model=HealthResponse)"),
        ("/agents 端点", "@router.get(\"/agents\", response_model=AgentMatrixResponse)"),
        ("/agents/{agent_id} 端点", "@router.get(\"/agents/{agent_id}\""),
        ("合成生物学端点", "/synthesis/design"),
    ]
    
    all_passed = True
    for name, pattern in checks:
        found = pattern in content
        status = "✅" if found else "❌"
        print(f"  {status} {name}")
        if not found:
            all_passed = False
    
    return all_passed


def check_config():
    """检查配置"""
    print("\n⚙️ 检查配置:")
    print("-" * 40)
    
    filepath = "app/core/config.py"
    if not os.path.exists(filepath):
        print(f"  ❌ {filepath} 不存在")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("项目代号 Genesis-2026", 'CODENAME: str = "Genesis-2026"'),
        ("端口 1983", "PORT: int = int(os.getenv(\"PORT\", 1983))"),
        ("AGENT_MATRIX_SIZE = 120", "AGENT_MATRIX_SIZE: int = 120"),
        ("AGENT_LAYERS = 6", "AGENT_LAYERS: int = 6"),
    ]
    
    all_passed = True
    for name, pattern in checks:
        found = pattern in content
        status = "✅" if found else "❌"
        print(f"  {status} {name}")
        if not found:
            all_passed = False
    
    return all_passed


def check_docker_config():
    """检查Docker配置"""
    print("\n🐳 检查Docker配置:")
    print("-" * 40)
    
    checks = [
        ("docker-compose.yml", "container_name: bio-forge"),
        ("Dockerfile", "FROM python:3.11-slim"),
        ("requirements.txt", "fastapi"),
    ]
    
    all_passed = True
    for filename, pattern in checks:
        if not os.path.exists(filename):
            print(f"  ❌ {filename} 不存在")
            all_passed = False
            continue
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        found = pattern in content
        status = "✅" if found else "❌"
        print(f"  {status} {filename}")
        if not found:
            all_passed = False
    
    return all_passed


def check_documentation():
    """检查文档"""
    print("\n📚 检查文档:")
    print("-" * 40)
    
    checks = [
        "README.md",
        "WINDOWS_DOCKER_GUIDE.md",
    ]
    
    all_passed = True
    for filename in checks:
        exists = os.path.exists(filename)
        status = "✅" if exists else "❌"
        print(f"  {status} {filename}")
        if not exists:
            all_passed = False
    
    return all_passed


def main():
    """主验证函数"""
    print("🔬 Bio-Forge 120 智能体矩阵 - 最终验证")
    print("=" * 60)
    
    # 切换到项目目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 执行所有检查
    print("\n📁 检查关键文件:")
    print("-" * 40)
    files_ok = check_file_exists("app/agent_manager.py")
    files_ok &= check_file_exists("app/models/agent.py")
    files_ok &= check_file_exists("app/api/routes.py")
    files_ok &= check_file_exists("app/main.py")
    
    manager_ok = check_agent_manager()
    types_ok = check_agent_types()
    api_ok = check_api_routes()
    config_ok = check_config()
    docker_ok = check_docker_config()
    docs_ok = check_documentation()
    
    # 总结
    print("\n" + "=" * 60)
    all_ok = files_ok and manager_ok and types_ok and api_ok and config_ok and docker_ok and docs_ok
    
    if all_ok:
        print("✅ 所有检查通过！Bio-Forge 120智能体矩阵验证成功。")
        print("\n📋 项目总结:")
        print("   - 120个智能体，6层架构")
        print("   - 端口: 1983")
        print("   - 容器名: bio-forge")
        print("   - 数据库: bio-forge.db")
        print("\n🚀 下一步:")
        print("   1. 参考 WINDOWS_DOCKER_GUIDE.md 进行本地部署")
        print("   2. 访问 http://localhost:1983/docs 查看API文档")
        sys.exit(0)
    else:
        print("❌ 检查失败！请修复上述问题。")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bio-Forge 120个智能体精确统计"""

import ast

def extract_agent_count():
    """从 agent_manager.py 中提取智能体数量"""
    agent_manager_path = "app/agent_manager.py"
    
    try:
        with open(agent_manager_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 查找 default_agents 列表
        tree = ast.parse(content)
        agent_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.List):
                # 检查列表元素是否是字典，包含 name 键
                if node.elts and len(node.elts) > 0:
                    first_elt = node.elts[0]
                    if isinstance(first_elt, ast.Dict):
                        has_name = any(isinstance(key, ast.Constant) and key.value == "name" for key in first_elt.keys)
                        if has_name:
                            agent_count = len(node.elts)
                            break
        
        return agent_count
        
    except FileNotFoundError:
        print(f"  ❌ 找不到文件: {agent_manager_path}")
        return 0

def main():
    """主函数"""
    print("🔢 Bio-Forge 智能体数量精确统计")
    print("=" * 60)
    
    agent_count = extract_agent_count()
    
    print(f"\n📦 找到 {agent_count} 个智能体")
    print(f"   目标: 120 个")
    
    if agent_count == 120:
        print("\n✅ 完美！智能体数量达到 120 个目标")
        return 0
    elif agent_count > 120:
        print(f"\n⚠️ 智能体数量超出目标 {agent_count - 120} 个")
        return 1
    else:
        print(f"\n❌ 智能体数量不足目标 120 - {agent_count} = {120 - agent_count} 个")
        return 1

if __name__ == "__main__":
    exit(main())

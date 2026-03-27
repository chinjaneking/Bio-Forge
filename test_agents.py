#!/usr/bin/env python3
"""测试智能体初始化"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from app.database import init_db, SessionLocal
from app.agent_manager import AgentManager

def test_agent_initialization():
    """测试智能体初始化"""
    print("="*60)
    print("DeerFlow 2.0 智能体矩阵初始化测试")
    print("="*60)
    
    # 初始化数据库
    print("\n1. 初始化数据库...")
    init_db()
    print("   ✓ 数据库初始化完成")
    
    # 创建会话
    db = SessionLocal()
    
    try:
        # 初始化智能体管理器
        print("\n2. 初始化智能体管理器...")
        agent_manager = AgentManager(db)
        print("   ✓ 智能体管理器创建完成")
        
        # 初始化默认智能体
        print("\n3. 初始化默认智能体矩阵...")
        agent_manager.initialize_default_agents()
        print("   ✓ 默认智能体初始化完成")
        
        # 统计智能体
        print("\n4. 智能体统计:")
        all_agents = agent_manager.list_agents(limit=100)
        print(f"   总智能体数: {len(all_agents)}")
        
        # 按类型分组统计
        from collections import defaultdict
        type_counts = defaultdict(int)
        for agent in all_agents:
            type_counts[agent.agent_type] += 1
        
        print("\n5. 按类型分布:")
        for agent_type, count in sorted(type_counts.items()):
            print(f"   {agent_type.value}: {count}个")
        
        # 列出所有智能体
        print("\n6. 智能体列表:")
        for i, agent in enumerate(all_agents, 1):
            status_icon = "⚡" if agent.priority <= 2 else "✓"
            print(f"   {i:2d}. {status_icon} [{agent.priority}] {agent.name}")
            print(f"        类型: {agent.agent_type.value}")
            print(f"        描述: {agent.description}")
            if agent.capabilities:
                print(f"        能力: {', '.join(agent.capabilities[:3])}{'...' if len(agent.capabilities) > 3 else ''}")
        
        print("\n" + "="*60)
        print("✓ 智能体矩阵初始化测试完成！")
        print("="*60)
        
    finally:
        db.close()

if __name__ == "__main__":
    test_agent_initialization()

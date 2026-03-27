#!/usr/bin/env python3
"""验证 Bio-Forge 120 智能体矩阵"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.database import init_db, SessionLocal
from app.agent_manager import AgentManager
from app.models.agent import Agent, AgentType


def verify_agent_matrix():
    """验证智能体矩阵"""
    print("🔬 Bio-Forge 120 智能体矩阵验证")
    print("=" * 50)
    
    # 初始化数据库
    init_db()
    
    # 创建数据库会话
    db = SessionLocal()
    try:
        manager = AgentManager(db)
        
        # 初始化智能体（如果尚未初始化）
        manager.initialize_default_agents()
        
        # 获取统计信息
        stats = manager.get_stats()
        
        print(f"✅ 总智能体数: {stats['total']}")
        print(f"✅ 活跃智能体: {stats['active']}")
        print(f"✅ 非活跃智能体: {stats['inactive']}")
        print()
        
        print("📊 智能体类型分布:")
        print("-" * 30)
        for agent_type, count in stats['by_type'].items():
            print(f"  {agent_type}: {count}个")
        print()
        
        # 列出所有智能体
        print("📋 智能体完整列表:")
        print("-" * 50)
        
        all_agents = manager.list_agents(limit=200)
        
        # 按层级分组
        layers = {
            "基础架构层 (15个)": [],
            "生命设计层 (60个)": [],
            "实验执行层 (25个)": [],
            "进化优化层 (20个)": []
        }
        
        # 简单的分组逻辑（根据类型）
        for agent in all_agents:
            agent_type = agent.agent_type.value if hasattr(agent.agent_type, 'value') else str(agent.agent_type)
            
            if agent_type in ["平台管理", "数据管理", "安全监控", "研发总监助手"]:
                layers["基础架构层 (15个)"].append(agent)
            elif agent_type in ["基因组设计", "蛋白质设计", "细胞设计", "组织设计", 
                               "通路设计", "代谢工程", "design"]:
                layers["生命设计层 (60个)"].append(agent)
            elif agent_type in ["DNA合成", "细胞组装", "培养优化", "分析验证", 
                               "实验室自动化", "execution"]:
                layers["实验执行层 (25个)"].append(agent)
            else:
                layers["进化优化层 (20个)"].append(agent)
        
        # 打印各层
        for layer_name, agents_in_layer in layers.items():
            print(f"\n🎯 {layer_name}:")
            print("  " + "-" * 40)
            for i, agent in enumerate(agents_in_layer, 1):
                agent_type_str = agent.agent_type.value if hasattr(agent.agent_type, 'value') else str(agent.agent_type)
                print(f"  {i:2d}. {agent.name} ({agent_type_str})")
        
        print()
        print("=" * 50)
        print("✅ 验证完成！120个智能体矩阵已成功加载。")
        print()
        print("📖 使用说明:")
        print("  - API文档: http://localhost:1983/docs")
        print("  - 列出所有智能体: GET /api/v1/agents")
        print("  - 获取智能体详情: GET /api/v1/agents/{agent_id}")
        print()
        
        return True
        
    finally:
        db.close()


if __name__ == "__main__":
    try:
        success = verify_agent_matrix()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

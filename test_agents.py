#!/usr/bin/env python3
"""
Bio-Forge 智能体初始化测试
Tests 120-agent matrix initialization
"""

import sys
import os
import io

# 设置stdout为UTF-8编码（解决Windows终端emoji显示问题）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.agent_manager import AgentManager
from app.models.agent import Agent, AgentStatus
from sqlalchemy import text


def test_database_connection():
    """测试数据库连接"""
    print("📊 测试数据库连接...")
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ 数据库连接成功")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False


def test_init_database():
    """测试数据库初始化"""
    print("\n📊 测试数据库初始化...")
    try:
        init_db()
        print("✅ 数据库表创建成功")
        return True
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False


def test_agent_initialization():
    """测试智能体初始化"""
    print("\n📊 测试智能体初始化...")
    try:
        db = SessionLocal()
        manager = AgentManager(db)
        
        # 初始化默认智能体
        manager.initialize_default_agents()
        
        # 统计智能体数量
        total_agents = db.query(Agent).count()
        
        # 按类型统计
        from sqlalchemy import func
        by_type = db.query(
            Agent.agent_type,
            func.count(Agent.id)
        ).group_by(Agent.agent_type).all()
        
        print(f"✅ 已初始化 {total_agents} 个智能体")
        print("\n智能体类型分布:")
        for agent_type, count in by_type:
            print(f"  - {agent_type.value}: {count}")
        
        db.close()
        return total_agents == 120
    except Exception as e:
        print(f"❌ 智能体初始化失败: {e}")
        return False


def test_agent_operations():
    """测试智能体操作"""
    print("\n📊 测试智能体操作...")
    try:
        db = SessionLocal()
        manager = AgentManager(db)
        
        # 获取第一个智能体
        agent = manager.list_agents(limit=1)[0]
        print(f"  智能体名称: {agent.name}")
        print(f"  智能体类型: {agent.agent_type.value}")
        print(f"  智能体状态: {agent.status.value}")
        
        # 测试激活/停用
        manager.activate_agent(agent.id)
        agent = manager.get_agent(agent.id)
        assert agent.status == AgentStatus.ACTIVE
        
        manager.deactivate_agent(agent.id)
        agent = manager.get_agent(agent.id)
        assert agent.status == AgentStatus.INACTIVE
        
        print("✅ 智能体操作测试通过")
        db.close()
        return True
    except Exception as e:
        print(f"❌ 智能体操作测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("🧬 Bio-Forge 智能体矩阵测试")
    print("=" * 60)
    
    tests = [
        ("数据库连接", test_database_connection),
        ("数据库初始化", test_init_database),
        ("智能体初始化", test_agent_initialization),
        ("智能体操作", test_agent_operations),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'=' * 60}")
        result = test_func()
        results.append((name, result))
    
    print(f"\n{'=' * 60}")
    print("📊 测试结果汇总:")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n⚠️ 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
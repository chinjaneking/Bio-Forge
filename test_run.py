#!/usr/bin/env python3
"""
Bio-Forge 运行测试
Tests the complete system startup and API endpoints
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """测试所有模块导入"""
    print("📦 测试模块导入...")
    try:
        from app.core.config import settings
        print(f"  ✅ app.core.config")
        
        from app.database import Base, SessionLocal, init_db
        print(f"  ✅ app.database")
        
        from app.models.agent import Agent, AgentType, AgentStatus
        print(f"  ✅ app.models.agent")
        
        from app.models.task import Task, TaskStatus, TaskPriority
        print(f"  ✅ app.models.task")
        
        from app.agent_manager import AgentManager
        print(f"  ✅ app.agent_manager")
        
        from app.task_scheduler import TaskScheduler
        print(f"  ✅ app.task_scheduler")
        
        from app.redis_client import redis_client
        print(f"  ✅ app.redis_client")
        
        from app.api.routes import router
        print(f"  ✅ app.api.routes")
        
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        return False


def test_settings():
    """测试配置"""
    print("\n⚙️ 测试配置...")
    try:
        from app.core.config import settings
        
        print(f"  VERSION: {settings.VERSION}")
        print(f"  PROJECT_NAME: {settings.PROJECT_NAME}")
        print(f"  CODENAME: {settings.CODENAME}")
        print(f"  AGENT_MATRIX_SIZE: {settings.AGENT_MATRIX_SIZE}")
        print(f"  DATABASE_URL: {settings.DATABASE_URL}")
        print(f"  PORT: {settings.PORT}")
        
        assert settings.AGENT_MATRIX_SIZE == 120
        print("  ✅ 配置验证通过")
        return True
    except Exception as e:
        print(f"  ❌ 配置测试失败: {e}")
        return False


def test_database_models():
    """测试数据库模型"""
    print("\n📊 测试数据库模型...")
    try:
        from app.database import Base
        from app.models.agent import Agent
        from app.models.task import Task
        
        # 检查表是否存在
        assert 'agents' in Agent.__tablename__
        assert 'tasks' in Task.__tablename__
        
        print("  ✅ 模型定义正确")
        return True
    except Exception as e:
        print(f"  ❌ 模型测试失败: {e}")
        return False


def test_enums():
    """测试枚举类型"""
    print("\n📋 测试枚举类型...")
    try:
        from app.models.agent import AgentStatus, AgentType
        from app.models.task import TaskStatus, TaskPriority
        
        # 测试枚举值
        assert AgentStatus.ACTIVE.value == "active"
        assert AgentStatus.INACTIVE.value == "inactive"
        
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"
        
        assert TaskPriority.HIGH.value == "high"
        assert TaskPriority.LOW.value == "low"
        
        # 测试智能体类型
        agent_types = list(AgentType)
        print(f"  智能体类型数量: {len(agent_types)}")
        print(f"  包含: {[t.value for t in agent_types[:5]]}...")
        
        print("  ✅ 枚举测试通过")
        return True
    except Exception as e:
        print(f"  ❌ 枚举测试失败: {e}")
        return False


def test_app_creation():
    """测试FastAPI应用创建"""
    print("\n🚀 测试FastAPI应用创建...")
    try:
        from app.main import app
        
        # 检查路由
        routes = [route.path for route in app.routes]
        print(f"  路由数量: {len(routes)}")
        
        assert "/" in routes
        assert "/health" in routes
        assert "/docs" in routes
        
        print("  ✅ FastAPI应用创建成功")
        return True
    except Exception as e:
        print(f"  ❌ 应用创建失败: {e}")
        return False


def test_agent_matrix():
    """测试智能体矩阵"""
    print("\n🤖 测试智能体矩阵...")
    try:
        from app.agent_manager import AgentManager
        from app.models.agent import AgentType
        
        # 检查AgentType枚举中是否包含所有需要的类型
        expected_types = [
            "R_D_ASSISTANT", "PLATFORM_MANAGEMENT", "DATA_MANAGEMENT",
            "SECURITY_MONITORING", "MOLECULAR_MODELING", "PROTEIN_ENGINEERING",
            "PATHWAY_DESIGN", "GENOME_DESIGN", "MOLECULAR_BIOLOGY", "MICROBIOLOGY",
            "FERMENTATION_OPTIMIZATION", "ANALYTICAL_CHEMISTRY", "YIELD_OPTIMIZATION",
            "STABILITY_ENHANCEMENT", "SCALE_UP", "LITERATURE_RESEARCH", "PATENT_RESEARCH",
            "EXPERIMENT_DESIGN", "BIOINFORMATICS", "STATISTICAL_MODELING",
            "PROJECT_MANAGEMENT", "QUALITY_CONTROL", "REGULATORY_AFFAIRS",
            "RHODIOLA_PROJECT"
        ]
        
        for type_name in expected_types:
            assert hasattr(AgentType, type_name), f"缺少AgentType.{type_name}"
        
        print(f"  ✅ 智能体类型完整: {len(expected_types)}种")
        return True
    except Exception as e:
        print(f"  ❌ 智能体矩阵测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("🧬 Bio-Forge 运行测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("配置验证", test_settings),
        ("数据库模型", test_database_models),
        ("枚举类型", test_enums),
        ("应用创建", test_app_creation),
        ("智能体矩阵", test_agent_matrix),
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
        print("\n🎉 所有测试通过！系统准备就绪")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
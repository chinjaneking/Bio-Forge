#!/usr/bin/env python3
"""简化启动脚本"""
import sys
import os
from pathlib import Path

# 确保项目路径在最前面
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print(f"项目根目录: {project_root}")
print(f"Python路径: {sys.path[:5]}")

# 测试导入
try:
    print("\n测试导入模块...")
    import sqlalchemy
    print(f"  ✓ SQLAlchemy: {sqlalchemy.__version__}")
    
    import fastapi
    print(f"  ✓ FastAPI: {fastapi.__version__}")
    
    import uvicorn
    print(f"  ✓ Uvicorn: {uvicorn.__version__}")
    
    from app.database import init_db, SessionLocal
    print("  ✓ 数据库模块导入成功")
    
    from app.agent_manager import AgentManager
    print("  ✓ 智能体管理器导入成功")
    
except Exception as e:
    print(f"  ✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n所有模块导入成功！")

# 初始化
print("\n初始化系统...")
init_db()
db = SessionLocal()

try:
    agent_manager = AgentManager(db)
    agent_manager.initialize_default_agents()
    
    # 统计
    agents = agent_manager.list_agents(limit=100)
    print(f"\n✓ 系统初始化完成！")
    print(f"✓ 已加载 {len(agents)} 个智能体")
    
    print("\n前10个智能体:")
    for i, agent in enumerate(agents[:10], 1):
        print(f"  {i}. [{agent.priority}] {agent.name}")
    
    print(f"\n... 还有 {len(agents)-10} 个智能体")
    
finally:
    db.close()

print("\n系统就绪！")

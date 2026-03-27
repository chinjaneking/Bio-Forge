"""DeerFlow 2.0 简单测试"""
import sys
import time
from app.main import app
from app.database import init_db, SessionLocal
from app.agent_manager import AgentManager
from app.task_scheduler import TaskScheduler
from app.models.agent import AgentType

print("🦌 DeerFlow 2.0 测试开始...")

# 初始化数据库
print("1. 初始化数据库...")
init_db()

# 创建会话
db = SessionLocal()

try:
    # 初始化默认智能体
    print("2. 初始化默认智能体...")
    manager = AgentManager(db)
    manager.initialize_default_agents()
    
    # 列出所有智能体
    print("\n3. 当前智能体列表:")
    agents = manager.list_agents()
    for agent in agents:
        print(f"   - [{agent.id}] {agent.name} ({agent.agent_type}) - 优先级: {agent.priority}")
    
    # 激活智能体
    print("\n4. 激活智能体...")
    for agent in agents:
        manager.activate_agent(agent.id)
        print(f"   ✓ {agent.name} 已激活")
    
    # 创建任务
    print("\n5. 创建测试任务...")
    scheduler = TaskScheduler(db)
    
    test_agent = agents[0]
    task = scheduler.create_task(
        name="测试任务-001",
        agent_id=test_agent.id,
        input_data={"test": "hello", "value": 123},
        description="这是一个测试任务"
    )
    print(f"   ✓ 创建任务: {task.task_id} - {task.name}")
    
    # 执行任务
    print("\n6. 执行任务...")
    scheduler.queue_task(task.task_id)
    result = scheduler.execute_task(task)
    print(f"   ✓ 任务执行结果: {'成功' if result else '失败'}")
    
    # 检查任务状态
    final_task = scheduler.get_task_by_task_id(task.task_id)
    print(f"\n7. 任务详情:")
    print(f"   任务ID: {final_task.task_id}")
    print(f"   状态: {final_task.status}")
    print(f"   执行时间: {final_task.execution_time}秒")
    print(f"   输出数据: {final_task.output_data}")
    
    print("\n✅ DeerFlow 2.0 核心框架测试成功！")
    print("\n下一步:")
    print("  - 运行: python -m app.main")
    print("  - 访问: http://localhost:8000/docs")
    
finally:
    db.close()

"""
DeerFlow Engine - Bio-Forge 集成层

将 Bio-Forge 的120个智能体桥接到 DeerFlow 2.0 执行引擎。

核心组件:
- BaseDeerFlowAgent: 智能体基类，桥接 Bio-Forge Agent 模型到 DeerFlow 执行
- WorkflowGenerator: DAG工作流生成器，多智能体任务编排
- AgentMemory: 记忆与进化系统
- ConfigManager: DeerFlow配置管理

使用示例:
    from deerflow_engine import BaseDeerFlowAgent, WorkflowGenerator
    
    # 创建智能体执行器
    agent = BaseDeerFlowAgent(bioforge_agent_id=1)
    response = agent.execute("分析这个蛋白质结构")
    
    # 创建工作流
    workflow = WorkflowGenerator()
    dag = workflow.create_enzyme_design_pipeline(target_sequence="MKT...")
"""

from deerflow_engine.base_agent import BaseDeerFlowAgent
from deerflow_engine.workflow import WorkflowGenerator, WorkflowNode, WorkflowEdge
from deerflow_engine.config import DeerFlowConfig, get_deerflow_config
from deerflow_engine.memory import AgentMemory, MemoryEntry

__all__ = [
    "BaseDeerFlowAgent",
    "WorkflowGenerator",
    "WorkflowNode",
    "WorkflowEdge",
    "DeerFlowConfig",
    "get_deerflow_config",
    "AgentMemory",
    "MemoryEntry",
]

__version__ = "0.1.0"
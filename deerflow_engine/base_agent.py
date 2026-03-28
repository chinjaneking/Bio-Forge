"""
BaseDeerFlowAgent - Bio-Forge 智能体到 DeerFlow 的桥接层

将 Bio-Forge 数据库中的 Agent 实体桥接到 DeerFlow 执行引擎，
实现从静态智能体定义到动态执行智能体的转换。

核心功能:
1. 从 Bio-Forge Agent 模型加载配置
2. 创建 DeerFlow 执行环境
3. 执行任务并返回结果
4. 管理会话上下文和记忆
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List, Generator, Callable

logger = logging.getLogger(__name__)


class ExecutionStatus(Enum):
    """执行状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ExecutionResult:
    """执行结果"""
    status: ExecutionStatus
    content: str = ""
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    usage: Dict[str, int] = field(default_factory=dict)
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """计算执行时长"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "status": self.status.value,
            "content": self.content,
            "tool_calls": self.tool_calls,
            "artifacts": self.artifacts,
            "usage": self.usage,
            "error": self.error,
            "duration_seconds": self.duration_seconds,
        }


@dataclass
class AgentContext:
    """智能体执行上下文"""
    thread_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    parent_agent_id: Optional[int] = None
    workflow_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "thread_id": self.thread_id,
            "session_id": self.session_id,
            "parent_agent_id": self.parent_agent_id,
            "workflow_id": self.workflow_id,
            "metadata": self.metadata,
        }


class BaseDeerFlowAgent:
    """
    Bio-Forge 智能体到 DeerFlow 的桥接基类
    
    将 Bio-Forge 数据库中的 Agent 实体转换为可执行的 DeerFlow 智能体。
    
    使用示例:
        # 从数据库加载
        agent = BaseDeerFlowAgent.from_db(agent_id=1)
        
        # 或手动创建
        agent = BaseDeerFlowAgent(
            name="研发总监助手",
            agent_type="R_D_ASSISTANT",
            description="协助研发总监...",
            capabilities=["任务分解", "进度追踪"]
        )
        
        # 执行任务
        result = agent.execute("设计一个酶来催化反应X")
        print(result.content)
        
        # 流式执行
        for event in agent.stream("分析这个蛋白质"):
            print(f"{event.type}: {event.data}")
    """
    
    def __init__(
        self,
        name: str,
        agent_type: str,
        description: str = "",
        capabilities: Optional[List[str]] = None,
        priority: int = 5,
        agent_id: Optional[int] = None,
        config_override: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化 BaseDeerFlowAgent
        
        Args:
            name: 智能体名称
            agent_type: 智能体类型（对应 AgentType 枚举）
            description: 智能体描述
            capabilities: 能力列表
            priority: 优先级 (1-10)
            agent_id: Bio-Forge 数据库中的智能体ID
            config_override: 配置覆盖
        """
        self.name = name
        self.agent_type = agent_type
        self.description = description
        self.capabilities = capabilities or []
        self.priority = priority
        self.agent_id = agent_id
        self.config_override = config_override or {}
        
        self._client = None
        self._context = AgentContext()
        self._initialized = False
    
    @classmethod
    def from_db(cls, agent_id: int) -> "BaseDeerFlowAgent":
        """从数据库加载智能体
        
        Args:
            agent_id: Bio-Forge 数据库中的智能体ID
            
        Returns:
            BaseDeerFlowAgent 实例
            
        Raises:
            ValueError: 如果智能体不存在
        """
        # 延迟导入避免循环依赖
        from sqlalchemy.orm import Session
        from app.database import get_db
        from app.models.agent import Agent
        
        db: Session = next(get_db())
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise ValueError(f"Agent with id {agent_id} not found")
            
            return cls(
                name=agent.name,
                agent_type=agent.agent_type.value if hasattr(agent.agent_type, 'value') else str(agent.agent_type),
                description=agent.description or "",
                capabilities=agent.capabilities or [],
                priority=agent.priority,
                agent_id=agent.id,
            )
        finally:
            db.close()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseDeerFlowAgent":
        """从字典创建智能体"""
        return cls(
            name=data.get("name", "Unknown Agent"),
            agent_type=data.get("agent_type", "UNKNOWN"),
            description=data.get("description", ""),
            capabilities=data.get("capabilities", []),
            priority=data.get("priority", 5),
            agent_id=data.get("agent_id"),
            config_override=data.get("config_override"),
        )
    
    def _ensure_client(self):
        """确保 DeerFlow Client 已初始化"""
        if self._client is not None:
            return
        
        try:
            from deerflow_engine.config import get_deerflow_client
            self._client = get_deerflow_client()
            self._initialized = True
            logger.info(f"DeerFlow client initialized for agent {self.name}")
        except ImportError as e:
            logger.warning(f"DeerFlow not available, using simulation mode: {e}")
            self._client = None
            self._initialized = True
    
    def _build_system_prompt(self) -> str:
        """构建智能体系统提示"""
        capabilities_str = ", ".join(self.capabilities) if self.capabilities else "通用能力"
        
        prompt = f"""你是Bio-Forge多智能体系统中的{self.name}。

角色类型: {self.agent_type}
职责描述: {self.description}
核心能力: {capabilities_str}
优先级: {self.priority}/10

作为生物合成研发智能体，你的职责包括:
1. 理解和执行分配给你的研发任务
2. 与其他智能体协作完成复杂工作流
3. 生成符合科学规范的分析报告
4. 提供专业领域的建议和决策支持

请根据你的角色类型和能力，专业地完成用户请求。"""
        
        return prompt
    
    def execute(
        self,
        message: str,
        thread_id: Optional[str] = None,
        **kwargs
    ) -> ExecutionResult:
        """
        执行任务并返回完整结果
        
        Args:
            message: 用户消息
            thread_id: 会话线程ID（可选，用于多轮对话）
            **kwargs: 额外参数传递给 DeerFlow
            
        Returns:
            ExecutionResult 包含执行状态、内容、工具调用等
        """
        self._ensure_client()
        
        # 更新上下文
        if thread_id:
            self._context.thread_id = thread_id
        
        result = ExecutionResult(
            status=ExecutionStatus.PENDING,
            started_at=datetime.now(),
        )
        
        try:
            if self._client is None:
                # 模拟执行模式
                result = self._simulate_execution(message, result)
            else:
                # 实际 DeerFlow 执行
                result = self._real_execution(message, result, **kwargs)
            
            result.status = ExecutionStatus.SUCCESS
            
        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.error = str(e)
            logger.error(f"Agent {self.name} execution failed: {e}")
        
        finally:
            result.completed_at = datetime.now()
        
        return result
    
    def _real_execution(
        self,
        message: str,
        result: ExecutionResult,
        **kwargs
    ) -> ExecutionResult:
        """使用 DeerFlow 实际执行"""
        # 构建带系统提示的消息
        full_message = f"{self._build_system_prompt()}\n\n用户请求: {message}"
        
        # 执行
        response = self._client.chat(
            full_message,
            thread_id=self._context.thread_id,
            **kwargs
        )
        
        result.content = response
        result.status = ExecutionStatus.SUCCESS
        
        return result
    
    def _simulate_execution(
        self,
        message: str,
        result: ExecutionResult
    ) -> ExecutionResult:
        """模拟执行（当 DeerFlow 不可用时）"""
        import time
        time.sleep(0.5)  # 模拟执行延迟
        
        result.content = f"[模拟执行-{self.name}]\n\n已接收任务: {message}\n\n" \
            f"智能体类型: {self.agent_type}\n" \
            f"能力: {', '.join(self.capabilities)}\n" \
            f"\n注意: DeerFlow 引擎未连接，这是模拟响应。"
        result.status = ExecutionStatus.SUCCESS
        
        return result
    
    def stream(
        self,
        message: str,
        thread_id: Optional[str] = None,
        **kwargs
    ) -> Generator[Any]:
        """
        流式执行任务
        
        Args:
            message: 用户消息
            thread_id: 会话线程ID
            **kwargs: 额外参数
            
        Yields:
            StreamEvent 事件流
        """
        self._ensure_client()
        
        if thread_id:
            self._context.thread_id = thread_id
        
        if self._client is None:
            # 模拟流式响应
            yield from self._simulate_stream(message)
        else:
            # 实际 DeerFlow 流式执行
            full_message = f"{self._build_system_prompt()}\n\n用户请求: {message}"
            yield from self._client.stream(full_message, thread_id=self._context.thread_id, **kwargs)
    
    def _simulate_stream(self, message: str) -> Generator[Any, None, None]:
        """模拟流式响应"""
        from dataclasses import dataclass as stream_dataclass
        
        @stream_dataclass
        class SimulatedEvent:
            type: str
            data: Dict[str, Any]
        
        responses = [
            f"[{self.name}] ",
            f"正在处理请求...\n\n",
            f"智能体类型: {self.agent_type}\n",
            f"任务: {message}\n\n",
            f"[模拟模式 - DeerFlow 未连接]",
        ]
        
        full_content = ""
        for resp in responses:
            full_content += resp
            yield SimulatedEvent(
                type="messages-tuple",
                data={"type": "ai", "content": resp}
            )
        
        yield SimulatedEvent(
            type="end",
            data={"usage": {"input_tokens": 0, "output_tokens": len(full_content)}}
        )
    
    def reset_context(self):
        """重置执行上下文"""
        self._context = AgentContext()
        if self._client:
            self._client.reset_agent()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示"""
        return {
            "name": self.name,
            "agent_type": self.agent_type,
            "description": self.description,
            "capabilities": self.capabilities,
            "priority": self.priority,
            "agent_id": self.agent_id,
            "context": self._context.to_dict(),
        }


# 工厂函数
def create_agent_by_type(agent_type: str, **kwargs) -> BaseDeerFlowAgent:
    """
    根据类型创建智能体
    
    Args:
        agent_type: 智能体类型（AgentType 枚举值）
        **kwargs: 额外参数
        
    Returns:
        BaseDeerFlowAgent 实例
    """
    from app.agent_manager import AGENT_TEMPLATES
    
    # 查找智能体模板
    template = AGENT_TEMPLATES.get(agent_type, {})
    
    return BaseDeerFlowAgent(
        name=template.get("name", agent_type),
        agent_type=agent_type,
        description=template.get("description", ""),
        capabilities=template.get("capabilities", []),
        priority=template.get("priority", 5),**kwargs
    )
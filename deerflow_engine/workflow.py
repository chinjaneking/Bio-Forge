"""
Workflow Generator - 多智能体工作流编排

基于 DAG (有向无环图) 的工作流生成器，用于编排 Bio-Forge 的多智能体协作。

核心功能:
1. 定义工作流节点（智能体执行单元）
2. 定义边（依赖关系）
3. 工作流执行和调度
4. 预定义工作流模板（如酶设计流程）
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List, Callable, Set
from collections import defaultdict

logger = __import__("logging").getLogger(__name__)


class WorkflowStatus(Enum):
    """工作流状态"""
    DRAFT = "draft"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NodeStatus(Enum):
    """节点状态"""
    PENDING = "pending"
    WAITING = "waiting"  # 等待依赖完成
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowNode:
    """工作流节点"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    agent_type: str = ""  # 对应 AgentType
    agent_id: Optional[int] = None  # 具体智能体ID
    description: str = ""
    input_template: str = ""  # 输入模板，支持变量替换
    dependencies: List[str] = field(default_factory=list)  # 依赖的节点ID
    config: Dict[str, Any] = field(default_factory=dict)  # 节点配置
    timeout: int = 300  # 超时秒数
    retry_count: int = 0
    status: NodeStatus = NodeStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "agent_type": self.agent_type,
            "agent_id": self.agent_id,
            "description": self.description,
            "dependencies": self.dependencies,
            "config": self.config,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
        }


@dataclass
class WorkflowEdge:
    """工作流边（依赖关系）"""
    from_node: str
    to_node: str
    condition: Optional[Callable[[Dict], bool]] = None  # 条件函数
    transform: Optional[Callable[[Dict], Dict]] = None  # 数据转换函数
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_node,
            "to": self.to_node,
            "has_condition": self.condition is not None,
            "has_transform": self.transform is not None,
        }


@dataclass
class WorkflowDefinition:
    """工作流定义"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    version: str = "1.0"
    nodes: Dict[str, WorkflowNode] = field(default_factory=dict)
    edges: List[WorkflowEdge] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    status: WorkflowStatus = WorkflowStatus.DRAFT
    
    def add_node(self, node: WorkflowNode) -> "WorkflowDefinition":
        """添加节点"""
        self.nodes[node.id] = node
        return self
    
    def add_edge(self, edge: WorkflowEdge) -> "WorkflowDefinition":
        """添加边"""
        self.edges.append(edge)
        # 更新依赖关系
        if edge.to_node in self.nodes:
            self.nodes[edge.to_node].dependencies.append(edge.from_node)
        return self
    
    def get_entry_nodes(self) -> List[WorkflowNode]:
        """获取入口节点（无依赖）"""
        return [n for n in self.nodes.values() if not n.dependencies]
    
    def get_successors(self, node_id: str) -> List[WorkflowNode]:
        """获取后继节点"""
        successors = []
        for edge in self.edges:
            if edge.from_node == node_id:
                if edge.to_node in self.nodes:
                    successors.append(self.nodes[edge.to_node])
        return successors
    
    def get_predecessors(self, node_id: str) -> List[WorkflowNode]:
        """获取前驱节点"""
        node = self.nodes.get(node_id)
        if not node:
            return []
        return [self.nodes[dep] for dep in node.dependencies if dep in self.nodes]
    
    def topological_sort(self) -> List[str]:
        """拓扑排序，返回可执行的节点顺序"""
        # 计算入度（有多少节点依赖当前节点）
        in_degree = defaultdict(int)
        
        # 构建依赖图
        for node in self.nodes.values():
            for dep in node.dependencies:
                if dep in self.nodes:
                    in_degree[node.id] += 1
        
        # 入度为0的节点（没有依赖）
        queue = [n.id for n in self.nodes.values() if in_degree[n.id] == 0]
        result = []
        
        while queue:
            node_id = queue.pop(0)
            result.append(node_id)
            
            # 找到所有依赖于当前节点的节点
            for other_node in self.nodes.values():
                if node_id in other_node.dependencies:
                    in_degree[other_node.id] -= 1
                    if in_degree[other_node.id] == 0:
                        queue.append(other_node.id)
        
        if len(result) != len(self.nodes):
            raise ValueError("Workflow contains a cycle")
        
        return result
    
    def validate(self) -> List[str]:
        """验证工作流有效性"""
        errors = []
        
        # 检查节点
        for node in self.nodes.values():
            for dep in node.dependencies:
                if dep not in self.nodes:
                    errors.append(f"Node {node.id} depends on non-existent node {dep}")
        
        # 检查循环
        try:
            self.topological_sort()
        except ValueError as e:
            errors.append(str(e))
        
        # 检查入口节点
        if not self.get_entry_nodes():
            errors.append("Workflow has no entry nodes")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "edges": [e.to_dict() for e in self.edges],
            "metadata": self.metadata,
            "status": self.status.value,
        }


class WorkflowGenerator:
    """
    工作流生成器
    
    创建和管理多智能体协作的工作流。
    
    使用示例:
        workflow = WorkflowGenerator()
        workflow.create_enzyme_design_pipeline(target_sequence="MKTLL...")
        result = workflow.execute()
    """
    
    def __init__(self):
        self.current_workflow: Optional[WorkflowDefinition] = None
        self._execution_context: Dict[str, Any] = {}
    
    def create_workflow(
        self,
        name: str,
        description: str = "",
        version: str = "1.0"
    ) -> "WorkflowGenerator":
        """创建新工作流"""
        self.current_workflow = WorkflowDefinition(
            name=name,
            description=description,
            version=version,
        )
        return self
    
    def add_node(
        self,
        name: str,
        agent_type: str,
        input_template: str = "",
        dependencies: Optional[List[str]] = None,
        **config
    ) -> "WorkflowGenerator":
        """添加节点到当前工作流"""
        if not self.current_workflow:
            raise ValueError("No workflow created. Call create_workflow() first.")
        
        node = WorkflowNode(
            name=name,
            agent_type=agent_type,
            input_template=input_template,
            dependencies=dependencies or [],
            config=config,
        )
        self.current_workflow.add_node(node)
        return self
    
    def add_edge(
        self,
        from_node: str,
        to_node: str,
        condition: Optional[Callable] = None,
        transform: Optional[Callable] = None,
    ) -> "WorkflowGenerator":
        """添加边到当前工作流"""
        if not self.current_workflow:
            raise ValueError("No workflow created. Call create_workflow() first.")
        
        edge = WorkflowEdge(
            from_node=from_node,
            to_node=to_node,
            condition=condition,
            transform=transform,
        )
        self.current_workflow.add_edge(edge)
        return self
    
    # =========================================================================
    # 预定义工作流模板
    # =========================================================================
    
    def create_enzyme_design_pipeline(
        self,
        target_sequence: str,
        target_reaction: Optional[str] = None,**kwargs
    ) -> WorkflowDefinition:
        """
        创建酶设计工作流 pipeline
        
        智能体流程:
        1. 研发总监助手 - 任务分解和调度
        2. 蛋白质结构预测Agent- 结构分析
        3. 酶工程Agent - 设计候选序列
        4. 自由能计算Agent - 稳定性评估
        5. 量子化学计算Agent- 催化机制分析
        6. PCR引物设计Agent- 实验准备
        
        Args:
            target_sequence: 目标蛋白质序列
            target_reaction: 目标催化反应
            **kwargs: 额外配置
            
        Returns:
            WorkflowDefinition 工作流定义
        """
        self.create_workflow(
            name="Enzyme Design Pipeline",
            description="多智能体协作进行酶设计和优化",
            version="1.0"
        )
        
        # 节点定义
        nodes_config = [
            {
                "name": "Task Decomposition",
                "agent_type": "R_D_ASSISTANT",
                "input_template": f"分析以下酶设计任务并分解为子任务:\n目标序列: {target_sequence}\n目标反应: {target_reaction or '未指定'}",
            },
            {
                "name": "Structure Prediction",
                "agent_type": "PROTEIN_STRUCTURE_PREDICTOR",
                "input_template": "预测蛋白质结构: {task_decomposition_result}\n使用AlphaFold进行结构预测",
                "dependencies": ["node_0"],
            },
            {
                "name": "Enzyme Engineering",
                "agent_type": "ENZYME_ENGINEER",
                "input_template": "基于结构分析设计酶变体:\n结构预测结果: {structure_prediction_result}\n目标: 提高催化效率和稳定性",
                "dependencies": ["node_1"],
            },
            {
                "name": "Energy Calculation",
                "agent_type": "FREE_ENERGY_CALCULATOR",
                "input_template": "计算酶变体的自由能变化:\n变体序列: {enzyme_design_result}\n分析方法: FEP/MM-PBSA",
                "dependencies": ["node_2"],
            },
            {
                "name": "Mechanism Analysis",
                "agent_type": "QUANTUM_CHEMISTRY",
                "input_template": "分析催化机制:\n最优变体: {energy_calculation_result}\n计算过渡态和反应路径",
                "dependencies": ["node_3"],
            },
            {
                "name": "PCR Primer Design",
                "agent_type": "PCR_PRIMER_DESIGNER",
                "input_template": "设计PCR引物:\n最终序列: {mechanism_analysis_result}\n实验准备: 基因合成和克隆",
                "dependencies": ["node_4"],
            },
        ]
        
        # 添加节点（只使用 dependencies，不再额外添加边）
        for i, config in enumerate(nodes_config):
            node = WorkflowNode(
                id=f"node_{i}",
                name=config["name"],
                agent_type=config["agent_type"],
                input_template=config["input_template"],
                dependencies=config.get("dependencies", []),
            )
            self.current_workflow.add_node(node)
        
        # 验证
        errors = self.current_workflow.validate()
        if errors:
            raise ValueError(f"Invalid workflow: {errors}")
        
        self.current_workflow.status = WorkflowStatus.READY
        return self.current_workflow
    
    def create_synasalid_production_pipeline(
        self,
        target_concentration: float = 100.0,  # mg/L
        **kwargs
    ) -> WorkflowDefinition:
        """
        创建Synasalid (红景天苷) 生产工作流
        
        智能体流程:
        1. 研发总监助手 - 项目规划
        2. 代谢通路Agent- 路线设计
        3. 发酵优化Agent- 工艺参数
        4. 分析检测Agent- 质量控制
        5. 法规事务Agent- 合规审查
        
        Args:
            target_concentration: 目标产量 (mg/L)
            **kwargs: 额外配置
            
        Returns:
            WorkflowDefinition
        """
        self.create_workflow(
            name="Synasalid Production Pipeline",
            description="Synasalid生物合成生产全流程",
            version="1.0"
        )
        
        nodes_config = [
            {
                "name": "Project Planning",
                "agent_type": "R_D_DIRECTOR",
                "input_template": f"规划Synasalid生产项目:\n目标产量: {target_concentration} mg/L\n制定研发计划和里程碑",
            },
            {
                "name": "Pathway Design",
                "agent_type": "METABOLIC_PATHWAY",
                "input_template": "设计Synasalid生物合成途径:\n{project_planning_result}\n优化代谢流和前体供应",
                "dependencies": ["node_0"],
            },
            {
                "name": "Fermentation Optimization",
                "agent_type": "FERMENTATION_ENGINEER",
                "input_template": "优化发酵工艺:\n途径设计: {pathway_design_result}\n目标: 提高产率和降低成本",
                "dependencies": ["node_1"],
            },
            {
                "name": "Quality Control",
                "agent_type": "ANALYTICAL_CHEMIST",
                "input_template": "建立质量控制方案:\n发酵参数: {fermentation_result}\n检测方法: HPLC, MS",
                "dependencies": ["node_2"],
            },
            {
                "name": "Regulatory Review",
                "agent_type": "REGULATORY_EXPERT",
                "input_template": "合规性审查:\n质量方案: {qc_result}\n法规要求: FDA, EFSA",
                "dependencies": ["node_3"],
            },
        ]
        
        # 添加节点（只使用 dependencies，不再额外添加边）
        for i, config in enumerate(nodes_config):
            node = WorkflowNode(
                id=f"node_{i}",
                name=config["name"],
                agent_type=config["agent_type"],
                input_template=config["input_template"],
                dependencies=config.get("dependencies", []),
            )
            self.current_workflow.add_node(node)
        
        errors = self.current_workflow.validate()
        if errors:
            raise ValueError(f"Invalid workflow: {errors}")
        
        self.current_workflow.status = WorkflowStatus.READY
        return self.current_workflow


class WorkflowExecutor:
    """
    工作流执行器
    
    执行工作流并管理执行状态。
    """
    
    def __init__(self, workflow: WorkflowDefinition):
        self.workflow = workflow
        self.context: Dict[str, Any] = {}
        self.results: Dict[str, Dict[str, Any]] = {}
    
    def execute(self) -> Dict[str, Any]:
        """
        执行工作流
        
        Returns:
            执行结果字典
        """
        # 验证工作流
        errors = self.workflow.validate()
        if errors:
            raise ValueError(f"Invalid workflow: {errors}")
        
        # 获取执行顺序
        execution_order = self.workflow.topological_sort()
        
        # 执行节点
        for node_id in execution_order:
            node = self.workflow.nodes[node_id]
            self._execute_node(node)
        
        return self.results
    
    def _execute_node(self, node: WorkflowNode) -> None:
        """执行单个节点"""
        from deerflow_engine.base_agent import BaseDeerFlowAgent, ExecutionStatus
        
        node.status = NodeStatus.RUNNING
        node.started_at = datetime.now()
        
        try:
            # 准备输入
            input_data = self._prepare_input(node)
            
            # 创建智能体
            agent = BaseDeerFlowAgent(
                name=node.name,
                agent_type=node.agent_type,
                agent_id=node.agent_id,
                **node.config
            )
            
            # 执行
            result = agent.execute(input_data)
            
            if result.status == ExecutionStatus.SUCCESS:
                node.status = NodeStatus.SUCCESS
                node.result = result.to_dict()
                self.results[node.id] = result.to_dict()
                self.context[f"{node.id}_result"] = result.content
            else:
                node.status = NodeStatus.FAILED
                node.error = result.error
                raise Exception(f"Node {node.id} failed: {result.error}")
                
        except Exception as e:
            node.status = NodeStatus.FAILED
            node.error = str(e)
            logger.error(f"Node {node.id} execution failed: {e}")
            raise
        
        finally:
            node.completed_at = datetime.now()
    
    def _prepare_input(self, node: WorkflowNode) -> str:
        """准备节点输入"""
        input_text = node.input_template
        
        # 替换变量
        for key, value in self.context.items():
            placeholder = f"{{{key}}}"
            if placeholder in input_text:
                input_text = input_text.replace(placeholder, str(value))
        
        return input_text
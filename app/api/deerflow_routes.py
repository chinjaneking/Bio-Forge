"""
DeerFlow Integration API Routes

提供 DeerFlow 集成的 REST API 端点。
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, BackgroundTasks

router = APIRouter(prefix="/deerflow", tags=["DeerFlow Integration"])


# ============================================================================
# Request/Response Models
# ============================================================================

class EnzymeDesignRequest(BaseModel):
    """酶设计工作流请求"""
    target_sequence: str = Field(..., description="目标蛋白质序列")
    target_reaction: str = Field(..., description="目标催化反应")
    optimization_goals: Optional[List[str]] = Field(
        default=["thermal_stability", "catalytic_efficiency"],
        description="优化目标列表"
    )
    use_memory: bool = Field(default=True, description="是否启用记忆系统")
    callback_url: Optional[str] = Field(default=None, description="完成回调URL")


class SynasalidProductionRequest(BaseModel):
    """Synasalid 生产工作流请求"""
    target_concentration: float = Field(default=100.0, description="目标产量 (mg/L)")
    optimization_goals: Optional[List[str]] = Field(
        default=["yield", "purity", "cost_efficiency"],
        description="优化目标列表"
    )


class WorkflowStatus(BaseModel):
    """工作流状态"""
    workflow_id: str
    status: str
    progress: float
    current_node: Optional[str]
    completed_nodes: List[str]
    started_at: datetime
    estimated_completion: Optional[datetime]


class WorkflowResult(BaseModel):
    """工作流结果"""
    workflow_id: str
    workflow_name: str
    status: str
    total_duration: float
    success_rate: float
    nodes: List[Dict[str, Any]]
    memory_summary: Optional[Dict[str, Any]]
    generated_at: datetime


# ============================================================================
# In-Memory Workflow Registry (生产环境应使用 Redis)
# ============================================================================

_active_workflows: Dict[str, Dict[str, Any]] = {}


# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/enzyme-design", response_model=WorkflowStatus)
async def start_enzyme_design(
    request: EnzymeDesignRequest,
    background_tasks: BackgroundTasks,
):
    """
    启动酶设计工作流
    
    创建并异步执行酶设计多智能体协作流程。
    
    智能体流程:
    1. 研发总监助手 - 任务分解
    2. 蛋白质结构预测 - 结构分析
    3. 酶工程 - 设计候选序列
    4. 自由能计算 - 稳定性评估
    5. 量子化学计算 - 催化机制分析
    6. PCR引物设计 - 实验准备
    """
    import uuid
    from deerflow_engine import WorkflowGenerator, WorkflowExecutor
    
    # 生成工作流ID
    workflow_id = str(uuid.uuid4())[:8]
    
    # 创建工作流
    generator = WorkflowGenerator()
    workflow = generator.create_enzyme_design_pipeline(
        target_sequence=request.target_sequence,
        target_reaction=request.target_reaction,
    )
    
    # 添加优化目标
    if request.optimization_goals:
        workflow.metadata["optimization_goals"] = request.optimization_goals
    
    # 注册工作流
    _active_workflows[workflow_id] = {
        "workflow": workflow,
        "status": "pending",
        "progress": 0.0,
        "current_node": None,
        "completed_nodes": [],
        "started_at": datetime.now(),
        "request": request.dict(),
    }
    
    # 异步执行
    background_tasks.add_task(
        _execute_workflow_background,
        workflow_id,
        workflow,
        request.use_memory,
    )
    
    return WorkflowStatus(
        workflow_id=workflow_id,
        status="pending",
        progress=0.0,
        current_node=None,
        completed_nodes=[],
        started_at=datetime.now(),
        estimated_completion=None,
    )


@router.post("/synasalid-production", response_model=WorkflowStatus)
async def start_synasalid_production(
    request: SynasalidProductionRequest,
    background_tasks: BackgroundTasks,
):
    """
    启动 Synasalid 生产工作流
    
    创建并异步执行 Synasalid 生物合成生产全流程。
    
    智能体流程:
    1. 研发总监 - 项目规划
    2. 代谢通路设计 - 路线设计
    3. 发酵优化 - 工艺参数
    4. 分析检测 - 质量控制
    5. 法规事务 - 合规审查
    """
    import uuid
    from deerflow_engine import WorkflowGenerator
    
    # 生成工作流ID
    workflow_id = str(uuid.uuid4())[:8]
    
    # 创建工作流
    generator = WorkflowGenerator()
    workflow = generator.create_synasalid_production_pipeline(
        target_concentration=request.target_concentration,
    )
    
    # 添加优化目标
    if request.optimization_goals:
        workflow.metadata["optimization_goals"] = request.optimization_goals
    
    # 注册工作流
    _active_workflows[workflow_id] = {
        "workflow": workflow,
        "status": "pending",
        "progress": 0.0,
        "current_node": None,
        "completed_nodes": [],
        "started_at": datetime.now(),
        "request": request.dict(),
    }
    
    # 异步执行
    background_tasks.add_task(
        _execute_workflow_background,
        workflow_id,
        workflow,
        use_memory=True,
    )
    
    return WorkflowStatus(
        workflow_id=workflow_id,
        status="pending",
        progress=0.0,
        current_node=None,
        completed_nodes=[],
        started_at=datetime.now(),
        estimated_completion=None,
    )


@router.get("/workflow/{workflow_id}/status", response_model=WorkflowStatus)
async def get_workflow_status(workflow_id: str):
    """
    获取工作流状态
    
    返回指定工作流的当前执行状态。
    """
    if workflow_id not in _active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    wf = _active_workflows[workflow_id]
    
    return WorkflowStatus(
        workflow_id=workflow_id,
        status=wf.get("status", "unknown"),
        progress=wf.get("progress", 0.0),
        current_node=wf.get("current_node"),
        completed_nodes=wf.get("completed_nodes", []),
        started_at=wf.get("started_at"),
        estimated_completion=wf.get("estimated_completion"),
    )


@router.get("/workflow/{workflow_id}/result", response_model=WorkflowResult)
async def get_workflow_result(workflow_id: str):
    """
    获取工作流结果
    
    返回已完成工作流的详细结果。
    """
    if workflow_id not in _active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    wf = _active_workflows[workflow_id]
    
    if wf.get("status") != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Workflow is not completed. Current status: {wf.get('status')}"
        )
    
    return WorkflowResult(
        workflow_id=workflow_id,
        workflow_name=wf.get("workflow_name", "Unknown"),
        status=wf.get("status"),
        total_duration=wf.get("total_duration", 0),
        success_rate=wf.get("success_rate", 0),
        nodes=wf.get("node_results", []),
        memory_summary=wf.get("memory_summary"),
        generated_at=datetime.now(),
    )


@router.get("/workflows", response_model=List[Dict[str, Any]])
async def list_workflows(
    status: Optional[str] = None,
    limit: int = 20,
):
    """
    列出工作流
    
    返回所有或指定状态的工作流列表。
    """
    workflows = []
    
    for wf_id, wf in _active_workflows.items():
        if status and wf.get("status") != status:
            continue
        
        workflows.append({
            "workflow_id": wf_id,
            "status": wf.get("status"),
            "started_at": wf.get("started_at"),
            "progress": wf.get("progress"),
            "workflow_name": wf.get("workflow", {}).name if wf.get("workflow") else None,
        })
    
    return workflows[:limit]


# ============================================================================
# Background Tasks
# ============================================================================

def _execute_workflow_background(
    workflow_id: str,
    workflow,
    use_memory: bool,
):
    """后台执行工作流"""
    from deerflow_engine import WorkflowExecutor, AgentMemory, MemoryType, MemoryImportance
    
    try:
        # 更新状态
        _active_workflows[workflow_id]["status"] = "running"
        
        # 创建执行器
        executor = WorkflowExecutor(workflow)
        memory = AgentMemory(agent_id=1000) if use_memory else None
        
        # 获取执行顺序
        execution_order = workflow.topological_sort()
        total_nodes = len(execution_order)
        completed_nodes = []
        
        # 执行每个节点
        for node_id in execution_order:
            node = workflow.nodes[node_id]
            
            # 更新当前节点
            _active_workflows[workflow_id]["current_node"] = node_id
            
            # 执行节点
            executor._execute_node(node)
            
            # 更新进度
            completed_nodes.append(node_id)
            progress = len(completed_nodes) / total_nodes
            _active_workflows[workflow_id]["progress"] = progress
            _active_workflows[workflow_id]["completed_nodes"] = completed_nodes
        
        # 计算统计
        total_duration = sum(
            (node.completed_at - node.started_at).total_seconds()
            for node in workflow.nodes.values()
            if node.started_at and node.completed_at
        )
        
        success_count = sum(
            1 for node in workflow.nodes.values()
            if node.status.value == "success"
        )
        
        # 更新结果
        _active_workflows[workflow_id].update({
            "status": "completed",
            "progress": 1.0,
            "current_node": None,
            "completed_nodes": completed_nodes,
            "total_duration": total_duration,
            "success_rate": success_count / total_nodes,
            "node_results": [node.to_dict() for node in workflow.nodes.values()],
            "memory_summary": memory.get_summary() if memory else None,
        })
        
        # 记忆更新
        if memory:
            memory.remember(
                content=f"完成工作流 {workflow.name}，成功 {success_count}/{total_nodes} 节点",
                memory_type=MemoryType.EPISODIC,
                importance=MemoryImportance.HIGH,
                tags=["workflow", "completion"],
            )
        
    except Exception as e:
        _active_workflows[workflow_id]["status"] = "failed"
        _active_workflows[workflow_id]["error"] = str(e)
        raise


# ============================================================================
# Register Router
# ============================================================================

def register_deerflow_routes(app):
    """注册 DeerFlow 路由到 FastAPI 应用"""
    app.include_router(router)
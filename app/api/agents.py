"""智能体API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.agent_manager import AgentManager
from app.models.agent import Agent, AgentStatus, AgentType
from pydantic import BaseModel, Field

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentCreate(BaseModel):
    name: str = Field(..., description="智能体名称")
    description: str = Field(default="", description="描述")
    agent_type: AgentType = Field(..., description="智能体类型")
    config: Optional[dict] = Field(default={}, description="配置")
    capabilities: Optional[list] = Field(default=[], description="能力列表")
    priority: int = Field(default=5, ge=1, le=10, description="优先级1-10")
    implementation: str = Field(default="", description="实现路径")


class AgentUpdate(BaseModel):
    description: Optional[str] = None
    config: Optional[dict] = None
    capabilities: Optional[list] = None
    priority: Optional[int] = None
    status: Optional[AgentStatus] = None


class AgentResponse(BaseModel):
    id: int
    name: str
    description: str
    agent_type: AgentType
    status: AgentStatus
    version: str
    priority: int
    config: dict
    capabilities: list
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    avg_execution_time: int
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("", response_model=AgentResponse)
def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    """创建智能体"""
    manager = AgentManager(db)
    
    # 检查名称是否已存在
    existing = manager.get_agent_by_name(agent_data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Agent name already exists")
    
    agent = manager.create_agent(**agent_data.model_dump())
    return agent


@router.get("", response_model=List[AgentResponse])
def list_agents(
    agent_type: Optional[AgentType] = None,
    status: Optional[AgentStatus] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """列出智能体"""
    manager = AgentManager(db)
    agents = manager.list_agents(agent_type=agent_type, status=status, skip=skip, limit=limit)
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """获取智能体详情"""
    manager = AgentManager(db)
    agent = manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{agent_id}/activate")
def activate_agent(agent_id: int, db: Session = Depends(get_db)):
    """激活智能体"""
    manager = AgentManager(db)
    if not manager.activate_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent activated"}


@router.put("/{agent_id}/deactivate")
def deactivate_agent(agent_id: int, db: Session = Depends(get_db)):
    """停用智能体"""
    manager = AgentManager(db)
    if not manager.deactivate_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deactivated"}


@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """删除智能体"""
    manager = AgentManager(db)
    if not manager.delete_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted"}

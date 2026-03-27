"""任务API"""
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.task_scheduler import TaskScheduler
from app.models.task import Task, TaskStatus, TaskPriority
from pydantic import BaseModel, Field

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    name: str = Field(..., description="任务名称")
    agent_id: int = Field(..., description="智能体ID")
    input_data: Optional[dict] = Field(default={}, description="输入数据")
    description: str = Field(default="", description="任务描述")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="优先级")
    timeout: int = Field(default=3600, ge=60, description="超时时间秒")


class TaskResponse(BaseModel):
    id: int
    task_id: str
    name: str
    description: str
    agent_id: int
    status: TaskStatus
    priority: TaskPriority
    progress: int
    input_data: dict
    output_data: dict
    error_message: Optional[str]
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    execution_time: Optional[int]
    
    class Config:
        from_attributes = True


def execute_task_background(task_id: str, db: Session):
    """后台执行任务"""
    scheduler = TaskScheduler(db)
    task = scheduler.get_task_by_task_id(task_id)
    if task:
        scheduler.execute_task(task)


@router.post("", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """创建并队列任务"""
    scheduler = TaskScheduler(db)
    task = scheduler.create_task(**task_data.model_dump())
    
    # 加入队列
    scheduler.queue_task(task.task_id)
    
    # 后台执行（简化演示）
    background_tasks.add_task(execute_task_background, task.task_id, db)
    
    return task


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[TaskStatus] = None,
    agent_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """列出任务"""
    scheduler = TaskScheduler(db)
    tasks = scheduler.list_tasks(status=status, agent_id=agent_id, skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    """获取任务详情"""
    scheduler = TaskScheduler(db)
    task = scheduler.get_task_by_task_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}/cancel")
def cancel_task(task_id: str, db: Session = Depends(get_db)):
    """取消任务"""
    scheduler = TaskScheduler(db)
    if not scheduler.cancel_task(task_id):
        raise HTTPException(status_code=400, detail="Cannot cancel task")
    return {"message": "Task cancelled"}


@router.get("/status/queue")
def get_queue_status(db: Session = Depends(get_db)):
    """获取队列状态"""
    scheduler = TaskScheduler(db)
    return scheduler.get_queue_status()

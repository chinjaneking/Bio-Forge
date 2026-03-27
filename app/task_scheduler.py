"""任务调度器"""
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
import time
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.agent import Agent, AgentStatus
from app.redis_client import redis_client
from app.agent_manager import AgentManager


class TaskScheduler:
    """任务调度核心类"""
    
    TASK_QUEUE = "deerflow:task_queue"
    RUNNING_TASKS = "deerflow:running_tasks"
    
    def __init__(self, db: Session):
        self.db = db
        self.agent_manager = AgentManager(db)
    
    def create_task(
        self,
        name: str,
        agent_id: int,
        input_data: Optional[Dict] = None,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        timeout: int = 3600,
        parent_task_id: Optional[int] = None
    ) -> Task:
        """创建任务"""
        task_id = f"task-{uuid.uuid4().hex[:12]}"
        
        task = Task(
            task_id=task_id,
            name=name,
            description=description,
            agent_id=agent_id,
            priority=priority,
            timeout=timeout,
            input_data=input_data or {},
            parent_task_id=parent_task_id,
            status=TaskStatus.PENDING
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def queue_task(self, task_id: str) -> bool:
        """将任务加入队列"""
        task = self.get_task_by_task_id(task_id)
        if not task:
            return False
        
        # 更新任务状态
        task.status = TaskStatus.QUEUED
        self.db.commit()
        
        # 加入Redis队列
        queue_data = {
            "task_id": task.task_id,
            "agent_id": task.agent_id,
            "priority": task.priority,
            "created_at": task.created_at.isoformat()
        }
        
        redis_client.push_queue(self.TASK_QUEUE, queue_data)
        return True
    
    def get_next_task(self) -> Optional[Task]:
        """获取下一个待执行任务"""
        queue_data = redis_client.pop_queue(self.TASK_QUEUE, timeout=1)
        if not queue_data:
            return None
        
        task = self.get_task_by_task_id(queue_data["task_id"])
        return task
    
    def execute_task(self, task: Task) -> bool:
        """执行任务"""
        agent = self.agent_manager.get_agent(task.agent_id)
        if not agent or agent.status != AgentStatus.ACTIVE:
            task.status = TaskStatus.FAILED
            task.error_message = "Agent not available"
            self.db.commit()
            return False
        
        # 更新任务状态
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        agent.status = AgentStatus.BUSY
        self.db.commit()
        
        # 记录运行中任务
        redis_client.set(f"{self.RUNNING_TASKS}:{task.task_id}", {
            "task_id": task.task_id,
            "agent_id": agent.id,
            "started_at": task.started_at.isoformat()
        })
        
        try:
            # 这里是实际执行智能体的地方
            # 目前先模拟执行
            result = self._simulate_agent_execution(task, agent)
            
            # 成功
            task.status = TaskStatus.COMPLETED
            task.output_data = result
            task.progress = 100
            
        except Exception as e:
            # 失败
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
        
        finally:
            # 更新完成时间和执行时间
            task.completed_at = datetime.utcnow()
            if task.started_at:
                task.execution_time = int((task.completed_at - task.started_at).total_seconds())
            
            # 更新智能体状态
            agent.status = AgentStatus.ACTIVE
            agent.total_tasks += 1
            if task.status == TaskStatus.COMPLETED:
                agent.successful_tasks += 1
            else:
                agent.failed_tasks += 1
            
            # 计算平均执行时间
            if task.execution_time:
                total_time = agent.avg_execution_time * (agent.total_tasks - 1) + task.execution_time
                agent.avg_execution_time = total_time // agent.total_tasks
            
            self.db.commit()
            
            # 清理运行中任务
            redis_client.delete(f"{self.RUNNING_TASKS}:{task.task_id}")
        
        return task.status == TaskStatus.COMPLETED
    
    def _simulate_agent_execution(self, task: Task, agent: Agent) -> Dict:
        """模拟智能体执行"""
        # 模拟执行时间
        import time
        time.sleep(2)
        
        # 返回模拟结果
        return {
            "status": "success",
            "agent": agent.name,
            "task": task.name,
            "input": task.input_data,
            "timestamp": datetime.utcnow().isoformat(),
            "result": "Task executed successfully"
        }
    
    def get_task(self, task_db_id: int) -> Optional[Task]:
        """获取任务"""
        return self.db.query(Task).filter(Task.id == task_db_id).first()
    
    def get_task_by_task_id(self, task_id: str) -> Optional[Task]:
        """通过任务ID获取任务"""
        return self.db.query(Task).filter(Task.task_id == task_id).first()
    
    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        agent_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """列出任务"""
        query = self.db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if agent_id:
            query = query.filter(Task.agent_id == agent_id)
        
        return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self.get_task_by_task_id(task_id)
        if not task or task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            return False
        
        task.status = TaskStatus.CANCELLED
        self.db.commit()
        return True
    
    def get_queue_status(self) -> Dict:
        """获取队列状态"""
        return {
            "queue_length": redis_client.queue_len(self.TASK_QUEUE),
            "pending": self.db.query(Task).filter(Task.status == TaskStatus.PENDING).count(),
            "queued": self.db.query(Task).filter(Task.status == TaskStatus.QUEUED).count(),
            "running": self.db.query(Task).filter(Task.status == TaskStatus.RUNNING).count(),
            "completed": self.db.query(Task).filter(Task.status == TaskStatus.COMPLETED).count(),
            "failed": self.db.query(Task).filter(Task.status == TaskStatus.FAILED).count()
        }

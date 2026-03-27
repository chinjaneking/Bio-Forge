"""任务模型"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database import Base


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """任务优先级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    """任务"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # 关联
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    agent = relationship("Agent", back_populates="tasks")
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    # 状态
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, index=True)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM)
    progress = Column(Integer, default=0)  # 0-100
    
    # 数据
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    error_message = Column(Text)
    logs = Column(JSON, default=list)
    
    # 时间
    timeout = Column(Integer, default=3600)  # 秒
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    execution_time = Column(Integer)  # 秒
    
    # 关系
    subtasks = relationship("Task", remote_side=[id])
    
    def __repr__(self):
        return f"<Task {self.task_id} {self.status}>"

"""智能体模型"""
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database import Base


class AgentStatus(str, Enum):
    """智能体状态"""
    INACTIVE = "inactive"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"


class AgentType(str, Enum):
    """智能体类型"""
    # 基础架构类
    FOUNDATION = "foundation"
    PLATFORM_MANAGEMENT = "platform_management"
    DATA_MANAGEMENT = "data_management"
    SECURITY_MONITORING = "security_monitoring"
    
    # 计算设计类
    MOLECULAR_MODELING = "molecular_modeling"
    PROTEIN_ENGINEERING = "protein_engineering"
    PATHWAY_DESIGN = "pathway_design"
    GENOME_DESIGN = "genome_design"
    
    # 实验实验室类
    MOLECULAR_BIOLOGY = "molecular_biology"
    MICROBIOLOGY = "microbiology"
    FERMENTATION_OPTIMIZATION = "fermentation_optimization"
    ANALYTICAL_CHEMISTRY = "analytical_chemistry"
    
    # 优化验证类
    YIELD_OPTIMIZATION = "yield_optimization"
    STABILITY_ENHANCEMENT = "stability_enhancement"
    SCALE_UP = "scale_up"
    
    # 研发助理类
    LITERATURE_RESEARCH = "literature_research"
    PATENT_RESEARCH = "patent_research"
    EXPERIMENT_DESIGN = "experiment_design"
    BIOINFORMATICS = "bioinformatics"
    STATISTICAL_MODELING = "statistical_modeling"
    PROJECT_MANAGEMENT = "project_management"
    QUALITY_CONTROL = "quality_control"
    REGULATORY_AFFAIRS = "regulatory_affairs"
    
    # 项目专项类
    R_D_ASSISTANT = "r_d_assistant"
    RHODIOLA_PROJECT = "rhodiola_project"


class Agent(Base):
    """智能体"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text)
    agent_type = Column(SQLEnum(AgentType), nullable=False, index=True)
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.INACTIVE)
    version = Column(String(50), default="1.0.0")
    priority = Column(Integer, default=5)
    
    # 配置
    config = Column(JSON, default=dict)
    capabilities = Column(JSON, default=list)
    input_schema = Column(JSON, default=dict)
    output_schema = Column(JSON, default=dict)
    
    # 技术实现
    implementation = Column(Text)  # 实现代码路径或引用
    container_image = Column(String(500))
    requirements = Column(JSON, default=list)
    dependencies = Column(JSON, default=list)
    
    # 统计
    total_tasks = Column(Integer, default=0)
    successful_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    avg_execution_time = Column(Integer, default=0)  # 秒
    
    # 时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active_at = Column(DateTime)
    
    # 关系
    tasks = relationship("Task", back_populates="agent")
    
    def __repr__(self):
        return f"<Agent {self.name} ({self.agent_type})>"

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
    PLATFORM_MANAGEMENT = "平台管理"
    DATA_MANAGEMENT = "数据管理"
    SECURITY_MONITORING = "安全监控"
    
    # 生命设计类
    DESIGN = "design"
    GENOME_DESIGN = "基因组设计"
    PROTEIN_DESIGN = "蛋白质设计"
    CELL_DESIGN = "细胞设计"
    TISSUE_DESIGN = "组织设计"
    PATHWAY_DESIGN = "通路设计"
    METABOLIC_ENGINEERING = "代谢工程"
    
    # 实验执行类
    EXECUTION = "execution"
    DNA_SYNTHESIS = "DNA合成"
    CELL_ASSEMBLY = "细胞组装"
    CULTURE_OPTIMIZATION = "培养优化"
    ASSAY_VALIDATION = "分析验证"
    LAB_AUTOMATION = "实验室自动化"
    
    # 进化优化类
    OPTIMIZATION = "optimization"
    ADAPTIVE_EVOLUTION = "适应性进化"
    FUNCTION_OPTIMIZATION = "功能优化"
    STABILITY_ENHANCEMENT = "稳定性增强"
    DIRECTED_EVOLUTION = "定向进化"
    
    # 研发管理类
    R_D_ASSISTANT = "研发总监助手"
    PROJECT_MANAGEMENT = "项目管理"
    LITERATURE_RESEARCH = "文献调研"
    EXPERIMENT_DESIGN = "实验设计"
    DATA_ANALYSIS = "数据分析"
    BIOINFORMATICS = "生物信息学"
    CHEMINFORMATICS = "化学信息学"
    STATISTICAL_MODELING = "统计建模"
    PATENT_RESEARCH = "专利调研"
    REGULATORY_AFFAIRS = "注册事务"
    QUALITY_CONTROL = "质量控制"
    
    # 项目专项类
    RHODIOLA_PROJECT = "红景天苷项目专项"
    SYNTHETIC_BIOLOGY = "合成生物学专项"
    PROTEIN_DRUG_DISCOVERY = "蛋白质药物发现"
    CELL_THERAPY_ENGINEERING = "细胞治疗工程"


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

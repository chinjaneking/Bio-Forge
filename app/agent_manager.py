"""
Bio-Forge 120智能体矩阵 - Agent管理器
Copyright (c) 2026 灵知生物科技
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.agent import Agent, AgentType, AgentStatus


class AgentManager:
    """智能体管理器"""
    
    def __init__(self, db: Session):
        self.db = db
        self._agents_cache: Dict[int, Agent] = {}
    
    def create_agent(
        self,
        name: str,
        description: str,
        agent_type: AgentType,
        priority: int = 3,
        capabilities: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Agent:
        """创建智能体"""
        agent = Agent(
            name=name,
            description=description,
            agent_type=agent_type,
            status=AgentStatus.ACTIVE,
            priority=priority,
            capabilities=capabilities or [],
            config=config or {}
        )
        
        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)
        
        self._agents_cache[agent.id] = agent
        return agent
    
    def get_agent(self, agent_id: int) -> Optional[Agent]:
        """通过ID获取智能体"""
        if agent_id in self._agents_cache:
            return self._agents_cache[agent_id]
        
        agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        if agent:
            self._agents_cache[agent.id] = agent
        return agent
    
    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """通过名称获取智能体"""
        return self.db.query(Agent).filter(Agent.name == name).first()
    
    def list_agents(
        self,
        agent_type: Optional[AgentType] = None,
        status: Optional[AgentStatus] = None,
        skip: int = 0,
        limit: int = 200
    ) -> List[Agent]:
        """列出智能体"""
        query = self.db.query(Agent)
        
        if agent_type:
            query = query.filter(Agent.agent_type == agent_type)
        if status:
            query = query.filter(Agent.status == status)
        
        return query.order_by(Agent.priority.desc()).offset(skip).limit(limit).all()
    
    def update_agent_status(self, agent_id: int, status: AgentStatus) -> bool:
        """更新智能体状态"""
        agent = self.get_agent(agent_id)
        if not agent:
            return False
        
        agent.status = status
        agent.last_active_at = datetime.utcnow()
        self.db.commit()
        
        if agent_id in self._agents_cache:
            self._agents_cache[agent_id] = agent
        
        return True
    
    def activate_agent(self, agent_id: int) -> bool:
        """激活智能体"""
        return self.update_agent_status(agent_id, AgentStatus.ACTIVE)
    
    def deactivate_agent(self, agent_id: int) -> bool:
        """停用智能体"""
        return self.update_agent_status(agent_id, AgentStatus.INACTIVE)
    
    def delete_agent(self, agent_id: int) -> bool:
        """删除智能体"""
        agent = self.get_agent(agent_id)
        if not agent:
            return False
        
        self.db.delete(agent)
        self.db.commit()
        
        if agent_id in self._agents_cache:
            del self._agents_cache[agent_id]
        
        return True
    
    def get_available_agent(self, agent_type: Optional[AgentType] = None) -> Optional[Agent]:
        """获取可用的智能体"""
        query = self.db.query(Agent).filter(
            Agent.status == AgentStatus.ACTIVE
        )
        
        if agent_type:
            query = query.filter(Agent.agent_type == agent_type)
        
        return query.order_by(Agent.priority.desc()).first()
    
    def initialize_default_agents(self):
        """初始化120个分层专业智能体矩阵"""
        if self.db.query(Agent).count() > 0:
            return
        
        default_agents = [
            { "name": "研发总监助手", "description": "协助研发总监进行日常管理、任务协调和决策支持", "agent_type": AgentType.R_D_ASSISTANT, "priority": 1, "capabilities": [] },
            { "name": "平台架构师", "description": "Bio-Forge平台架构设计、技术选型和系统集成", "agent_type": AgentType.PLATFORM_MANAGEMENT, "priority": 2, "capabilities": [] },
            { "name": "API网关管理", "description": "API接口管理、路由配置和负载均衡", "agent_type": AgentType.PLATFORM_MANAGEMENT, "priority": 3, "capabilities": [] },
            { "name": "容器编排智能体", "description": "Docker容器管理、部署和扩缩容", "agent_type": AgentType.PLATFORM_MANAGEMENT, "priority": 3, "capabilities": [] },
            { "name": "监控告警智能体", "description": "系统监控、性能指标收集和异常告警", "agent_type": AgentType.PLATFORM_MANAGEMENT, "priority": 4, "capabilities": [] },
            { "name": "数据架构师", "description": "数据架构设计、数据模型和数据治理", "agent_type": AgentType.DATA_MANAGEMENT, "priority": 2, "capabilities": [] },
            { "name": "数据集成智能体", "description": "多源数据集成、ETL流程和数据同步", "agent_type": AgentType.DATA_MANAGEMENT, "priority": 3, "capabilities": [] },
            { "name": "数据质量智能体", "description": "数据质量检查、清洗和质量报告", "agent_type": AgentType.DATA_MANAGEMENT, "priority": 3, "capabilities": [] },
            { "name": "数据备份恢复", "description": "数据备份策略、恢复演练和灾难恢复", "agent_type": AgentType.DATA_MANAGEMENT, "priority": 3, "capabilities": [] },
            { "name": "知识图谱管理", "description": "知识图谱构建、维护和知识推理", "agent_type": AgentType.DATA_MANAGEMENT, "priority": 4, "capabilities": [] },
            { "name": "身份认证管理", "description": "用户身份认证、权限管理和访问控制", "agent_type": AgentType.SECURITY_MONITORING, "priority": 2, "capabilities": [] },
            { "name": "漏洞扫描智能体", "description": "系统漏洞扫描、安全评估和修复建议", "agent_type": AgentType.SECURITY_MONITORING, "priority": 3, "capabilities": [] },
            { "name": "日志审计智能体", "description": "安全日志收集、分析和异常检测", "agent_type": AgentType.SECURITY_MONITORING, "priority": 3, "capabilities": [] },
            { "name": "加密管理智能体", "description": "数据加密、密钥管理和加密策略", "agent_type": AgentType.SECURITY_MONITORING, "priority": 3, "capabilities": [] },
            { "name": "合规管理智能体", "description": "法规合规检查、合规报告和合规培训", "agent_type": AgentType.SECURITY_MONITORING, "priority": 4, "capabilities": [] },
            { "name": "量子化学计算智能体", "description": "量子化学计算、电子结构和反应机制", "agent_type": AgentType.MOLECULAR_MODELING, "priority": 1, "capabilities": [] },
            { "name": "分子动力学模拟智能体", "description": "分子动力学模拟、构象分析和动力学", "agent_type": AgentType.MOLECULAR_MODELING, "priority": 1, "capabilities": [] },
            { "name": "分子对接智能体", "description": "分子对接、虚拟筛选和结合模式", "agent_type": AgentType.MOLECULAR_MODELING, "priority": 1, "capabilities": [] },
            { "name": "自由能计算智能体", "description": "自由能计算、结合亲和力和热力学", "agent_type": AgentType.MOLECULAR_MODELING, "priority": 2, "capabilities": [] },
            { "name": "量子力学/分子力学智能体", "description": "QM/MM计算、酶催化和反应路径", "agent_type": AgentType.MOLECULAR_MODELING, "priority": 2, "capabilities": [] },
            { "name": "多尺度模拟智能体", "description": "多尺度模拟、粗粒化和尺度桥接", "agent_type": AgentType.MOLECULAR_MODELING, "priority": 2, "capabilities": [] },
            { "name": "光谱模拟智能体", "description": "光谱模拟、NMR和IR光谱预测", "agent_type": AgentType.MOLECULAR_MODELING, "priority": 3, "capabilities": [] },
            { "name": "蛋白质结构预测智能体", "description": "蛋白质结构预测、结构建模和结构分析", "agent_type": AgentType.PROTEIN_ENGINEERING, "priority": 1, "capabilities": [] },
            { "name": "蛋白质设计智能体", "description": "蛋白质设计、序列设计和功能设计", "agent_type": AgentType.PROTEIN_ENGINEERING, "priority": 1, "capabilities": [] },
            { "name": "蛋白质功能预测智能体", "description": "蛋白质功能预测、功能注释和功能分析", "agent_type": AgentType.PROTEIN_ENGINEERING, "priority": 1, "capabilities": [] },
            { "name": "酶工程智能体", "description": "酶工程、催化优化和底物特异性", "agent_type": AgentType.PROTEIN_ENGINEERING, "priority": 1, "capabilities": [] },
            { "name": "抗体工程智能体", "description": "抗体工程、人源化和亲和力成熟", "agent_type": AgentType.PROTEIN_ENGINEERING, "priority": 2, "capabilities": [] },
            { "name": "蛋白质-蛋白质对接智能体", "description": "蛋白质-蛋白质对接、复合物建模和相互作用", "agent_type": AgentType.PROTEIN_ENGINEERING, "priority": 2, "capabilities": [] },
            { "name": "变构位点预测智能体", "description": "变构位点预测、变构调节和变构药物", "agent_type": AgentType.PROTEIN_ENGINEERING, "priority": 3, "capabilities": [] },
            { "name": "代谢途径设计智能体", "description": "代谢途径设计、途径重建和途径优化", "agent_type": AgentType.PATHWAY_DESIGN, "priority": 1, "capabilities": [] },
            { "name": "代谢流分析智能体", "description": "代谢流分析、FBA和通量预测", "agent_type": AgentType.PATHWAY_DESIGN, "priority": 1, "capabilities": [] },
            { "name": "基因回路设计智能体", "description": "基因回路设计、逻辑电路和调控网络", "agent_type": AgentType.PATHWAY_DESIGN, "priority": 2, "capabilities": [] },
            { "name": "途径鲁棒性分析智能体", "description": "途径鲁棒性分析、敏感性分析和稳定性", "agent_type": AgentType.PATHWAY_DESIGN, "priority": 2, "capabilities": [] },
            { "name": "辅因子平衡智能体", "description": "辅因子平衡、氧化还原平衡和能量平衡", "agent_type": AgentType.PATHWAY_DESIGN, "priority": 2, "capabilities": [] },
            { "name": "途径优化算法智能体", "description": "途径优化算法、多目标优化和全局优化", "agent_type": AgentType.PATHWAY_DESIGN, "priority": 3, "capabilities": [] },
            { "name": "基因组分析智能体", "description": "基因组分析、基因组注释和比较基因组", "agent_type": AgentType.GENOME_DESIGN, "priority": 1, "capabilities": [] },
            { "name": "DNA序列生成智能体", "description": "DNA序列生成、密码子优化和序列设计", "agent_type": AgentType.GENOME_DESIGN, "priority": 1, "capabilities": [] },
            { "name": "基因敲除预测智能体", "description": "基因敲除预测、必需基因分析和表型预测", "agent_type": AgentType.GENOME_DESIGN, "priority": 1, "capabilities": [] },
            { "name": "启动子设计智能体", "description": "启动子设计、调控元件和表达调控", "agent_type": AgentType.GENOME_DESIGN, "priority": 2, "capabilities": [] },
            { "name": "终止子设计智能体", "description": "终止子设计、转录终止和mRNA稳定性", "agent_type": AgentType.GENOME_DESIGN, "priority": 2, "capabilities": [] },
            { "name": "PCR引物设计智能体", "description": "PCR引物设计、qPCR引物和突变引物", "agent_type": AgentType.MOLECULAR_BIOLOGY, "priority": 1, "capabilities": [] },
            { "name": "克隆策略设计智能体", "description": "克隆策略设计、组装策略和质粒构建", "agent_type": AgentType.MOLECULAR_BIOLOGY, "priority": 1, "capabilities": [] },
            { "name": "测序数据分析智能体", "description": "测序数据分析、序列比对和变异检测", "agent_type": AgentType.MOLECULAR_BIOLOGY, "priority": 1, "capabilities": [] },
            { "name": "qPCR分析智能体", "description": "qPCR数据分析、相对定量和表达分析", "agent_type": AgentType.MOLECULAR_BIOLOGY, "priority": 2, "capabilities": [] },
            { "name": "CRISPR设计智能体", "description": "CRISPR设计、sgRNA设计和脱靶预测", "agent_type": AgentType.MOLECULAR_BIOLOGY, "priority": 1, "capabilities": [] },
            { "name": "RNAi设计智能体", "description": "RNAi设计、siRNA设计和shRNA设计", "agent_type": AgentType.MOLECULAR_BIOLOGY, "priority": 3, "capabilities": [] },
            { "name": "菌株选择智能体", "description": "菌株选择、宿主选择和底盘优化", "agent_type": AgentType.MICROBIOLOGY, "priority": 1, "capabilities": [] },
            { "name": "培养基优化智能体", "description": "培养基优化、成分优化和营养平衡", "agent_type": AgentType.MICROBIOLOGY, "priority": 1, "capabilities": [] },
            { "name": "发酵工艺优化智能体", "description": "发酵工艺优化、参数优化和控制策略", "agent_type": AgentType.FERMENTATION_OPTIMIZATION, "priority": 1, "capabilities": [] },
            { "name": "生长曲线分析智能体", "description": "生长曲线分析、比生长速率和生长动力学", "agent_type": AgentType.MICROBIOLOGY, "priority": 2, "capabilities": [] },
            { "name": "无菌控制智能体", "description": "无菌控制、污染检测和污染防控", "agent_type": AgentType.MICROBIOLOGY, "priority": 2, "capabilities": [] },
            { "name": "菌种保藏智能体", "description": "菌种保藏、保藏方法和菌种复苏", "agent_type": AgentType.MICROBIOLOGY, "priority": 3, "capabilities": [] },
            { "name": "微生物鉴定智能体", "description": "微生物鉴定、物种鉴定和分型", "agent_type": AgentType.MICROBIOLOGY, "priority": 3, "capabilities": [] },
            { "name": "HPLC分析智能体", "description": "HPLC分析、方法开发和数据分析", "agent_type": AgentType.ANALYTICAL_CHEMISTRY, "priority": 1, "capabilities": [] },
            { "name": "GC分析智能体", "description": "GC分析、方法开发和质谱联用", "agent_type": AgentType.ANALYTICAL_CHEMISTRY, "priority": 1, "capabilities": [] },
            { "name": "质谱分析智能体", "description": "质谱分析、化合物鉴定和定量分析", "agent_type": AgentType.ANALYTICAL_CHEMISTRY, "priority": 1, "capabilities": [] },
            { "name": "光谱分析智能体", "description": "光谱分析、UV-Vis、荧光和红外", "agent_type": AgentType.ANALYTICAL_CHEMISTRY, "priority": 2, "capabilities": [] },
            { "name": "蛋白定量智能体", "description": "蛋白定量、BCA、Bradford和WB", "agent_type": AgentType.ANALYTICAL_CHEMISTRY, "priority": 2, "capabilities": [] },
            { "name": "代谢组学分析智能体", "description": "代谢组学分析、代谢物鉴定和通路分析", "agent_type": AgentType.ANALYTICAL_CHEMISTRY, "priority": 2, "capabilities": [] },
            { "name": "数据分析可视化智能体", "description": "数据分析、统计分析和可视化", "agent_type": AgentType.ANALYTICAL_CHEMISTRY, "priority": 3, "capabilities": [] },
            { "name": "产量优化智能体", "description": "产量优化、滴度提升和生产效率", "agent_type": AgentType.YIELD_OPTIMIZATION, "priority": 1, "capabilities": [] },
            { "name": "底物利用优化智能体", "description": "底物利用优化、碳源优化和副产物减少", "agent_type": AgentType.YIELD_OPTIMIZATION, "priority": 1, "capabilities": [] },
            { "name": "代谢瓶颈识别智能体", "description": "代谢瓶颈识别、限速步骤和通量分析", "agent_type": AgentType.YIELD_OPTIMIZATION, "priority": 1, "capabilities": [] },
            { "name": "反馈抑制解除智能体", "description": "反馈抑制解除、变构调节和代谢调控", "agent_type": AgentType.YIELD_OPTIMIZATION, "priority": 2, "capabilities": [] },
            { "name": "前体供应优化智能体", "description": "前体供应优化、前体合成和供给策略", "agent_type": AgentType.YIELD_OPTIMIZATION, "priority": 2, "capabilities": [] },
            { "name": "能量代谢优化智能体", "description": "能量代谢优化、ATP再生和能量效率", "agent_type": AgentType.YIELD_OPTIMIZATION, "priority": 2, "capabilities": [] },
            { "name": "多目标优化智能体", "description": "多目标优化、帕累托优化和权衡分析", "agent_type": AgentType.YIELD_OPTIMIZATION, "priority": 3, "capabilities": [] },
            { "name": "蛋白质稳定性增强智能体", "description": "蛋白质稳定性增强、突变设计和稳定性预测", "agent_type": AgentType.STABILITY_ENHANCEMENT, "priority": 2, "capabilities": [] },
            { "name": "遗传稳定性智能体", "description": "遗传稳定性优化、重组避免和基因组稳定", "agent_type": AgentType.STABILITY_ENHANCEMENT, "priority": 2, "capabilities": [] },
            { "name": "生产稳定性智能体", "description": "生产稳定性优化、传代稳定和规模稳定", "agent_type": AgentType.STABILITY_ENHANCEMENT, "priority": 2, "capabilities": [] },
            { "name": "储存稳定性智能体", "description": "储存稳定性优化、配方优化和储存条件", "agent_type": AgentType.STABILITY_ENHANCEMENT, "priority": 3, "capabilities": [] },
            { "name": "降解机制分析智能体", "description": "降解机制分析、降解途径和降解预测", "agent_type": AgentType.STABILITY_ENHANCEMENT, "priority": 3, "capabilities": [] },
            { "name": "稳定剂筛选智能体", "description": "稳定剂筛选、添加剂优化和配方开发", "agent_type": AgentType.STABILITY_ENHANCEMENT, "priority": 3, "capabilities": [] },
            { "name": "压力耐受性智能体", "description": "压力耐受性增强、胁迫抵抗和鲁棒性优化", "agent_type": AgentType.STABILITY_ENHANCEMENT, "priority": 2, "capabilities": [] },
            { "name": "中试放大智能体", "description": "中试放大、工艺放大和规模转移", "agent_type": AgentType.SCALE_UP, "priority": 1, "capabilities": [] },
            { "name": "工艺验证智能体", "description": "工艺验证、验证方案和确认报告", "agent_type": AgentType.SCALE_UP, "priority": 1, "capabilities": [] },
            { "name": "清洁验证智能体", "description": "清洁验证、清洁方法和残留检测", "agent_type": AgentType.SCALE_UP, "priority": 2, "capabilities": [] },
            { "name": "连续生产智能体", "description": "连续生产、灌流培养和连续发酵", "agent_type": AgentType.SCALE_UP, "priority": 2, "capabilities": [] },
            { "name": "过程分析技术智能体", "description": "过程分析技术、PAT和实时监控", "agent_type": AgentType.SCALE_UP, "priority": 2, "capabilities": [] },
            { "name": "成本分析优化智能体", "description": "成本分析、成本优化和经济性评估", "agent_type": AgentType.SCALE_UP, "priority": 3, "capabilities": [] },
            { "name": "文献调研智能体", "description": "文献检索、文献综述和文献分析", "agent_type": AgentType.LITERATURE_RESEARCH, "priority": 2, "capabilities": [] },
            { "name": "专利分析智能体", "description": "专利检索、专利分析和专利战略", "agent_type": AgentType.PATENT_RESEARCH, "priority": 2, "capabilities": [] },
            { "name": "实验设计智能体", "description": "实验设计、DOE和实验方案", "agent_type": AgentType.EXPERIMENT_DESIGN, "priority": 1, "capabilities": [] },
            { "name": "生物信息分析智能体", "description": "生物信息学分析、序列分析和组学分析", "agent_type": AgentType.BIOINFORMATICS, "priority": 1, "capabilities": [] },
            { "name": "统计建模智能体", "description": "统计建模、数据分析和机器学习", "agent_type": AgentType.STATISTICAL_MODELING, "priority": 2, "capabilities": [] },
            { "name": "项目规划智能体", "description": "项目规划、进度管理和里程碑", "agent_type": AgentType.PROJECT_MANAGEMENT, "priority": 1, "capabilities": [] },
            { "name": "风险管理智能体", "description": "风险识别、风险评估和风险缓解", "agent_type": AgentType.PROJECT_MANAGEMENT, "priority": 2, "capabilities": [] },
            { "name": "进度追踪智能体", "description": "进度追踪、任务管理和进度报告", "agent_type": AgentType.PROJECT_MANAGEMENT, "priority": 2, "capabilities": [] },
            { "name": "资源管理智能体", "description": "资源管理、预算控制和资源优化", "agent_type": AgentType.PROJECT_MANAGEMENT, "priority": 3, "capabilities": [] },
            { "name": "团队协作智能体", "description": "团队协作、沟通协调和知识共享", "agent_type": AgentType.PROJECT_MANAGEMENT, "priority": 3, "capabilities": [] },
            { "name": "质量标准智能体", "description": "质量标准制定、质量控制和质量保证", "agent_type": AgentType.QUALITY_CONTROL, "priority": 2, "capabilities": [] },
            { "name": "方法验证智能体", "description": "分析方法验证、方法确认和方法转移", "agent_type": AgentType.QUALITY_CONTROL, "priority": 2, "capabilities": [] },
            { "name": "偏差调查智能体", "description": "偏差调查、CAPA和整改措施", "agent_type": AgentType.QUALITY_CONTROL, "priority": 2, "capabilities": [] },
            { "name": "审计准备智能体", "description": "审计准备、审计支持和审计跟踪", "agent_type": AgentType.QUALITY_CONTROL, "priority": 3, "capabilities": [] },
            { "name": "合规性检查智能体", "description": "合规性检查、法规符合性和内部审计", "agent_type": AgentType.QUALITY_CONTROL, "priority": 2, "capabilities": [] },
            { "name": "申报资料准备智能体", "description": "申报资料准备、CTD格式和申报策略", "agent_type": AgentType.REGULATORY_AFFAIRS, "priority": 1, "capabilities": [] },
            { "name": "法规解读智能体", "description": "法规解读、法规跟踪和法规咨询", "agent_type": AgentType.REGULATORY_AFFAIRS, "priority": 2, "capabilities": [] },
            { "name": "沟通协调智能体", "description": "与监管机构沟通、会议准备和反馈响应", "agent_type": AgentType.REGULATORY_AFFAIRS, "priority": 2, "capabilities": [] },
            { "name": "生命周期管理智能体", "description": "产品生命周期管理、变更控制和上市后监测", "agent_type": AgentType.REGULATORY_AFFAIRS, "priority": 3, "capabilities": [] },
            { "name": "GRAS认证智能体", "description": "GRAS认证、安全性评估和资料准备", "agent_type": AgentType.REGULATORY_AFFAIRS, "priority": 1, "capabilities": [] },
            { "name": "红景天苷发酵优化智能体", "description": "红景天苷发酵工艺优化、参数调整和产量提升", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 1, "capabilities": [] },
            { "name": "红景天苷提取纯化智能体", "description": "红景天苷提取工艺优化、纯化方法和回收率提升", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 1, "capabilities": [] },
            { "name": "红景天苷质量分析智能体", "description": "红景天苷质量标准建立、分析方法和质量控制", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] },
            { "name": "红景天苷稳定性研究智能体", "description": "红景天苷稳定性考察、影响因素和储存条件", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] },
            { "name": "红景天苷中试放大智能体", "description": "红景天苷中试放大工艺、参数优化和验证", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 1, "capabilities": [] },
            { "name": "红景天苷申报资料智能体", "description": "红景天苷申报资料准备、CTD格式和注册策略", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] },
            { "name": "红景天苷专利保护智能体", "description": "红景天苷专利布局、专利申请和专利战略", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 3, "capabilities": [] },
            { "name": "红景天苷市场分析智能体", "description": "红景天苷市场调研、竞品分析和市场定位", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 3, "capabilities": [] },
            { "name": "红景天苷合作对接智能体", "description": "红景天苷商务合作、技术合作和资源对接", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 3, "capabilities": [] },
            { "name": "红景天苷产业化规划智能体", "description": "红景天苷产业化规划、产能布局和商业计划", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] },
            { "name": "红景天苷酶工程智能体", "description": "红景天苷关键酶工程、催化效率优化和稳定性提升", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 1, "capabilities": [] },
            { "name": "红景天苷途径优化智能体", "description": "红景天苷代谢途径优化、通量平衡和前体供应", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 1, "capabilities": [] },
            { "name": "红景天苷菌株改造智能体", "description": "红景天苷生产菌株改造、基因编辑和底盘优化", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] },
            { "name": "红景天苷培养基筛选智能体", "description": "红景天苷培养基筛选、成分优化和成本控制", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] },
            { "name": "红景天苷补料策略智能体", "description": "红景天苷补料策略优化、溶氧控制和pH控制", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] },
            { "name": "红景天苷分离工艺智能体", "description": "红景天苷分离工艺优化、树脂筛选和纯度提升", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] },
            { "name": "红景天苷结晶工艺智能体", "description": "红景天苷结晶工艺优化、晶型控制和收率提升", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 3, "capabilities": [] },
            { "name": "红景天苷干燥工艺智能体", "description": "红景天苷干燥工艺优化、水分控制和稳定性", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 3, "capabilities": [] },
            { "name": "红景天苷包装材料智能体", "description": "红景天苷包装材料选择、相容性考察和稳定性", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 3, "capabilities": [] },
            { "name": "红景天苷质量标准智能体", "description": "红景天苷质量标准制定、方法验证和质量控制", "agent_type": AgentType.RHODIOLA_PROJECT, "priority": 2, "capabilities": [] }
        ]
        
        for agent_data in default_agents:
            agent = Agent(
                name=agent_data["name"],
                description=agent_data["description"],
                agent_type=agent_data["agent_type"],
                status=AgentStatus.ACTIVE,
                priority=agent_data["priority"],
                capabilities=agent_data.get("capabilities", []),
                config=agent_data.get("config", {})
            )
            self.db.add(agent)
        
        self.db.commit()

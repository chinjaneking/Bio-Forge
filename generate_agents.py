#!/usr/bin/env python3
"""生成精确包含120个智能体的agent_manager.py"""

# 智能体模板
agent_templates = [
    # 一、基础架构层 (15个)
    ("研发总监助手", "协助研发总监进行日常管理、任务协调和决策支持", "R_D_ASSISTANT", 1),
    ("平台架构师", "Bio-Forge平台架构设计、技术选型和系统集成", "PLATFORM_MANAGEMENT", 2),
    ("API网关管理", "API接口管理、路由配置和负载均衡", "PLATFORM_MANAGEMENT", 3),
    ("容器编排智能体", "Docker容器管理、部署和扩缩容", "PLATFORM_MANAGEMENT", 3),
    ("监控告警智能体", "系统监控、性能指标收集和异常告警", "PLATFORM_MANAGEMENT", 4),
    
    ("数据架构师", "数据架构设计、数据模型和数据治理", "DATA_MANAGEMENT", 2),
    ("数据集成智能体", "多源数据集成、ETL流程和数据同步", "DATA_MANAGEMENT", 3),
    ("数据质量智能体", "数据质量检查、清洗和质量报告", "DATA_MANAGEMENT", 3),
    ("数据备份恢复", "数据备份策略、恢复演练和灾难恢复", "DATA_MANAGEMENT", 3),
    ("知识图谱管理", "知识图谱构建、维护和知识推理", "DATA_MANAGEMENT", 4),
    
    ("身份认证管理", "用户身份认证、权限管理和访问控制", "SECURITY_MONITORING", 2),
    ("漏洞扫描智能体", "系统漏洞扫描、安全评估和修复建议", "SECURITY_MONITORING", 3),
    ("日志审计智能体", "安全日志收集、分析和异常检测", "SECURITY_MONITORING", 3),
    ("加密管理智能体", "数据加密、密钥管理和加密策略", "SECURITY_MONITORING", 3),
    ("合规管理智能体", "法规合规检查、合规报告和合规培训", "SECURITY_MONITORING", 4),
    
    # 二、计算设计层 (25个)
    ("量子化学计算智能体", "量子化学计算、电子结构和反应机制", "MOLECULAR_MODELING", 1),
    ("分子动力学模拟智能体", "分子动力学模拟、构象分析和动力学", "MOLECULAR_MODELING", 1),
    ("分子对接智能体", "分子对接、虚拟筛选和结合模式", "MOLECULAR_MODELING", 1),
    ("自由能计算智能体", "自由能计算、结合亲和力和热力学", "MOLECULAR_MODELING", 2),
    ("量子力学/分子力学智能体", "QM/MM计算、酶催化和反应路径", "MOLECULAR_MODELING", 2),
    ("多尺度模拟智能体", "多尺度模拟、粗粒化和尺度桥接", "MOLECULAR_MODELING", 2),
    ("光谱模拟智能体", "光谱模拟、NMR和IR光谱预测", "MOLECULAR_MODELING", 3),
    
    ("蛋白质结构预测智能体", "蛋白质结构预测、结构建模和结构分析", "PROTEIN_ENGINEERING", 1),
    ("蛋白质设计智能体", "蛋白质设计、序列设计和功能设计", "PROTEIN_ENGINEERING", 1),
    ("蛋白质功能预测智能体", "蛋白质功能预测、功能注释和功能分析", "PROTEIN_ENGINEERING", 1),
    ("酶工程智能体", "酶工程、催化优化和底物特异性", "PROTEIN_ENGINEERING", 1),
    ("抗体工程智能体", "抗体工程、人源化和亲和力成熟", "PROTEIN_ENGINEERING", 2),
    ("蛋白质-蛋白质对接智能体", "蛋白质-蛋白质对接、复合物建模和相互作用", "PROTEIN_ENGINEERING", 2),
    ("变构位点预测智能体", "变构位点预测、变构调节和变构药物", "PROTEIN_ENGINEERING", 3),
    
    ("代谢途径设计智能体", "代谢途径设计、途径重建和途径优化", "PATHWAY_DESIGN", 1),
    ("代谢流分析智能体", "代谢流分析、FBA和通量预测", "PATHWAY_DESIGN", 1),
    ("基因回路设计智能体", "基因回路设计、逻辑电路和调控网络", "PATHWAY_DESIGN", 2),
    ("途径鲁棒性分析智能体", "途径鲁棒性分析、敏感性分析和稳定性", "PATHWAY_DESIGN", 2),
    ("辅因子平衡智能体", "辅因子平衡、氧化还原平衡和能量平衡", "PATHWAY_DESIGN", 2),
    ("途径优化算法智能体", "途径优化算法、多目标优化和全局优化", "PATHWAY_DESIGN", 3),
    
    ("基因组分析智能体", "基因组分析、基因组注释和比较基因组", "GENOME_DESIGN", 1),
    ("DNA序列生成智能体", "DNA序列生成、密码子优化和序列设计", "GENOME_DESIGN", 1),
    ("基因敲除预测智能体", "基因敲除预测、必需基因分析和表型预测", "GENOME_DESIGN", 1),
    ("启动子设计智能体", "启动子设计、调控元件和表达调控", "GENOME_DESIGN", 2),
    ("终止子设计智能体", "终止子设计、转录终止和mRNA稳定性", "GENOME_DESIGN", 2),
    
    # 三、实验实验室层 (20个)
    ("PCR引物设计智能体", "PCR引物设计、qPCR引物和突变引物", "MOLECULAR_BIOLOGY", 1),
    ("克隆策略设计智能体", "克隆策略设计、组装策略和质粒构建", "MOLECULAR_BIOLOGY", 1),
    ("测序数据分析智能体", "测序数据分析、序列比对和变异检测", "MOLECULAR_BIOLOGY", 1),
    ("qPCR分析智能体", "qPCR数据分析、相对定量和表达分析", "MOLECULAR_BIOLOGY", 2),
    ("CRISPR设计智能体", "CRISPR设计、sgRNA设计和脱靶预测", "MOLECULAR_BIOLOGY", 1),
    ("RNAi设计智能体", "RNAi设计、siRNA设计和shRNA设计", "MOLECULAR_BIOLOGY", 3),
    
    ("菌株选择智能体", "菌株选择、宿主选择和底盘优化", "MICROBIOLOGY", 1),
    ("培养基优化智能体", "培养基优化、成分优化和营养平衡", "MICROBIOLOGY", 1),
    ("发酵工艺优化智能体", "发酵工艺优化、参数优化和控制策略", "FERMENTATION_OPTIMIZATION", 1),
    ("生长曲线分析智能体", "生长曲线分析、比生长速率和生长动力学", "MICROBIOLOGY", 2),
    ("无菌控制智能体", "无菌控制、污染检测和污染防控", "MICROBIOLOGY", 2),
    ("菌种保藏智能体", "菌种保藏、保藏方法和菌种复苏", "MICROBIOLOGY", 3),
    ("微生物鉴定智能体", "微生物鉴定、物种鉴定和分型", "MICROBIOLOGY", 3),
    
    ("HPLC分析智能体", "HPLC分析、方法开发和数据分析", "ANALYTICAL_CHEMISTRY", 1),
    ("GC分析智能体", "GC分析、方法开发和质谱联用", "ANALYTICAL_CHEMISTRY", 1),
    ("质谱分析智能体", "质谱分析、化合物鉴定和定量分析", "ANALYTICAL_CHEMISTRY", 1),
    ("光谱分析智能体", "光谱分析、UV-Vis、荧光和红外", "ANALYTICAL_CHEMISTRY", 2),
    ("蛋白定量智能体", "蛋白定量、BCA、Bradford和WB", "ANALYTICAL_CHEMISTRY", 2),
    ("代谢组学分析智能体", "代谢组学分析、代谢物鉴定和通路分析", "ANALYTICAL_CHEMISTRY", 2),
    ("数据分析可视化智能体", "数据分析、统计分析和可视化", "ANALYTICAL_CHEMISTRY", 3),
    
    # 四、优化验证层 (20个)
    ("产量优化智能体", "产量优化、滴度提升和生产效率", "YIELD_OPTIMIZATION", 1),
    ("底物利用优化智能体", "底物利用优化、碳源优化和副产物减少", "YIELD_OPTIMIZATION", 1),
    ("代谢瓶颈识别智能体", "代谢瓶颈识别、限速步骤和通量分析", "YIELD_OPTIMIZATION", 1),
    ("反馈抑制解除智能体", "反馈抑制解除、变构调节和代谢调控", "YIELD_OPTIMIZATION", 2),
    ("前体供应优化智能体", "前体供应优化、前体合成和供给策略", "YIELD_OPTIMIZATION", 2),
    ("能量代谢优化智能体", "能量代谢优化、ATP再生和能量效率", "YIELD_OPTIMIZATION", 2),
    ("多目标优化智能体", "多目标优化、帕累托优化和权衡分析", "YIELD_OPTIMIZATION", 3),
    
    ("蛋白质稳定性增强智能体", "蛋白质稳定性增强、突变设计和稳定性预测", "STABILITY_ENHANCEMENT", 2),
    ("遗传稳定性智能体", "遗传稳定性优化、重组避免和基因组稳定", "STABILITY_ENHANCEMENT", 2),
    ("生产稳定性智能体", "生产稳定性优化、传代稳定和规模稳定", "STABILITY_ENHANCEMENT", 2),
    ("储存稳定性智能体", "储存稳定性优化、配方优化和储存条件", "STABILITY_ENHANCEMENT", 3),
    ("降解机制分析智能体", "降解机制分析、降解途径和降解预测", "STABILITY_ENHANCEMENT", 3),
    ("稳定剂筛选智能体", "稳定剂筛选、添加剂优化和配方开发", "STABILITY_ENHANCEMENT", 3),
    ("压力耐受性智能体", "压力耐受性增强、胁迫抵抗和鲁棒性优化", "STABILITY_ENHANCEMENT", 2),
    
    ("中试放大智能体", "中试放大、工艺放大和规模转移", "SCALE_UP", 1),
    ("工艺验证智能体", "工艺验证、验证方案和确认报告", "SCALE_UP", 1),
    ("清洁验证智能体", "清洁验证、清洁方法和残留检测", "SCALE_UP", 2),
    ("连续生产智能体", "连续生产、灌流培养和连续发酵", "SCALE_UP", 2),
    ("过程分析技术智能体", "过程分析技术、PAT和实时监控", "SCALE_UP", 2),
    ("成本分析优化智能体", "成本分析、成本优化和经济性评估", "SCALE_UP", 3),
    
    # 五、研发助理层 (20个)
    ("文献调研智能体", "文献检索、文献综述和文献分析", "LITERATURE_RESEARCH", 2),
    ("专利分析智能体", "专利检索、专利分析和专利战略", "PATENT_RESEARCH", 2),
    ("实验设计智能体", "实验设计、DOE和实验方案", "EXPERIMENT_DESIGN", 1),
    ("生物信息分析智能体", "生物信息学分析、序列分析和组学分析", "BIOINFORMATICS", 1),
    ("统计建模智能体", "统计建模、数据分析和机器学习", "STATISTICAL_MODELING", 2),
    
    ("项目规划智能体", "项目规划、进度管理和里程碑", "PROJECT_MANAGEMENT", 1),
    ("风险管理智能体", "风险识别、风险评估和风险缓解", "PROJECT_MANAGEMENT", 2),
    ("进度追踪智能体", "进度追踪、任务管理和进度报告", "PROJECT_MANAGEMENT", 2),
    ("资源管理智能体", "资源管理、预算控制和资源优化", "PROJECT_MANAGEMENT", 3),
    ("团队协作智能体", "团队协作、沟通协调和知识共享", "PROJECT_MANAGEMENT", 3),
    
    ("质量标准智能体", "质量标准制定、质量控制和质量保证", "QUALITY_CONTROL", 2),
    ("方法验证智能体", "分析方法验证、方法确认和方法转移", "QUALITY_CONTROL", 2),
    ("偏差调查智能体", "偏差调查、CAPA和整改措施", "QUALITY_CONTROL", 2),
    ("审计准备智能体", "审计准备、审计支持和审计跟踪", "QUALITY_CONTROL", 3),
    ("合规性检查智能体", "合规性检查、法规符合性和内部审计", "QUALITY_CONTROL", 2),
    
    ("申报资料准备智能体", "申报资料准备、CTD格式和申报策略", "REGULATORY_AFFAIRS", 1),
    ("法规解读智能体", "法规解读、法规跟踪和法规咨询", "REGULATORY_AFFAIRS", 2),
    ("沟通协调智能体", "与监管机构沟通、会议准备和反馈响应", "REGULATORY_AFFAIRS", 2),
    ("生命周期管理智能体", "产品生命周期管理、变更控制和上市后监测", "REGULATORY_AFFAIRS", 3),
    ("GRAS认证智能体", "GRAS认证、安全性评估和资料准备", "REGULATORY_AFFAIRS", 1),
    
    # 六、红景天苷专项 (20个)
    ("红景天苷发酵优化智能体", "红景天苷发酵工艺优化、参数调整和产量提升", "RHODIOLA_PROJECT", 1),
    ("红景天苷提取纯化智能体", "红景天苷提取工艺优化、纯化方法和回收率提升", "RHODIOLA_PROJECT", 1),
    ("红景天苷质量分析智能体", "红景天苷质量标准建立、分析方法和质量控制", "RHODIOLA_PROJECT", 2),
    ("红景天苷稳定性研究智能体", "红景天苷稳定性考察、影响因素和储存条件", "RHODIOLA_PROJECT", 2),
    ("红景天苷中试放大智能体", "红景天苷中试放大工艺、参数优化和验证", "RHODIOLA_PROJECT", 1),
    ("红景天苷申报资料智能体", "红景天苷申报资料准备、CTD格式和注册策略", "RHODIOLA_PROJECT", 2),
    ("红景天苷专利保护智能体", "红景天苷专利布局、专利申请和专利战略", "RHODIOLA_PROJECT", 3),
    ("红景天苷市场分析智能体", "红景天苷市场调研、竞品分析和市场定位", "RHODIOLA_PROJECT", 3),
    ("红景天苷合作对接智能体", "红景天苷商务合作、技术合作和资源对接", "RHODIOLA_PROJECT", 3),
    ("红景天苷产业化规划智能体", "红景天苷产业化规划、产能布局和商业计划", "RHODIOLA_PROJECT", 2),
    
    ("红景天苷酶工程智能体", "红景天苷关键酶工程、催化效率优化和稳定性提升", "RHODIOLA_PROJECT", 1),
    ("红景天苷途径优化智能体", "红景天苷代谢途径优化、通量平衡和前体供应", "RHODIOLA_PROJECT", 1),
    ("红景天苷菌株改造智能体", "红景天苷生产菌株改造、基因编辑和底盘优化", "RHODIOLA_PROJECT", 2),
    ("红景天苷培养基筛选智能体", "红景天苷培养基筛选、成分优化和成本控制", "RHODIOLA_PROJECT", 2),
    ("红景天苷补料策略智能体", "红景天苷补料策略优化、溶氧控制和pH控制", "RHODIOLA_PROJECT", 2),
    ("红景天苷分离工艺智能体", "红景天苷分离工艺优化、树脂筛选和纯度提升", "RHODIOLA_PROJECT", 2),
    ("红景天苷结晶工艺智能体", "红景天苷结晶工艺优化、晶型控制和收率提升", "RHODIOLA_PROJECT", 3),
    ("红景天苷干燥工艺智能体", "红景天苷干燥工艺优化、水分控制和稳定性", "RHODIOLA_PROJECT", 3),
    ("红景天苷包装材料智能体", "红景天苷包装材料选择、相容性考察和稳定性", "RHODIOLA_PROJECT", 3),
    ("红景天苷质量标准智能体", "红景天苷质量标准制定、方法验证和质量控制", "RHODIOLA_PROJECT", 2),
]

# 验证数量
print(f"智能体总数: {len(agent_templates)}")

# 生成agent_manager.py
header = '''"""
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
'''

footer = '''
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
'''

# 生成智能体列表
agent_list = []
for name, desc, type_name, priority in agent_templates:
    agent_str = f'            {{ "name": "{name}", "description": "{desc}", "agent_type": AgentType.{type_name}, "priority": {priority}, "capabilities": [] }}'
    agent_list.append(agent_str)

agent_list_str = ",\n".join(agent_list)

# 写入文件
with open("app/agent_manager.py", "w", encoding="utf-8") as f:
    f.write(header)
    f.write(agent_list_str)
    f.write(footer)

print(f"✅ 已生成包含 {len(agent_templates)} 个智能体的 app/agent_manager.py")

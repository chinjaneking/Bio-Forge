"""智能体管理器"""
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from app.models.agent import Agent, AgentStatus, AgentType
from app.redis_client import redis_client
from datetime import datetime


class AgentManager:
    """智能体管理核心类"""
    
    def __init__(self, db: Session):
        self.db = db
        self._agents_cache: Dict[int, Agent] = {}
    
    def create_agent(
        self,
        name: str,
        description: str,
        agent_type: AgentType,
        config: Optional[Dict] = None,
        capabilities: Optional[List] = None,
        priority: int = 5,
        implementation: str = "",
        **kwargs
    ) -> Agent:
        """创建智能体"""
        agent = Agent(
            name=name,
            description=description,
            agent_type=agent_type,
            config=config or {},
            capabilities=capabilities or [],
            priority=priority,
            implementation=implementation,
            **kwargs
        )
        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)
        
        # 缓存
        self._agents_cache[agent.id] = agent
        return agent
    
    def get_agent(self, agent_id: int) -> Optional[Agent]:
        """获取智能体"""
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
        
        # 更新缓存
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
        """初始化120个智能体矩阵"""
        # 检查是否已存在
        if self.db.query(Agent).count() > 0:
            return
        
        default_agents = [
            # =====================================================================
            # 一、基础架构层 (15个)
            # =====================================================================
            
            # ---- 平台管理组 (5个) ----
            {
                "name": "研发总监助手",
                "description": "协助研发总监进行日常管理、任务协调和决策支持",
                "agent_type": AgentType.R_D_ASSISTANT,
                "priority": 1,
                "capabilities": ["任务协调", "日程管理", "决策支持", "团队沟通"]
            },
            {
                "name": "平台架构师",
                "description": "DeerFlow平台架构设计、技术选型和系统集成",
                "agent_type": AgentType.PLATFORM_MANAGEMENT,
                "priority": 2,
                "capabilities": ["架构设计", "技术选型", "系统集成", "性能优化"]
            },
            {
                "name": "API网关管理",
                "description": "API接口管理、路由配置和负载均衡",
                "agent_type": AgentType.PLATFORM_MANAGEMENT,
                "priority": 3,
                "capabilities": ["API管理", "路由配置", "负载均衡", "API文档"]
            },
            {
                "name": "容器编排智能体",
                "description": "Docker/Kubernetes容器管理、部署和扩缩容",
                "agent_type": AgentType.PLATFORM_MANAGEMENT,
                "priority": 3,
                "capabilities": ["容器管理", "部署编排", "扩缩容", "服务发现"]
            },
            {
                "name": "监控告警智能体",
                "description": "系统监控、性能指标收集和异常告警",
                "agent_type": AgentType.PLATFORM_MANAGEMENT,
                "priority": 4,
                "capabilities": ["系统监控", "指标收集", "异常告警", "性能分析"]
            },
            
            # ---- 数据管理组 (5个) ----
            {
                "name": "数据架构师",
                "description": "数据架构设计、数据模型和数据治理",
                "agent_type": AgentType.DATA_MANAGEMENT,
                "priority": 2,
                "capabilities": ["数据架构", "数据建模", "数据治理", "数据标准"]
            },
            {
                "name": "数据集成智能体",
                "description": "多源数据集成、ETL流程和数据同步",
                "agent_type": AgentType.DATA_MANAGEMENT,
                "priority": 3,
                "capabilities": ["数据集成", "ETL流程", "数据同步", "格式转换"]
            },
            {
                "name": "数据质量智能体",
                "description": "数据质量检查、清洗和质量报告",
                "agent_type": AgentType.DATA_MANAGEMENT,
                "priority": 3,
                "capabilities": ["质量检查", "数据清洗", "质量报告", "异常修复"]
            },
            {
                "name": "数据备份恢复",
                "description": "数据备份策略、恢复演练和灾难恢复",
                "agent_type": AgentType.DATA_MANAGEMENT,
                "priority": 3,
                "capabilities": ["备份策略", "恢复演练", "灾难恢复", "备份监控"]
            },
            {
                "name": "知识图谱管理",
                "description": "知识图谱构建、维护和知识推理",
                "agent_type": AgentType.DATA_MANAGEMENT,
                "priority": 4,
                "capabilities": ["图谱构建", "知识抽取", "知识推理", "图谱更新"]
            },
            
            # ---- 安全监控组 (5个) ----
            {
                "name": "身份认证管理",
                "description": "用户身份认证、权限管理和访问控制",
                "agent_type": AgentType.SECURITY_MONITORING,
                "priority": 2,
                "capabilities": ["身份认证", "权限管理", "访问控制", "SSO集成"]
            },
            {
                "name": "漏洞扫描智能体",
                "description": "系统漏洞扫描、安全评估和修复建议",
                "agent_type": AgentType.SECURITY_MONITORING,
                "priority": 3,
                "capabilities": ["漏洞扫描", "安全评估", "修复建议", "合规检查"]
            },
            {
                "name": "日志审计智能体",
                "description": "安全日志收集、分析和异常检测",
                "agent_type": AgentType.SECURITY_MONITORING,
                "priority": 3,
                "capabilities": ["日志收集", "日志分析", "异常检测", "审计报告"]
            },
            {
                "name": "加密管理智能体",
                "description": "数据加密、密钥管理和加密策略",
                "agent_type": AgentType.SECURITY_MONITORING,
                "priority": 3,
                "capabilities": ["数据加密", "密钥管理", "加密策略", "解密服务"]
            },
            {
                "name": "合规管理智能体",
                "description": "法规合规检查、合规报告和合规培训",
                "agent_type": AgentType.SECURITY_MONITORING,
                "priority": 4,
                "capabilities": ["合规检查", "合规报告", "合规培训", "法规跟踪"]
            },
            
            # =====================================================================
            # 二、生命设计层 (60个) - 核心创新层
            # =====================================================================
            
            # ---- 基因组设计组 (12个) ----
            {
                "name": "DNA序列生成智能体",
                "description": "基于Evo2模型的DNA序列生成、GC含量优化和重复序列避免",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 1,
                "capabilities": ["序列生成", "GC优化", "重复序列", "密码子偏好"]
            },
            {
                "name": "启动子优化智能体",
                "description": "启动子序列设计、强度预测和表达调控",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 2,
                "capabilities": ["启动子设计", "强度预测", "表达调控", "正交性"]
            },
            {
                "name": "密码子优化智能体",
                "description": "密码子偏好优化、翻译效率提升和表达水平优化",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 2,
                "capabilities": ["密码子优化", "翻译效率", "表达优化", "tRNA适应"]
            },
            {
                "name": "基因回路设计智能体",
                "description": "合成基因回路设计、逻辑门构建和动态调控",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 2,
                "capabilities": ["回路设计", "逻辑门", "动态调控", "反馈回路"]
            },
            {
                "name": "代谢通路设计智能体",
                "description": "代谢通路设计、酶选择和途径优化",
                "agent_type": AgentType.PATHWAY_DESIGN,
                "priority": 1,
                "capabilities": ["通路设计", "酶选择", "途径优化", "通量分析"]
            },
            {
                "name": "调控网络设计智能体",
                "description": "基因调控网络设计、信号通路整合和协同调控",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 2,
                "capabilities": ["调控网络", "信号通路", "协同调控", "网络优化"]
            },
            {
                "name": "正交性设计智能体",
                "description": "正交系统设计、交叉互作避免和模块化设计",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 3,
                "capabilities": ["正交设计", "交叉互作", "模块化", "绝缘设计"]
            },
            {
                "name": "基因组稳定性智能体",
                "description": "基因组稳定性设计、重复序列去除和重组避免",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 2,
                "capabilities": ["稳定性设计", "重复序列", "重组避免", "错配修复"]
            },
            {
                "name": "进化适应性智能体",
                "description": "进化潜力设计、适应度 landscape 优化和可进化性",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 3,
                "capabilities": ["进化设计", "适应度优化", "可进化性", "变异控制"]
            },
            {
                "name": "功能模块化智能体",
                "description": "功能模块设计、标准接口和模块组装",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 3,
                "capabilities": ["模块设计", "标准接口", "模块组装", "接口标准化"]
            },
            {
                "name": "合成可行性智能体",
                "description": "合成难度评估、拼接策略设计和成本优化",
                "agent_type": AgentType.DNA_SYNTHESIS,
                "priority": 3,
                "capabilities": ["难度评估", "拼接策略", "成本优化", "合成计划"]
            },
            {
                "name": "生物安全设计智能体",
                "description": "生物安全设计、自杀开关和生物遏制系统",
                "agent_type": AgentType.GENOME_DESIGN,
                "priority": 2,
                "capabilities": ["安全设计", "自杀开关", "生物遏制", "安全评估"]
            },
            
            # ---- 蛋白质工程组 (10个) ----
            {
                "name": "蛋白质结构预测智能体",
                "description": "基于AlphaFold 3的蛋白质结构预测和结构分析",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 1,
                "capabilities": ["结构预测", "结构分析", "构象分析", "模型质量评估"]
            },
            {
                "name": "蛋白质功能设计智能体",
                "description": "蛋白质功能设计、活性位点设计和底物特异性",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 1,
                "capabilities": ["功能设计", "活性位点", "底物特异性", "催化机制"]
            },
            {
                "name": "蛋白质稳定性优化智能体",
                "description": "蛋白质稳定性优化、折叠优化和热稳定性",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 2,
                "capabilities": ["稳定性优化", "折叠优化", "热稳定性", "抗降解"]
            },
            {
                "name": "蛋白质亲和力设计智能体",
                "description": "蛋白质-蛋白质互作设计、结合亲和力优化",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 2,
                "capabilities": ["互作设计", "亲和力优化", "结合界面", "特异性设计"]
            },
            {
                "name": "酶活性设计智能体",
                "description": "酶活性设计、催化效率优化和底物选择性",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 2,
                "capabilities": ["酶活设计", "催化优化", "底物选择", "反应机制"]
            },
            {
                "name": "多聚体设计智能体",
                "description": "蛋白质多聚体设计、亚基组装和复合物结构",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 3,
                "capabilities": ["多聚体设计", "亚基组装", "复合物", "对称性设计"]
            },
            {
                "name": "膜蛋白设计智能体",
                "description": "膜蛋白设计、跨膜区优化和膜定位",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 3,
                "capabilities": ["膜蛋白设计", "跨膜区", "膜定位", "转运蛋白"]
            },
            {
                "name": "药物靶点设计智能体",
                "description": "药物靶点设计、成药性优化和靶点验证",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 2,
                "capabilities": ["靶点设计", "成药性", "靶点验证", "药物结合"]
            },
            {
                "name": "抗体设计智能体",
                "description": "抗体设计、CDR优化和亲和力成熟",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 2,
                "capabilities": ["抗体设计", "CDR优化", "亲和力成熟", "人源化"]
            },
            {
                "name": "信号肽设计智能体",
                "description": "信号肽设计、分泌效率优化和亚细胞定位",
                "agent_type": AgentType.PROTEIN_DESIGN,
                "priority": 3,
                "capabilities": ["信号肽", "分泌优化", "亚细胞定位", "转运信号"]
            },
            
            # ---- 细胞设计组 (15个) ----
            {
                "name": "细胞器设计智能体",
                "description": "细胞器工程、人工细胞器设计和功能重建",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 2,
                "capabilities": ["细胞器设计", "人工细胞器", "功能重建", "区室化"]
            },
            {
                "name": "代谢网络设计智能体",
                "description": "代谢网络重构、通量平衡分析和代谢流优化",
                "agent_type": AgentType.METABOLIC_ENGINEERING,
                "priority": 1,
                "capabilities": ["网络重构", "通量分析", "代谢流优化", "FBA"]
            },
            {
                "name": "信号通路设计智能体",
                "description": "信号通路工程、信号转导优化和信号整合",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 2,
                "capabilities": ["通路设计", "信号转导", "信号整合", "通路优化"]
            },
            {
                "name": "细胞周期设计智能体",
                "description": "细胞周期调控、分裂控制和增殖优化",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["周期调控", "分裂控制", "增殖优化", "checkpoints"]
            },
            {
                "name": "分化程序设计智能体",
                "description": "细胞分化程序设计、转分化和重编程",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["分化设计", "转分化", "重编程", "谱系特异性"]
            },
            {
                "name": "免疫逃避设计智能体",
                "description": "免疫逃避机制设计、免疫抑制和免疫耐受",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["免疫逃避", "免疫抑制", "免疫耐受", "免疫编辑"]
            },
            {
                "name": "环境响应设计智能体",
                "description": "环境响应系统设计、传感器和响应开关",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["环境响应", "传感器设计", "响应开关", "条件激活"]
            },
            {
                "name": "能量代谢设计智能体",
                "description": "能量代谢优化、ATP生产和能量平衡",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 2,
                "capabilities": ["能量代谢", "ATP生产", "能量平衡", "呼吸链优化"]
            },
            {
                "name": "物质运输设计智能体",
                "description": "物质运输系统设计、转运蛋白优化和跨膜运输",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["运输系统", "转运蛋白", "跨膜运输", "分泌优化"]
            },
            {
                "name": "细胞通讯设计智能体",
                "description": "细胞间通讯设计、信号分子和群体感应",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["细胞通讯", "信号分子", "群体感应", "信号传递"]
            },
            {
                "name": "应激响应智能体",
                "description": "应激响应系统、压力抵抗和损伤修复",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["应激响应", "压力抵抗", "损伤修复", "压力适应"]
            },
            {
                "name": "修复机制智能体",
                "description": "DNA修复系统、损伤修复和基因组稳定",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["DNA修复", "损伤修复", "基因组稳定", "错配修复"]
            },
            {
                "name": "衰老控制智能体",
                "description": "衰老调控、端粒维持和寿命优化",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 4,
                "capabilities": ["衰老调控", "端粒维持", "寿命优化", "氧化应激"]
            },
            {
                "name": "增殖调控智能体",
                "description": "细胞增殖调控、生长控制和密度调控",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["增殖调控", "生长控制", "密度调控", "接触抑制"]
            },
            {
                "name": "凋亡控制智能体",
                "description": "细胞凋亡调控、死亡开关和存活机制",
                "agent_type": AgentType.CELL_DESIGN,
                "priority": 3,
                "capabilities": ["凋亡调控", "死亡开关", "存活机制", "抗凋亡"]
            },
            
            # ---- 组织器官组 (12个) ----
            {
                "name": "组织结构设计智能体",
                "description": "组织结构设计、细胞排列和空间组织",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 2,
                "capabilities": ["结构设计", "细胞排列", "空间组织", "形态发生"]
            },
            {
                "name": "血管网络设计智能体",
                "description": "血管网络设计、血管生成和灌注系统",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 2,
                "capabilities": ["血管网络", "血管生成", "灌注系统", "微循环"]
            },
            {
                "name": "神经连接设计智能体",
                "description": "神经网络设计、突触连接和神经环路",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 3,
                "capabilities": ["神经网络", "突触连接", "神经环路", "电活动"]
            },
            {
                "name": "免疫系统设计智能体",
                "description": "免疫系统设计、免疫细胞组成和免疫功能",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 3,
                "capabilities": ["免疫系统", "免疫细胞", "免疫功能", "免疫应答"]
            },
            {
                "name": "内分泌系统设计智能体",
                "description": "内分泌系统设计、激素分泌和信号调节",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 3,
                "capabilities": ["内分泌", "激素分泌", "信号调节", "反馈调节"]
            },
            {
                "name": "再生能力设计智能体",
                "description": "再生能力设计、干细胞巢和再生程序",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 3,
                "capabilities": ["再生能力", "干细胞巢", "再生程序", "去分化"]
            },
            {
                "name": "功能整合智能体",
                "description": "组织功能整合、多细胞协调和系统功能",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 2,
                "capabilities": ["功能整合", "多细胞协调", "系统功能", "协同作用"]
            },
            {
                "name": "仿生优化智能体",
                "description": "仿生设计优化、生物启发和自然模拟",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 3,
                "capabilities": ["仿生优化", "生物启发", "自然模拟", "进化优化"]
            },
            {
                "name": "机械性能智能体",
                "description": "机械性能设计、力学特性和结构力学",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 3,
                "capabilities": ["机械性能", "力学特性", "结构力学", "材料特性"]
            },
            {
                "name": "物质交换智能体",
                "description": "物质交换系统、营养供应和废物排出",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 3,
                "capabilities": ["物质交换", "营养供应", "废物排出", "扩散运输"]
            },
            {
                "name": "能量供应智能体",
                "description": "能量供应系统、能量代谢和能量分配",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 3,
                "capabilities": ["能量供应", "能量代谢", "能量分配", "氧供应"]
            },
            {
                "name": "信息处理智能体",
                "description": "信息处理系统、信号处理和决策系统",
                "agent_type": AgentType.TISSUE_DESIGN,
                "priority": 4,
                "capabilities": ["信息处理", "信号处理", "决策系统", "学习记忆"]
            },
            
            # ---- 系统整合组 (11个) ----
            {
                "name": "多尺度建模智能体",
                "description": "多尺度建模、从分子到系统的整合模型",
                "agent_type": AgentType.DESIGN,
                "priority": 1,
                "capabilities": ["多尺度建模", "模型整合", "尺度桥接", "多物理场"]
            },
            {
                "name": "系统验证智能体",
                "description": "系统级验证、功能验证和性能测试",
                "agent_type": AgentType.DESIGN,
                "priority": 2,
                "capabilities": ["系统验证", "功能验证", "性能测试", "集成测试"]
            },
            {
                "name": "功能测试智能体",
                "description": "功能测试设计、测试用例和测试报告",
                "agent_type": AgentType.DESIGN,
                "priority": 2,
                "capabilities": ["功能测试", "测试用例", "测试报告", "回归测试"]
            },
            {
                "name": "稳定性评估智能体",
                "description": "系统稳定性评估、鲁棒性分析和容错设计",
                "agent_type": AgentType.DESIGN,
                "priority": 2,
                "capabilities": ["稳定性评估", "鲁棒性分析", "容错设计", "压力测试"]
            },
            {
                "name": "进化预测智能体",
                "description": "进化轨迹预测、适应度预测和进化潜力评估",
                "agent_type": AgentType.DESIGN,
                "priority": 3,
                "capabilities": ["进化预测", "适应度预测", "进化潜力", "轨迹模拟"]
            },
            {
                "name": "环境适应性智能体",
                "description": "环境适应性设计、环境压力测试和适应度优化",
                "agent_type": AgentType.DESIGN,
                "priority": 3,
                "capabilities": ["环境适应", "压力测试", "适应度优化", "生态位设计"]
            },
            {
                "name": "生物安全智能体",
                "description": "生物安全评估、风险分析和安全措施验证",
                "agent_type": AgentType.DESIGN,
                "priority": 2,
                "capabilities": ["生物安全", "风险分析", "安全验证", "遏制评估"]
            },
            {
                "name": "伦理审查智能体",
                "description": "伦理审查、伦理评估和合规检查",
                "agent_type": AgentType.DESIGN,
                "priority": 2,
                "capabilities": ["伦理审查", "伦理评估", "合规检查", "伦理咨询"]
            },
            {
                "name": "社会影响智能体",
                "description": "社会影响评估、公众接受度和社会风险分析",
                "agent_type": AgentType.DESIGN,
                "priority": 3,
                "capabilities": ["社会影响", "公众接受", "社会风险", "传播分析"]
            },
            {
                "name": "法规合规智能体",
                "description": "法规研究、合规策略和申报准备",
                "agent_type": AgentType.REGULATORY_AFFAIRS,
                "priority": 2,
                "capabilities": ["法规研究", "合规策略", "申报准备", "监管沟通"]
            },
            {
                "name": "风险评估智能体",
                "description": "全面风险评估、风险矩阵和风险管理策略",
                "agent_type": AgentType.DESIGN,
                "priority": 2,
                "capabilities": ["风险评估", "风险矩阵", "风险管理", "缓解措施"]
            },
            
            # =====================================================================
            # 三、实验执行层 (25个)
            # =====================================================================
            
            # ---- DNA合成控制组 (6个) ----
            {
                "name": "DNA合成计划智能体",
                "description": "DNA合成计划制定、合成策略和资源规划",
                "agent_type": AgentType.DNA_SYNTHESIS,
                "priority": 2,
                "capabilities": ["合成计划", "合成策略", "资源规划", "成本估算"]
            },
            {
                "name": "寡核苷酸合成智能体",
                "description": "寡核苷酸合成、纯化和质量控制",
                "agent_type": AgentType.DNA_SYNTHESIS,
                "priority": 3,
                "capabilities": ["寡核苷酸合成", "纯化", "质量控制", "QC检测"]
            },
            {
                "name": "DNA拼接组装智能体",
                "description": "DNA拼接组装、Gibson组装和Golden Gate组装",
                "agent_type": AgentType.DNA_SYNTHESIS,
                "priority": 2,
                "capabilities": ["DNA拼接", "Gibson组装", "Golden Gate", "组装优化"]
            },
            {
                "name": "合成验证智能体",
                "description": "合成产物验证、测序分析和序列确认",
                "agent_type": AgentType.DNA_SYNTHESIS,
                "priority": 2,
                "capabilities": ["合成验证", "测序分析", "序列确认", "变体检测"]
            },
            {
                "name": "合成错误修复智能体",
                "description": "合成错误修复、突变校正和重新合成",
                "agent_type": AgentType.DNA_SYNTHESIS,
                "priority": 3,
                "capabilities": ["错误修复", "突变校正", "重新合成", "修复策略"]
            },
            {
                "name": "合成库管理智能体",
                "description": "合成DNA库管理、库存跟踪和检索",
                "agent_type": AgentType.DNA_SYNTHESIS,
                "priority": 3,
                "capabilities": ["库管理", "库存跟踪", "检索", "存储优化"]
            },
            
            # ---- 细胞组装控制组 (8个) ----
            {
                "name": "转化策略智能体",
                "description": "转化策略设计、转化方法优化和效率提升",
                "agent_type": AgentType.CELL_ASSEMBLY,
                "priority": 2,
                "capabilities": ["转化策略", "方法优化", "效率提升", "宿主选择"]
            },
            {
                "name": "质粒构建智能体",
                "description": "质粒构建、载体设计和克隆策略",
                "agent_type": AgentType.CELL_ASSEMBLY,
                "priority": 2,
                "capabilities": ["质粒构建", "载体设计", "克隆策略", "质粒验证"]
            },
            {
                "name": "基因组编辑智能体",
                "description": "CRISPR/Cas9基因组编辑、精确编辑和脱靶检测",
                "agent_type": AgentType.CELL_ASSEMBLY,
                "priority": 1,
                "capabilities": ["基因组编辑", "CRISPR", "精确编辑", "脱靶检测"]
            },
            {
                "name": "克隆验证智能体",
                "description": "克隆验证、PCR鉴定和序列验证",
                "agent_type": AgentType.CELL_ASSEMBLY,
                "priority": 2,
                "capabilities": ["克隆验证", "PCR鉴定", "序列验证", "基因型分析"]
            },
            {
                "name": "细胞系建立智能体",
                "description": "稳定细胞系建立、单克隆筛选和细胞库构建",
                "agent_type": AgentType.CELL_ASSEMBLY,
                "priority": 2,
                "capabilities": ["细胞系建立", "单克隆筛选", "细胞库", "稳定性测试"]
            },
            {
                "name": "细胞器移植智能体",
                "description": "细胞器移植、线粒体移植和叶绿体工程",
                "agent_type": AgentType.CELL_ASSEMBLY,
                "priority": 3,
                "capabilities": ["细胞器移植", "线粒体", "叶绿体", "胞质杂交"]
            },
            {
                "name": "细胞融合智能体",
                "description": "细胞融合、杂交瘤技术和体细胞杂交",
                "agent_type": AgentType.CELL_ASSEMBLY,
                "priority": 3,
                "capabilities": ["细胞融合", "杂交瘤", "体细胞杂交", "融合优化"]
            },
            {
                "name": "人工细胞构建智能体",
                "description": "人工细胞构建、脂质体组装和原细胞工程",
                "agent_type": AgentType.CELL_ASSEMBLY,
                "priority": 3,
                "capabilities": ["人工细胞", "脂质体", "原细胞", "区室化"]
            },
            
            # ---- 培养优化控制组 (6个) ----
            {
                "name": "培养基优化智能体",
                "description": "培养基设计、成分优化和成本控制",
                "agent_type": AgentType.CULTURE_OPTIMIZATION,
                "priority": 2,
                "capabilities": ["培养基优化", "成分设计", "成本控制", "响应面"]
            },
            {
                "name": "发酵参数优化智能体",
                "description": "发酵参数优化、pH/温度/溶氧控制和补料策略",
                "agent_type": AgentType.CULTURE_OPTIMIZATION,
                "priority": 1,
                "capabilities": ["参数优化", "pH控制", "温度控制", "溶氧控制"]
            },
            {
                "name": "补料策略智能体",
                "description": "补料策略设计、分批补料和连续培养",
                "agent_type": AgentType.CULTURE_OPTIMIZATION,
                "priority": 2,
                "capabilities": ["补料策略", "分批补料", "连续培养", "反馈控制"]
            },
            {
                "name": "污染控制智能体",
                "description": "污染监测、污染预防和污染处理",
                "agent_type": AgentType.CULTURE_OPTIMIZATION,
                "priority": 2,
                "capabilities": ["污染控制", "污染监测", "污染预防", "灭菌策略"]
            },
            {
                "name": "放大生产智能体",
                "description": "工艺放大、规模扩展和生产优化",
                "agent_type": AgentType.CULTURE_OPTIMIZATION,
                "priority": 1,
                "capabilities": ["放大生产", "工艺放大", "规模扩展", "生产优化"]
            },
            {
                "name": "培养监控智能体",
                "description": "实时监控、在线检测和过程分析",
                "agent_type": AgentType.CULTURE_OPTIMIZATION,
                "priority": 2,
                "capabilities": ["培养监控", "在线检测", "过程分析", "数据采集"]
            },
            
            # ---- 功能验证控制组 (5个) ----
            {
                "name": "功能测定智能体",
                "description": "功能测定、活性检测和功能分析",
                "agent_type": AgentType.ASSAY_VALIDATION,
                "priority": 1,
                "capabilities": ["功能测定", "活性检测", "功能分析", "剂量反应"]
            },
            {
                "name": "表型分析智能体",
                "description": "表型分析、形态观察和表型组学",
                "agent_type": AgentType.ASSAY_VALIDATION,
                "priority": 2,
                "capabilities": ["表型分析", "形态观察", "表型组学", "表型分类"]
            },
            {
                "name": "组学分析智能体",
                "description": "多组学分析、基因组/转录组/蛋白质组/代谢组",
                "agent_type": AgentType.ASSAY_VALIDATION,
                "priority": 2,
                "capabilities": ["组学分析", "基因组", "转录组", "蛋白质组", "代谢组"]
            },
            {
                "name": "稳定性测试智能体",
                "description": "稳定性测试、加速试验和货架期预测",
                "agent_type": AgentType.ASSAY_VALIDATION,
                "priority": 2,
                "capabilities": ["稳定性测试", "加速试验", "货架期", "降解分析"]
            },
            {
                "name": "生物活性验证智能体",
                "description": "生物活性验证、体内试验和疗效评估",
                "agent_type": AgentType.ASSAY_VALIDATION,
                "priority": 2,
                "capabilities": ["生物活性", "体内试验", "疗效评估", "动物模型"]
            },
            
            # =====================================================================
            # 四、进化优化层 (20个)
            # =====================================================================
            
            # ---- 适应性进化组 (7个) ----
            {
                "name": "适应性进化策略智能体",
                "description": "适应性进化策略设计、选择压力和进化方案",
                "agent_type": AgentType.ADAPTIVE_EVOLUTION,
                "priority": 2,
                "capabilities": ["进化策略", "选择压力", "进化方案", "实验设计"]
            },
            {
                "name": "连续传代进化智能体",
                "description": "连续传代进化、传代方案和进化跟踪",
                "agent_type": AgentType.ADAPTIVE_EVOLUTION,
                "priority": 2,
                "capabilities": ["连续传代", "传代方案", "进化跟踪", "种群管理"]
            },
            {
                "name": "环境压力设计智能体",
                "description": "环境压力设计、胁迫条件和压力梯度",
                "agent_type": AgentType.ADAPTIVE_EVOLUTION,
                "priority": 2,
                "capabilities": ["压力设计", "胁迫条件", "压力梯度", "多因素压力"]
            },
            {
                "name": "进化轨迹分析智能体",
                "description": "进化轨迹分析、种群遗传学和进化动力学",
                "agent_type": AgentType.ADAPTIVE_EVOLUTION,
                "priority": 2,
                "capabilities": ["轨迹分析", "种群遗传", "进化动力学", "溯祖分析"]
            },
            {
                "name": "突变谱分析智能体",
                "description": "突变谱分析、突变检测和突变热点",
                "agent_type": AgentType.ADAPTIVE_EVOLUTION,
                "priority": 3,
                "capabilities": ["突变谱分析", "突变检测", "突变热点", "突变注释"]
            },
            {
                "name": "表型进化追踪智能体",
                "description": "表型进化追踪、表型变化和适应度测量",
                "agent_type": AgentType.ADAPTIVE_EVOLUTION,
                "priority": 3,
                "capabilities": ["表型追踪", "表型变化", "适应度测量", "竞争实验"]
            },
            {
                "name": "进化终点鉴定智能体",
                "description": "进化终点鉴定、克隆分离和特性鉴定",
                "agent_type": AgentType.ADAPTIVE_EVOLUTION,
                "priority": 2,
                "capabilities": ["终点鉴定", "克隆分离", "特性鉴定", "基因型-表型"]
            },
            
            # ---- 功能优化组 (6个) ----
            {
                "name": "目标功能定义智能体",
                "description": "目标功能定义、功能指标和成功标准",
                "agent_type": AgentType.FUNCTION_OPTIMIZATION,
                "priority": 1,
                "capabilities": ["功能定义", "功能指标", "成功标准", "需求分析"]
            },
            {
                "name": "多目标优化智能体",
                "description": "多目标优化、Pareto优化和权衡分析",
                "agent_type": AgentType.FUNCTION_OPTIMIZATION,
                "priority": 2,
                "capabilities": ["多目标优化", "Pareto优化", "权衡分析", "目标优先级"]
            },
            {
                "name": "机器学习优化智能体",
                "description": "机器学习驱动优化、贝叶斯优化和主动学习",
                "agent_type": AgentType.FUNCTION_OPTIMIZATION,
                "priority": 1,
                "capabilities": ["ML优化", "贝叶斯优化", "主动学习", "surrogate模型"]
            },
            {
                "name": "定向进化优化智能体",
                "description": "定向进化策略、突变文库和筛选优化",
                "agent_type": AgentType.DIRECTED_EVOLUTION,
                "priority": 2,
                "capabilities": ["定向进化", "突变文库", "筛选优化", "富集策略"]
            },
            {
                "name": "组合优化智能体",
                "description": "组合优化、组合文库和遗传算法",
                "agent_type": AgentType.FUNCTION_OPTIMIZATION,
                "priority": 3,
                "capabilities": ["组合优化", "组合文库", "遗传算法", "网格搜索"]
            },
            {
                "name": "性能评估智能体",
                "description": "性能评估、性能指标和基准测试",
                "agent_type": AgentType.FUNCTION_OPTIMIZATION,
                "priority": 2,
                "capabilities": ["性能评估", "性能指标", "基准测试", "比较分析"]
            },
            
            # ---- 稳定性增强组 (7个) ----
            {
                "name": "蛋白质稳定性增强智能体",
                "description": "蛋白质稳定性增强、突变设计和稳定性预测",
                "agent_type": AgentType.STABILITY_ENHANCEMENT,
                "priority": 2,
                "capabilities": ["蛋白稳定", "突变设计", "稳定性预测", "热稳定性"]
            },
            {
                "name": "遗传稳定性智能体",
                "description": "遗传稳定性优化、重组避免和基因组稳定",
                "agent_type": AgentType.STABILITY_ENHANCEMENT,
                "priority": 2,
                "capabilities": ["遗传稳定", "重组避免", "基因组稳定", "拷贝数稳定"]
            },
            {
                "name": "生产稳定性智能体",
                "description": "生产稳定性优化、传代稳定和规模稳定",
                "agent_type": AgentType.STABILITY_ENHANCEMENT,
                "priority": 2,
                "capabilities": ["生产稳定", "传代稳定", "规模稳定", "批次一致性"]
            },
            {
                "name": "储存稳定性智能体",
                "description": "储存稳定性优化、配方优化和储存条件",
                "agent_type": AgentType.STABILITY_ENHANCEMENT,
                "priority": 3,
                "capabilities": ["储存稳定", "配方优化", "储存条件", "保质期"]
            },
            {
                "name": "降解机制分析智能体",
                "description": "降解机制分析、降解途径和降解预测",
                "agent_type": AgentType.STABILITY_ENHANCEMENT,
                "priority": 3,
                "capabilities": ["降解分析", "降解途径", "降解预测", "稳定性指示"]
            },
            {
                "name": "稳定剂筛选智能体",
                "description": "稳定剂筛选、添加剂优化和配方开发",
                "agent_type": AgentType.STABILITY_ENHANCEMENT,
                "priority": 3,
                "capabilities": ["稳定剂筛选", "添加剂优化", "配方开发", "协同作用"]
            },
            {
                "name": "压力耐受性智能体",
                "description": "压力耐受性增强、胁迫抵抗和鲁棒性优化",
                "agent_type": AgentType.STABILITY_ENHANCEMENT,
                "priority": 2,
                "capabilities": ["压力耐受", "胁迫抵抗", "鲁棒性", "抗逆性"]
            }
        ]
        
        for agent_data in default_agents:
            self.create_agent(**agent_data)
        
        print(f"已初始化 {len(default_agents)} 个智能体")
    
    def record_task_execution(self, agent_id: int, success: bool, execution_time: int):
        """记录任务执行"""
        agent = self.get_agent(agent_id)
        if not agent:
            return
        
        agent.total_tasks += 1
        if success:
            agent.successful_tasks += 1
        else:
            agent.failed_tasks += 1
        
        # 平均执行时间
        if agent.total_tasks > 0:
            total_time = agent.avg_execution_time * (agent.total_tasks - 1) + execution_time
            agent.avg_execution_time = total_time // agent.total_tasks
        
        self.db.commit()
        self._agents_cache[agent_id] = agent
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self.db.query(Agent).count()
        active = self.db.query(Agent).filter(Agent.status == AgentStatus.ACTIVE).count()
        inactive = self.db.query(Agent).filter(Agent.status == AgentStatus.INACTIVE).count()
        busy = self.db.query(Agent).filter(Agent.status == AgentStatus.BUSY).count()
        error = self.db.query(Agent).filter(Agent.status == AgentStatus.ERROR).count()
        
        by_type = {}
        for agent_type in AgentType:
            count = self.db.query(Agent).filter(Agent.agent_type == agent_type).count()
            if count > 0:
                by_type[agent_type.value] = count
        
        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "busy": busy,
            "error": error,
            "by_type": by_type
        }


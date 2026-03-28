"""
DeerFlow Configuration Management for Bio-Forge

管理 DeerFlow 2.0 集成配置，包括:
- DeerFlow 项目路径
- 模型配置
- 智能体映射配置
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from functools import lru_cache


@dataclass
class DeerFlowConfig:
    """DeerFlow 集成配置"""
    
    # DeerFlow 项目路径
    deerflow_root: Path = field(default_factory=lambda: Path(os.environ.get("DEERFLOW_ROOT", r"C:\Users\chinjaneking\deer-flow")))
    
    # DeerFlow 配置文件路径
    config_path: Optional[Path] = None
    
    # 默认模型配置
    default_model: str = "claude-sonnet-4-20250514"
    thinking_enabled: bool = True
    subagent_enabled: bool = False
    plan_mode: bool = False
    
    # 智能体映射配置
    agent_type_to_deerflow: Dict[str, str] = field(default_factory=lambda: {
        # L1 核心智能体
        "R_D_DIRECTOR": "lead_agent",
        "R_D_ASSISTANT": "lead_agent",
        "PROJECT_COORDINATOR": "lead_agent",
        
        # L2 数据分析
        "DATA_CURATOR": "data_agent",
        "LITERATURE_MINER": "data_agent",
        "PATENT_ANALYZER": "data_agent",
        
        # L3 计算智能体
        "PROTEIN_STRUCTURE_PREDICTOR": "computation_agent",
        "MOLECULAR_DYNAMICS": "computation_agent",
        "QUANTUM_CHEMISTRY": "computation_agent",
        
        # L4 设计智能体
        "ENZYME_ENGINEER": "design_agent",
        "METABOLIC_PATHWAY": "design_agent",
        "GENE_CIRCUIT": "design_agent",
        
        # L5 实验智能体
        "EXPERIMENT_DESIGNER": "experiment_agent",
        "PROTOCOL_WRITER": "experiment_agent",
        
        # L6 产品智能体
        "REGULATORY_EXPERT": "product_agent",
        "MARKET_ANALYST": "product_agent",
    })
    
    # 工作流配置
    max_workflow_depth: int = 10
    max_concurrent_agents: int = 5
    default_timeout: int = 300  # seconds
    
    # 记忆配置
    memory_enabled: bool = True
    memory_max_entries: int = 1000
    
    def __post_init__(self):
        """后处理配置"""
        if isinstance(self.deerflow_root, str):
            self.deerflow_root = Path(self.deerflow_root)
        if self.config_path and isinstance(self.config_path, str):
            self.config_path = Path(self.config_path)
    
    @property
    def backend_path(self) -> Path:
        """DeerFlow backend 路径"""
        return self.deerflow_root / "backend"
    
    @property
    def client_module_path(self) -> Path:
        """DeerFlowClient 模块路径"""
        return self.backend_path / "packages" / "harness" / "deerflow" / "client.py"
    
    @property
    def config_file_path(self) -> Optional[Path]:
        """配置文件完整路径"""
        if self.config_path:
            return self.config_path
        # 默认配置文件路径
        default_config = self.deerflow_root / "backend" / "config.yaml"
        if default_config.exists():
            return default_config
        return None
    
    def validate(self) -> List[str]:
        """验证配置有效性"""
        errors = []
        
        if not self.deerflow_root.exists():
            errors.append(f"DeerFlow root path does not exist: {self.deerflow_root}")
        
        client_path = self.client_module_path
        if not client_path.exists():
            errors.append(f"DeerFlow client module not found: {client_path}")
        
        return errors
    
    def to_deerflow_client_kwargs(self) -> Dict[str, Any]:
        """转换为 DeerFlowClient 初始化参数"""
        kwargs = {
            "model_name": self.default_model,
            "thinking_enabled": self.thinking_enabled,
            "subagent_enabled": self.subagent_enabled,
            "plan_mode": self.plan_mode,
        }
        if self.config_file_path:
            kwargs["config_path"] = str(self.config_file_path)
        return kwargs


@lru_cache(maxsize=1)
def get_deerflow_config() -> DeerFlowConfig:
    """获取全局 DeerFlow 配置（单例）"""
    return DeerFlowConfig()


def get_deerflow_client():
    """
    获取 DeerFlow Client 实例
    
    Returns:
        DeerFlowClient 实例
        
    Raises:
        ImportError: 如果 deerflow 模块不可用
        FileNotFoundError: 如果 DeerFlow 路径不存在
    """
    import sys
    
    config = get_deerflow_config()
    
    # 添加 DeerFlow 到 Python 路径
    backend_path = str(config.backend_path)
    packages_path = str(config.backend_path / "packages")
    
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    if packages_path not in sys.path:
        sys.path.insert(0, packages_path)
    
    # 延迟导入 DeerFlowClient
    try:
        from deerflow.client import DeerFlowClient
    except ImportError:
        # 尝试另一种导入方式
        try:
            from harness.deerflow.client import DeerFlowClient
        except ImportError as e:
            raise ImportError(
                f"Cannot import DeerFlowClient. "
                f"Ensure DeerFlow is properly installed at {config.deerflow_root}. "
                f"Error: {e}"
            )
    
    return DeerFlowClient(**config.to_deerflow_client_kwargs())
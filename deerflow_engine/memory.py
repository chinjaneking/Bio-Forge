"""
Agent Memory - 智能体记忆与进化系统

管理 Bio-Forge 智能体的学习记忆和进化能力，
支持跨会话的知识积累和能力提升。

核心功能:
1. 记忆存储和检索
2. 经验累积和学习
3. 能力进化追踪
4. 知识图谱构建
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List
from collections import defaultdict

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """记忆类型"""
    EPISODIC = "episodic"      # 情景记忆 - 具体事件
    SEMANTIC = "semantic"       # 语义记忆 - 概念知识
    PROCEDURAL = "procedural"   # 程序记忆 - 技能方法
    WORKING = "working"         # 工作记忆 - 临时上下文


class MemoryImportance(Enum):
    """记忆重要性"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    agent_id: int
    memory_type: MemoryType
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: MemoryImportance = MemoryImportance.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "memory_type": self.memory_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "importance": self.importance.value,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "tags": self.tags,
            "related_memories": self.related_memories,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntry":
        """从字典创建"""
        return cls(
            id=data["id"],
            agent_id=data["agent_id"],
            memory_type=MemoryType(data["memory_type"]),
            content=data["content"],
            metadata=data.get("metadata", {}),
            importance=MemoryImportance(data.get("importance", 2)),
            created_at=datetime.fromisoformat(data["created_at"]),
            last_accessed=datetime.fromisoformat(data["last_accessed"]),
            access_count=data.get("access_count", 0),
            tags=data.get("tags", []),
            related_memories=data.get("related_memories", []),
        )


@dataclass
class EvolutionRecord:
    """进化记录"""
    agent_id: int
    timestamp: datetime
    capability: str
    before_value: Any
    after_value: Any
    reason: str
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
            "capability": self.capability,
            "before_value": self.before_value,
            "after_value": self.after_value,
            "reason": self.reason,
            "confidence": self.confidence,
        }


class AgentMemory:
    """
    智能体记忆系统
    
    管理单个或多个智能体的记忆存储、检索和进化。
    
    使用示例:
        memory = AgentMemory(agent_id=1)
        
        # 存储记忆
        memory.remember("成功设计了高温稳定的变体", memory_type=MemoryType.EPISODIC)
        
        # 检索记忆
        experiences = memory.recall(query="变体设计", limit=5)
        
        # 记录进化
        memory.record_evolution("thermal_stability", 0.7, 0.85, "学习了新的稳定性设计策略")
    """
    
    def __init__(
        self,
        agent_id: Optional[int] = None,
        storage_path: Optional[Path] = None,
        max_entries: int = 1000,
    ):
        """
        初始化记忆系统
        
        Args:
            agent_id: 智能体ID（None表示全局记忆）
            storage_path: 存储路径
            max_entries: 最大记忆条目数
        """
        self.agent_id = agent_id
        self.storage_path = storage_path or Path("data/memory")
        self.max_entries = max_entries
        
        self._memories: Dict[str, MemoryEntry] = {}
        self._evolutions: List[EvolutionRecord] = []
        self._knowledge_graph: Dict[str, List[str]] = defaultdict(list)
        
        # 初始化存储
        self._ensure_storage()
        self._load_memories()
    
    def _ensure_storage(self):
        """确保存储目录存在"""
        if self.agent_id:
            self.storage_path = self.storage_path / f"agent_{self.agent_id}"
        else:
            self.storage_path = self.storage_path / "global"
        
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def _get_memory_file(self) -> Path:
        """获取记忆文件路径"""
        return self.storage_path / "memories.json"
    
    def _get_evolution_file(self) -> Path:
        """获取进化记录文件路径"""
        return self.storage_path / "evolutions.json"
    
    def _load_memories(self):
        """加载记忆"""
        memory_file = self._get_memory_file()
        if memory_file.exists():
            try:
                with open(memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._memories = {
                        k: MemoryEntry.from_dict(v) for k, v in data.get("memories", {}).items()
                    }
                    self._evolutions = [
                        EvolutionRecord(**e) for e in data.get("evolutions", [])
                    ]
                logger.info(f"Loaded {len(self._memories)} memories for agent {self.agent_id}")
            except Exception as e:
                logger.error(f"Failed to load memories: {e}")
    
    def _save_memories(self):
        """保存记忆"""
        memory_file = self._get_memory_file()
        try:
            data = {
                "memories": {k: v.to_dict() for k, v in self._memories.items()},
                "evolutions": [e.to_dict() for e in self._evolutions],
            }
            with open(memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Saved {len(self._memories)} memories")
        except Exception as e:
            logger.error(f"Failed to save memories: {e}")
    
    def remember(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.EPISODIC,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> MemoryEntry:
        """
        存储新记忆
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性
            metadata: 元数据
            tags: 标签
            
        Returns:
            创建的记忆条目
        """
        import uuid
        
        entry = MemoryEntry(
            id=str(uuid.uuid4())[:8],
            agent_id=self.agent_id or 0,
            memory_type=memory_type,
            content=content,
            metadata=metadata or {},
            importance=importance,
            tags=tags or [],
        )
        
        self._memories[entry.id] = entry
        
        # 添加到知识图谱
        for tag in (tags or []):
            self._knowledge_graph[tag].append(entry.id)
        
        # 维护最大条目数
        if len(self._memories) > self.max_entries:
            self._prune_memories()
        
        self._save_memories()
        return entry
    
    def recall(
        self,
        query: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[MemoryEntry]:
        """
        检索记忆根据query进行模糊匹配，memory_type过滤类型，tags过滤标签
        
        Args:
            query: 查询字符串（模糊匹配）
            memory_type: 记忆类型过滤
            tags: 标签过滤
            limit: 返回数量限制
            
        Returns:
            匹配的记忆列表
        """
        results = []
        
        for entry in self._memories.values():
            # 类型过滤
            if memory_type and entry.memory_type != memory_type:
                continue
            
            # 标签过滤
            if tags and not any(t in entry.tags for t in tags):
                continue
            
            # 查询匹配
            if query:
                query_lower = query.lower()
                content_lower = entry.content.lower()
                if query_lower not in content_lower:
                    # 检查元数据
                    if not any(
                        query_lower in str(v).lower()
                        for v in entry.metadata.values()
                    ):
                        continue
            
            # 更新访问记录
            entry.last_accessed = datetime.now()
            entry.access_count += 1
            
            results.append(entry)
        
        # 按重要性和访问次数排序
        results.sort(key=lambda x: (x.importance.value, x.access_count), reverse=True)
        
        return results[:limit]
    
    def forget(self, memory_id: str) -> bool:
        """
        删除记忆
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            是否成功删除
        """
        if memory_id in self._memories:
            del self._memories[memory_id]
            self._save_memories()
            return True
        return False
    
    def record_evolution(
        self,
        capability: str,
        before_value: Any,
        after_value: Any,
        reason: str,
        confidence: float = 1.0,
    ) -> EvolutionRecord:
        """
        记录能力进化
        
        Args:
            capability: 能力名称
            before_value: 之前值
            after_value: 之后值
            reason: 进化原因
            confidence: 置信度
            
        Returns:
            进化记录
        """
        record = EvolutionRecord(
            agent_id=self.agent_id or 0,
            timestamp=datetime.now(),
            capability=capability,
            before_value=before_value,
            after_value=after_value,
            reason=reason,
            confidence=confidence,
        )
        
        self._evolutions.append(record)
        self._save_memories()
        
        return record
    
    def get_evolution_history(
        self,
        capability: Optional[str] = None,
        limit: int = 50,
    ) -> List[EvolutionRecord]:
        """
        获取进化历史
        
        Args:
            capability: 能力过滤
            limit: 返回数量限制
            
        Returns:
            进化记录列表
        """
        records = self._evolutions
        
        if capability:
            records = [r for r in records if r.capability == capability]
        
        return sorted(records, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def _prune_memories(self):
        """清理低重要性记忆"""
        # 按重要性和访问次数排序
        sorted_memories = sorted(
            self._memories.values(),
            key=lambda x: (x.importance.value, x.access_count)
        )
        
        # 删除最不重要的记忆
        while len(self._memories) > self.max_entries:
            entry = sorted_memories.pop(0)
            self._memories.pop(entry.id, None)
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        获取当前能力状态
        
        Returns:
            能力字典
        """
        capabilities = {}
        
        for record in self._evolutions:
            cap = record.capability
            if cap not in capabilities:
                capabilities[cap] = {
                    "current_value": record.after_value,
                    "evolution_count": 1,
                    "last_evolution": record.timestamp,
                }
            else:
                capabilities[cap]["current_value"] = record.after_value
                capabilities[cap]["evolution_count"] += 1
                capabilities[cap]["last_evolution"] = record.timestamp
        
        return capabilities
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取记忆摘要"""
        return {
            "agent_id": self.agent_id,
            "total_memories": len(self._memories),
            "memory_types": {
                t.value: len([m for m in self._memories.values() if m.memory_type == t])
                for t in MemoryType
            },
            "total_evolutions": len(self._evolutions),
            "capabilities": self.get_capabilities(),
            "top_tags": sorted(
                [(k, len(v)) for k, v in self._knowledge_graph.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10],
        }


class MemoryIntegrator:
    """
    记忆整合器
    
    整合多个智能体的记忆，构建全局知识图谱。
    """
    
    def __init__(self):
        self.agent_memories: Dict[int, AgentMemory] = {}
        self.global_memory = AgentMemory(agent_id=None)
    
    def register_agent(self, agent_id: int) -> AgentMemory:
        """注册智能体记忆"""
        if agent_id not in self.agent_memories:
            self.agent_memories[agent_id] = AgentMemory(agent_id=agent_id)
        return self.agent_memories[agent_id]
    
    def share_knowledge(
        self,
        from_agent_id: int,
        to_agent_ids: List[int],
        memory_id: str,
    ) -> bool:
        """
        共享知识到其他智能体
        
        Args:
            from_agent_id: 来源智能体ID
            to_agent_ids: 目标智能体ID列表
            memory_id: 记忆ID
            
        Returns:
            是否成功共享
        """
        if from_agent_id not in self.agent_memories:
            return False
        
        source_memory = self.agent_memories[from_agent_id]
        if memory_id not in source_memory._memories:
            return False
        
        entry = source_memory._memories[memory_id]
        
        for to_id in to_agent_ids:
            if to_id not in self.agent_memories:
                self.register_agent(to_id)
            
            target_memory = self.agent_memories[to_id]
            target_memory.remember(
                content=entry.content,
                memory_type=entry.memory_type,
                importance=entry.importance,
                metadata={**entry.metadata, "shared_from": from_agent_id},
                tags=entry.tags + ["shared"],
            )
        
        return True
    
    def get_global_knowledge(self) -> Dict[str, Any]:
        """获取全局知识"""
        return self.global_memory.get_summary()
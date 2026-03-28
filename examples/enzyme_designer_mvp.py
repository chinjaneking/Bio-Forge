"""
Enzyme Designer MVP - 酶设计工作流演示

展示如何使用 DeerFlow 集成层执行酶设计工作流。

MVP 功能:
1. 多智能体协作流程
2. 工作流执行和结果追踪
3. 记忆累积和进化记录
4. 结果输出和可视化

使用方式:
    python examples/enzyme_designer_mvp.py --sequence "MKTLLIAG..." --reaction "ATP + Glucose -> ADP + Glucose-6-P"
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# 配置 Windows 控制台 UTF-8 编码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from deerflow_engine import (
    BaseDeerFlowAgent,
    WorkflowGenerator,
    WorkflowDefinition,
    WorkflowExecutor,
    WorkflowNode,
    AgentMemory,
    MemoryType,
    MemoryImportance,
)


class EnzymeDesignerMVP:
    """
    酶设计 MVP 工作流管理器
    
    协调多个智能体完成酶设计任务，包括:
    - 任务分解
    - 蛋白质结构预测
    - 酶工程优化
    - 自由能计算
    - 量子化学分析
    - PCR引物设计
    """
    
    def __init__(self, use_memory: bool = True):
        """
        初始化酶设计器
        
        Args:
            use_memory: 是否启用记忆系统
        """
        self.use_memory = use_memory
        self.memory = AgentMemory(agent_id=1000) if use_memory else None
        self.workflow: Optional[WorkflowDefinition] = None
        self.results: Dict[str, Any] = {}
        self.execution_log: List[Dict[str, Any]] = []
    
    def create_workflow(
        self,
        target_sequence: str,
        target_reaction: str,
        optimization_goals: Optional[List[str]] = None,
    ) -> WorkflowDefinition:
        """
        创建酶设计工作流
        
        Args:
            target_sequence: 目标蛋白质序列
            target_reaction: 目标催化反应
            optimization_goals: 优化目标列表
            
        Returns:
            工作流定义
        """
        generator = WorkflowGenerator()
        
        # 使用预定义的酶设计流程
        workflow = generator.create_enzyme_design_pipeline(
            target_sequence=target_sequence,
            target_reaction=target_reaction,
        )
        
        # 添加优化目标到元数据
        if optimization_goals:
            workflow.metadata["optimization_goals"] = optimization_goals
        
        self.workflow = workflow
        
        # 记录工作流创建
        if self.memory:
            self.memory.remember(
                content=f"创建酶设计工作流: 序列长度={len(target_sequence)}, 反应={target_reaction}",
                memory_type=MemoryType.EPISODIC,
                importance=MemoryImportance.HIGH,
                tags=["workflow", "enzyme_design", "creation"],
            )
        
        return workflow
    
    def execute(self, verbose: bool = True) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            verbose: 是否打印详细输出
            
        Returns:
            执行结果
        """
        if not self.workflow:
            raise ValueError("No workflow created. Call create_workflow() first.")
        
        if verbose:
            print("=" * 70)
            print("🧬 Enzyme Designer MVP - 工作流执行")
            print("=" * 70)
            print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"节点数量: {len(self.workflow.nodes)}")
            print()
        
        # 创建执行器
        executor = WorkflowExecutor(self.workflow)
        
        # 按拓扑顺序执行
        execution_order = self.workflow.topological_sort()
        
        if verbose:
            print("执行顺序:")
            for i, node_id in enumerate(execution_order, 1):
                node = self.workflow.nodes[node_id]
                print(f"  {i}. {node.name} ({node.agent_type})")
            print()
        
        # 执行每个节点
        start_time = time.time()
        
        for node_id in execution_order:
            node = self.workflow.nodes[node_id]
            
            if verbose:
                print(f"\n{'─' * 50}")
                print(f"📊 执行节点: {node.name}")
                print(f"   智能体类型: {node.agent_type}")
            
            node_start = time.time()
            
            # 准备输入
            input_message = self._prepare_input(node, executor.context)
            
            # 创建智能体
            agent = BaseDeerFlowAgent(
                name=node.name,
                agent_type=node.agent_type,
                description=f"酶设计工作流节点: {node.name}",
                capabilities=self._get_capabilities(node.agent_type),
            )
            
            # 执行
            result = agent.execute(input_message)
            
            node_duration = time.time() - node_start
            
            # 记录结果
            executor.results[node_id] = result.to_dict()
            executor.context[f"{node_id}_result"] = result.content
            
            # 记录执行日志
            self.execution_log.append({
                "node_id": node_id,
                "node_name": node.name,
                "agent_type": node.agent_type,
                "status": result.status.value,
                "duration": node_duration,
                "output_length": len(result.content),
                "timestamp": datetime.now().isoformat(),
            })
            
            if verbose:
                status_icon = "✅" if result.status.value == "success" else "❌"
                print(f"   状态: {status_icon} {result.status.value}")
                print(f"   耗时: {node_duration:.2f}s")
                print(f"   输出预览: {result.content[:200]}...")
        
        total_duration = time.time() - start_time
        
        if verbose:
            print("\n" + "=" * 70)
            print("📊 执行摘要")
            print("=" * 70)
            print(f"总耗时: {total_duration:.2f}秒")
            print(f"节点数: {len(execution_order)}")
            print(f"成功: {sum(1 for log in self.execution_log if log['status'] == 'success')}")
            print(f"失败: {sum(1 for log in self.execution_log if log['status'] == 'failed')}")
        
        # 更新记忆
        if self.memory:
            self.memory.remember(
                content=f"完成酶设计工作流执行: {len(execution_order)}个节点, {total_duration:.1f}秒",
                memory_type=MemoryType.EPISODIC,
                importance=MemoryImportance.HIGH,
                tags=["workflow", "enzyme_design", "completion"],
            )
            
            # 记录能力进化
            self.memory.record_evolution(
                capability="workflow_execution_count",
                before_value=len(self.execution_log) - 1,
                after_value=len(self.execution_log),
                reason="完成新的工作流执行",
            )
        
        self.results = executor.results
        return self.results
    
    def _prepare_input(self, node: WorkflowNode, context: Dict[str, Any]) -> str:
        """准备节点输入"""
        input_text = node.input_template
        
        # 替换上下文变量
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            if placeholder in input_text:
                input_text = input_text.replace(placeholder, str(value))
        
        return input_text
    
    def _get_capabilities(self, agent_type: str) -> List[str]:
        """获取智能体能力"""
        capabilities_map = {
            "R_D_ASSISTANT": ["任务分解", "进度追踪", "资源协调"],
            "PROTEIN_STRUCTURE_PREDICTOR": ["结构预测", "折叠分析", "稳定性评估"],
            "ENZYME_ENGINEER": ["酶设计", "变体生成", "活性优化"],
            "FREE_ENERGY_CALCULATOR": ["自由能计算", "稳定性分析", "结合亲和力"],
            "QUANTUM_CHEMISTRY": ["量子化学计算", "过渡态分析", "反应机理"],
            "PCR_PRIMER_DESIGNER": ["引物设计", "序列优化", "实验准备"],
        }
        return capabilities_map.get(agent_type, ["通用能力"])
    
    def get_report(self) -> Dict[str, Any]:
        """生成执行报告"""
        return {
            "workflow": {
                "name": self.workflow.name if self.workflow else None,
                "nodes": len(self.workflow.nodes) if self.workflow else 0,
            },
            "execution": {
                "log": self.execution_log,
                "total_duration": sum(log["duration"] for log in self.execution_log),
                "success_rate": sum(1 for log in self.execution_log if log["status"] == "success") / len(self.execution_log) if self.execution_log else 0,
            },
            "memory": self.memory.get_summary() if self.memory else None,
            "results": self.results,
            "generated_at": datetime.now().isoformat(),
        }
    
    def save_report(self, filepath: str) -> None:
        """保存报告到文件"""
        report = self.get_report()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)


def demo_synasalid_production():
    """Synasalid 生产工作流演示"""
    print("\n" + "=" * 70)
    print("🌿 Synasalid 生产工作流演示")
    print("=" * 70)
    
    generator = WorkflowGenerator()
    workflow = generator.create_synasalid_production_pipeline(
        target_concentration=150.0  # mg/L
    )
    
    print(f"\n工作流名称: {workflow.name}")
    print(f"节点数量: {len(workflow.nodes)}")
    print(f"\n节点列表:")
    for node_id, node in workflow.nodes.items():
        print(f"  {node_id}: {node.name} ({node.agent_type})")
    
    print(f"\n执行顺序: {' → '.join(workflow.topological_sort())}")


def main():
    parser = argparse.ArgumentParser(description="Enzyme Designer MVP")
    parser.add_argument("--sequence", type=str, default="MKTLLIAG...",
                       help="目标蛋白质序列")
    parser.add_argument("--reaction", type=str, default="ATP + Glucose -> ADP + Glucose-6-P",
                       help="目标催化反应")
    parser.add_argument("--optimization", type=str, nargs="+",
                       default=["thermal_stability", "catalytic_efficiency"],
                       help="优化目标")
    parser.add_argument("--output", type=str, default=None,
                       help="输出报告文件路径")
    parser.add_argument("--demo-synasalid", action="store_true",
                       help="运行 Synasalid 生产演示")
    parser.add_argument("--no-memory", action="store_true",
                       help="禁用记忆系统")
    
    args = parser.parse_args()
    
    # Synasalid 演示模式
    if args.demo_synasalid:
        demo_synasalid_production()
        return
    
    # 酶设计 MVP
    designer = EnzymeDesignerMVP(use_memory=not args.no_memory)
    
    # 创建工作流
    print(f"\n📋 创建酶设计工作流...")
    print(f"   目标序列: {args.sequence[:30]}...")
    print(f"   目标反应: {args.reaction}")
    print(f"   优化目标: {', '.join(args.optimization)}")
    
    workflow = designer.create_workflow(
        target_sequence=args.sequence,
        target_reaction=args.reaction,
        optimization_goals=args.optimization,
    )
    
    # 执行工作流
    results = designer.execute(verbose=True)
    
    # 保存报告
    if args.output:
        designer.save_report(args.output)
        print(f"\n📄 报告已保存: {args.output}")
    else:
        # 默认保存路径
        output_dir = project_root / "data" / "enzyme_designer"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        designer.save_report(str(output_file))
        print(f"\n📄 报告已保存: {output_file}")
    
    # 打印记忆摘要
    if designer.memory:
        print("\n🧠 记忆摘要:")
        summary = designer.memory.get_summary()
        print(f"   总记忆: {summary['total_memories']}")
        print(f"   进化次数: {summary['total_evolutions']}")
        if summary['capabilities']:
            print("   能力状态:")
            for cap, data in summary['capabilities'].items():
                print(f"     {cap}: {data['current_value']}")


if __name__ == "__main__":
    main()
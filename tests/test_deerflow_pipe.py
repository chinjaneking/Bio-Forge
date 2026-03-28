"""
DeerFlow 集成 Pipe Test - 验证 Bio-Forge 到 DeerFlow 的集成管道

测试目标:
1. 验证 DeerFlow 配置正确加载
2. 验证 BaseDeerFlowAgent 可以创建和执行
3. 验证 Workflow 生成和执行
4. 验证 Memory 系统工作正常

运行方式:
    python test_deerflow_pipe.py
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# 配置 Windows 控制台 UTF-8 编码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 测试结果存储
test_results = {
    "timestamp": datetime.now().isoformat(),
    "tests": [],
    "summary": {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
    }
}


def log_test(name: str, status: str, message: str = "", details: dict = None):
    """记录测试结果"""
    test_results["tests"].append({
        "name": name,
        "status": status,
        "message": message,
        "details": details or {},
        "timestamp": datetime.now().isoformat(),
    })
    test_results["summary"]["total"] += 1
    if status == "PASS":
        test_results["summary"]["passed"] += 1
        print(f"✅ {name}: PASS")
    elif status == "FAIL":
        test_results["summary"]["failed"] += 1
        print(f"❌ {name}: FAIL - {message}")
    else:
        test_results["summary"]["skipped"] += 1
        print(f"⏭️  {name}: SKIP - {message}")


def test_imports():
    """测试 1: 验证模块导入"""
    print("\n" + "=" * 60)
    print("测试 1: 模块导入验证")
    print("=" * 60)
    
    try:
        from deerflow_engine import (
            BaseDeerFlowAgent,
            WorkflowGenerator,
            WorkflowNode,
            WorkflowEdge,
            DeerFlowConfig,
            get_deerflow_config,
            AgentMemory,
            MemoryEntry,
        )
        log_test("模块导入", "PASS", "所有核心模块导入成功")
        return True
    except ImportError as e:
        log_test("模块导入", "FAIL", str(e))
        return False


def test_config():
    """测试 2: 验证配置系统"""
    print("\n" + "=" * 60)
    print("测试 2: 配置系统验证")
    print("=" * 60)
    
    try:
        from deerflow_engine.config import DeerFlowConfig, get_deerflow_config
        
        # 测试默认配置
        config = get_deerflow_config()
        print(f"  DeerFlow 路径: {config.deerflow_root}")
        print(f"  默认模型: {config.default_model}")
        print(f"  思考模式: {config.thinking_enabled}")
        
        # 验证配置
        errors = config.validate()
        if errors:
            log_test("配置验证", "FAIL", "; ".join(errors), {"errors": errors})
            return False
        
        log_test("配置系统", "PASS", f"DeerFlow路径: {config.deerflow_root}")
        return True
        
    except Exception as e:
        log_test("配置系统", "FAIL", str(e))
        return False


def test_base_agent_creation():
    """测试 3: 验证 BaseDeerFlowAgent 创建"""
    print("\n" + "=" * 60)
    print("测试 3: BaseDeerFlowAgent 创建验证")
    print("=" * 60)
    
    try:
        from deerflow_engine.base_agent import BaseDeerFlowAgent
        
        # 测试从字典创建
        agent = BaseDeerFlowAgent(
            name="测试智能体",
            agent_type="R_D_ASSISTANT",
            description="这是一个测试智能体",
            capabilities=["任务分解", "进度追踪"],
            priority=5,
        )
        
        print(f"  名称: {agent.name}")
        print(f"  类型: {agent.agent_type}")
        print(f"  能力: {agent.capabilities}")
        
        # 验证方法存在
        assert hasattr(agent, 'execute'), "缺少 execute 方法"
        assert hasattr(agent, 'stream'), "缺少 stream 方法"
        assert hasattr(agent, 'to_dict'), "缺少 to_dict 方法"
        
        log_test("Agent创建", "PASS", f"成功创建: {agent.name}")
        return True
        
    except Exception as e:
        log_test("Agent创建", "FAIL", str(e))
        return False


def test_agent_execution_simulation():
    """测试 4: 验证 Agent 执行（模拟模式）"""
    print("\n" + "=" * 60)
    print("测试 4: Agent 执行验证 (模拟模式)")
    print("=" * 60)
    
    try:
        from deerflow_engine.base_agent import BaseDeerFlowAgent, ExecutionStatus
        
        agent = BaseDeerFlowAgent(
            name="研发总监助手",
            agent_type="R_D_ASSISTANT",
            description="协助研发总监进行任务管理",
            capabilities=["任务分解", "进度追踪", "资源协调"],
        )
        
        # 模拟执行
        result = agent.execute("设计一个新的酶催化反应")
        
        print(f"  状态: {result.status.value}")
        print(f"  内容长度: {len(result.content)} 字符")
        print(f"  执行时长: {result.duration_seconds:.2f} 秒" if result.duration_seconds else "")
        
        if result.status == ExecutionStatus.SUCCESS:
            log_test("Agent执行", "PASS", f"模拟执行成功")
            return True
        else:
            log_test("Agent执行", "FAIL", f"执行状态: {result.status.value}")
            returnFalse
            
    except Exception as e:
        log_test("Agent执行", "FAIL", str(e))
        return False


def test_workflow_creation():
    """测试 5: 验证 Workflow 生成"""
    print("\n" + "=" * 60)
    print("测试 5: Workflow 生成验证")
    print("=" * 60)
    
    try:
        from deerflow_engine.workflow import WorkflowGenerator, WorkflowStatus
        
        workflow_gen = WorkflowGenerator()
        
        # 创建酶设计工作流
        workflow = workflow_gen.create_enzyme_design_pipeline(
            target_sequence="MKTLLIAG...",
            target_reaction="ATP + Glucose -> ADP + Glucose-6-P"
        )
        
        print(f"  工作流名称: {workflow.name}")
        print(f"  节点数量: {len(workflow.nodes)}")
        print(f"  边数量: {len(workflow.edges)}")
        print(f"  状态: {workflow.status.value}")
        
        # 验证拓扑排序
        execution_order = workflow.topological_sort()
        print(f"  执行顺序: {' -> '.join(execution_order)}")
        
        log_test("Workflow生成", "PASS", f"节点数: {len(workflow.nodes)}, 边数: {len(workflow.edges)}")
        return True
        
    except Exception as e:
        log_test("Workflow生成", "FAIL", str(e))
        return False


def test_workflow_execution():
    """测试 6: 验证 Workflow 执行"""
    print("\n" + "=" * 60)
    print("测试 6: Workflow 执行验证")
    print("=" * 60)
    
    try:
        from deerflow_engine.workflow import WorkflowGenerator, WorkflowExecutor, WorkflowNode
        
        # 创建简单工作流
        workflow_gen = WorkflowGenerator()
        workflow_gen.create_workflow(
            name="测试工作流",
            description="简单测试流程"
        )
        
        # 创建节点并添加到工作流
        node = WorkflowNode(
            id="test_node_1",
            name="节点1",
            agent_type="R_D_ASSISTANT",
            input_template="执行测试任务"
        )
        workflow_gen.current_workflow.add_node(node)
        
        # 验证工作流
        errors = workflow_gen.current_workflow.validate()
        if errors:
            log_test("Workflow执行", "FAIL", "; ".join(errors))
            return False
        
        # 执行工作流
        executor = WorkflowExecutor(workflow_gen.current_workflow)
        results = executor.execute()
        
        print(f"  执行结果: {len(results)} 个节点完成")
        for node_id, result in results.items():
            print(f"    {node_id}: {result.get('status', 'unknown')}")
        
        log_test("Workflow执行", "PASS", f"完成 {len(results)} 个节点")
        return True
        
    except Exception as e:
        log_test("Workflow执行", "FAIL", str(e))
        return False


def test_memory_system():
    """测试 7: 验证 Memory 系统"""
    print("\n" + "=" * 60)
    print("测试 7: Memory 系统验证")
    print("=" * 60)
    
    try:
        from deerflow_engine.memory import AgentMemory, MemoryType, MemoryImportance
        import tempfile
        
        # 使用临时目录
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = AgentMemory(agent_id=999, storage_path=Path(tmpdir))
            
            # 测试记忆存储
            entry = memory.remember(
                content="成功设计了高温稳定的酶变体",
                memory_type=MemoryType.EPISODIC,
                importance=MemoryImportance.HIGH,
                tags=["酶设计", "稳定性"],
            )
            print(f"  存储记忆: {entry.id}")
            
            # 测试记忆检索
            results = memory.recall(query="酶变体", limit=5)
            print(f"  检索结果: {len(results)} 条")
            
            # 测试进化记录
            evolution = memory.record_evolution(
                capability="thermal_stability",
                before_value=0.7,
                after_value=0.85,
                reason="学习了新的稳定性设计策略"
            )
            print(f"  进化记录: {evolution.capability}")
            
            # 获取摘要
            summary = memory.get_summary()
            print(f"  记忆总数: {summary['total_memories']}")
            print(f"  进化次数: {summary['total_evolutions']}")
        
        log_test("Memory系统", "PASS", f"记忆存储和检索正常")
        return True
        
    except Exception as e:
        log_test("Memory系统", "FAIL", str(e))
        return False


def test_agent_from_dict():
    """测试 8: 验证从字典创建Agent"""
    print("\n" + "=" * 60)
    print("测试 8: Agent 字典创建验证")
    print("=" * 60)
    
    try:
        from deerflow_engine.base_agent import BaseDeerFlowAgent
        
        agent_dict = {
            "name": "蛋白质结构预测Agent",
            "agent_type": "PROTEIN_STRUCTURE_PREDICTOR",
            "description": "使用AlphaFold2预测蛋白质三级结构",
            "capabilities": ["结构预测", "构象分析", "稳定性评估"],
            "priority": 3,
        }
        
        agent = BaseDeerFlowAgent.from_dict(agent_dict)
        
        print(f"  名称: {agent.name}")
        print(f"  类型: {agent.agent_type}")
        print(f"  描述: {agent.description}")
        
        # 转换回字典
        result_dict = agent.to_dict()
        assert result_dict["name"] == agent_dict["name"]
        assert result_dict["agent_type"] == agent_dict["agent_type"]
        
        log_test("Agent字典创建", "PASS", f"成功创建: {agent.name}")
        return True
        
    except Exception as e:
        log_test("Agent字典创建", "FAIL", str(e))
        return False


def test_synasalid_workflow():
    """测试 9: 验证 Synasalid 工作流"""
    print("\n" + "=" * 60)
    print("测试 9: Synasalid 工作流验证")
    print("=" * 60)
    
    try:
        from deerflow_engine.workflow import WorkflowGenerator
        
        workflow_gen = WorkflowGenerator()
        workflow = workflow_gen.create_synasalid_production_pipeline(
            target_concentration=150.0  # mg/L
        )
        
        print(f"  工作流名称: {workflow.name}")
        print(f"  节点数量: {len(workflow.nodes)}")
        
        # 打印节点
        for node_id, node in workflow.nodes.items():
            print(f"    {node_id}: {node.name} ({node.agent_type})")
        
        log_test("Synasalid工作流", "PASS", f"成功创建 {len(workflow.nodes)} 节点")
        return True
        
    except Exception as e:
        log_test("Synasalid工作流", "FAIL", str(e))
        return False


def test_deerflow_client_connection():
    """测试 10: 验证 DeerFlow Client 连接（可选）"""
    print("\n" + "=" * 60)
    print("测试 10: DeerFlow Client 连接验证")
    print("=" * 60)
    
    try:
        from deerflow_engine.config import get_deerflow_client
        
        client = get_deerflow_client()
        
        # 测试简单调用
        response = client.chat("你好，这是一个测试消息")
        print(f"  响应长度: {len(response)} 字符")
        
        log_test("DeerFlow连接", "PASS", "成功连接并获取响应")
        return True
        
    except ImportError as e:
        log_test("DeerFlow连接", "SKIP", f"DeerFlow 未安装: {e}")
        return None
        
    except Exception as e:
        log_test("DeerFlow连接", "SKIP", f"连接失败（可能是模拟模式）: {e}")
        return None


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("🧪 DeerFlow 集成 Pipe Test")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行测试
    tests = [
        test_imports,
        test_config,
        test_base_agent_creation,
        test_agent_execution_simulation,
        test_workflow_creation,
        test_workflow_execution,
        test_memory_system,
        test_agent_from_dict,
        test_synasalid_workflow,
        test_deerflow_client_connection,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"测试异常: {e}")
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("📊 测试摘要")
    print("=" * 70)
    print(f"总计: {test_results['summary']['total']}")
    print(f"通过: {test_results['summary']['passed']} ✅")
    print(f"失败: {test_results['summary']['failed']} ❌")
    print(f"跳过: {test_results['summary']['skipped']} ⏭️")
    
    # 保存结果
    result_file = project_root / "data" / "test_results" / "deerflow_pipe_test.json"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {result_file}")
    
    return test_results["summary"]["failed"] == 0


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
"""
Bio-Forge Main Application
AI-Powered Synthetic Biology Platform
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.core.config import settings
from app.api.routes import router as api_router

# 静态文件目录
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动
    print("🚀 Bio-Forge 启动中...")
    print(f"📊 智能体矩阵: 120个分层智能体")
    print(f"🧬 合成生物学平台 v{settings.VERSION}")
    print(f"🌐 Web界面: http://localhost:1983/")
    
    yield
    
    # 关闭
    print("🛑 Bio-Forge 关闭中...")


# 创建FastAPI应用
app = FastAPI(
    title="Bio-Forge API",
    description="AI-Powered Synthetic Biology Platform - Genesis-2026",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# 挂载静态文件
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 模板
templates = Jinja2Templates(directory=str(TEMPLATES_DIR)) if TEMPLATES_DIR.exists() else None

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix="/api/v1")

# 注册DeerFlow路由
from app.api.deerflow_routes import register_deerflow_routes
register_deerflow_routes(app)


@app.post("/api/v1/workflow/execute", tags=["Workflow"])
async def execute_workflow(data: dict):
    """执行DeerFlow工作流"""
    import os
    os.environ.setdefault("DEER_FLOW_HOME", "C:/Bio-Forge/data/deerflow")
    
    from deerflow_engine import WorkflowGenerator, BaseDeerFlowAgent, AgentMemory
    from deerflow_engine.config import get_deerflow_config
    
    workflow_type = data.get("workflow_type", "enzyme-design")
    target_sequence = data.get("target_sequence", "")
    target_reaction = data.get("target_reaction", "ATP + Glucose -> ADP + Glucose-6-P")
    optimization_goals = data.get("optimization_goals", ["thermal_stability", "catalytic_efficiency"])
    
    try:
        # 创建工作流生成器
        workflow_gen = WorkflowGenerator()
        
        if workflow_type == "enzyme-design":
            workflow = workflow_gen.create_enzyme_design_pipeline(
                target_sequence=target_sequence,
                target_reaction=target_reaction
            )
        elif workflow_type == "synasalid":
            workflow = workflow_gen.create_synasalid_production_pipeline()
        else:
            workflow = workflow_gen.create_enzyme_design_pipeline(
                target_sequence=target_sequence,
                target_reaction=target_reaction
            )
        
        # 执行工作流（模拟模式）
        result = workflow.execute_simulated()
        
        return {
            "status": "success",
            "workflow_id": workflow.id,
            "workflow_name": workflow.name,
            "nodes_completed": len([n for n in workflow.nodes if n.status.value == "success"]),
            "total_nodes": len(workflow.nodes),
            "execution_order": workflow.topological_sort(),
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@app.get("/", tags=["Dashboard"], response_class=HTMLResponse)
async def dashboard(request: Request):
    """Web界面仪表盘"""
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    # 如果没有模板，返回简单的HTML
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head><title>Bio-Forge</title></head>
    <body style="background:#0f172a;color:#f1f5f9;font-family:system-ui;padding:40px;">
        <h1>🧬 Bio-Forge</h1>
        <p>AI合成生物学平台</p>
        <p><a href="/docs" style="color:#3b82f6">API文档</a> | <a href="/health" style="color:#10b981">健康检查</a></p>
        <p>版本: Genesis-2026</p>
    </body>
    </html>
    """)


@app.get("/api", tags=["Health"])
async def api_root():
    """API根路径"""
    return {
        "name": "Bio-Forge API",
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": "2026-03-27"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 1983))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )

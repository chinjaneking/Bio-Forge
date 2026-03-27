"""DeerFlow 2.0 主应用"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import init_db, SessionLocal
from app.agent_manager import AgentManager
from app.api import agents, tasks

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print(f"🚀 启动 DeerFlow 2.0...")
    init_db()
    
    # 初始化默认智能体
    db = SessionLocal()
    try:
        manager = AgentManager(db)
        manager.initialize_default_agents()
    finally:
        db.close()
    
    print("✅ DeerFlow 2.0 启动成功!")
    yield
    
    # 关闭时
    print("👋 关闭 DeerFlow 2.0...")


# 创建FastAPI应用
app = FastAPI(
    title="DeerFlow 2.0",
    description="智能体协调中枢与任务调度平台",
    version="2.0.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(agents.router, prefix=settings.api_prefix)
app.include_router(tasks.router, prefix=settings.api_prefix)


@app.get("/")
def root():
    """根路径"""
    return {
        "name": "DeerFlow 2.0",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.get("/api/v1/status")
def system_status():
    """系统状态"""
    return {
        "app": "DeerFlow 2.0",
        "status": "active",
        "max_agents": settings.max_agents,
        "api_prefix": settings.api_prefix
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

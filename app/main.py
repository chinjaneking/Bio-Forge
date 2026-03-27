"""
Bio-Forge Main Application
AI-Powered Synthetic Biology Platform
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动
    print("🚀 Bio-Forge 启动中...")
    print(f"📊 智能体矩阵: 120个分层智能体")
    print(f"🧬 合成生物学平台 v{settings.VERSION}")
    
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


@app.get("/", tags=["Health"])
async def root():
    """根路径 - 服务状态"""
    return {
        "name": "Bio-Forge",
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "agent_matrix": "120 agents (6 layers)",
        "codename": "Genesis-2026"
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

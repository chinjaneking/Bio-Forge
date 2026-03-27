# Bio-Forge

<div align="center">

**AI-Powered Synthetic Biology Platform**

*Genesis-2026 | 120 Intelligent Agents*

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 项目简介

Bio-Forge 是一个基于120分层智能体矩阵的合成生物学AI平台，为生物研发提供从分子设计到工艺放大的全流程智能支持。

### 核心特性

- **120个智能体矩阵**: 覆盖生物研发全流程
- **6层架构设计**: 从基础架构到项目专项
- **RESTful API**: 完整的智能体管理和任务调度接口
- **Docker部署**: 一键部署，开箱即用

### 智能体架构

| 层级 | 类型 | 数量 | 描述 |
|------|------|------|------|
| L1 | 基础架构 | 20 | 平台管理、数据管理、安全监控 |
| L2 | 计算设计 | 25 | 分子建模、蛋白质设计、途径设计 |
| L3 | 实验执行 | 20 | 分子生物学、微生物学、分析化学 |
| L4 | 优化验证 | 20 | 产量优化、稳定性增强、放大生产 |
| L5 | 研发助理 | 20 | 文献调研、项目管理、质量控制 |
| L6 | 项目专项 | 15 | Synasalid项目专项智能体 |

### 快速开始

#### Docker 部署（推荐）

```bash
# 克隆项目
git clone https://github.com/chinjaneking/Bio-Forge.git
cd Bio-Forge

# 配置环境变量
cp .env.example .env

# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps

# 运行测试
python test_run.py
```

#### 本地部署

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env

# 启动服务
python -m app.main

# 访问API文档
# http://localhost:1983/docs
```

### 项目结构

```
Bio-Forge/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── agent_manager.py     # 智能体管理核心
│   ├── task_scheduler.py    # 任务调度器
│   ├── core/
│   │   └── config.py        # 配置管理
│   ├── models/
│   │   ├── agent.py         # 智能体模型
│   │   └── task.py          # 任务模型
│   └── api/
│       └── routes.py        # API路由
├── docs/
│   └── project-plans/       # 项目规划文档
├── data/                    # 数据库存储
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── test_agents.py           # 智能体测试
├── test_run.py              # 系统测试
└── README.md
```

### API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/v1/agents` | GET | 获取智能体列表 |
| `/api/v1/agents/{id}` | GET | 获取智能体详情 |
| `/api/v1/tasks` | POST | 创建任务 |
| `/api/v1/tasks/{id}` | GET | 获取任务状态 |

### 配置说明

```env
# 应用配置
APP_NAME=Bio-Forge
APP_ENV=development
PORT=1983

# 数据库
DATABASE_URL=sqlite:///./data/bio-forge.db

# Redis (可选)
REDIS_URL=redis://localhost:6379/0

# 智能体配置
AGENT_MATRIX_SIZE=120
AGENT_LAYERS=6
```

### 版本信息

- **版本**: 1.0.0
- **代号**: Genesis-2026
- **智能体数量**: 120
- **端口**: 1983

---

## English

### Overview

Bio-Forge is a synthetic biology AI platform based on a 120-agent matrix, providing intelligent support for biotechnology R&D from molecular design to process scale-up.

### Key Features

- **120 Agent Matrix**: Full-spectrum biotech R&D coverage
- **6-Layer Architecture**: From infrastructure to project-specific agents
- **RESTful API**: Complete agent management and task scheduling
- **Docker Ready**: One-command deployment

### Quick Start

```bash
# Clone and setup
git clone https://github.com/chinjaneking/Bio-Forge.git
cd Bio-Forge
cp .env.example .env

# Start with Docker
docker-compose up -d

# Run tests
python test_run.py
```

### Architecture

| Layer | Type | Count | Description |
|-------|------|-------|-------------|
| L1 | Infrastructure | 20 | Platform, Data, Security |
| L2 | Computational | 25 | Molecular modeling, Protein design |
| L3 | Experimental | 20 | Molecular biology, Analytics |
| L4 | Optimization | 20 | Yield, Stability, Scale-up |
| L5 | R&D Support | 20 | Literature, PM, QC |
| L6 | Project-Specific | 15 | Synasalid project agents |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/agents` | GET | List all agents |
| `/api/v1/agents/{id}` | GET | Get agent details |
| `/api/v1/tasks` | POST | Create task |

---

## License

Copyright 2026 Bio-Forge Project

## Contributing

欢迎提交 Issue 和 Pull Request。

---

<div align="center">

**Built with ❤️ for Synthetic Biology**

</div>
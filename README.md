# 🧬 Bio-Forge

> 智能体协调中枢与生物研发任务调度平台

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 简介

Bio-Forge 是一个基于 DeerFlow 2.0 框架构建的生物研发智能体协调平台，专为合成生物学、蛋白质工程、细胞工程等领域的研究团队设计。

### 核心特性

- 🤖 **120个智能体矩阵** - 覆盖基因组设计、蛋白质工程、细胞工程等生物研发全流程
- 📋 **智能任务调度** - 自动分配任务、状态跟踪、结果管理
- 🔌 **RESTful API** - 完整的智能体管理和任务调度接口
- 🐳 **Docker 部署** - 一键启动，开箱即用
- 📊 **可扩展架构** - 支持 PostgreSQL、Redis、Neo4j、MinIO 等扩展

---

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

```bash
# 1. 克隆/进入项目目录
cd bio-forge

# 2. 配置环境
cp .env.example .env

# 3. 构建并启动
docker-compose up -d --build

# 4. 验证部署
curl http://localhost:1983/health
# 响应: {"status":"healthy"}
```

### 方式二：本地部署

```bash
# 1. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境
cp .env.example .env

# 4. 启动服务
python -m app.main

# 5. 运行测试
python test_agents.py
python test_run.py
```

### 访问地址

| 端点 | 地址 | 说明 |
|------|------|------|
| API 文档 | http://localhost:1983/docs | Swagger UI |
| 健康检查 | http://localhost:1983/health | 服务状态 |
| 智能体列表 | http://localhost:1983/api/v1/agents | REST API |

---

## 📚 文档

- **[部署指南](./DEPLOYMENT.md)** - 详细的部署、配置和运维文档
- **API 文档** - http://localhost:1983/docs（服务启动后访问）

---

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Bio-Forge 架构                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ FastAPI     │  │ SQLAlchemy  │  │ Pydantic    │         │
│  │ (Web API)   │  │ (ORM)       │  │ (数据验证)   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│  ┌───────────────────────┴───────────────────────┐          │
│  │              Agent Manager (核心)              │          │
│  │  - 智能体注册、激活、停用                       │          │
│  │  - 任务分配、状态跟踪                          │          │
│  │  - 120个预定义智能体                          │          │
│  └───────────────────────┬───────────────────────┘          │
│                          │                                  │
│  ┌───────────────────────┴───────────────────────┐          │
│  │                 数据层                         │          │
│  │  SQLite (开发)  │  PostgreSQL (生产)          │          │
│  └────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 智能体列表

Bio-Forge 预设30个核心智能体，支持扩展至120个：

### 基础架构层

| 智能体 | 类型 | 描述 |
|--------|------|------|
| 研发总监助手 | R_D_ASSISTANT | 项目协调、决策支持 |
| 项目经理 | PROJECT_MANAGEMENT | 进度跟踪、资源管理 |
| 数据管理员 | DATA_MANAGEMENT | 数据存储、版本控制 |
| 安全监控员 | SECURITY_MONITORING | 系统安全、访问控制 |
| 团队协调员 | PLATFORM_MANAGEMENT | 跨团队沟通、信息同步 |

### 生命设计层

| 智能体 | 类型 | 描述 |
|--------|------|------|
| 基因组设计 | GENOME_DESIGN | 基因组合成、密码子优化 |
| 蛋白质设计 | PROTEIN_DESIGN | 结构预测、功能设计 |
| 细胞设计 | CELL_DESIGN | 细胞工程、信号通路 |
| 代谢通路设计 | PATHWAY_DESIGN | 代谢通路、酶选择 |

### 实验执行层

| 智能体 | 类型 | 描述 |
|--------|------|------|
| DNA合成 | DNA_SYNTHESIS | 合成计划、拼接策略 |
| 细胞组装 | CELL_ASSEMBLY | DNA组装、转化策略 |
| 发酵优化智能体 | CULTURE_OPTIMIZATION | 发酵参数、放大生产 |
| 分析方法开发 | ASSAY_VALIDATION | HPLC/LC-MS方法开发 |

### 进化优化层

| 智能体 | 类型 | 描述 |
|--------|------|------|
| 适应性进化 | ADAPTIVE_EVOLUTION | 进化策略、压力设计 |
| 定向进化 | DIRECTED_EVOLUTION | 突变文库、筛选方案 |
| 功能优化 | FUNCTION_OPTIMIZATION | 多目标优化、性能评估 |
| 稳定性增强 | STABILITY_ENHANCEMENT | 蛋白稳定、遗传稳定 |

### 研发管理类

| 智能体 | 类型 | 描述 |
|--------|------|------|
| 文献调研 | LITERATURE_RESEARCH | 文献检索、趋势分析 |
| 实验设计 | EXPERIMENT_DESIGN | DOE设计、方案优化 |
| 数据分析 | DATA_ANALYSIS | 统计分析、数据可视化 |
| 生物信息学 | BIOINFORMATICS | 基因组分析、序列比对 |
| 化学信息学 | CHEMINFORMATICS | 化合物管理、虚拟筛选 |
| 统计建模 | STATISTICAL_MODELING | 回归分析、预测建模 |
| 专利调研 | PATENT_RESEARCH | 专利检索、侵权分析 |
| 注册事务智能体 | REGULATORY_AFFAIRS | self-GRAS认证、法规研究 |
| 质量控制 | QUALITY_CONTROL | 质量标准、偏差处理 |

### 项目专项类

| 智能体 | 类型 | 描述 |
|--------|------|------|
| 红景天苷项目专项 | RHODIOLA_PROJECT | 发酵工艺、中试放大 |

---

## 🔧 API 使用示例

### 创建智能体

```bash
curl -X POST "http://localhost:1983/api/v1/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "新型智能体",
    "description": "智能体描述",
    "agent_type": "design",
    "priority": 5,
    "capabilities": ["能力1", "能力2"]
  }'
```

### 列出智能体

```bash
curl "http://localhost:1983/api/v1/agents?status=active"
```

### 创建任务

```bash
curl -X POST "http://localhost:1983/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试任务",
    "agent_id": 1,
    "input_data": {"param": "value"}
  }'
```

---

## 📁 项目结构

```
bio-forge/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── agent_manager.py     # 智能体管理核心
│   ├── task_scheduler.py    # 任务调度器
│   ├── models/              # 数据模型
│   │   ├── agent.py
│   │   └── task.py
│   └── api/                 # API 路由
│       ├── agents.py
│       └── tasks.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── DEPLOYMENT.md            # 部署指南
└── README.md
```

---

## 🧪 测试

```bash
# 运行智能体初始化测试
python test_agents.py

# 运行完整功能测试
python test_run.py

# Docker 环境测试
docker exec bio-forge python test_agents.py
docker exec bio-forge python test_run.py
```

---

## 📋 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DATABASE_URL` | `sqlite:///./deerflow.db` | 数据库连接 |
| `APP_ENV` | `development` | 环境 |
| `APP_PORT` | `1983` | 服务端口 |
| `MAX_AGENTS` | `120` | 最大智能体数 |

完整配置见 [DEPLOYMENT.md](./DEPLOYMENT.md#4-详细配置)

---

## 📜 License

MIT License

---

## 📞 支持

- 📖 [部署文档](./DEPLOYMENT.md)
- 🐛 [问题反馈](https://github.com/your-repo/bio-forge/issues)
- 💬 [讨论区](https://github.com/your-repo/bio-forge/discussions)

---

**基于 DeerFlow 2.0 框架构建**
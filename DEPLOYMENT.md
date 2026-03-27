# 🧬 Bio-Forge 部署指南

> 智能体协调中枢与生物研发任务调度平台 - 独立部署文档

---

## 目录

1. [项目概述](#1-项目概述)
2. [系统要求](#2-系统要求)
3. [快速部署](#3-快速部署)
4. [详细配置](#4-详细配置)
5. [生产环境部署](#5-生产环境部署)
6. [API 文档](#6-api-文档)
7. [运维指南](#7-运维指南)
8. [故障排除](#8-故障排除)

---

## 1. 项目概述

### 1.1 简介

Bio-Forge 是基于 DeerFlow 2.0 框架构建的生物研发智能体协调平台，提供：

- **120个智能体矩阵**：覆盖基因组设计、蛋白质工程、细胞工程等生物研发全流程
- **任务调度系统**：智能分配、状态跟踪、结果管理
- **RESTful API**：完整的智能体管理和任务调度接口

### 1.2 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| Web框架 | FastAPI | ≥0.109.0 |
| ORM | SQLAlchemy | ≥2.0.0 |
| 数据验证 | Pydantic | ≥2.0.0 |
| ASGI服务器 | Uvicorn | ≥0.27.0 |
| 数据库 | SQLite / PostgreSQL | - |
| 容器化 | Docker | ≥20.10 |

### 1.3 项目结构

```
bio-forge/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── agent_manager.py     # 智能体管理核心
│   ├── task_scheduler.py    # 任务调度器
│   ├── redis_client.py      # Redis 客户端（可选）
│   ├── models/
│   │   ├── agent.py         # 智能体模型
│   │   └── task.py          # 任务模型
│   └── api/
│       ├── agents.py        # 智能体 API
│       └── tasks.py         # 任务 API
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── start.sh                # Linux/Mac 启动脚本
├── test_docker.bat         # Windows Docker 测试
├── test_local.bat          # Windows 本地测试
├── test_agents.py          # 智能体测试
├── test_run.py             # 运行测试
├── simple_start.py         # 简单启动脚本
└── README.md
```

---

## 2. 系统要求

### 2.1 开发环境

| 要求 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 2核 | 4核+ |
| 内存 | 2GB | 4GB+ |
| 磁盘 | 500MB | 1GB+ |
| Python | 3.10+ | 3.12+ |
| Docker | 20.10+ | 24.0+ |

### 2.2 生产环境

| 要求 | 配置 |
|------|------|
| CPU | 4核+ |
| 内存 | 8GB+ |
| 磁盘 | 10GB+ SSD |
| 数据库 | PostgreSQL 14+ |
| 缓存 | Redis 7+ |

---

## 3. 快速部署

### 3.1 Docker 部署（推荐）

#### Windows 环境

```batch
:: 1. 进入项目目录
cd bio-forge

:: 2. 创建环境配置（使用 SQLite）
copy .env.example .env

:: 3. 构建并启动
docker-compose up -d --build

:: 4. 检查状态
docker-compose ps

:: 5. 查看日志
docker-compose logs -f

:: 6. 运行测试
docker exec bio-forge python test_agents.py
docker exec bio-forge python test_run.py
```

#### Linux/Mac 环境

```bash
# 1. 进入项目目录
cd bio-forge

# 2. 创建环境配置
cp .env.example .env

# 3. 构建并启动
docker-compose up -d --build

# 4. 检查状态
docker-compose ps

# 5. 查看日志
docker-compose logs -f
```

### 3.2 本地部署

#### Windows 环境

```batch
:: 1. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

:: 2. 安装依赖
pip install -r requirements.txt

:: 3. 配置环境
copy .env.example .env

:: 4. 启动服务
python -m app.main

:: 5. 运行测试
python test_agents.py
python test_run.py
```

#### Linux/Mac 环境

```bash
# 1. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境
cp .env.example .env

# 4. 启动服务（快速启动）
chmod +x start.sh
./start.sh

# 或手动启动
python -m app.main
```

### 3.3 验证部署

```bash
# 健康检查
curl http://localhost:1983/health
# 响应: {"status":"healthy"}

# 智能体列表
curl http://localhost:1983/api/v1/agents

# API 文档
# 浏览器访问: http://localhost:1983/docs
```

---

## 4. 详细配置

### 4.1 环境变量

创建 `.env` 文件（从 `.env.example` 复制）：

```env
# =====================
# 应用配置
# =====================
APP_NAME=Bio-Forge
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:1983
API_PREFIX=/api/v1

# =====================
# 数据库配置
# =====================
# SQLite（开发环境推荐）
DATABASE_URL=sqlite:///./deerflow.db

# PostgreSQL（生产环境推荐）
# DATABASE_URL=postgresql://user:password@localhost:5432/bioforge

# =====================
# Redis 配置（可选）
# =====================
REDIS_URL=redis://localhost:6379/0

# =====================
# Neo4j 配置（可选）
# =====================
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# =====================
# MinIO 配置（可选）
# =====================
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_USE_SSL=false

# =====================
# 任务队列配置
# =====================
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# =====================
# 安全配置
# =====================
SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# =====================
# 智能体配置
# =====================
MAX_AGENTS=120
DEFAULT_AGENT_TIMEOUT=3600
TASK_QUEUE_SIZE=10000
```

### 4.2 端口配置

修改 `docker-compose.yml` 更改端口：

```yaml
services:
  bio-forge:
    ports:
      - "你的端口:8000"  # 默认 1983:8000
```

### 4.3 数据库配置

#### SQLite（默认，零配置）

```env
DATABASE_URL=sqlite:///./deerflow.db
```

#### PostgreSQL（生产环境）

1. 添加 PostgreSQL 服务到 `docker-compose.yml`：

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: bioforge
      POSTGRES_PASSWORD: bioforge123
      POSTGRES_DB: bioforge
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

2. 更新 `.env`：

```env
DATABASE_URL=postgresql://bioforge:bioforge123@postgres:5432/bioforge
```

3. 添加依赖到 `requirements.txt`：

```
psycopg2-binary>=2.9.0
```

---

## 5. 生产环境部署

### 5.1 Docker Compose 生产配置

创建 `docker-compose.prod.yml`：

```yaml
version: '3.8'

services:
  bio-forge:
    build: .
    container_name: bio-forge-prod
    restart: always
    ports:
      - "1983:8000"
    environment:
      - APP_ENV=production
      - APP_DEBUG=false
    env_file:
      - .env.prod
    volumes:
      - ./data:/app/data
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: bioforge
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - bio-forge

volumes:
  postgres_data:
  redis_data:
```

### 5.2 Nginx 反向代理配置

创建 `nginx.conf`：

```nginx
events {
    worker_connections 1024;
}

http {
    upstream bioforge {
        server bio-forge:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/certs/cert.pem;
        ssl_certificate_key /etc/nginx/certs/key.pem;

        location / {
            proxy_pass http://bioforge;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://bioforge/health;
            access_log off;
        }
    }
}
```

### 5.3 启动生产环境

```bash
# 创建生产环境配置
cp .env.example .env.prod

# 编辑生产配置
nano .env.prod  # 修改 SECRET_KEY、数据库密码等

# 启动服务
docker-compose -f docker-compose.prod.yml up -d

# 查看状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 6. API 文档

### 6.1 智能体管理 API

#### 创建智能体

```http
POST /api/v1/agents
Content-Type: application/json

{
  "name": "新型智能体",
  "description": "智能体描述",
  "agent_type": "design",
  "priority": 5,
  "capabilities": ["能力1", "能力2"],
  "config": {"key": "value"}
}
```

#### 列出智能体

```http
GET /api/v1/agents?agent_type=design&status=active&skip=0&limit=100
```

#### 获取智能体详情

```http
GET /api/v1/agents/{agent_id}
```

#### 激活/停用智能体

```http
PUT /api/v1/agents/{agent_id}/activate
PUT /api/v1/agents/{agent_id}/deactivate
```

#### 删除智能体

```http
DELETE /api/v1/agents/{agent_id}
```

### 6.2 任务管理 API

#### 创建任务

```http
POST /api/v1/tasks
Content-Type: application/json

{
  "name": "任务名称",
  "agent_id": 1,
  "input_data": {"param": "value"},
  "priority": 5
}
```

#### 查询任务

```http
GET /api/v1/tasks?status=pending&skip=0&limit=100
GET /api/v1/tasks/{task_id}
```

### 6.3 健康检查

```http
GET /health
响应: {"status": "healthy"}
```

---

## 7. 运维指南

### 7.1 常用命令

```bash
# 查看容器状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 进入容器
docker exec -it bio-forge /bin/bash

# 备份数据库（SQLite）
cp data/deerflow.db backups/deerflow_$(date +%Y%m%d).db

# 备份数据库（PostgreSQL）
docker exec postgres pg_dump -U bioforge bioforge > backup.sql
```

### 7.2 日志管理

```bash
# 查看最近100行日志
docker-compose logs --tail=100

# 导出日志到文件
docker-compose logs > logs_$(date +%Y%m%d).log

# 实时监控错误
docker-compose logs -f | grep -i error
```

### 7.3 数据备份策略

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/bioforge"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份 SQLite 数据库
cp data/deerflow.db $BACKUP_DIR/deerflow_$DATE.db

# 备份配置文件
cp .env $BACKUP_DIR/env_$DATE.bak

# 删除7天前的备份
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.bak" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### 7.4 监控指标

关键监控指标：

| 指标 | 描述 | 告警阈值 |
|------|------|----------|
| 内存使用 | 容器内存占用 | >80% |
| CPU使用 | 容器CPU占用 | >70% |
| 磁盘空间 | 数据存储空间 | <20% 剩余 |
| 响应时间 | API响应延迟 | >500ms |
| 错误率 | HTTP 5xx比例 | >1% |
| 智能体数量 | 活跃智能体数 | <1或>120 |

---

## 8. 故障排除

### 8.1 常见问题

#### 问题1：容器启动失败

**症状**：
```
Container bio-forge Restarting (1)
```

**检查步骤**：
```bash
# 查看错误日志
docker logs bio-forge --tail 50

# 常见原因：
# 1. 数据库连接失败 - 检查 DATABASE_URL
# 2. 端口被占用 - 更改端口映射
# 3. 依赖未安装 - 检查 requirements.txt
```

#### 问题2：API 返回 500 错误

**症状**：
```json
{"detail": "Internal Server Error"}
```

**检查步骤**：
```bash
# 1. 查看详细日志
docker-compose logs -f

# 2. 检查数据库连接
docker exec bio-forge python -c "from app.database import engine; print(engine.url)"

# 3. 检查数据类型问题（常见）
# 确保 datetime 字段使用 datetime 对象而非 time.time()
```

#### 问题3：智能体初始化失败

**症状**：
```
Expected 120 agents, got 0
```

**解决方案**：
```bash
# 1. 重置数据库
docker-compose down
rm -f deerflow.db
docker-compose up -d --build

# 2. 或手动初始化
docker exec bio-forge python -c "from app.main import init_db; init_db()"
```

#### 问题4：端口冲突

**症状**：
```
Error: bind: address already in use
```

**解决方案**：
```bash
# Windows - 查找占用端口的进程
netstat -ano | findstr :1983
taskkill /PID <进程ID> /F

# Linux/Mac
lsof -i :1983
kill -9 <PID>

# 或更改端口
# 修改 docker-compose.yml 中的端口映射
```

### 8.2 数据恢复

```bash
# 恢复 SQLite 数据库
cp backups/deerflow_20240327.db data/deerflow.db
docker-compose restart

# 恢复 PostgreSQL 数据库
docker exec -i postgres psql -U bioforge bioforge < backup.sql
```

### 8.3 重置环境

```bash
# 完全重置（删除所有数据）
docker-compose down -v
rm -rf deerflow.db data/
docker-compose up -d --build

# 重新初始化智能体
docker exec bio-forge python test_agents.py
```

---

## 附录

### A. 智能体类型列表

Bio-Forge 预设30个智能体，分为以下类别：

| 类型 | 数量 | 描述 |
|------|------|------|
| 研发总监助手 | 1 | 项目协调、决策支持 |
| 项目管理 | 1 | 进度跟踪、资源管理 |
| 数据管理 | 1 | 数据存储、版本控制 |
| 安全监控 | 1 | 系统安全、访问控制 |
| 平台管理 | 1 | 系统架构、集成管理 |
| 基因组设计 | 1 | 基因组合成、密码子优化 |
| 蛋白质设计 | 1 | 结构预测、功能设计 |
| 细胞设计 | 1 | 细胞工程、信号通路 |
| 通路设计 | 1 | 代谢通路、酶选择 |
| 代谢工程 | 1 | 菌株改造、通路优化 |
| DNA合成 | 1 | 合成计划、拼接策略 |
| 细胞组装 | 1 | DNA组装、转化策略 |
| 培养优化 | 1 | 发酵参数、放大生产 |
| 分析验证 | 1 | 方法开发、质量标准 |
| 实验室自动化 | 1 | 流程自动化、设备集成 |
| 适应性进化 | 1 | 进化策略、压力设计 |
| 定向进化 | 1 | 突变文库、筛选方案 |
| 功能优化 | 1 | 多目标优化、性能评估 |
| 稳定性增强 | 1 | 蛋白稳定、遗传稳定 |
| 文献调研 | 1 | 文献检索、趋势分析 |
| 实验设计 | 1 | DOE设计、方案优化 |
| 数据分析 | 1 | 统计分析、数据可视化 |
| 生物信息学 | 1 | 基因组分析、序列比对 |
| 化学信息学 | 1 | 化合物管理、虚拟筛选 |
| 统计建模 | 1 | 回归分析、预测建模 |
| 专利调研 | 1 | 专利检索、侵权分析 |
| 注册事务 | 1 | self-GRAS认证、法规研究 |
| 质量控制 | 1 | 质量标准、偏差处理 |
| Synasalid项目专项 | 1 | 发酵工艺、中试放大 |
| 执行类 | 1 | 物料采购、成本控制 |

### B. 环境变量完整列表

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| APP_NAME | Bio-Forge | 应用名称 |
| APP_ENV | development | 环境（development/production） |
| APP_DEBUG | true | 调试模式 |
| APP_URL | http://localhost:1983 | 应用URL |
| API_PREFIX | /api/v1 | API前缀 |
| DATABASE_URL | sqlite:///./deerflow.db | 数据库连接 |
| REDIS_URL | redis://localhost:6379/0 | Redis连接 |
| NEO4J_URI | bolt://localhost:7687 | Neo4j连接 |
| MINIO_ENDPOINT | localhost:9000 | MinIO端点 |
| SECRET_KEY | - | JWT密钥（必须修改） |
| JWT_ALGORITHM | HS256 | JWT算法 |
| JWT_EXPIRE_MINUTES | 1440 | Token过期时间 |
| MAX_AGENTS | 120 | 最大智能体数 |
| DEFAULT_AGENT_TIMEOUT | 3600 | 默认超时（秒） |
| TASK_QUEUE_SIZE | 10000 | 任务队列大小 |

### C. 相关链接

- **FastAPI 文档**: https://fastapi.tiangolo.com/
- **SQLAlchemy 文档**: https://docs.sqlalchemy.org/
- **Docker 文档**: https://docs.docker.com/
- **项目仓库**: （待添加）

---

## 联系支持

如遇问题，请提供以下信息：

1. 错误日志（`docker-compose logs --tail=100`）
2. 环境信息（Python版本、操作系统、Docker版本）
3. 复现步骤
4. 预期行为 vs 实际行为

---

**文档版本**: 1.0.0
**最后更新**: 2026-03-27
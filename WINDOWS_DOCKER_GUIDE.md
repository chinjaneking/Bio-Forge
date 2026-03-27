
# Bio-Forge Windows Docker 部署说明书

## 文档信息

| 项目 | 内容 |
|------|------|
| **文档名称** | Bio-Forge Windows Docker 部署说明书 |
| **版本** | v2.0 |
| **日期** | 2026-03-27 |
| **适用平台** | Windows 10/11 (WSL 2) |
| **服务端口** | 1983 |
| **容器名称** | bio-forge |

---

## 目录

1. [前置准备](#1-前置准备)
2. [环境检查](#2-环境检查)
3. [文件准备](#3-文件准备)
4. [部署步骤](#4-部署步骤)
5. [验证部署](#5-验证部署)
6. [常见问题](#6-常见问题)
7. [运维管理](#7-运维管理)

---

## 1. 前置准备

### 1.1 系统要求

| 资源 | 最低要求 | 推荐配置 |
|------|----------|----------|
| **操作系统** | Windows 10 21H2+ 或 Windows 11 | Windows 11 23H2+ |
| **内存** | 4GB | 8GB+ |
| **磁盘空间** | 10GB | 20GB+ |
| **WSL版本** | WSL 2 | WSL 2 (最新) |

### 1.2 软件安装

#### 1.2.1 安装 Docker Desktop for Windows

1. 访问 Docker 官网: https://www.docker.com/products/docker-desktop/
2. 下载 Windows 版本安装包
3. 运行安装程序，确保勾选 "Use WSL 2 instead of Hyper-V"
4. 安装完成后重启电脑
5. 启动 Docker Desktop，等待 Docker Engine 启动完成

#### 1.2.2 验证 WSL 2

打开 PowerShell 或命令提示符，执行:

```powershell
wsl --status
```

如果显示 WSL 2 未安装，执行:

```powershell
wsl --install
```

然后重启电脑。

---

## 2. 环境检查

### 2.1 检查 Docker 状态

打开 PowerShell，执行:

```powershell
docker --version
docker-compose --version
```

预期输出示例:
```
Docker version 26.0.0, build 2ae903e
Docker Compose version v2.24.6
```

### 2.2 检查 Docker 运行状态

```powershell
docker info
```

如果显示 "Server: Docker Desktop" 说明 Docker 正常运行。

### 2.3 检查端口占用

确保 1983 端口未被占用:

```powershell
netstat -ano | findstr :1983
```

如果有输出，说明端口被占用，需要关闭相关程序或修改端口配置。

---

## 3. 文件准备

### 3.1 创建项目目录

在 C 盘根目录创建 bio-forge 文件夹:

```powershell
# 创建目录
mkdir C:\bio-forge

# 进入目录
cd C:\bio-forge
```

### 3.2 复制项目文件

将以下文件从项目源目录复制到 `C:\bio-forge`:

```
C:\bio-forge\
├── app/                      # 应用代码目录
│   ├── __init__.py
│   ├── main.py               # 主应用入口
│   ├── config.py             # 配置文件
│   ├── database.py           # 数据库管理
│   ├── agent_manager.py      # 智能体管理器
│   ├── task_scheduler.py     # 任务调度器
│   ├── redis_client.py       # Redis客户端
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── task.py
│   └── api/                  # API路由
│       ├── __init__.py
│       ├── agents.py
│       └── tasks.py
├── Dockerfile                 # Docker镜像构建文件
├── docker-compose.yml         # Docker Compose配置
├── requirements.txt           # Python依赖
├── README.md                  # 项目说明
├── DEPLOYMENT.md              # 详细部署文档
└── WINDOWS_DOCKER_GUIDE.md   # 本文档
```

### 3.3 验证文件完整性

在 PowerShell 中执行:

```powershell
cd C:\bio-forge
dir
```

确认所有文件都已正确复制。

---

## 4. 部署步骤

### 4.1 步骤一: 启动 Docker Desktop

确保 Docker Desktop 正在运行，系统托盘中应该能看到 Docker 图标且状态为 "Running"。

### 4.2 步骤二: 进入项目目录

```powershell
cd C:\bio-forge
```

### 4.3 步骤三: 构建并启动容器

```powershell
docker-compose up -d --build
```

**注意**: 
- 首次构建可能需要 5-15 分钟，取决于网络速度
- 过程中会下载 Python 基础镜像和依赖包
- 请保持网络连接稳定

### 4.4 步骤四: 查看构建日志

如果想查看详细构建过程，可以不加 `-d` 参数:

```powershell
docker-compose up --build
```

按 `Ctrl+C` 可以停止，然后用 `docker-compose up -d` 后台运行。

---

## 5. 验证部署

### 5.1 检查容器状态

```powershell
docker ps
```

预期输出应该包含:
```
CONTAINER ID   IMAGE           COMMAND       CREATED         STATUS         PORTS                    NAMES
xxxxxxxxxxxx   bio-forge       "python -m…"  x seconds ago   Up x seconds   0.0.0.0:1983->1983/tcp  bio-forge
```

### 5.2 查看容器日志

```powershell
docker logs bio-forge
```

预期输出应该包含:
```
🚀 启动 Bio-Forge - AI创造新生命智能体平台...
已初始化 120 个智能体
✅ Bio-Forge 启动成功!
```

### 5.3 浏览器访问验证

打开浏览器，依次访问:

| 测试项 | URL | 预期结果 |
|--------|-----|----------|
| **根路径** | http://localhost:1983 | 显示 Bio-Forge 版本和状态信息 |
| **健康检查** | http://localhost:1983/health | 显示 `{"status": "healthy"}` |
| **API文档** | http://localhost:1983/docs | 显示 Swagger API 文档界面 |
| **系统状态** | http://localhost:1983/api/v1/status | 显示系统状态和智能体数量 |

### 5.4 API 接口测试

在 PowerShell 中执行:

```powershell
# 测试健康检查
curl http://localhost:1983/health

# 测试获取智能体列表
curl http://localhost:1983/api/v1/agents
```

或者使用 API 文档页面 (http://localhost:1983/docs) 进行交互式测试。

---

## 6. 常见问题

### 6.1 端口被占用

**问题**: `Bind for 0.0.0.0:1983 failed: port is already allocated`

**解决方案**:
1. 查找占用端口的程序:
   ```powershell
   netstat -ano | findstr :1983
   ```
2. 结束该进程或修改 docker-compose.yml 中的端口映射

### 6.2 Docker 未运行

**问题**: `Cannot connect to the Docker daemon`

**解决方案**:
1. 启动 Docker Desktop
2. 等待 Docker Engine 完全启动（图标变为绿色）

### 6.3 文件复制问题

**问题**: C:\bio-forge 目录为空或文件缺失

**解决方案**:
1. 确认已从正确位置复制所有文件
2. 检查文件权限
3. 重新复制所有项目文件到 C:\bio-forge

### 6.4 构建失败

**问题**: docker-compose build 过程中出现错误

**解决方案**:
1. 检查网络连接
2. 清理 Docker 缓存:
   ```powershell
   docker system prune -a
   ```
3. 重新构建

### 6.5 容器启动后立即退出

**问题**: 容器状态显示 "Exited"

**解决方案**:
1. 查看日志:
   ```powershell
   docker logs bio-forge
   ```
2. 根据错误信息排查问题
3. 检查 docker-compose.yml 配置

---

## 7. 运维管理

### 7.1 常用命令

| 操作 | 命令 |
|------|------|
| **启动服务** | `docker-compose up -d` |
| **停止服务** | `docker-compose down` |
| **重启服务** | `docker-compose restart` |
| **查看日志** | `docker logs bio-forge` |
| **实时日志** | `docker logs -f bio-forge` |
| **进入容器** | `docker exec -it bio-forge bash` |
| **查看状态** | `docker ps` |
| **查看所有容器** | `docker ps -a` |

### 7.2 数据备份

Bio-Forge 使用 SQLite 数据库，文件位于:
- 容器内: `/app/bio-forge.db`
- 宿主机: `C:\bio-forge\bio-forge.db`

**备份步骤**:
1. 停止容器: `docker-compose down`
2. 复制 `C:\bio-forge\bio-forge.db` 到备份位置
3. 重启容器: `docker-compose up -d`

### 7.3 更新部署

当代码更新时:

```powershell
cd C:\bio-forge
# 1. 停止旧容器
docker-compose down

# 2. 复制新文件到 C:\bio-forge

# 3. 重新构建并启动
docker-compose up -d --build
```

### 7.4 清理资源

如需完全清理并重新开始:

```powershell
cd C:\bio-forge

# 停止并删除容器
docker-compose down -v

# 删除镜像
docker rmi bio-forge

# （可选）清理 Docker 缓存
docker system prune -a
```

---

## 附录

### A. 目录结构参考

```
C:\bio-forge\
├── app/                      # 应用代码
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── agent_manager.py
│   ├── task_scheduler.py
│   ├── redis_client.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── task.py
│   └── api/
│       ├── __init__.py
│       ├── agents.py
│       └── tasks.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── DEPLOYMENT.md
├── WINDOWS_DOCKER_GUIDE.md
├── bio-forge.db             # 运行后生成的数据库文件
└── .env                      # （可选）环境变量文件
```

### B. 联系方式

- **技术支持**: chinjaneking
- **项目主页**: 参考 README.md
- **详细文档**: DEPLOYMENT.md

---

**文档版本**: v2.0 | **最后更新**: 2026-03-27

# 🚀 DeerFlow 2.0 Windows Docker 快速启动指南

## 前置条件

确保你的 Windows 系统已安装：
- ✅ Docker Desktop（已启动运行）
- ✅ PowerShell 或命令提示符（CMD）

---

## 快速启动（3步搞定）

### 第1步：进入项目目录
打开 PowerShell 或 CMD，进入 deerflow2 文件夹：
```powershell
cd C:\path\to\deerflow2
```

### 第2步：构建并启动 Docker 容器
```powershell
docker-compose up -d --build
```

### 第3步：访问系统
打开浏览器访问：
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **系统状态**: http://localhost:8000/api/v1/status

---

## 常用 Docker 命令

### 查看日志
```powershell
docker-compose logs -f
```

### 停止服务
```powershell
docker-compose down
```

### 重启服务
```powershell
docker-compose restart
```

### 查看容器状态
```powershell
docker-compose ps
```

### 进入容器（如需要）
```powershell
docker exec -it deerflow2 bash
```

---

## 数据持久化

- **数据库文件**: `deerflow.db` 会自动保存在当前目录
- **配置文件**: `.env`（可选）会被挂载到容器中

---

## 验证系统状态

在浏览器打开 http://localhost:8000/docs，你应该看到：
1. Swagger API 文档界面
2. 可以点击 "Try it out" 测试各个 API

### 测试示例：列出所有智能体
```powershell
curl http://localhost:8000/api/v1/agents
```

或者在浏览器直接访问：
http://localhost:8000/api/v1/agents

---

## 故障排查

### 端口被占用？
修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:8000"  # 将左边改为其他端口，如8080
```

### 重新构建镜像？
```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 查看详细日志？
```powershell
docker logs deerflow2
```

---

## 系统已包含的30个智能体

启动成功后，系统自动初始化30个智能体：

| 类别 | 数量 | 优先级1-2 |
|------|------|-----------|
| 核心管理 | 5个 | 研发总监助手、项目经理 |
| 红景天苷专项 | 5个 | 红景天苷项目、发酵优化、菌株工程、注册事务 |
| 研究分析 | 10个 | 文献调研、实验设计、数据分析 |
| 合成生物学设计 | 10个 | 代谢通路设计、基因组设计、蛋白质设计、细胞设计、定向进化等 |

---

## 下一步

系统启动成功后，你可以：
1. 在 API 文档页面浏览所有可用接口
2. 测试创建和调度任务
3. 继续添加更多智能体到120个
4. 接入红景天苷项目实际数据

需要帮助？随时查看日志或重启服务！

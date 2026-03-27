# Bio-Forge Windows Docker 部署指南

## 系统要求

- Windows 10/11 (64-bit)
- Docker Desktop 4.0+
- 内存: 8GB+ (推荐 16GB)
- 磁盘空间: 10GB+

## 快速部署

### 1. 解压项目

将 `Bio-Forge-Deploy.zip` 解压到目标目录，例如 `C:\bio-forge`。

### 2. 启动 Docker Desktop

确保 Docker Desktop 正在运行。

### 3. 部署服务

打开 PowerShell 或 CMD，进入项目目录：

```powershell
cd C:\bio-forge
docker-compose up -d
```

### 4. 验证部署

访问 http://localhost:1983/docs 查看 API 文档。

## 常用命令

```powershell
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f bio-forge

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 更新镜像
docker-compose pull && docker-compose up -d
```

## 故障排除

### 端口被占用

如果 1983 端口被占用，修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8080:1983"  # 改为其他端口
```

### 内存不足

在 Docker Desktop 设置中增加内存限制：
Settings > Resources > Memory

### 数据库权限错误

确保数据目录有正确权限：

```powershell
# Windows PowerShell (管理员)
icacls C:\bio-forge\data /grant Everyone:F
```

## 配置说明

环境变量可在 `.env` 文件中配置：

```env
# 端口配置
PORT=1983

# 数据库
DATABASE_URL=sqlite:///data/bio-forge.db

# Redis
REDIS_URL=redis://redis:6379/0

# AI API Keys (可选)
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

## 支持

- 项目文档: http://localhost:1983/docs
- API 端点: http://localhost:1983/api/v1
- 健康检查: http://localhost:1983/health

---

**Bio-Forge** - Genesis-2026 | 120 Agents | 6 Layers

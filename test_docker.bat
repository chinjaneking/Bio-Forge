@echo off
REM Bio-Forge Docker Test Runner for Windows
REM location: bio-forge project directory

setlocal enabledelayedexpansion

echo ========================================
echo   Bio-Forge Docker Test Runner
echo ========================================
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check Docker
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Docker is not installed or not in PATH.
    echo Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker daemon is running
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Docker daemon is not running.
    echo Please start Docker Desktop.
    pause
    exit /b 1
)

echo [1/5] Checking Docker environment...
echo       Docker is ready.
echo.

REM Check if container exists
docker ps -a --filter "name=bio-forge" --format "{{.Names}}" | findstr bio-forge >nul
if %ERRORLEVEL% equ 0 (
    echo [2/5] Found existing container, stopping...
    docker-compose down
    echo       Container stopped.
) else (
    echo [2/5] No existing container found.
)

echo.
echo [3/5] Building Docker image...
docker-compose build --no-cache
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to build Docker image.
    pause
    exit /b 1
)
echo       Build complete.
echo.

echo [4/5] Starting container...
docker-compose up -d
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to start container.
    pause
    exit /b 1
)
echo       Container started.
echo.

echo [5/5] Running tests inside container...
echo.
echo ========================================
echo   Running test_agents.py
echo ========================================
docker exec bio-forge python test_agents.py
echo.

echo ========================================
echo   Running test_run.py
echo ========================================
docker exec bio-forge python test_run.py
echo.

echo ========================================
echo   Simple Start Test
echo ========================================
docker exec bio-forge python simple_start.py
echo.

echo ========================================
echo   Test Complete!
echo ========================================
echo.
echo.
echo ========================================
echo   Bio-Forge 服务已启动!
echo ========================================
echo.
echo   访问地址:
echo   - API 文档:    http://localhost:1983/docs
echo   - 健康检查:    http://localhost:1983/health
echo   - 智能体列表:  http://localhost:1983/api/v1/agents
echo   - 系统状态:    http://localhost:1983/api/v1/status
echo.
echo.
echo View logs:  docker-compose logs -f
echo Stop:        docker-compose down
echo.

pause
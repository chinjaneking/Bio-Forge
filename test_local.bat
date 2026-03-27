@echo off
REM Bio-Forge Local Test Runner for Windows
REM Usage: test_local.bat

setlocal enabledelayedexpansion

echo ========================================
echo   Bio-Forge Local Test Runner
echo ========================================
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Check if venv exists
if not exist ".venv" (
    echo [1/4] Creating virtual environment...
    python -m venv .venv
    echo       Created.
) else (
    echo [1/4] Virtual environment already exists.
)

echo.
echo [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [3/4] Installing dependencies...
pip install -r requirements.txt -q
echo       Dependencies installed.
echo.

echo [4/4] Running tests...
echo.
echo ========================================
echo   Running test_agents.py
echo ========================================
python test_agents.py
echo.

echo ========================================
echo   Running test_run.py
echo ========================================
python test_run.py
echo.

echo ========================================
echo   Simple Start Test
echo ========================================
python simple_start.py
echo.

echo ========================================
echo   Test Complete!
echo ========================================
echo.
echo To start the API server, run:
echo   .venv\Scripts\activate.bat
echo   python -m app.main
echo.
echo Then access: http://localhost:8000/docs
echo.

pause
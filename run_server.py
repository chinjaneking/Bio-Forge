#!/usr/bin/env python3
"""
Bio-Forge 启动脚本
一键启动 Bio-Forge API 服务和 Web 界面
"""

import os
import sys
import webbrowser
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("🧬 Bio-Forge 启动中...")
    print("=" * 60)
    
    # 设置环境变量
    env = os.environ.copy()
    env["DEER_FLOW_HOME"] = "C:/Bio-Forge/data/deerflow"
    env["ANTHROPIC_API_KEY"] = "79a65e78d55f43deae2a80b4b42dd78a.ZTnTFAO9zRoiNNVu"
    env["OPENAI_API_KEY"] = "79a65e78d55f43deae2a80b4b42dd78a.ZTnTFAO9zRoiNNVu"
    env["DEEPSEEK_API_KEY"] = "79a65e78d55f43deae2a80b4b42dd78a.ZTnTFAO9zRoiNNVu"
    
    # 切换到项目目录
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print(f"\n📁 项目目录: {project_dir}")
    print(f"🌐 服务地址: http://localhost:1983/")
    print(f"📖 API 文档: http://localhost:1983/docs")
    print(f"📊 Dashboard: 在浏览器中打开 http://localhost:1983/\n")
    
    # 打开浏览器
    print("正在打开浏览器...")
    webbrowser.open("http://localhost:1983/")
    
    # 启动服务
    print("=" * 60)
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "1983",
            "--reload"
        ], env=env)
    except KeyboardInterrupt:
        print("\n\n🛑 服务已停止")

if __name__ == "__main__":
    main()
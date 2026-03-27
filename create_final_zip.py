#!/usr/bin/env python3
"""
Bio-Forge 最终部署包生成脚本
创建干净的Windows Docker部署ZIP文件
"""

import os
import zipfile
from datetime import datetime


def create_deployment_zip():
    """创建部署ZIP文件"""
    # 项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 输出文件名
    zip_filename = f"Bio-Forge-Windows-Deploy-v1.0.zip"
    zip_path = os.path.join(project_root, zip_filename)
    
    # 要包含的文件和目录
    include_items = [
        "app/",
        "docker-compose.yml",
        "Dockerfile",
        "requirements.txt",
        "README.md",
        "WINDOWS_DOCKER_GUIDE.md",
        "check_agent_matrix.py",
    ]
    
    # 排除的文件模式
    exclude_patterns = [
        "__pycache__",
        ".pyc",
        ".pyo",
        ".log",
        ".swp",
        ".swo",
        ".bak",
        ".DS_Store",
        ".git",
        ".venv",
        "node_modules",
    ]
    
    print(f"📦 正在创建部署包: {zip_filename}")
    print("=" * 60)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        
        for item in include_items:
            item_path = os.path.join(project_root, item)
            
            if os.path.isfile(item_path):
                # 添加单个文件
                arcname = os.path.basename(item_path)
                zipf.write(item_path, arcname)
                file_count += 1
                print(f"  ✅ 添加文件: {arcname}")
            
            elif os.path.isdir(item_path):
                # 添加目录及其内容
                for root, dirs, files in os.walk(item_path):
                    # 检查是否需要排除当前目录
                    if any(pattern in root for pattern in exclude_patterns):
                        continue
                    
                    for file in files:
                        # 检查是否需要排除当前文件
                        if any(pattern in file for pattern in exclude_patterns):
                            continue
                        
                        file_path = os.path.join(root, file)
                        # 计算相对路径作为ZIP中的路径
                        arcname = os.path.relpath(file_path, project_root)
                        zipf.write(file_path, arcname)
                        file_count += 1
                
                print(f"  ✅ 添加目录: {item}")
    
    # 获取ZIP文件大小
    zip_size = os.path.getsize(zip_path) / 1024  # KB
    
    print("\n" + "=" * 60)
    print(f"✅ 部署包创建成功！")
    print(f"   📁 文件: {zip_filename}")
    print(f"   📊 包含: {file_count} 个文件")
    print(f"   📦 大小: {zip_size:.1f} KB")
    print(f"   📍 位置: {zip_path}")
    
    print("\n📋 部署包内容:")
    print("   - app/ (应用代码，含120个智能体)")
    print("   - docker-compose.yml (Docker编排配置)")
    print("   - Dockerfile (容器构建文件)")
    print("   - requirements.txt (Python依赖)")
    print("   - README.md (项目说明)")
    print("   - WINDOWS_DOCKER_GUIDE.md (Windows部署指南)")
    print("   - check_agent_matrix.py (验证脚本)")
    
    print("\n🚀 下一步:")
    print("   1. 将ZIP文件复制到Windows电脑")
    print("   2. 解压到 C:\\bio-forge")
    print("   3. 运行: docker-compose up -d")
    print("   4. 访问: http://localhost:1983/docs")
    
    return zip_path


if __name__ == "__main__":
    create_deployment_zip()

#!/usr/bin/env python3
"""
Bio-Forge 完整项目打包脚本
包含所有项目文件
"""

import os
import zipfile


def package_complete_project():
    """打包完整项目"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    zip_filename = "Bio-Forge-Complete-Project.zip"
    # 输出到项目外的目录
    output_dir = os.path.dirname(project_root)  # /mnt/user-data/outputs
    zip_path = os.path.join(output_dir, zip_filename)
    
    print(f"📦 正在打包完整Bio-Forge项目...")
    print("=" * 60)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        
        for root, dirs, files in os.walk(project_root):
            # 跳过一些临时目录
            if any(pattern in root for pattern in ['.git', '.venv', '__pycache__']):
                continue
                
            for file in files:
                # 排除临时文件和ZIP文件
                if any(file.endswith(ext) for ext in ['.pyc', '.pyo', '.log', '.swp', '.swo', '.bak', '.DS_Store', '.zip']):
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_root)
                zipf.write(file_path, arcname)
                file_count += 1
                print(f"  添加: {arcname}")
    
    zip_size = os.path.getsize(zip_path) / 1024
    
    print("\n" + "=" * 60)
    print(f"✅ 完整项目打包成功！")
    print(f"   📁 文件: {zip_filename}")
    print(f"   📊 包含: {file_count} 个文件")
    print(f"   📦 大小: {zip_size:.1f} KB")
    print(f"   📍 位置: {zip_path}")
    
    return zip_path


if __name__ == "__main__":
    package_complete_project()

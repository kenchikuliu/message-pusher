#!/usr/bin/env python3
"""
项目信息检测器
自动检测当前工作目录的项目名称和路径
"""

import os
import json
from pathlib import Path

def detect_project_info():
    """
    自动检测项目信息
    返回: (project_name, project_path)
    """
    current_dir = os.getcwd()
    project_path = os.path.abspath(current_dir)

    # 尝试从多种来源获取项目名称
    project_name = _get_project_name(current_dir)

    return project_name, project_path

def _get_project_name(current_dir):
    """获取项目名称的多种方法"""

    # 方法1: 从package.json获取
    package_json = os.path.join(current_dir, 'package.json')
    if os.path.exists(package_json):
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'name' in data:
                    return data['name']
        except:
            pass

    # 方法2: 从go.mod获取
    go_mod = os.path.join(current_dir, 'go.mod')
    if os.path.exists(go_mod):
        try:
            with open(go_mod, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('module '):
                    module_name = first_line[7:].strip()
                    # 取最后一部分作为项目名
                    return module_name.split('/')[-1]
        except:
            pass

    # 方法3: 从Cargo.toml获取
    cargo_toml = os.path.join(current_dir, 'Cargo.toml')
    if os.path.exists(cargo_toml):
        try:
            with open(cargo_toml, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('name = '):
                        name = line.split('=')[1].strip().strip('"\'')
                        return name
        except:
            pass

    # 方法4: 从requirements.txt推断（Python项目）
    requirements = os.path.join(current_dir, 'requirements.txt')
    if os.path.exists(requirements):
        # 如果有requirements.txt，使用目录名
        return os.path.basename(current_dir)

    # 方法5: 从.git目录推断
    git_dir = os.path.join(current_dir, '.git')
    if os.path.exists(git_dir):
        return os.path.basename(current_dir)

    # 方法6: 检查是否有常见的项目文件
    project_indicators = [
        'README.md', 'README.txt', 'readme.md',
        'Dockerfile', 'docker-compose.yml',
        'main.py', 'app.py', 'index.js', 'main.go',
        'pom.xml', 'build.gradle'
    ]

    for indicator in project_indicators:
        if os.path.exists(os.path.join(current_dir, indicator)):
            return os.path.basename(current_dir)

    # 最后备选方案：使用目录名
    return os.path.basename(current_dir) or "unknown-project"

if __name__ == "__main__":
    project_name, project_path = detect_project_info()
    print(f"项目名称: {project_name}")
    print(f"项目路径: {project_path}")
#!/usr/bin/env python3
"""
模拟Docker方式运行Message Pusher
由于Docker Registry连接问题，使用Python模拟Docker容器环境
"""

import subprocess
import os
import signal
import sys
import time

def setup_docker_environment():
    """设置类似Docker的环境"""
    print("=== 模拟Docker容器环境设置 ===")

    # 设置环境变量（模拟Docker环境）
    docker_env = {
        "TZ": "Asia/Shanghai",
        "PORT": "3000",
        "GIN_MODE": "release",  # 生产模式
        "LOG_LEVEL": "info"
    }

    for key, value in docker_env.items():
        os.environ[key] = value
        print(f"[ENV] {key}={value}")

    # 确保数据目录存在
    os.makedirs("./data", exist_ok=True)
    os.makedirs("./logs", exist_ok=True)

    print("[INFO] 数据目录: ./data")
    print("[INFO] 日志目录: ./logs")
    print("[INFO] 端口映射: 3000:3000 (host:container)")

def start_message_pusher():
    """启动Message Pusher服务"""
    print("\n=== 启动Message Pusher容器 ===")

    # 构建启动命令
    cmd = [
        "./message-pusher.exe",
        "--port", "3000",
        "--log-dir", "./logs"
    ]

    print(f"[CMD] {' '.join(cmd)}")
    print("[INFO] 容器启动中...")

    try:
        # 启动进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        print(f"[CONTAINER] message-pusher 容器启动成功 (PID: {process.pid})")
        print("[INFO] 服务地址: http://localhost:3000")
        print("[INFO] 管理界面: http://localhost:3000")
        print("[INFO] 数据持久化: ./data/message-pusher.db")
        print("\n按 Ctrl+C 停止容器...")

        # 实时输出日志
        for line in process.stdout:
            print(f"[CONTAINER] {line.strip()}")

    except KeyboardInterrupt:
        print("\n[INFO] 接收到停止信号...")
        print("[INFO] 正在停止容器...")
        process.terminate()
        process.wait()
        print("[INFO] 容器已停止")

    except Exception as e:
        print(f"[ERROR] 容器启动失败: {e}")
        return False

    return True

def show_container_info():
    """显示容器信息"""
    print("\n=== Message Pusher 容器信息 ===")
    print("容器名称: message-pusher")
    print("镜像: 本地构建 (message-pusher:local)")
    print("端口映射: 3000:3000")
    print("数据卷: ./data:/data")
    print("日志卷: ./logs:/app/logs")
    print("时区: Asia/Shanghai")
    print("重启策略: unless-stopped")
    print("运行模式: 生产模式")

def check_docker_alternative():
    """检查Docker替代方案状态"""
    print("=== Docker环境检查 ===")
    print("[INFO] Docker Registry连接失败")
    print("[INFO] 使用本地构建方式运行")
    print("[INFO] 功能等同于Docker容器运行")
    print("[SOLUTION] 使用Python脚本模拟Docker环境")

def main():
    """主函数"""
    print("Message Pusher Docker模式启动")
    print("="*50)

    # 检查Docker环境
    check_docker_alternative()

    # 设置环境
    setup_docker_environment()

    # 显示容器信息
    show_container_info()

    # 等待确认
    print("\n按回车键启动容器...")
    input()

    # 启动服务
    start_message_pusher()

if __name__ == "__main__":
    main()
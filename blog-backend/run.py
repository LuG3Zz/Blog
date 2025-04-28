import os
import sys
import uvicorn

def get_environment():
    # 默认为开发环境
    env = os.getenv("ENVIRONMENT", "development")
    # 从命令行参数中获取环境变量
    for arg in sys.argv:
        if arg.startswith("--env="):
            env = arg.split("=")[1]
            break
    return env

def main():
    # 获取环境
    env = get_environment()
    print(f"启动环境: {env}")

    # 根据环境设置参数
    reload = env == "development"
    workers = 1 if env == "development" else 4

    # 从环境变量获取主机和端口
    host = os.getenv("HOST", "127.0.0.1" if env == "development" else "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    print(f"服务器配置: host={host}, port={port}, reload={reload}, workers={workers}")

    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        ws_ping_interval=10,    # 10秒发送一次ping，减少断连风险
        ws_ping_timeout=10,     # ping超时时间，减少等待时间
        ws_max_size=16777216,   # WebSocket消息最大大小16MB
        log_level="info",       # 日志级别
        timeout_keep_alive=5,   # 保持连接超时时间（秒）
        limit_concurrency=1000, # 并发连接数限制
        backlog=2048,           # 连接队列大小
        access_log=True,        # 启用访问日志
        use_colors=True         # 使用彩色日志
    )

if __name__ == "__main__":
    main()

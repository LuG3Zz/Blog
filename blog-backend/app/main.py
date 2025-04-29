import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from datetime import datetime
import uvicorn

from app.utils.ip_utils import get_client_ip

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import routers
from app.utils.logging import get_logger
from app.services.unified_cache_service import UnifiedCacheService
from app.services.ip_location_service import IPLocationService
# 不再使用HTTP中间件记录访客
# from app.middleware import record_visitor

# Initialize logger
logger = get_logger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# 初始化缓存服务
view_count_cache_prefix = "view_count"

# 初始化 IP 地址归属地服务
IPLocationService.init_app()

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
    # 禁用自动重定向，避免与Nginx重定向冲突
    redirect_slashes=False
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=settings.STATIC_FILES_DIR), name="static")

# Configure CORS
if settings.IS_PRODUCTION:
    # 生产环境下限制跨域请求来源
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://brown1u.us.kg", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # 开发环境下允许所有来源
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add GZip compression middleware
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # 只压缩大于 1KB 的响应
)

# 不再使用HTTP中间件记录访客，改为使用WebSocket连接记录
# app.middleware("http")(record_visitor)


# Include all routers with API prefix
for router in routers:
    # 所有路由都使用API前缀
    app.include_router(router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint for API health check."""
    return {
        "message": "Blog API Service",
        "version": settings.PROJECT_VERSION,
        "status": "healthy"
    }

# 中间件：获取真实 IP
@app.middleware("http")
async def get_real_ip(request: Request, call_next):
    # 尝试从各种头部获取真实 IP
    x_client_ip = request.headers.get("X-Client-IP")
    x_real_ip = request.headers.get("X-Real-IP")
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    forwarded = request.headers.get("Forwarded")

    # 按优先级获取真实 IP
    if x_client_ip:
        real_ip = x_client_ip
    elif x_real_ip:
        real_ip = x_real_ip
    elif x_forwarded_for:
        # X-Forwarded-For 可能包含多个 IP，取第一个
        real_ip = x_forwarded_for.split(',')[0].strip()
    elif forwarded:
        # 解析 Forwarded 头部
        for part in forwarded.split(';'):
            if part.lower().startswith('for='):
                real_ip = part[4:].strip()
                # 移除可能的引号和 IPv6 括号
                real_ip = real_ip.strip('"[]')
                break
        else:
            real_ip = request.client.host
    else:
        real_ip = request.client.host

    # 将真实 IP 添加到请求状态中，以便在路由处理函数中使用
    request.state.real_ip = real_ip

    # 继续处理请求
    response = await call_next(request)
    return response

# IP 地址调试端点
@app.get("/debug/ip")
async def debug_ip(request: Request):
    """
    返回请求的 IP 地址信息，用于调试 IP 地址传递。
    """
    client_ip = get_client_ip(request)
    ip_location = IPLocationService.get_location(client_ip)

    return {
        "remote_addr": request.client.host,
        "x_client_ip": request.headers.get("X-Client-IP"),
        "x_real_ip": request.headers.get("X-Real-IP"),
        "x_forwarded_for": request.headers.get("X-Forwarded-For"),
        "forwarded": request.headers.get("Forwarded"),
        "real_ip": request.state.real_ip,  # 中间件中设置的真实 IP
        "client_ip": client_ip,  # 使用 get_client_ip 函数获取的客户端 IP
        "ip_location": ip_location  # IP 地址归属地
    }

# WebSocket 测试页面
@app.get("/websocket-test")
async def websocket_test():
    """
    返回 WebSocket 测试页面。
    """
    from fastapi.responses import FileResponse
    return FileResponse("app/static/websocket_test.html")


# Add middleware for view counting
@app.middleware("http")
async def add_view_count(request: Request, call_next):
    """Middleware to track article view counts."""
    # Process the request
    response = await call_next(request)

    # Only process successful GET requests
    if request.method == "GET" and response.status_code == 200:
        from app.services.article_service import ArticleService
        from app.core.database import get_db
        import re

        path = request.url.path

        # Match article detail page paths (with API prefix)
        api_prefix = settings.API_V1_STR
        article_id_match = re.match(f"{api_prefix}/articles/([0-9]+)$", path)
        article_slug_match = re.match(f"{api_prefix}/articles/by-slug/([\\w-]+)$", path)

        if article_id_match or article_slug_match:
            # Get visitor's real IP address
            client_ip = get_client_ip(request)

            # Get database session
            db = next(get_db())
            try:
                # Get article
                if article_id_match:
                    article_id = int(article_id_match.group(1))
                    article = ArticleService.get_article_by_id(db, article_id)
                else:
                    slug = article_slug_match.group(1)
                    article = ArticleService.get_article_by_slug(db, slug)

                if article:
                    # Create cache key
                    cache_key = f"{view_count_cache_prefix}:{article.id}:{client_ip}"
                    current_time = datetime.now().isoformat()

                    # Check if already viewed in the last 5 minutes
                    last_view_time = UnifiedCacheService.get(cache_key)

                    if last_view_time is None or \
                       (datetime.now() - datetime.fromisoformat(last_view_time)).total_seconds() > settings.VIEW_COUNT_CACHE_SECONDS:
                        # Update view count
                        ArticleService.increment_view_count(db, article.id)

                        # Update cache
                        UnifiedCacheService.set(cache_key, current_time, settings.VIEW_COUNT_CACHE_SECONDS)
            except Exception as e:
                logger.error(f"Error updating view count: {e}", exc_info=True)
            finally:
                db.close()

    return response

if __name__ == "__main__":
    # 根据环境设置参数
    host = "127.0.0.1" if settings.IS_DEVELOPMENT else "0.0.0.0"
    port = int(os.getenv("PORT", "8000"))
    reload = settings.IS_DEVELOPMENT
    workers = 1 if settings.IS_DEVELOPMENT else 4

    print(f"启动服务器: 环境={settings.ENVIRONMENT}, 主机={host}, 端口={port}, 热重载={reload}")

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
        backlog=2048            # 连接队列大小
    )

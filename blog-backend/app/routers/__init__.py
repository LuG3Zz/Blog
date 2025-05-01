# Export router modules
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.articles import router as articles_router
from app.routers.comments import router as comments_router
from app.routers.categories import router as categories_router
from app.routers.tags import router as tags_router
from app.routers.search import router as search_router
from app.routers.stats import router as stats_router
from app.routers.subscriptions import router as subscriptions_router
from app.routers.versions import router as versions_router
from app.routers.files import router as files_router
from app.routers.activities import router as activities_router
from app.routers.admin import router as admin_router
from app.routers.cache import router as cache_router
from app.routers.websocket import router as websocket_router
from app.routers.about import router as about_router
from app.routers.notification_history import router as notification_history_router
from app.routers.visitors import router as visitors_router
from app.routers.site_settings import router as site_settings_router
from app.routers.email_verification import router as email_verification_router
from app.routers.email_subscriptions import router as email_subscriptions_router

# List of all routers
routers = [
    auth_router,
    users_router,
    articles_router,
    comments_router,
    categories_router,
    tags_router,
    search_router,
    stats_router,
    subscriptions_router,
    versions_router,
    files_router,
    activities_router,
    admin_router,
    cache_router,
    websocket_router,
    about_router,
    notification_history_router,
    visitors_router,
    site_settings_router,
    email_verification_router,
    email_subscriptions_router,
]

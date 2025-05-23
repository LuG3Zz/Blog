from app.core.database import Base

# Import all models to make them available when importing from app.models
from app.models.user import User
from app.models.article import Article, Category, Tag
from app.models.comment import Comment
from app.models.activity import Activity
from app.models.subscription import Notification, EmailSubscription, SubscriptionType
from app.models.version import ArticleVersion
from app.models.about import AboutPage
from app.models.file import File
from app.models.notification_history import NotificationHistory
from app.models.visitor import Visitor
from app.models.site_settings import SiteSettings
from app.models.memo import Memo

# Export all models
__all__ = [
    "User",
    "Article",
    "Category",
    "Tag",
    "Comment",
    "Activity",
    "Notification",
    "EmailSubscription",
    "SubscriptionType",
    "ArticleVersion",
    "AboutPage",
    "File",
    "NotificationHistory",
    "Visitor",
    "SiteSettings",
    "Memo",
]

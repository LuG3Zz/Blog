from app.core.database import Base

# Import all models to make them available when importing from app.models
from app.models.user import User
from app.models.article import Article, Category, Tag
from app.models.comment import Comment
from app.models.activity import Activity
from app.models.subscription import Notification
from app.models.version import ArticleVersion
from app.models.about import AboutPage
from app.models.file import File
from app.models.notification_history import NotificationHistory

# Export all models
__all__ = [
    "User",
    "Article",
    "Category",
    "Tag",
    "Comment",
    "Activity",
    "Notification",
    "ArticleVersion",
    "AboutPage",
    "File",
    "NotificationHistory",
]

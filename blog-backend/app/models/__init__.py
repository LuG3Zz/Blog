from app.core.database import Base

# Import all models to make them available when importing from app.models
from app.models.user import User
from app.models.article import Article, Category, Tag
from app.models.comment import Comment
from app.models.activity import Activity
from app.models.subscription import Notification
from app.models.version import ArticleVersion

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
]

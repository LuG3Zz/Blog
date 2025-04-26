from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
import enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base
from app.models.subscription import user_category_subscriptions, user_author_subscriptions

class UserRole(str, enum.Enum):
    """User role enumeration."""
    admin = "admin"
    editor = "editor"
    author = "author"
    user = "user"

class User(Base):
    """User model representing blog users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    avatar = Column(String(255))
    bio = Column(Text, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.user)
    social_media = Column(Text, nullable=True)  # 社交媒体链接，存储为JSON字符串
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    articles = relationship("Article", back_populates="author")
    notifications = relationship("Notification", back_populates="user")
    files = relationship("File", back_populates="user")

    # Subscriptions
    subscribed_categories = relationship(
        "Category",
        secondary=user_category_subscriptions,
        backref="subscribers"
    )

    # Authors this user is subscribed to
    subscribed_authors = relationship(
        "User",
        secondary=user_author_subscriptions,
        primaryjoin=(id == user_author_subscriptions.c.subscriber_id),
        secondaryjoin=(id == user_author_subscriptions.c.author_id),
        backref="subscribers"
    )

    def __repr__(self):
        return f"<User {self.username}>"

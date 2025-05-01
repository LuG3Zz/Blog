from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.core.database import Base

# Association table for user-category subscriptions
user_category_subscriptions = Table(
    "user_category_subscriptions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)

# Association table for user-author subscriptions
user_author_subscriptions = Table(
    "user_author_subscriptions",
    Base.metadata,
    Column("subscriber_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("users.id"), primary_key=True)
)

class SubscriptionType(str, enum.Enum):
    """Enum for subscription types."""
    AUTHOR = "author"
    CATEGORY = "category"
    ALL = "all"  # 订阅所有文章

class EmailSubscription(Base):
    """Email subscription model for article notifications."""

    __tablename__ = "email_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, index=True)
    subscription_type = Column(Enum(SubscriptionType), nullable=False)
    reference_id = Column(Integer, nullable=True)  # 作者ID或分类ID，对于ALL类型为null
    is_active = Column(Boolean, default=True)
    token = Column(String(100), nullable=False, unique=True)  # 用于取消订阅的唯一令牌
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<EmailSubscription {self.id} for {self.email}>"

class Notification(Base):
    """Notification model for user notifications."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    type = Column(String(20), nullable=False)  # article, comment, system
    reference_id = Column(Integer, nullable=True)  # ID of the referenced object
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.id} for User {self.user_id}>"

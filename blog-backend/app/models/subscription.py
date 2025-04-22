from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

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

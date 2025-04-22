from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timezone

from app.core.database import Base

class Comment(Base):
    """Comment model for article comments."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Allow guest comments
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)  # For nested comments
    ip_address = Column(String(45), nullable=False)
    ip_region = Column(String(50), nullable=True)
    anonymous_name = Column(String(50), nullable=True)  # 匿名用户的显示名称
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_approved = Column(Boolean, default=False)
    like_count = Column(Integer, default=0)

    # Relationships
    article = relationship("Article", back_populates="comments")
    user = relationship("User")
    replies = relationship("Comment", backref=backref("parent", remote_side=[id]), cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Comment {self.id} on Article {self.article_id}>"

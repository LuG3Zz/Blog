from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base

class ArticleVersion(Base):
    """Article version model for tracking article changes."""
    
    __tablename__ = "article_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    version = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(Text, nullable=True)
    changes = Column(JSON, nullable=True)  # JSON field to store changes
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    article = relationship("Article")
    user = relationship("User")
    
    def __repr__(self):
        return f"<ArticleVersion {self.article_id}-v{self.version}>"

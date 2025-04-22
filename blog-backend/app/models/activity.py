from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.core.database import Base

class Activity(Base):
    """Activity model for tracking user actions."""
    
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String(20))  # Action type: article/comment/category
    user_id = Column(Integer, ForeignKey("users.id"))
    target_id = Column(Integer)  # Related object ID
    description = Column(String(255))  # Action description
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Activity {self.action_type} by User {self.user_id}>"

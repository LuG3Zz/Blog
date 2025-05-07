from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base

class Memo(Base):
    """备忘录模型，用于存储用户的备忘录/动态信息，支持密码加密。"""
    
    __tablename__ = "memos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(Text)
    is_encrypted = Column(Boolean, default=False)  # 是否加密
    password_hash = Column(String(255), nullable=True)  # 密码哈希，仅当is_encrypted为True时有值
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # 关系
    user = relationship("User", back_populates="memos")
    
    def __repr__(self):
        return f"<Memo {self.title} by User {self.user_id}>"

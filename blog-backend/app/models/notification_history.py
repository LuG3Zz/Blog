"""
通知历史数据库模型
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base

class NotificationHistory(Base):
    """通知历史数据库模型"""
    __tablename__ = "notification_history"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    level = Column(String(50), nullable=False)
    target_users = Column(JSON, nullable=True)  # 存储目标用户ID列表
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by_username = Column(String(100), nullable=False)

    # 关联关系
    creator = relationship("User", foreign_keys=[created_by])

"""
访客记录数据库模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from datetime import datetime, timezone

from app.core.database import Base

class Visitor(Base):
    """访客记录数据库模型"""
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), nullable=False, index=True)
    ip_region = Column(String(100), nullable=True)
    user_agent = Column(Text, nullable=True)
    referer = Column(String(255), nullable=True)
    path = Column(String(255), nullable=False)
    visit_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    is_mobile = Column(Boolean, default=False)
    is_bot = Column(Boolean, default=False)
    visitor_name = Column(String(100), nullable=True, default="访客")
    user_id = Column(String(50), nullable=True, index=True)
    client_id = Column(String(50), nullable=True, index=True)  # WebSocket客户端ID

    def __repr__(self):
        return f"<Visitor {self.ip_address} client_id={self.client_id} at {self.visit_time}>"

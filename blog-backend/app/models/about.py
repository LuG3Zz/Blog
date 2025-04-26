"""
About页面模型
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
from app.core.database import Base

class AboutPage(Base):
    """About页面内容模型"""
    __tablename__ = "about_page"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(JSON, nullable=False, comment="页面内容，JSON格式")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

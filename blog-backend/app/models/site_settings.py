from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from datetime import datetime, timezone
from typing import Dict, Any
import json

from app.core.database import Base

class SiteSettings(Base):
    """网站系统设置模型"""

    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    site_title = Column(String(100), nullable=False, default="BrownLu的博客")
    site_subtitle = Column(String(200), nullable=True, default="与你共享美好生活")
    nav_text = Column(JSON, nullable=True)  # 导航栏文字，存储为JSON
    nav_visible = Column(JSON, nullable=True)  # 导航栏项目显示控制，存储为JSON
    banner_image = Column(String(255), nullable=True)  # 首页banner图片URL
    footer_text = Column(String(255), nullable=True)  # 页脚文字
    logo_image = Column(String(255), nullable=True)  # 网站logo图片URL
    favicon = Column(String(255), nullable=True)  # 网站favicon图标URL
    meta_description = Column(String(500), nullable=True)  # 网站元描述
    meta_keywords = Column(String(255), nullable=True)  # 网站元关键词
    custom_css = Column(Text, nullable=True)  # 自定义CSS
    custom_js = Column(Text, nullable=True)  # 自定义JavaScript
    require_email_verification = Column(Boolean, default=False)  # 是否要求邮箱验证
    show_runtime = Column(Boolean, default=True)  # 是否显示网站运行时长
    site_start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # 网站创建日期
    comment_ai_review = Column(Boolean, default=True)  # 是否使用AI审核评论
    comment_review_all = Column(Boolean, default=False)  # 是否审核所有评论（包括已登录用户）
    comment_review_api_key = Column(String(255), nullable=True)  # 评论审核API密钥
    email_enabled = Column(Boolean, default=False)  # 是否启用邮件功能
    email_api_key = Column(String(255), nullable=True)  # Resend API密钥
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        """将模型转换为字典"""
        result = {
            "id": self.id,
            "site_title": self.site_title,
            "site_subtitle": self.site_subtitle,
            "banner_image": self.banner_image,
            "footer_text": self.footer_text,
            "logo_image": self.logo_image,
            "favicon": self.favicon,
            "meta_description": self.meta_description,
            "meta_keywords": self.meta_keywords,
            "custom_css": self.custom_css,
            "custom_js": self.custom_js,
            "require_email_verification": self.require_email_verification,
            "show_runtime": self.show_runtime,
            "site_start_date": self.site_start_date.isoformat() if self.site_start_date else None,
            "comment_ai_review": self.comment_ai_review,
            "comment_review_all": self.comment_review_all,
            "comment_review_api_key": self.comment_review_api_key,
            "email_enabled": self.email_enabled,
            "email_api_key": self.email_api_key,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

        # 处理nav_text字段
        if self.nav_text:
            if isinstance(self.nav_text, dict):
                result["nav_text"] = self.nav_text
            elif isinstance(self.nav_text, str):
                try:
                    result["nav_text"] = json.loads(self.nav_text)
                except json.JSONDecodeError:
                    result["nav_text"] = None
            else:
                result["nav_text"] = None
        else:
            result["nav_text"] = None

        # 处理nav_visible字段
        if self.nav_visible:
            if isinstance(self.nav_visible, dict):
                result["nav_visible"] = self.nav_visible
            elif isinstance(self.nav_visible, str):
                try:
                    result["nav_visible"] = json.loads(self.nav_visible)
                except json.JSONDecodeError:
                    result["nav_visible"] = None
            else:
                result["nav_visible"] = None
        else:
            result["nav_visible"] = None

        return result

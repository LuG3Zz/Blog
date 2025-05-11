from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class SiteSettingsBase(BaseModel):
    """系统设置基础模式"""
    site_title: Optional[str] = Field(None, description="网站标题")
    site_subtitle: Optional[str] = Field(None, description="网站副标题")
    nav_text: Optional[Dict[str, str]] = Field(default_factory=dict, description="导航栏文字，键为路由名称，值为显示文字")
    nav_visible: Optional[Dict[str, bool]] = Field(default_factory=dict, description="导航栏项目显示控制，键为路由名称，值为是否显示")
    banner_image: Optional[str] = Field(None, description="首页banner图片URL")
    footer_text: Optional[str] = Field(None, description="页脚文字")
    logo_image: Optional[str] = Field(None, description="网站logo图片URL")
    favicon: Optional[str] = Field(None, description="网站favicon图标URL")
    meta_description: Optional[str] = Field(None, description="网站元描述")
    meta_keywords: Optional[str] = Field(None, description="网站元关键词")
    custom_css: Optional[str] = Field(None, description="自定义CSS")
    custom_js: Optional[str] = Field(None, description="自定义JavaScript")
    require_email_verification: Optional[bool] = Field(False, description="是否要求邮箱验证")
    show_runtime: Optional[bool] = Field(True, description="是否显示网站运行时长")
    site_start_date: Optional[datetime] = Field(None, description="网站创建日期")
    comment_ai_review: Optional[bool] = Field(True, description="是否使用AI审核评论")
    comment_review_all: Optional[bool] = Field(False, description="是否审核所有评论（包括已登录用户）")
    comment_review_api_key: Optional[str] = Field(None, description="评论审核API密钥")
    email_enabled: Optional[bool] = Field(False, description="是否启用邮件功能")
    email_api_key: Optional[str] = Field(None, description="Resend API密钥")

class SiteSettingsCreate(SiteSettingsBase):
    """创建系统设置模式"""
    site_title: str = Field(..., description="网站标题")

class SiteSettingsUpdate(SiteSettingsBase):
    """更新系统设置模式"""
    pass

class SiteSettingsResponse(SiteSettingsBase):
    """系统设置响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        import json

        # 如果 nav_text 是字符串，尝试将其解析为 JSON
        if hasattr(obj, 'nav_text'):
            if isinstance(obj.nav_text, str) and obj.nav_text:
                try:
                    obj.nav_text = json.loads(obj.nav_text)
                except json.JSONDecodeError:
                    obj.nav_text = {}
            elif obj.nav_text is None:
                obj.nav_text = {}

        # 如果 nav_visible 是字符串，尝试将其解析为 JSON
        if hasattr(obj, 'nav_visible'):
            if isinstance(obj.nav_visible, str) and obj.nav_visible:
                try:
                    obj.nav_visible = json.loads(obj.nav_visible)
                except json.JSONDecodeError:
                    obj.nav_visible = {}
            elif obj.nav_visible is None:
                obj.nav_visible = {}

        return super().model_validate(obj, *args, **kwargs)

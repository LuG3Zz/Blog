import json
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.site_settings import SiteSettings
from app.schemas.site_settings import SiteSettingsCreate, SiteSettingsUpdate
from app.services.unified_cache_service import UnifiedCacheService
from app.utils.logging import get_logger

logger = get_logger(__name__)

# 缓存键
SITE_SETTINGS_CACHE_KEY = "site_settings"
# 缓存过期时间（秒）
SITE_SETTINGS_CACHE_TTL = 3600  # 1小时

class SiteSettingsService:
    """系统设置服务类"""

    @staticmethod
    def get_settings(db: Session) -> Optional[SiteSettings]:
        """
        获取系统设置

        Args:
            db: 数据库会话

        Returns:
            SiteSettings对象，如果不存在则返回None
        """
        # 尝试从缓存获取
        cached_settings = UnifiedCacheService.get(SITE_SETTINGS_CACHE_KEY)
        if cached_settings:
            try:
                # 检查缓存的数据类型
                settings_dict = cached_settings
                if isinstance(cached_settings, str):
                    # 如果是字符串，尝试解析为字典
                    settings_dict = json.loads(cached_settings)
                elif not isinstance(cached_settings, dict):
                    # 如果既不是字符串也不是字典，则抛出异常
                    raise ValueError(f"缓存的设置数据类型不正确: {type(cached_settings)}")

                # 创建SiteSettings对象
                settings = SiteSettings()
                for key, value in settings_dict.items():
                    if hasattr(settings, key):
                        # 如果是nav_text字段，确保它是一个字典
                        if key == 'nav_text' and isinstance(value, str):
                            try:
                                value = json.loads(value)
                            except json.JSONDecodeError:
                                value = None
                        setattr(settings, key, value)
                return settings
            except Exception as e:
                logger.error(f"从缓存解析系统设置失败: {e}")

        # 从数据库获取
        settings = db.query(SiteSettings).first()

        # 如果存在设置，则缓存
        if settings:
            try:
                # 将设置对象转换为字典，然后缓存
                settings_dict = settings.to_dict()
                UnifiedCacheService.set(
                    SITE_SETTINGS_CACHE_KEY,
                    json.dumps(settings_dict),
                    SITE_SETTINGS_CACHE_TTL
                )
            except Exception as e:
                logger.error(f"缓存系统设置失败: {e}")

        return settings

    @staticmethod
    def create_settings(db: Session, settings_data: SiteSettingsCreate) -> SiteSettings:
        """
        创建系统设置

        Args:
            db: 数据库会话
            settings_data: 设置数据

        Returns:
            创建的SiteSettings对象
        """
        # 检查是否已存在
        existing = SiteSettingsService.get_settings(db)
        if existing:
            return SiteSettingsService.update_settings(db, existing.id, settings_data.model_dump(exclude_unset=True))

        # 创建新记录
        settings_dict = settings_data.model_dump(exclude_unset=True)

        # 如果nav_text是字典，转换为JSON字符串
        if "nav_text" in settings_dict and isinstance(settings_dict["nav_text"], dict):
            settings_dict["nav_text"] = json.dumps(settings_dict["nav_text"])

        settings = SiteSettings(**settings_dict)
        db.add(settings)
        db.commit()
        db.refresh(settings)

        # 清除缓存
        UnifiedCacheService.delete(SITE_SETTINGS_CACHE_KEY)

        return settings

    @staticmethod
    def update_settings(db: Session, settings_id: int, settings_data: Dict[str, Any]) -> Optional[SiteSettings]:
        """
        更新系统设置

        Args:
            db: 数据库会话
            settings_id: 设置ID
            settings_data: 设置数据

        Returns:
            更新后的SiteSettings对象，如果不存在则返回None
        """
        settings = db.query(SiteSettings).filter(SiteSettings.id == settings_id).first()
        if not settings:
            return None

        # 如果nav_text是字典，转换为JSON字符串
        if "nav_text" in settings_data and isinstance(settings_data["nav_text"], dict):
            settings_data["nav_text"] = json.dumps(settings_data["nav_text"])

        # 更新字段
        for key, value in settings_data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

        db.commit()
        db.refresh(settings)

        # 清除缓存
        UnifiedCacheService.delete(SITE_SETTINGS_CACHE_KEY)

        return settings

    @staticmethod
    def get_default_settings() -> Dict[str, Any]:
        """
        获取默认系统设置

        Returns:
            默认设置字典
        """
        return {
            "site_title": "BrownLu的博客",
            "site_subtitle": "与你共享美好生活",
            "nav_text": {
                "Home": "首页",
                "ArticleList": "文章",
                "CategoryList": "分类",
                "About": "关于",
                "Login": "登录"
            },
            "footer_text": "© 2024 BrownLu的博客 - 保留所有权利",
            "meta_description": "BrownLu的个人博客，分享技术、生活和思考",
            "meta_keywords": "博客,技术,编程,生活"
        }

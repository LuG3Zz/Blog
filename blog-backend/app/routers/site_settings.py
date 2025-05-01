from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core import security
from app.core.permissions import is_admin
from app.models.user import User
from app.schemas.site_settings import SiteSettingsResponse, SiteSettingsCreate, SiteSettingsUpdate
from app.services.site_settings_service import SiteSettingsService

router = APIRouter(
    prefix="/site-settings",
    tags=["site-settings"],
)

@router.get("", response_model=SiteSettingsResponse)
async def get_site_settings(db: Session = Depends(get_db)):
    """
    获取网站系统设置

    不需要认证，任何人都可以访问
    """
    settings = SiteSettingsService.get_settings(db)

    # 如果没有设置，返回默认设置
    if not settings:
        default_settings = SiteSettingsService.get_default_settings()
        settings = SiteSettingsService.create_settings(db, SiteSettingsCreate(**default_settings))

    # 确保 nav_text 是字典类型
    if hasattr(settings, 'nav_text') and isinstance(settings.nav_text, str):
        try:
            import json
            settings.nav_text = json.loads(settings.nav_text)
        except json.JSONDecodeError:
            settings.nav_text = {}

    return settings

@router.put("", response_model=SiteSettingsResponse)
async def update_site_settings(
    settings_data: SiteSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    """
    更新网站系统设置

    需要管理员权限
    """
    # 检查权限
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update site settings"
        )

    # 获取现有设置
    settings = SiteSettingsService.get_settings(db)

    if not settings:
        # 如果不存在，创建新的
        settings_dict = settings_data.model_dump(exclude_unset=True)
        # 确保至少有site_title
        if "site_title" not in settings_dict or not settings_dict["site_title"]:
            settings_dict["site_title"] = "BrownLu的博客"

        return SiteSettingsService.create_settings(db, SiteSettingsCreate(**settings_dict))

    # 更新现有设置
    updated_settings = SiteSettingsService.update_settings(
        db,
        settings.id,
        settings_data.model_dump(exclude_unset=True)
    )

    if not updated_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site settings not found"
        )

    # 确保 nav_text 是字典类型
    if hasattr(updated_settings, 'nav_text') and isinstance(updated_settings.nav_text, str):
        try:
            import json
            updated_settings.nav_text = json.loads(updated_settings.nav_text)
        except json.JSONDecodeError:
            updated_settings.nav_text = {}

    return updated_settings

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.schemas.user import UserBriefResponse

class ActivityBase(BaseModel):
    """Base activity schema with common attributes."""
    action_type: str
    user_id: int
    target_id: int
    description: str

class ActivityResponse(ActivityBase):
    """Schema for activity response."""
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class ActivityDetail(BaseModel):
    """Detailed information about the target of an activity."""
    title: Optional[str] = None
    slug: Optional[str] = None
    content_preview: Optional[str] = None

class EnhancedActivityResponse(ActivityResponse):
    """Enhanced activity response with detailed information."""
    user: Optional[UserBriefResponse] = None
    target_detail: Optional[ActivityDetail] = None
    formatted_description: str
    relative_time: str

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 如果 user 存在且有 social_media 字段，处理字符串形式的 social_media
        if hasattr(obj, 'user') and obj.user and hasattr(obj.user, 'social_media') and isinstance(obj.user.social_media, str) and obj.user.social_media:
            try:
                import json
                obj.user.social_media = json.loads(obj.user.social_media)
            except json.JSONDecodeError:
                obj.user.social_media = None
        return super().model_validate(obj, *args, **kwargs)

class ActivityBatchDeleteRequest(BaseModel):
    """Request schema for batch deleting activities."""
    activity_ids: List[int]

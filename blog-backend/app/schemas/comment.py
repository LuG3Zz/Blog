from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.schemas.user import UserResponse

class CommentBase(BaseModel):
    """Base comment schema with common attributes."""
    content: str
    article_id: int
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    """Schema for comment creation."""
    anonymous_name: Optional[str] = Field(None, max_length=50, description="匿名用户的显示名称")

class CommentUpdate(BaseModel):
    """Schema for comment update."""
    content: str

class CommentLike(BaseModel):
    """Schema for comment like response."""
    comment_id: int
    like_count: int
    message: str

class CommentBrief(BaseModel):
    """Brief comment schema for nested responses."""
    id: int
    content: str
    user: Optional[UserResponse] = None
    anonymous_name: Optional[str] = None
    ip_region: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    like_count: int
    commenter_name: str = ""  # 评论者名称，将在模型验证时计算

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 如果用户存在且有 social_media 字段，处理字符串形式的 social_media
        if hasattr(obj, 'user') and obj.user and hasattr(obj.user, 'social_media') and isinstance(obj.user.social_media, str) and obj.user.social_media:
            try:
                import json
                obj.user.social_media = json.loads(obj.user.social_media)
            except json.JSONDecodeError:
                obj.user.social_media = None
        return super().model_validate(obj, *args, **kwargs)

class CommentResponse(CommentBrief):
    """Schema for comment response."""
    article_id: int
    article_title: Optional[str] = None
    parent_id: Optional[int] = None
    is_approved: bool
    replies: List["CommentBrief"] = []
    # commenter_name 已经从 CommentBrief 继承

    model_config = {
        "from_attributes": True
    }

class CommentWithReplies(CommentResponse):
    """Schema for comment with replies."""
    replies: List[CommentBrief] = []

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 先调用父类的 model_validate 处理当前对象的 user.social_media
        result = super().model_validate(obj, *args, **kwargs)

        # 处理回复中的 user.social_media
        if hasattr(result, 'replies') and result.replies:
            for reply in result.replies:
                if hasattr(reply, 'user') and reply.user and hasattr(reply.user, 'social_media') and isinstance(reply.user.social_media, str) and reply.user.social_media:
                    try:
                        import json
                        reply.user.social_media = json.loads(reply.user.social_media)
                    except json.JSONDecodeError:
                        reply.user.social_media = None

        return result

class CommentPaginationResponse(BaseModel):
    """Schema for paginated comment response."""
    items: List[CommentWithReplies]
    total: int
    page: int
    page_size: int
    pages: int

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 处理列表中的每个项目
        if hasattr(obj, 'items') and obj.items:
            for item in obj.items:
                # 处理当前评论的 user.social_media
                if hasattr(item, 'user') and item.user and hasattr(item.user, 'social_media') and isinstance(item.user.social_media, str) and item.user.social_media:
                    try:
                        import json
                        item.user.social_media = json.loads(item.user.social_media)
                    except json.JSONDecodeError:
                        item.user.social_media = None

                # 处理回复中的 user.social_media
                if hasattr(item, 'replies') and item.replies:
                    for reply in item.replies:
                        if hasattr(reply, 'user') and reply.user and hasattr(reply.user, 'social_media') and isinstance(reply.user.social_media, str) and reply.user.social_media:
                            try:
                                import json
                                reply.user.social_media = json.loads(reply.user.social_media)
                            except json.JSONDecodeError:
                                reply.user.social_media = None

        return super().model_validate(obj, *args, **kwargs)

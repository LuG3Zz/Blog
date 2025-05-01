from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    """User role enumeration for schemas."""
    admin = "admin"
    editor = "editor"
    author = "author"
    user = "user"

class UserBase(BaseModel):
    """Base user schema with common attributes."""
    username: str
    email: EmailStr
    role: Optional[UserRole] = UserRole.user

class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(..., min_length=6)
    verification_code: Optional[str] = None

class UserUpdate(BaseModel):
    """Schema for user updates."""
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None
    role: Optional[UserRole] = None

class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str = Field(..., min_length=6)

class UserInDB(UserBase):
    """Schema for user in database."""
    id: int
    created_at: datetime
    updated_at: datetime
    email_verified: bool = False
    avatar: Optional[str] = None
    bio: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None
    comment_count: int = 0
    article_count: int = 0

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 如果 social_media 是字符串，尝试将其解析为 JSON
        if hasattr(obj, 'social_media') and isinstance(obj.social_media, str) and obj.social_media:
            try:
                import json
                obj.social_media = json.loads(obj.social_media)
            except json.JSONDecodeError:
                obj.social_media = None
        return super().model_validate(obj, *args, **kwargs)

class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    email: EmailStr
    email_verified: bool = False
    avatar: Optional[str] = None
    bio: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None
    role: UserRole
    created_at: datetime
    comment_count: int = 0
    article_count: int = 0

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 处理 social_media 字段
        if hasattr(obj, 'social_media') and obj.social_media:
            if isinstance(obj.social_media, str):
                try:
                    import json
                    obj.social_media = json.loads(obj.social_media)
                except json.JSONDecodeError:
                    obj.social_media = {}
            elif obj.social_media is None:
                obj.social_media = {}
        return super().model_validate(obj, *args, **kwargs)

class UserBriefResponse(BaseModel):
    """Schema for brief user response (used in article listings)."""
    id: int
    username: str
    avatar: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 如果是 SQLAlchemy 模型对象，先转换为字典
        if hasattr(obj, '__table__'):
            data = {
                'id': getattr(obj, 'id', None),
                'username': getattr(obj, 'username', None),
                'avatar': getattr(obj, 'avatar', None),
                'social_media': None
            }

            # 处理 social_media 字段
            if hasattr(obj, 'social_media') and obj.social_media:
                if isinstance(obj.social_media, str):
                    try:
                        import json
                        data['social_media'] = json.loads(obj.social_media)
                    except json.JSONDecodeError:
                        data['social_media'] = {}
                else:
                    data['social_media'] = obj.social_media

            return super().model_validate(data, *args, **kwargs)

        return super().model_validate(obj, *args, **kwargs)

class UserBriefNoSocial(BaseModel):
    """Schema for brief user response without social media field."""
    id: int
    username: str
    avatar: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 如果是 SQLAlchemy 模型对象，先转换为字典
        if hasattr(obj, '__table__'):
            data = {
                'id': getattr(obj, 'id', None),
                'username': getattr(obj, 'username', None),
                'avatar': getattr(obj, 'avatar', None)
            }
            return super().model_validate(data, *args, **kwargs)

        return super().model_validate(obj, *args, **kwargs)


class EmailVerification(BaseModel):
    """邮箱验证码请求"""
    email: EmailStr


class VerifyEmailCode(BaseModel):
    """验证邮箱验证码"""
    email: EmailStr
    code: str
from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr

from app.schemas.user import UserResponse
from app.models.subscription import SubscriptionType

class NotificationBase(BaseModel):
    """Base notification schema."""
    title: str
    content: str
    type: str
    reference_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    """Schema for notification creation."""
    user_id: int

class NotificationResponse(NotificationBase):
    """Schema for notification response."""
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class SubscriptionBase(BaseModel):
    """Base subscription schema."""
    pass

class CategorySubscriptionCreate(SubscriptionBase):
    """Schema for category subscription creation."""
    category_id: int

class AuthorSubscriptionCreate(SubscriptionBase):
    """Schema for author subscription creation."""
    author_id: int

class SubscriptionResponse(BaseModel):
    """Schema for subscription response."""
    user_id: int
    category_ids: List[int] = []
    author_ids: List[int] = []

    model_config = {
        "from_attributes": True
    }

class EmailSubscriptionBase(BaseModel):
    """Base email subscription schema."""
    email: EmailStr
    subscription_type: SubscriptionType
    reference_id: Optional[int] = None

class EmailSubscriptionCreate(EmailSubscriptionBase):
    """Schema for email subscription creation."""
    pass

class EmailSubscriptionResponse(EmailSubscriptionBase):
    """Schema for email subscription response."""
    id: int
    is_active: bool
    created_at: datetime
    reference_name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class EmailSubscriptionUpdate(BaseModel):
    """Schema for email subscription update."""
    is_active: Optional[bool] = None

class EmailSubscriptionUnsubscribe(BaseModel):
    """Schema for email subscription unsubscribe."""
    token: str

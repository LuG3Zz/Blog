from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.user import UserResponse, UserBriefResponse

class CategoryBase(BaseModel):
    """Base category schema."""
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Schema for category creation."""
    pass

class CategoryUpdate(BaseModel):
    """Schema for category update."""
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    """Schema for category response."""
    id: int

    model_config = {
        "from_attributes": True
    }

class CategoryWithCount(CategoryBase):
    """Schema for category with article count."""
    id: int
    articleCount: int = 0

    model_config = {
        "from_attributes": True
    }

class TagResponse(BaseModel):
    """Schema for tag response."""
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class ArticleBase(BaseModel):
    """Base article schema with common attributes."""
    title: str
    content: str
    excerpt: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: int
    # tags 字段已移除，使用 tags_list 代替

class ArticleCreate(ArticleBase):
    """Schema for article creation."""
    slug: Optional[str] = None  # Optional, can be auto-generated
    tags: Optional[List[str]] = Field(default=None, description="List of tag names")

class ArticleUpdate(BaseModel):
    """Schema for article updates."""
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = Field(default=None, description="List of tag names")
    is_featured: Optional[bool] = None
    slug: Optional[str] = None

class ArticleInDB(BaseModel):
    """Schema for article in database."""
    id: int
    title: str
    content: str
    slug: str
    excerpt: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    view_count: int
    like_count: int
    is_featured: bool

    model_config = {
        "from_attributes": True
    }

class ArticleResponse(ArticleInDB):
    """Schema for article response."""
    author: UserResponse
    category: CategoryResponse
    tags_list: Optional[List[TagResponse]] = Field(default=None, description="List of tags associated with the article")

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 如果 author 存在且有 social_media 字段，处理字符串形式的 social_media
        if hasattr(obj, 'author') and obj.author and hasattr(obj.author, 'social_media') and isinstance(obj.author.social_media, str) and obj.author.social_media:
            try:
                import json
                obj.author.social_media = json.loads(obj.author.social_media)
            except json.JSONDecodeError:
                obj.author.social_media = None
        return super().model_validate(obj, *args, **kwargs)

class ArticleList(BaseModel):
    """Schema for article list response."""
    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    cover_image: Optional[str] = None
    author: UserBriefResponse
    category: Optional[CategoryResponse] = None
    created_at: datetime
    view_count: int
    like_count: int
    is_featured: bool
    tags_list: Optional[List[TagResponse]] = Field(default=None, description="List of tags associated with the article")

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 如果 author 存在且有 social_media 字段，处理字符串形式的 social_media
        if hasattr(obj, 'author') and obj.author and hasattr(obj.author, 'social_media') and isinstance(obj.author.social_media, str) and obj.author.social_media:
            try:
                import json
                obj.author.social_media = json.loads(obj.author.social_media)
            except json.JSONDecodeError:
                obj.author.social_media = None
        return super().model_validate(obj, *args, **kwargs)

class LikeResponse(BaseModel):
    """Schema for article like response."""
    article_id: int
    like_count: int
    message: str

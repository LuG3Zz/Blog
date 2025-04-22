from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class ArticleVersionBase(BaseModel):
    """Base article version schema."""
    article_id: int
    version: int
    title: str
    content: str
    excerpt: Optional[str] = None
    changes: Optional[Dict[str, Any]] = None

class ArticleVersionCreate(ArticleVersionBase):
    """Schema for article version creation."""
    created_by: int

class ArticleVersionResponse(ArticleVersionBase):
    """Schema for article version response."""
    id: int
    created_by: int
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class ArticleVersionDiff(BaseModel):
    """Schema for article version diff."""
    field: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None

from typing import Optional
from pydantic import BaseModel, Field

class TagBase(BaseModel):
    """Base tag schema."""
    name: str = Field(..., min_length=1, max_length=50)

class TagCreate(TagBase):
    """Schema for tag creation."""
    description: Optional[str] = Field(None, max_length=200)

class TagUpdate(BaseModel):
    """Schema for tag update."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

class TagResponse(TagBase):
    """Schema for tag response."""
    id: int
    description: Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }

class TagWithCount(TagResponse):
    """Schema for tag with article count."""
    article_count: int = 0
    
    model_config = {
        "from_attributes": True
    }

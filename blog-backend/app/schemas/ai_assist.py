from typing import List
from pydantic import BaseModel, Field

class AIAssistRequest(BaseModel):
    """Request model for AI assistance."""
    content: str = Field(..., min_length=50, description="文章正文内容")

class AIAssistResponse(BaseModel):
    """Response model for AI assistance."""
    excerpt: str = Field(..., description="生成的摘要")
    tags: List[str] = Field(..., description="生成的标签列表")

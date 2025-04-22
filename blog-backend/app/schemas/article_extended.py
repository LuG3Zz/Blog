from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.article import TagResponse

class ArticleWithContent(BaseModel):
    """Article model with full content."""
    id: int
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None  # 添加分类名称字段
    # tags 字段已移除，使用 tags_list 代替
    tags_list: Optional[List[TagResponse]] = None
    cover_image: Optional[str] = None
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    is_featured: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }

class FeaturedArticle(BaseModel):
    """Featured article model."""
    id: int
    title: str
    cover_image: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class HomeResponse(BaseModel):
    """Home page response model."""
    articles: List
    categories: List
    featuredArticles: List

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # 处理文章列表中的作者社交媒体字段
        if hasattr(obj, 'articles') and obj.articles:
            for article in obj.articles:
                if hasattr(article, 'author') and article.author and hasattr(article.author, 'social_media') and isinstance(article.author.social_media, str) and article.author.social_media:
                    try:
                        import json
                        article.author.social_media = json.loads(article.author.social_media)
                    except json.JSONDecodeError:
                        article.author.social_media = None

        return super().model_validate(obj, *args, **kwargs)

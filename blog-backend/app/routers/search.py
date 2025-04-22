from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_, and_, func

from app.core.database import get_db
from app.utils.pagination import PaginationParams, PagedResponse
from app.schemas.article import ArticleList
from app.schemas.user import UserResponse
from app import models
from app.models import Article, User, Category, Tag

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/articles", response_model=PagedResponse[ArticleList])
async def search_articles(
    q: str = Query(..., min_length=1, description="Search query"),
    category_id: Optional[int] = None,
    tag: Optional[str] = None,
    author_id: Optional[int] = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Search articles by title, content, excerpt, author, category, or tags.
    """
    # Base query
    query = db.query(Article)

    # Apply search filter
    search_term = f"%{q}%"
    search_filter = or_(
        Article.title.ilike(search_term),
        Article.content.ilike(search_term),
        Article.excerpt.ilike(search_term)
    )
    query = query.filter(search_filter)

    # Apply additional filters if provided
    if category_id:
        query = query.filter(Article.category_id == category_id)

    if tag:
        # 使用多对多关系查询标签
        query = query.join(models.article_tags).join(models.Tag).filter(models.Tag.name == tag)

    if author_id:
        query = query.filter(Article.author_id == author_id)

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    articles = query.order_by(Article.created_at.desc())\
        .offset(pagination.skip)\
        .limit(pagination.page_size)\
        .all()

    return PagedResponse.create(articles, total, pagination)

@router.get("/users", response_model=PagedResponse[UserResponse])
async def search_users(
    q: str = Query(..., min_length=1, description="Search query"),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Search users by username, email, or bio.
    """
    # Base query
    query = db.query(User)

    # Apply search filter
    search_term = f"%{q}%"
    search_filter = or_(
        User.username.ilike(search_term),
        User.email.ilike(search_term),
        User.bio.ilike(search_term)
    )
    query = query.filter(search_filter)

    # Get total count
    total = query.count()

    # Apply pagination
    users = query.offset(pagination.skip).limit(pagination.page_size).all()

    return PagedResponse.create(users, total, pagination)

@router.get("/tags", response_model=List[str])
async def search_tags(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Search tags by name.
    """
    search_term = f"%{q}%"
    tags = db.query(Tag.name).filter(Tag.name.ilike(search_term)).limit(limit).all()
    return [tag[0] for tag in tags]

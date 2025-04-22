from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from fastapi import HTTPException, status

from app import models, schemas
from app.utils.validators import generate_slug, is_valid_slug
from app.utils.logging import get_logger
from app.schemas.version import ArticleVersionCreate
from app.services.version_service import VersionService
from app.services.unified_cache_service import cached

logger = get_logger(__name__)

class ArticleService:
    """Service for article-related operations."""

    @staticmethod
    @cached(prefix="article_by_id", ttl=300)
    def get_article_by_id(db: Session, article_id: int) -> Optional[models.Article]:
        """Get an article by ID."""
        return db.query(models.Article).filter(models.Article.id == article_id).first()

    @staticmethod
    @cached(prefix="article_by_slug", ttl=300)
    def get_article_by_slug(db: Session, slug: str) -> Optional[models.Article]:
        """Get an article by slug."""
        return db.query(models.Article).filter(models.Article.slug == slug).first()

    @staticmethod
    @cached(prefix="articles_list", ttl=60)  # 较短的缓存时间，因为文章列表可能会频繁更新
    def get_articles(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        featured_only: bool = False
    ) -> Tuple[List[models.Article], int]:
        """
        Get a list of articles with optional filtering.

        Returns:
            Tuple containing list of articles and total count
        """
        query = db.query(models.Article)

        # Apply filters
        if category_id:
            query = query.filter(models.Article.category_id == category_id)

        if tag:
            # 使用多对多关系查询标签
            query = query.join(models.article_tags).join(models.Tag).filter(models.Tag.name == tag)

        if search:
            # Search in title and content
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    models.Article.title.like(search_term),
                    models.Article.content.like(search_term)
                )
            )

        if featured_only:
            query = query.filter(models.Article.is_featured == True)

        # Get total count before pagination
        total = query.count()

        # Apply pagination and ordering
        articles = query.order_by(models.Article.created_at.desc()).offset(skip).limit(limit).all()

        return articles, total

    @staticmethod
    def create_article(db: Session, article: schemas.ArticleCreate, author_id: int) -> models.Article:
        """Create a new article."""
        # Generate slug if not provided
        slug = article.slug if article.slug else generate_slug(article.title)

        # Validate slug
        if not is_valid_slug(slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid slug format"
            )

        # Check if slug already exists
        existing_article = ArticleService.get_article_by_slug(db, slug)
        if existing_article:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slug already exists"
            )

        # Create article
        db_article = models.Article(
            title=article.title,
            slug=slug,
            content=article.content,
            excerpt=article.excerpt,
            cover_image=article.cover_image,
            category_id=article.category_id,
            # tags 字段已移除，使用 tags_relationship 多对多关系代替
            author_id=author_id
        )

        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        # Create initial version
        version = ArticleVersionCreate(
            article_id=db_article.id,
            version=1,  # Initial version
            title=db_article.title,
            content=db_article.content,
            excerpt=db_article.excerpt,
            created_by=author_id
        )
        VersionService.create_article_version(db, version)

        logger.info(f"Created new article: {article.title}")
        return db_article

    @staticmethod
    def update_article(
        db: Session,
        article_id: int,
        article_update: schemas.ArticleUpdate
    ) -> models.Article:
        """Update an article."""
        db_article = ArticleService.get_article_by_id(db, article_id)
        if not db_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        # Save current state before update for versioning
        old_title = db_article.title
        old_content = db_article.content
        old_excerpt = db_article.excerpt

        # Update article fields if provided
        update_data = article_update.model_dump(exclude_unset=True)

        # Update article attributes
        for key, value in update_data.items():
            setattr(db_article, key, value)

        db.commit()
        db.refresh(db_article)

        # Create new version if content, title or excerpt changed
        if (old_title != db_article.title or
            old_content != db_article.content or
            old_excerpt != db_article.excerpt):

            version = ArticleVersionCreate(
                article_id=db_article.id,
                version=0,  # Will be set by the service
                title=db_article.title,
                content=db_article.content,
                excerpt=db_article.excerpt,
                created_by=db_article.author_id
            )
            VersionService.create_article_version(db, version)

        logger.info(f"Updated article: {db_article.title}")
        return db_article

    @staticmethod
    def delete_article(db: Session, article_id: int) -> bool:
        """Delete an article."""
        db_article = ArticleService.get_article_by_id(db, article_id)
        if not db_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        db.delete(db_article)
        db.commit()

        logger.info(f"Deleted article: {db_article.title}")
        return True

    @staticmethod
    def increment_view_count(db: Session, article_id: int) -> models.Article:
        """Increment the view count of an article."""
        # 直接从数据库获取文章，不使用缓存
        db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if not db_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        db_article.view_count = (db_article.view_count or 0) + 1
        db.commit()
        db.refresh(db_article)

        return db_article

    @staticmethod
    def like_article(db: Session, article_id: int) -> models.Article:
        """Increment the like count of an article."""
        # 直接从数据库获取文章，不使用缓存
        db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if not db_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        db_article.like_count = (db_article.like_count or 0) + 1
        db.commit()
        db.refresh(db_article)

        return db_article

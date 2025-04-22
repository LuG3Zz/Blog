from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.core import security
from app.core.database import get_db
from app.schemas.version import ArticleVersionResponse
from app.services.version_service import VersionService
from app.services.article_service import ArticleService

router = APIRouter(prefix="/versions", tags=["versions"])

@router.get("/articles/{article_id}", response_model=List[ArticleVersionResponse])
async def get_article_versions(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Get all versions of an article.
    """
    # Check if user has access to the article
    article = ArticleService.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # Only allow the author or admin to view versions
    if article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view article versions"
        )

    return VersionService.get_article_versions(db, article_id)

@router.get("/articles/{article_id}/{version}", response_model=ArticleVersionResponse)
async def get_article_version(
    article_id: int,
    version: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Get a specific version of an article.
    """
    # Check if user has access to the article
    article = ArticleService.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # Only allow the author or admin to view versions
    if article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view article versions"
        )

    version_obj = VersionService.get_article_version(db, article_id, version)
    if not version_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version {version} not found for article {article_id}"
        )

    return version_obj

@router.post("/articles/{article_id}/restore/{version}")
async def restore_article_version(
    article_id: int,
    version: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Restore an article to a specific version.
    """
    # Check if user has access to the article
    article = ArticleService.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # Only allow the author to restore versions
    if article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to restore article versions"
        )

    VersionService.restore_article_version(db, article_id, version, current_user.id)

    return {"message": f"Article restored to version {version}"}

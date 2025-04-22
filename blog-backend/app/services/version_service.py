from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import difflib

from app import models
from app.schemas.version import ArticleVersionCreate
from app.utils.logging import get_logger

logger = get_logger(__name__)

class VersionService:
    """Service for article version-related operations."""
    
    @staticmethod
    def create_article_version(db: Session, version: ArticleVersionCreate) -> models.ArticleVersion:
        """Create a new article version."""
        # Check if article exists
        article = db.query(models.Article).filter(models.Article.id == version.article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Get the latest version number
        latest_version = db.query(models.ArticleVersion)\
            .filter(models.ArticleVersion.article_id == version.article_id)\
            .order_by(models.ArticleVersion.version.desc())\
            .first()
        
        new_version_number = 1
        if latest_version:
            new_version_number = latest_version.version + 1
        
        # Create changes object if this is not the first version
        changes = None
        if latest_version:
            changes = VersionService.compute_changes(latest_version, version)
        
        # Create new version
        db_version = models.ArticleVersion(
            article_id=version.article_id,
            version=new_version_number,
            title=version.title,
            content=version.content,
            excerpt=version.excerpt,
            changes=changes,
            created_by=version.created_by
        )
        
        db.add(db_version)
        db.commit()
        db.refresh(db_version)
        
        logger.info(f"Created version {new_version_number} for article {version.article_id}")
        return db_version
    
    @staticmethod
    def get_article_versions(db: Session, article_id: int) -> List[models.ArticleVersion]:
        """Get all versions of an article."""
        # Check if article exists
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Get versions
        versions = db.query(models.ArticleVersion)\
            .filter(models.ArticleVersion.article_id == article_id)\
            .order_by(models.ArticleVersion.version.desc())\
            .all()
        
        return versions
    
    @staticmethod
    def get_article_version(db: Session, article_id: int, version: int) -> Optional[models.ArticleVersion]:
        """Get a specific version of an article."""
        return db.query(models.ArticleVersion)\
            .filter(
                models.ArticleVersion.article_id == article_id,
                models.ArticleVersion.version == version
            )\
            .first()
    
    @staticmethod
    def compute_changes(old_version: models.ArticleVersion, new_version: ArticleVersionCreate) -> Dict[str, Any]:
        """Compute changes between two versions."""
        changes = {}
        
        # Check title changes
        if old_version.title != new_version.title:
            changes["title"] = {
                "old": old_version.title,
                "new": new_version.title
            }
        
        # Check excerpt changes
        if old_version.excerpt != new_version.excerpt:
            changes["excerpt"] = {
                "old": old_version.excerpt,
                "new": new_version.excerpt
            }
        
        # Check content changes using difflib
        if old_version.content != new_version.content:
            # Generate a unified diff
            diff = difflib.unified_diff(
                old_version.content.splitlines(),
                new_version.content.splitlines(),
                lineterm=""
            )
            
            # Convert diff to a list
            diff_lines = list(diff)
            
            # Skip the first two lines (header)
            if len(diff_lines) > 2:
                diff_lines = diff_lines[2:]
            
            changes["content"] = {
                "diff": diff_lines
            }
        
        return changes
    
    @staticmethod
    def restore_article_version(db: Session, article_id: int, version: int, user_id: int) -> models.Article:
        """Restore an article to a specific version."""
        # Check if article exists
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Check if version exists
        version_obj = VersionService.get_article_version(db, article_id, version)
        if not version_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Version {version} not found for article {article_id}"
            )
        
        # Create a new version first (to save the current state)
        current_version = ArticleVersionCreate(
            article_id=article_id,
            version=0,  # Will be set by the service
            title=article.title,
            content=article.content,
            excerpt=article.excerpt,
            created_by=user_id
        )
        
        VersionService.create_article_version(db, current_version)
        
        # Update article with version data
        article.title = version_obj.title
        article.content = version_obj.content
        article.excerpt = version_obj.excerpt
        
        db.commit()
        db.refresh(article)
        
        logger.info(f"Restored article {article_id} to version {version}")
        return article

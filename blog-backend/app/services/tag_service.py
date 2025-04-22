from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app import models
from app.schemas.tag import TagCreate, TagUpdate
from app.utils.logging import get_logger

logger = get_logger(__name__)

class TagService:
    """Service for tag-related operations."""

    @staticmethod
    def get_tag_by_id(db: Session, tag_id: int) -> Optional[models.Tag]:
        """Get a tag by ID."""
        return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

    @staticmethod
    def get_tag_by_name(db: Session, name: str) -> Optional[models.Tag]:
        """Get a tag by name."""
        return db.query(models.Tag).filter(models.Tag.name == name).first()

    @staticmethod
    def get_tags(db: Session, skip: int = 0, limit: int = 100) -> List[models.Tag]:
        """Get a list of tags."""
        return db.query(models.Tag).offset(skip).limit(limit).all()

    @staticmethod
    def get_tags_with_count(db: Session, skip: int = 0, limit: int = 100) -> List:
        """Get a list of tags with article count."""
        # 使用多对多关系表获取标签及其文章数量
        from app.models.article import article_tags

        # 使用子查询计算每个标签的文章数量
        tag_counts = db.query(
            models.Tag.id,
            func.count(article_tags.c.article_id).label('article_count')
        ).outerjoin(
            article_tags,
            models.Tag.id == article_tags.c.tag_id
        ).group_by(models.Tag.id).subquery()

        # 获取标签及其文章数量
        tags_with_count = db.query(
            models.Tag,
            tag_counts.c.article_count
        ).outerjoin(
            tag_counts,
            models.Tag.id == tag_counts.c.id
        ).order_by(tag_counts.c.article_count.desc()).offset(skip).limit(limit).all()

        # 将文章数量添加到标签对象中
        result = []
        for tag, count in tags_with_count:
            setattr(tag, "article_count", count or 0)
            result.append(tag)

        return result

    @staticmethod
    def create_tag(db: Session, tag: TagCreate) -> models.Tag:
        """Create a new tag."""
        # Check if tag already exists
        existing_tag = TagService.get_tag_by_name(db, tag.name)
        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag already exists"
            )

        # Create new tag
        db_tag = models.Tag(
            name=tag.name,
            description=tag.description
        )

        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)

        logger.info(f"Created new tag: {tag.name}")
        return db_tag

    @staticmethod
    def update_tag(db: Session, tag_id: int, tag_update: TagUpdate) -> models.Tag:
        """Update a tag."""
        db_tag = TagService.get_tag_by_id(db, tag_id)
        if not db_tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )

        # Check if new name already exists
        if tag_update.name and tag_update.name != db_tag.name:
            existing_tag = TagService.get_tag_by_name(db, tag_update.name)
            if existing_tag:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tag name already exists"
                )

        # Update tag fields if provided
        update_data = tag_update.model_dump(exclude_unset=True)

        # Update tag attributes
        for key, value in update_data.items():
            setattr(db_tag, key, value)

        db.commit()
        db.refresh(db_tag)

        logger.info(f"Updated tag: {db_tag.name}")
        return db_tag

    @staticmethod
    def delete_tag(db: Session, tag_id: int) -> bool:
        """Delete a tag."""
        db_tag = TagService.get_tag_by_id(db, tag_id)
        if not db_tag:
            return False

        db.delete(db_tag)
        db.commit()

        logger.info(f"Deleted tag: {db_tag.name}")
        return True

    @staticmethod
    def get_article_tags(db: Session, article_id: int) -> List[models.Tag]:
        """Get all tags for an article."""
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        return article.tags_relationship

    @staticmethod
    def add_tag_to_article(db: Session, article_id: int, tag_id: int) -> bool:
        """Add a tag to an article."""
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        tag = TagService.get_tag_by_id(db, tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )

        # 检查标签是否已经关联到文章
        if tag in article.tags_relationship:
            return True  # 已经关联，无需重复添加

        # 添加标签到文章
        article.tags_relationship.append(tag)
        db.commit()

        logger.info(f"Added tag '{tag.name}' to article ID {article_id}")
        return True

    @staticmethod
    def remove_tag_from_article(db: Session, article_id: int, tag_id: int) -> bool:
        """Remove a tag from an article."""
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        tag = TagService.get_tag_by_id(db, tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )

        # 检查标签是否关联到文章
        if tag not in article.tags_relationship:
            return True  # 标签未关联，无需移除

        # 从文章中移除标签
        article.tags_relationship.remove(tag)
        db.commit()

        logger.info(f"Removed tag '{tag.name}' from article ID {article_id}")
        return True

    @staticmethod
    def update_article_tags(db: Session, article_id: int, tag_ids: List[int]) -> List[models.Tag]:
        """Update all tags for an article."""
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        # 获取所有标签
        tags = db.query(models.Tag).filter(models.Tag.id.in_(tag_ids)).all()

        # 检查是否有标签不存在
        if len(tags) != len(tag_ids):
            found_ids = [tag.id for tag in tags]
            missing_ids = [tag_id for tag_id in tag_ids if tag_id not in found_ids]
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tags not found: {missing_ids}"
            )

        # 更新文章的标签
        article.tags_relationship = tags
        db.commit()

        logger.info(f"Updated tags for article ID {article_id}: {[tag.name for tag in tags]}")
        return tags

    @staticmethod
    def get_articles_by_tag(db: Session, tag_id: int, skip: int = 0, limit: int = 10) -> List[models.Article]:
        """Get all articles with a specific tag."""
        tag = TagService.get_tag_by_id(db, tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )

        articles = tag.articles[skip:skip+limit]

        # 处理文章作者的 social_media 字段
        for article in articles:
            if hasattr(article, 'author') and article.author and hasattr(article.author, 'social_media') and isinstance(article.author.social_media, str) and article.author.social_media:
                try:
                    import json
                    article.author.social_media = json.loads(article.author.social_media)
                except json.JSONDecodeError:
                    article.author.social_media = None

        return articles

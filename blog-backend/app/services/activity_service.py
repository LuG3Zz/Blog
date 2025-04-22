from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
import humanize

from app import models, schemas
from app.schemas.activity import ActivityDetail, EnhancedActivityResponse
from app.utils.logging import get_logger
from app.utils.time_utils import get_relative_time_zh
from app.core.cache import clear_cache_by_prefix

logger = get_logger(__name__)

class ActivityService:
    """Service for activity-related operations."""

    @staticmethod
    def get_activity_by_id(db: Session, activity_id: int) -> Optional[models.Activity]:
        """Get an activity by ID."""
        return db.query(models.Activity).filter(models.Activity.id == activity_id).first()

    @staticmethod
    def get_activities_by_user(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Activity]:
        """Get activities for a user."""
        return db.query(models.Activity)\
            .filter(models.Activity.user_id == user_id)\
            .order_by(models.Activity.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    def create_activity(
        db: Session,
        action_type: str,
        user_id: int,
        target_id: int,
        description: str
    ) -> models.Activity:
        """Create a new activity record."""
        db_activity = models.Activity(
            action_type=action_type,
            user_id=user_id,
            target_id=target_id,
            description=description
        )

        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)

        # 清除相关缓存
        ActivityService.clear_activity_related_caches(action_type)

        logger.info(f"Created new activity: {action_type} by user {user_id}")
        return db_activity

    @staticmethod
    def clear_activity_related_caches(action_type: str) -> None:
        """清除与活动相关的缓存"""
        # 清除活动热力图缓存
        clear_cache_by_prefix("activity_heatmap")

        # 清除活动时间线缓存
        clear_cache_by_prefix("activity_timeline")

        # 清除公开活动缓存
        if action_type in ["article_create", "comment_create"]:
            clear_cache_by_prefix("public_activities")

        # 根据活动类型清除特定缓存
        if action_type.startswith("article"):
            clear_cache_by_prefix("articles_list")
            clear_cache_by_prefix("popular_articles")
            clear_cache_by_prefix("stats_overview")

        elif action_type.startswith("comment"):
            clear_cache_by_prefix("comments_by_article")
            clear_cache_by_prefix("stats_overview")

        # 清除用户活动缓存
        clear_cache_by_prefix("user_activity")

    @staticmethod
    def log_article_creation(db: Session, user_id: int, article_id: int, title: str) -> models.Activity:
        """Log article creation activity."""
        return ActivityService.create_activity(
            db=db,
            action_type="article_create",
            user_id=user_id,
            target_id=article_id,
            description=f"Created article: {title}"
        )

    @staticmethod
    def log_article_update(db: Session, user_id: int, article_id: int, title: str) -> models.Activity:
        """Log article update activity."""
        return ActivityService.create_activity(
            db=db,
            action_type="article_update",
            user_id=user_id,
            target_id=article_id,
            description=f"Updated article: {title}"
        )

    @staticmethod
    def log_comment_creation(db: Session, user_id: int, comment_id: int, article_id: int) -> models.Activity:
        """Log comment creation activity."""
        return ActivityService.create_activity(
            db=db,
            action_type="comment_create",
            user_id=user_id,
            target_id=comment_id,
            description=f"Commented on article #{article_id}"
        )

    @staticmethod
    def get_enhanced_activities(
        db: Session,
        start_date: datetime,
        user_id: Optional[int] = None,
        limit: int = 100,
        public_only: bool = False
    ) -> List[EnhancedActivityResponse]:
        """Get enhanced activities with detailed information."""
        # 查询活动记录
        query = db.query(models.Activity).filter(models.Activity.created_at >= start_date)

        if user_id:
            query = query.filter(models.Activity.user_id == user_id)

        # 如果是公开活动，只获取文章创建和评论创建的活动
        if public_only:
            query = query.filter(models.Activity.action_type.in_(["article_create", "comment_create"]))

        activities = query.order_by(models.Activity.created_at.desc()).limit(limit).all()

        # 收集所有用户ID和目标ID
        user_ids = set(activity.user_id for activity in activities)

        # 按活动类型分组目标ID
        article_ids = set()
        comment_ids = set()

        for activity in activities:
            if activity.action_type in ["article_create", "article_update", "like"]:
                article_ids.add(activity.target_id)
            elif activity.action_type == "comment_create":
                comment_ids.add(activity.target_id)

        # 批量查询用户信息
        users = {}
        if user_ids:
            user_records = db.query(models.User).filter(models.User.id.in_(user_ids)).all()
            users = {user.id: user for user in user_records}

        # 批量查询文章信息
        articles = {}
        if article_ids:
            article_records = db.query(models.Article).filter(models.Article.id.in_(article_ids)).all()
            articles = {article.id: article for article in article_records}

        # 批量查询评论信息
        comments = {}
        if comment_ids:
            comment_records = db.query(models.Comment).filter(models.Comment.id.in_(comment_ids)).all()
            comments = {comment.id: comment for comment in comment_records}

        # 构建增强的活动响应
        result = []
        for activity in activities:
            # 获取用户信息
            user = None
            if activity.user_id in users:
                user_obj = users[activity.user_id]
                user = schemas.UserBriefResponse(
                    id=user_obj.id,
                    username=user_obj.username,
                    avatar=user_obj.avatar
                )

            # 获取目标详情
            target_detail = None
            formatted_description = activity.description

            if activity.action_type in ["article_create", "article_update", "like"]:
                if activity.target_id in articles:
                    article = articles[activity.target_id]
                    target_detail = ActivityDetail(
                        title=article.title,
                        slug=article.slug,
                        content_preview=article.excerpt[:100] if article.excerpt else None
                    )

                    # 格式化描述
                    action_verb = "创建了" if activity.action_type == "article_create" else \
                                "更新了" if activity.action_type == "article_update" else "点赞了"
                    formatted_description = f"{action_verb}文章 《{article.title}》"

            elif activity.action_type == "comment_create":
                if activity.target_id in comments:
                    comment = comments[activity.target_id]
                    article_id = comment.article_id
                    article_title = "未知文章"

                    if article_id in articles:
                        article_title = articles[article_id].title

                    target_detail = ActivityDetail(
                        title=article_title,
                        content_preview=comment.content[:100] if comment.content else None
                    )

                    # 格式化描述
                    formatted_description = f"评论了文章 《{article_title}》"

            # 计算相对时间
            now = datetime.now(timezone.utc)

            # 安全地处理时区问题
            try:
                # 确保 activity.created_at 有时区信息
                if activity.created_at.tzinfo is None:
                    activity_time = activity.created_at.replace(tzinfo=timezone.utc)
                else:
                    activity_time = activity.created_at

                # 使用中文相对时间
                relative_time = get_relative_time_zh(activity_time, now)
            except Exception as e:
                # 如果出现错误，使用默认值
                print(f"Error calculating relative time: {e}")
                relative_time = "最近"

            # 创建增强的活动响应
            enhanced_activity = EnhancedActivityResponse(
                id=activity.id,
                action_type=activity.action_type,
                user_id=activity.user_id,
                target_id=activity.target_id,
                description=activity.description,
                created_at=activity.created_at,
                user=user,
                target_detail=target_detail,
                formatted_description=formatted_description,
                relative_time=relative_time
            )

            result.append(enhanced_activity)

        return result

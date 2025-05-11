from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from fastapi import HTTPException, status
from datetime import datetime, timezone
import json

from app import models
from app.schemas.comment import CommentBase, CommentCreate, CommentResponse, CommentUpdate, CommentWithReplies, CommentBrief, CommentBriefNoSocial
from app.utils.logging import get_logger
from app.utils.pagination import PaginationParams, PagedResponse
from app.services.content_filter_service import ContentFilterService
from app.services.ip_location_service import IPLocationService
from app.services.unified_cache_service import cached
from app.services.site_settings_service import SiteSettingsService

logger = get_logger(__name__)

class CommentService:
    """Service for comment-related operations."""

    @staticmethod
    @cached(prefix="comment_by_id", ttl=300)
    def get_comment_by_id(db: Session, comment_id: int) -> Optional[models.Comment]:
        """Get a comment by ID."""
        return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    @staticmethod
    @cached(prefix="comments_by_article", ttl=60)
    def get_comments_by_article(
        db: Session,
        article_id: int,
        params: PaginationParams,
        approved_only: bool = True,
        sort_by: str = "newest",
        parent_only: bool = True,
        current_user: Optional[models.User] = None
    ) -> PagedResponse[CommentWithReplies]:
        """
        Get comments for an article with pagination and sorting.

        Args:
            db: Database session
            article_id: ID of the article
            params: Pagination parameters
            approved_only: Whether to return only approved comments
            sort_by: Sorting method ("newest", "oldest", "most_liked")
            parent_only: Whether to return only top-level comments

        Returns:
            Paginated response with comments and their replies
        """
        # 获取文章标题
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        article_title = article.title if article else None

        # Base query for parent comments
        query = db.query(models.Comment).filter(
            models.Comment.article_id == article_id
        )

        # Filter by approval status if needed
        if approved_only:
            query = query.filter(models.Comment.is_approved == True)

        # Filter for parent comments only if requested
        if parent_only:
            query = query.filter(models.Comment.parent_id == None)

        # Apply sorting
        if sort_by == "oldest":
            query = query.order_by(asc(models.Comment.created_at))
        elif sort_by == "most_liked":
            query = query.order_by(desc(models.Comment.like_count), desc(models.Comment.created_at))
        else:  # default to "newest"
            query = query.order_by(desc(models.Comment.created_at))

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        comments = query.offset(params.skip).limit(params.page_size).all()

        # Prepare result with replies
        result = []
        for comment in comments:
            # Get replies for this comment
            replies_query = db.query(models.Comment).filter(
                models.Comment.parent_id == comment.id
            )

            if approved_only:
                replies_query = replies_query.filter(models.Comment.is_approved == True)

            replies = replies_query.order_by(asc(models.Comment.created_at)).all()

            # 处理用户的社交媒体字段
            if comment.user and comment.user.social_media and isinstance(comment.user.social_media, str):
                try:
                    comment.user.social_media = json.loads(comment.user.social_media)
                except json.JSONDecodeError:
                    comment.user.social_media = None

            # 处理回复中用户的社交媒体字段
            for reply in replies:
                if reply.user and reply.user.social_media and isinstance(reply.user.social_media, str):
                    try:
                        reply.user.social_media = json.loads(reply.user.social_media)
                    except json.JSONDecodeError:
                        reply.user.social_media = None

            # Convert to schema
            comment_dict = CommentWithReplies.model_validate(comment)
            comment_dict.article_title = article_title

            # 批量获取用户信息，解决 N+1 查询问题
            # 收集所有评论和回复的用户ID
            all_user_ids = []
            if comment.user_id:
                all_user_ids.append(comment.user_id)

            for reply in replies:
                if reply.user_id:
                    all_user_ids.append(reply.user_id)

            # 去重
            unique_user_ids = list(set(all_user_ids))

            # 批量查询用户
            users = {}
            user_social_media = {}
            if unique_user_ids:
                user_records = db.query(models.User.id, models.User.username, models.User.social_media).filter(
                    models.User.id.in_(unique_user_ids)
                ).all()
                users = {user.id: user.username for user in user_records}

                # 处理社交媒体字段
                for user in user_records:
                    if user.social_media:
                        try:
                            user_social_media[user.id] = json.loads(user.social_media)
                        except json.JSONDecodeError:
                            user_social_media[user.id] = None

            # 设置评论者名称
            if comment.user_id:
                # 如果是当前登录用户的评论，直接使用当前用户对象
                if current_user and current_user.id == comment.user_id:
                    comment_dict.commenter_name = current_user.username
                    # 处理当前用户的社交媒体字段
                    if current_user.social_media:
                        try:
                            comment_dict.user.social_media = json.loads(current_user.social_media) if isinstance(current_user.social_media, str) else current_user.social_media
                        except json.JSONDecodeError:
                            comment_dict.user.social_media = None
                else:
                    comment_dict.commenter_name = users.get(comment.user_id, "未知用户")
                    # 设置用户的社交媒体字段
                    if comment_dict.user and comment.user_id in user_social_media:
                        comment_dict.user.social_media = user_social_media[comment.user_id]
            else:
                comment_dict.commenter_name = comment.anonymous_name or "匿名用户"

            # 处理回复
            replies_with_names = []
            for reply in replies:
                reply_dict = CommentBrief.model_validate(reply)

                # 设置回复者名称
                if reply.user_id:
                    # 如果是当前登录用户的回复，直接使用当前用户对象
                    if current_user and current_user.id == reply.user_id:
                        reply_dict.commenter_name = current_user.username
                        # 处理当前用户的社交媒体字段
                        if current_user.social_media:
                            try:
                                reply_dict.user.social_media = json.loads(current_user.social_media) if isinstance(current_user.social_media, str) else current_user.social_media
                            except json.JSONDecodeError:
                                reply_dict.user.social_media = None
                    else:
                        reply_dict.commenter_name = users.get(reply.user_id, "未知用户")
                        # 设置用户的社交媒体字段
                        if reply_dict.user and reply.user_id in user_social_media:
                            reply_dict.user.social_media = user_social_media[reply.user_id]
                else:
                    reply_dict.commenter_name = reply.anonymous_name or "匿名用户"

                replies_with_names.append(reply_dict)

            comment_dict.replies = replies_with_names
            result.append(comment_dict)

        # Create paginated response
        return PagedResponse.create(result, total, params)

    @staticmethod
    async def create_comment(
        db: Session,
        comment: CommentCreate,
        ip_address: str,
        api_key: Optional[str] = None,
        user_id: Optional[int] = None,  # 用户ID只能从 token 中获取，不能由用户传入
        anonymous_name: Optional[str] = None
    ) -> models.Comment:
        """Create a new comment."""
        # Check if article exists
        article = db.query(models.Article).filter(models.Article.id == comment.article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

        # Check if parent comment exists if specified
        if comment.parent_id:
            parent_comment = CommentService.get_comment_by_id(db, comment.parent_id)
            if not parent_comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent comment not found"
                )

            # Ensure parent comment belongs to the same article
            if parent_comment.article_id != comment.article_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parent comment does not belong to the specified article"
                )

        # Get IP location
        ip_region = IPLocationService.get_location(ip_address)

        # 获取系统设置
        site_settings = SiteSettingsService.get_settings(db)

        # 确定是否需要审核所有评论（包括已登录用户）
        review_all = site_settings and site_settings.comment_review_all

        # 确定是否使用AI审核
        use_ai_review = site_settings and site_settings.comment_ai_review

        # 获取API密钥（优先使用传入的API密钥，其次使用系统设置中的API密钥）
        review_api_key = api_key or (site_settings and site_settings.comment_review_api_key)

        # 确定评论是否应该自动批准
        # 如果设置了审核所有评论，则已登录用户的评论也需要审核
        # 否则，已登录用户的评论自动批准
        is_auto_approved = user_id is not None and not review_all

        # 需要审核的评论（匿名评论或已登录用户的评论但设置了审核所有评论）
        ai_approved = True
        if not is_auto_approved and use_ai_review and review_api_key:
            # 使用AI审核内容
            ai_approved, reason = await ContentFilterService.moderate_content(comment.content, review_api_key)
            if not ai_approved:
                logger.warning(f"Comment rejected by AI: {reason}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"评论被拒绝: {reason}"
                )

        # 创建评论
        db_comment = models.Comment(
            content=comment.content,
            article_id=comment.article_id,
            parent_id=comment.parent_id,
            user_id=user_id,
            ip_address=ip_address,
            ip_region=ip_region,
            anonymous_name=anonymous_name,  # 使用传入的匿名名称参数
            # 已登录用户或AI审核通过的评论自动批准
            is_approved=is_auto_approved or ai_approved,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            like_count=0
        )

        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)

        # Create notification for article author if different from commenter
        if article.author_id and article.author_id != user_id:
            notification = models.Notification(
                user_id=article.author_id,
                title="新评论",
                content=f"您的文章《{article.title}》收到了新评论",
                type="comment",
                reference_id=db_comment.id,
                is_read=False,
                created_at=datetime.now(timezone.utc)
            )
            db.add(notification)

            # Create notification for parent comment author if different from commenter
            if comment.parent_id:
                parent_comment = CommentService.get_comment_by_id(db, comment.parent_id)
                if parent_comment and parent_comment.user_id and parent_comment.user_id != user_id:
                    reply_notification = models.Notification(
                        user_id=parent_comment.user_id,
                        title="评论回复",
                        content=f"您的评论收到了新回复",
                        type="reply",
                        reference_id=db_comment.id,
                        is_read=False,
                        created_at=datetime.now(timezone.utc)
                    )
                    db.add(reply_notification)

            db.commit()

        logger.info(f"Created new comment on article {comment.article_id}")
        return db_comment

    @staticmethod
    def update_comment(
        db: Session,
        comment_id: int,
        comment_update: CommentUpdate,
        user_id: int
    ) -> models.Comment:
        """Update a comment."""
        db_comment = CommentService.get_comment_by_id(db, comment_id)
        if not db_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        # Check if user is the author of the comment
        if db_comment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        # Update comment
        db_comment.content = comment_update.content
        db_comment.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_comment)

        logger.info(f"Updated comment {comment_id}")
        return db_comment

    @staticmethod
    def approve_comment(db: Session, comment_id: int) -> models.Comment:
        """Approve a comment."""
        db_comment = CommentService.get_comment_by_id(db, comment_id)
        if not db_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        db_comment.is_approved = True
        db.commit()
        db.refresh(db_comment)

        logger.info(f"Approved comment {comment_id}")
        return db_comment

    @staticmethod
    def delete_comment(db: Session, comment_id: int, user_id: int, is_admin: bool = False) -> bool:
        """Delete a comment."""
        db_comment = CommentService.get_comment_by_id(db, comment_id)
        if not db_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        # Check if user is the author of the comment or an admin
        if not is_admin and db_comment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        db.delete(db_comment)
        db.commit()

        logger.info(f"Deleted comment {comment_id}")
        return True

    @staticmethod
    def like_comment(db: Session, comment_id: int, user_id: int) -> Dict[str, Any]:
        """Like or unlike a comment."""
        db_comment = CommentService.get_comment_by_id(db, comment_id)
        if not db_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        # Check if user has already liked this comment
        existing_like = db.query(models.Activity).filter(
            models.Activity.user_id == user_id,
            models.Activity.target_id == comment_id,
            models.Activity.action_type == "comment_like"
        ).first()

        if existing_like:
            # User has already liked this comment, so unlike it
            db.delete(existing_like)
            db_comment.like_count = max(0, db_comment.like_count - 1)  # Ensure like_count doesn't go below 0
            db.commit()
            db.refresh(db_comment)

            return {
                "comment_id": comment_id,
                "like_count": db_comment.like_count,
                "message": "取消点赞成功"
            }
        else:
            # User hasn't liked this comment yet, so like it
            new_activity = models.Activity(
                action_type="comment_like",
                user_id=user_id,
                target_id=comment_id,
                description=f"用户点赞了评论 #{comment_id}",
                created_at=datetime.now(timezone.utc)
            )
            db.add(new_activity)

            db_comment.like_count += 1
            db.commit()
            db.refresh(db_comment)

            return {
                "comment_id": comment_id,
                "like_count": db_comment.like_count,
                "message": "点赞成功"
            }

    @staticmethod
    def get_pending_comments(
        db: Session,
        params: PaginationParams,
        article_ids: Optional[List[int]] = None,
        parent_only: bool = False
    ) -> PagedResponse[CommentResponse]:
        """
        Get pending comments for admin approval.

        Args:
            db: Database session
            params: Pagination parameters
            article_ids: Optional list of article IDs to filter by (for editors)
            parent_only: Whether to return only top-level comments
        """
        query = db.query(models.Comment).filter(models.Comment.is_approved == False)

        # 如果指定了文章ID列表，则只获取这些文章的评论
        if article_ids is not None:
            if not article_ids:  # 如果是空列表，返回空结果
                return PagedResponse.create([], 0, params)
            query = query.filter(models.Comment.article_id.in_(article_ids))

        # Filter for parent comments only if requested
        if parent_only:
            query = query.filter(models.Comment.parent_id == None)

        # Get total count before pagination
        total = query.count()

        # Apply pagination and ordering (newest first)
        comments = query.order_by(desc(models.Comment.created_at)).offset(params.skip).limit(params.page_size).all()

        # 获取所有评论相关的文章ID
        article_ids = [comment.article_id for comment in comments]

        # 获取文章标题
        articles = db.query(models.Article.id, models.Article.title).filter(
            models.Article.id.in_(article_ids)
        ).all()

        # 创建文章ID到标题的映射
        article_titles = {article.id: article.title for article in articles}

        # 批量获取用户信息，解决 N+1 查询问题
        user_ids = [comment.user_id for comment in comments if comment.user_id is not None]
        users = {}
        user_social_media = {}
        if user_ids:
            user_records = db.query(models.User.id, models.User.username, models.User.social_media).filter(
                models.User.id.in_(user_ids)
            ).all()
            users = {user.id: user.username for user in user_records}

            # 处理社交媒体字段
            for user in user_records:
                if user.social_media:
                    try:
                        user_social_media[user.id] = json.loads(user.social_media)
                    except json.JSONDecodeError:
                        user_social_media[user.id] = None

        # 获取所有回复评论的父评论ID
        parent_ids = [comment.parent_id for comment in comments if comment.parent_id is not None]

        # 批量获取父评论
        parent_comments = {}
        if parent_ids:
            parent_records = db.query(models.Comment).filter(
                models.Comment.id.in_(parent_ids)
            ).all()
            parent_comments = {parent.id: parent for parent in parent_records}

        # Convert to schema
        result = []

        # 如果只获取父评论，则需要获取每个父评论的回复
        if parent_only:
            # 获取所有父评论的ID
            parent_ids = [comment.id for comment in comments]

            # 获取所有回复
            replies_query = db.query(models.Comment).filter(
                models.Comment.parent_id.in_(parent_ids),
                models.Comment.is_approved == False  # 只获取待审核的回复
            )

            # 如果指定了文章ID列表，则只获取这些文章的评论回复
            if article_ids is not None and article_ids:
                replies_query = replies_query.filter(models.Comment.article_id.in_(article_ids))

            # 获取所有回复
            all_replies = replies_query.all()

            # 按父评论ID组织回复
            replies_by_parent = {}
            for reply in all_replies:
                if reply.parent_id not in replies_by_parent:
                    replies_by_parent[reply.parent_id] = []
                replies_by_parent[reply.parent_id].append(reply)

        for comment in comments:
            # 如果是回复评论且不是只获取父评论，确保父评论信息可用
            if not parent_only and comment.parent_id and comment.parent_id in parent_comments:
                # 将父评论对象设置到当前评论的parent属性
                comment.parent = parent_comments[comment.parent_id]

            # 创建评论字典
            if parent_only:
                # 使用带有回复的模型
                comment_dict = CommentWithReplies.model_validate(comment)
            else:
                # 使用普通评论模型
                comment_dict = CommentResponse.model_validate(comment)

            comment_dict.article_title = article_titles.get(comment.article_id)

            # 设置评论者名称
            if comment.user_id:
                comment_dict.commenter_name = users.get(comment.user_id, "未知用户")
                # 不再处理社交媒体字段
            else:
                comment_dict.commenter_name = comment.anonymous_name or "匿名用户"

            # 如果只获取父评论，添加回复
            if parent_only and comment.id in replies_by_parent:
                replies = replies_by_parent[comment.id]
                replies_with_names = []

                for reply in replies:
                    # 使用不包含社交媒体字段的模型
                    reply_dict = CommentBriefNoSocial.model_validate(reply)

                    # 设置回复者名称
                    if reply.user_id:
                        reply_dict.commenter_name = users.get(reply.user_id, "未知用户")
                        # 不再处理社交媒体字段
                    else:
                        reply_dict.commenter_name = reply.anonymous_name or "匿名用户"

                    replies_with_names.append(reply_dict)

                comment_dict.replies = replies_with_names

            result.append(comment_dict)

        # Create paginated response
        return PagedResponse.create(result, total, params)

    @staticmethod
    def get_all_comments(
        db: Session,
        params: PaginationParams,
        approved_only: Optional[bool] = None,
        user_id: Optional[int] = None,
        sort_by: str = "newest",
        current_user: Optional[models.User] = None,
        parent_only: bool = False
    ) -> PagedResponse[CommentResponse]:
        """Get all comments with pagination and filtering.

        Args:
            db: Database session
            params: Pagination parameters
            approved_only: Filter by approval status (None for all, True for approved only, False for pending only)
            user_id: Filter by user ID
            sort_by: Sorting method ("newest", "oldest", "most_liked")
            current_user: Optional current user object
            parent_only: Whether to return only top-level comments

        Returns:
            Paginated response with comments
        """
        # Base query
        query = db.query(models.Comment)

        # Apply filters
        if approved_only is not None:
            query = query.filter(models.Comment.is_approved == approved_only)

        if user_id is not None:
            query = query.filter(models.Comment.user_id == user_id)

        # Filter for parent comments only if requested
        if parent_only:
            query = query.filter(models.Comment.parent_id == None)

        # Apply sorting
        if sort_by == "oldest":
            query = query.order_by(asc(models.Comment.created_at))
        elif sort_by == "most_liked":
            query = query.order_by(desc(models.Comment.like_count), desc(models.Comment.created_at))
        else:  # default to "newest"
            query = query.order_by(desc(models.Comment.created_at))

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        comments = query.offset(params.skip).limit(params.page_size).all()

        # 获取所有评论相关的文章ID
        article_ids = [comment.article_id for comment in comments]

        # 获取所有回复评论的父评论ID
        parent_ids = [comment.parent_id for comment in comments if comment.parent_id is not None]

        # 获取父评论内容
        parent_comments = {}
        if parent_ids:
            parent_query = db.query(models.Comment).filter(models.Comment.id.in_(parent_ids))
            for parent in parent_query.all():
                parent_comments[parent.id] = parent

        # 获取文章标题
        articles = db.query(models.Article.id, models.Article.title).filter(
            models.Article.id.in_(article_ids)
        ).all()

        # 创建文章ID到标题的映射
        article_titles = {article.id: article.title for article in articles}

        # 批量获取用户信息，解决 N+1 查询问题
        user_ids = [comment.user_id for comment in comments if comment.user_id is not None]
        users = {}
        user_social_media = {}
        if user_ids:
            user_records = db.query(models.User.id, models.User.username, models.User.social_media).filter(
                models.User.id.in_(user_ids)
            ).all()
            users = {user.id: user.username for user in user_records}

            # 处理社交媒体字段
            for user in user_records:
                if user.social_media:
                    try:
                        user_social_media[user.id] = json.loads(user.social_media)
                    except json.JSONDecodeError:
                        user_social_media[user.id] = None

        # 获取所有回复评论的父评论ID
        parent_ids = [comment.parent_id for comment in comments if comment.parent_id is not None]

        # 批量获取父评论
        parent_comments = {}
        if parent_ids:
            parent_records = db.query(models.Comment).filter(
                models.Comment.id.in_(parent_ids)
            ).all()
            parent_comments = {parent.id: parent for parent in parent_records}

        # Convert to schema
        result = []

        # 如果只获取父评论，则需要获取每个父评论的回复
        if parent_only:
            # 获取所有父评论的ID
            parent_ids = [comment.id for comment in comments]

            # 获取所有回复
            replies_query = db.query(models.Comment).filter(
                models.Comment.parent_id.in_(parent_ids)
            )

            # 如果需要过滤已审核评论
            if approved_only is not None:
                replies_query = replies_query.filter(models.Comment.is_approved == approved_only)

            # 获取所有回复
            all_replies = replies_query.all()

            # 按父评论ID组织回复
            replies_by_parent = {}
            for reply in all_replies:
                if reply.parent_id not in replies_by_parent:
                    replies_by_parent[reply.parent_id] = []
                replies_by_parent[reply.parent_id].append(reply)

        for comment in comments:
            # 如果是回复评论且不是只获取父评论，确保父评论信息可用
            if not parent_only and comment.parent_id and comment.parent_id in parent_comments:
                # 将父评论对象设置到当前评论的parent属性
                comment.parent = parent_comments[comment.parent_id]

            # 创建评论字典
            if parent_only:
                # 使用带有回复的模型
                comment_dict = CommentWithReplies.model_validate(comment)
            else:
                # 使用普通评论模型
                comment_dict = CommentResponse.model_validate(comment)

            comment_dict.article_title = article_titles.get(comment.article_id)

            # 设置评论者名称
            if comment.user_id:
                # 如果是当前登录用户的评论，直接使用当前用户对象
                if current_user and current_user.id == comment.user_id:
                    comment_dict.commenter_name = current_user.username
                    # 不再处理社交媒体字段
                else:
                    comment_dict.commenter_name = users.get(comment.user_id, "未知用户")
                    # 不再处理社交媒体字段
            else:
                comment_dict.commenter_name = comment.anonymous_name or "匿名用户"

            # 如果只获取父评论，添加回复
            if parent_only and comment.id in replies_by_parent:
                replies = replies_by_parent[comment.id]
                replies_with_names = []

                for reply in replies:
                    # 使用不包含社交媒体字段的模型
                    reply_dict = CommentBriefNoSocial.model_validate(reply)

                    # 设置回复者名称
                    if reply.user_id:
                        # 如果是当前登录用户的回复，直接使用当前用户对象
                        if current_user and current_user.id == reply.user_id:
                            reply_dict.commenter_name = current_user.username
                            # 不再处理社交媒体字段
                        else:
                            reply_dict.commenter_name = users.get(reply.user_id, "未知用户")
                            # 不再处理社交媒体字段
                    else:
                        reply_dict.commenter_name = reply.anonymous_name or "匿名用户"

                    replies_with_names.append(reply_dict)

                comment_dict.replies = replies_with_names

            result.append(comment_dict)

        # Create paginated response
        return PagedResponse.create(result, total, params)
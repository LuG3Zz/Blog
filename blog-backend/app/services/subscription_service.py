from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
import secrets
from datetime import datetime, timezone

from app import models
from app.schemas.subscription import NotificationCreate, EmailSubscriptionCreate
from app.models.subscription import SubscriptionType
from app.services.email_service import EmailService
from app.utils.logging import get_logger

logger = get_logger(__name__)

class EmailSubscriptionService:
    """Service for email subscription operations."""

    @staticmethod
    def generate_token() -> str:
        """Generate a unique token for email subscription."""
        return secrets.token_urlsafe(32)

    @staticmethod
    def create_email_subscription(
        db: Session,
        subscription: EmailSubscriptionCreate
    ) -> models.EmailSubscription:
        """Create a new email subscription."""
        # Check if email is already subscribed to this type and reference
        existing = db.query(models.EmailSubscription).filter(
            models.EmailSubscription.email == subscription.email,
            models.EmailSubscription.subscription_type == subscription.subscription_type,
            models.EmailSubscription.reference_id == subscription.reference_id,
            models.EmailSubscription.is_active == True
        ).first()

        if existing:
            return existing

        # Generate token
        token = EmailSubscriptionService.generate_token()

        # Create subscription
        db_subscription = models.EmailSubscription(
            email=subscription.email,
            subscription_type=subscription.subscription_type,
            reference_id=subscription.reference_id,
            token=token,
            is_active=True
        )

        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)

        logger.info(f"Created email subscription for {subscription.email}")
        return db_subscription

    @staticmethod
    def get_email_subscriptions(
        db: Session,
        email: Optional[str] = None,
        subscription_type: Optional[SubscriptionType] = None,
        reference_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get email subscriptions with optional filters and pagination."""
        query = db.query(models.EmailSubscription)

        if email:
            query = query.filter(models.EmailSubscription.email.ilike(f"%{email}%"))

        if subscription_type:
            query = query.filter(models.EmailSubscription.subscription_type == subscription_type)

        if reference_id is not None:
            query = query.filter(models.EmailSubscription.reference_id == reference_id)

        if is_active is not None:
            query = query.filter(models.EmailSubscription.is_active == is_active)

        # 获取总数
        total = query.count()

        # 应用排序和分页
        items = query.order_by(models.EmailSubscription.created_at.desc())\
            .offset(skip).limit(limit).all()

        # 获取引用对象名称
        for subscription in items:
            if subscription.subscription_type == SubscriptionType.AUTHOR and subscription.reference_id:
                author = db.query(models.User).filter(models.User.id == subscription.reference_id).first()
                if author:
                    subscription.reference_name = author.username
            elif subscription.subscription_type == SubscriptionType.CATEGORY and subscription.reference_id:
                category = db.query(models.Category).filter(models.Category.id == subscription.reference_id).first()
                if category:
                    subscription.reference_name = category.name

        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "page_size": limit
        }

    @staticmethod
    def unsubscribe_by_token(db: Session, token: str) -> bool:
        """Unsubscribe using a token."""
        subscription = db.query(models.EmailSubscription).filter(
            models.EmailSubscription.token == token,
            models.EmailSubscription.is_active == True
        ).first()

        if not subscription:
            return False

        subscription.is_active = False
        subscription.updated_at = datetime.now(timezone.utc)
        db.commit()

        logger.info(f"Unsubscribed email {subscription.email} using token")
        return True

    @staticmethod
    def unsubscribe_by_email(
        db: Session,
        email: str,
        subscription_type: Optional[SubscriptionType] = None,
        reference_id: Optional[int] = None
    ) -> int:
        """Unsubscribe an email from all or specific subscriptions."""
        query = db.query(models.EmailSubscription).filter(
            models.EmailSubscription.email == email,
            models.EmailSubscription.is_active == True
        )

        if subscription_type:
            query = query.filter(models.EmailSubscription.subscription_type == subscription_type)

        if reference_id is not None:
            query = query.filter(models.EmailSubscription.reference_id == reference_id)

        subscriptions = query.all()
        count = 0

        for subscription in subscriptions:
            subscription.is_active = False
            subscription.updated_at = datetime.now(timezone.utc)
            count += 1

        if count > 0:
            db.commit()
            logger.info(f"Unsubscribed email {email} from {count} subscriptions")

        return count

    @staticmethod
    def update_subscription_status(
        db: Session,
        subscription_id: int,
        is_active: bool
    ) -> Optional[models.EmailSubscription]:
        """Update the status of an email subscription."""
        subscription = db.query(models.EmailSubscription).filter(
            models.EmailSubscription.id == subscription_id
        ).first()

        if not subscription:
            return None

        subscription.is_active = is_active
        subscription.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(subscription)

        logger.info(f"Updated subscription status for ID {subscription_id} to {is_active}")
        return subscription

    @staticmethod
    async def send_article_notification_emails(
        db: Session,
        article_id: int,
        article_title: str,
        article_excerpt: str,
        article_url: str,
        author_name: str,
        author_id: int,
        category_id: int,
        category_name: str
    ) -> int:
        """Send email notifications to subscribers about a new article."""
        # Get author subscribers
        author_result = EmailSubscriptionService.get_email_subscriptions(
            db=db,
            subscription_type=SubscriptionType.AUTHOR,
            reference_id=author_id,
            is_active=True
        )
        author_subscriptions = author_result.get('items', [])
        logger.info(f"找到 {len(author_subscriptions)} 个作者订阅者")

        # Get category subscribers
        category_result = EmailSubscriptionService.get_email_subscriptions(
            db=db,
            subscription_type=SubscriptionType.CATEGORY,
            reference_id=category_id,
            is_active=True
        )
        category_subscriptions = category_result.get('items', [])
        logger.info(f"找到 {len(category_subscriptions)} 个分类订阅者")

        # Get all articles subscribers
        all_result = EmailSubscriptionService.get_email_subscriptions(
            db=db,
            subscription_type=SubscriptionType.ALL,
            is_active=True
        )
        all_subscriptions = all_result.get('items', [])
        logger.info(f"找到 {len(all_subscriptions)} 个全站订阅者")

        # Combine subscribers (avoiding duplicates)
        email_set = set()
        all_subscriptions_map = {}

        for subscription in author_subscriptions + category_subscriptions + all_subscriptions:
            if subscription.email not in email_set:
                email_set.add(subscription.email)
                all_subscriptions_map[subscription.email] = subscription

        # Send emails
        email_count = 0
        for email, subscription in all_subscriptions_map.items():
            # Create email content
            subject = f"新文章发布: {article_title}"

            # 根据订阅类型自定义内容
            subscription_type_text = ""
            if subscription.subscription_type == SubscriptionType.AUTHOR:
                subscription_type_text = f"您订阅的作者 {author_name}"
            elif subscription.subscription_type == SubscriptionType.CATEGORY:
                subscription_type_text = f"您订阅的分类 {category_name}"
            else:
                subscription_type_text = "您订阅的博客"

            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
                <h2 style="color: #333; text-align: center;">{article_title}</h2>
                <p>您好，</p>
                <p>{subscription_type_text} 发布了新文章:</p>
                <div style="background-color: #f5f5f5; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
                    <p style="font-style: italic;">{article_excerpt}</p>
                </div>
                <p>作者: {author_name}</p>
                <p>分类: {category_name}</p>
                <div style="text-align: center; margin: 25px 0;">
                    <a href="{article_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        阅读全文
                    </a>
                </div>
                <p style="margin-top: 30px; font-size: 12px; color: #999;">
                    如果您不想再收到此类邮件，<a href="{article_url}/unsubscribe?token={subscription.token}">点击这里取消订阅</a>。
                </p>
                <p style="font-size: 12px; color: #999; text-align: center;">
                    此邮件由系统自动发送，请勿回复。
                </p>
            </div>
            """

            try:
                # 发送邮件
                await EmailService.send_email(
                    to_email=email,
                    subject=subject,
                    html_content=html_content
                )
                email_count += 1
                logger.info(f"Sent article notification email to {email}")
            except Exception as e:
                logger.error(f"Failed to send article notification email to {email}: {str(e)}")

        return email_count

class SubscriptionService:
    """Service for subscription-related operations."""

    @staticmethod
    def subscribe_to_category(db: Session, user_id: int, category_id: int) -> bool:
        """Subscribe a user to a category."""
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if category exists
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        # Check if already subscribed
        if category in user.subscribed_categories:
            return False

        # Add subscription
        user.subscribed_categories.append(category)
        db.commit()

        logger.info(f"User {user_id} subscribed to category {category_id}")
        return True

    @staticmethod
    def unsubscribe_from_category(db: Session, user_id: int, category_id: int) -> bool:
        """Unsubscribe a user from a category."""
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if category exists
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        # Check if subscribed
        if category not in user.subscribed_categories:
            return False

        # Remove subscription
        user.subscribed_categories.remove(category)
        db.commit()

        logger.info(f"User {user_id} unsubscribed from category {category_id}")
        return True

    @staticmethod
    def subscribe_to_author(db: Session, subscriber_id: int, author_id: int) -> bool:
        """Subscribe a user to an author."""
        # Check if subscriber exists
        subscriber = db.query(models.User).filter(models.User.id == subscriber_id).first()
        if not subscriber:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscriber not found"
            )

        # Check if author exists
        author = db.query(models.User).filter(models.User.id == author_id).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )

        # Check if subscriber is trying to subscribe to themselves
        if subscriber_id == author_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot subscribe to yourself"
            )

        # Check if already subscribed
        if author in subscriber.subscribed_authors:
            return False

        # Add subscription
        subscriber.subscribed_authors.append(author)
        db.commit()

        logger.info(f"User {subscriber_id} subscribed to author {author_id}")
        return True

    @staticmethod
    def unsubscribe_from_author(db: Session, subscriber_id: int, author_id: int) -> bool:
        """Unsubscribe a user from an author."""
        # Check if subscriber exists
        subscriber = db.query(models.User).filter(models.User.id == subscriber_id).first()
        if not subscriber:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscriber not found"
            )

        # Check if author exists
        author = db.query(models.User).filter(models.User.id == author_id).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )

        # Check if subscribed
        if author not in subscriber.subscribed_authors:
            return False

        # Remove subscription
        subscriber.subscribed_authors.remove(author)
        db.commit()

        logger.info(f"User {subscriber_id} unsubscribed from author {author_id}")
        return True

    @staticmethod
    def get_user_subscriptions(db: Session, user_id: int) -> Dict[str, List[int]]:
        """Get a user's subscriptions."""
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Get subscribed categories
        category_ids = [category.id for category in user.subscribed_categories]

        # Get subscribed authors
        author_ids = [author.id for author in user.subscribed_authors]

        return {
            "category_ids": category_ids,
            "author_ids": author_ids
        }

class NotificationService:
    """Service for notification-related operations."""

    @staticmethod
    def create_notification(db: Session, notification: NotificationCreate) -> models.Notification:
        """Create a new notification."""
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == notification.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create notification
        db_notification = models.Notification(
            user_id=notification.user_id,
            title=notification.title,
            content=notification.content,
            type=notification.type,
            reference_id=notification.reference_id
        )

        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)

        logger.info(f"Created notification for user {notification.user_id}")
        return db_notification

    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False
    ) -> List[models.Notification]:
        """Get a user's notifications."""
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Build query
        query = db.query(models.Notification).filter(models.Notification.user_id == user_id)

        # Filter by read status if requested
        if unread_only:
            query = query.filter(models.Notification.is_read == False)

        # Apply pagination and ordering
        notifications = query.order_by(models.Notification.created_at.desc())\
            .offset(skip).limit(limit).all()

        return notifications

    @staticmethod
    def mark_notification_as_read(db: Session, notification_id: int, user_id: int) -> models.Notification:
        """Mark a notification as read."""
        # Get notification
        notification = db.query(models.Notification).filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == user_id
        ).first()

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )

        # Mark as read
        notification.is_read = True
        db.commit()
        db.refresh(notification)

        return notification

    @staticmethod
    def mark_all_notifications_as_read(db: Session, user_id: int) -> int:
        """Mark all notifications for a user as read."""
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update all unread notifications
        result = db.query(models.Notification).filter(
            models.Notification.user_id == user_id,
            models.Notification.is_read == False
        ).update({"is_read": True})

        db.commit()

        return result

    @staticmethod
    def delete_notification(db: Session, notification_id: int, user_id: int) -> bool:
        """Delete a notification."""
        # Get notification
        notification = db.query(models.Notification).filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == user_id
        ).first()

        if not notification:
            return False

        # Delete notification
        db.delete(notification)
        db.commit()

        return True

    @staticmethod
    async def notify_subscribers_new_article(
        db: Session,
        article_id: int,
        title: str,
        excerpt: str,
        author_id: int,
        author_name: str,
        category_id: int,
        category_name: str,
        article_url: str
    ) -> Dict[str, int]:
        """Notify subscribers about a new article."""
        # Get article author's subscribers
        author_subscribers = db.query(models.User).filter(
            models.User.subscribed_authors.any(models.User.id == author_id)
        ).all()

        # Get category subscribers
        category_subscribers = db.query(models.User).filter(
            models.User.subscribed_categories.any(models.Category.id == category_id)
        ).all()

        # Combine subscribers (avoiding duplicates)
        subscriber_ids = set()
        for user in author_subscribers + category_subscribers:
            if user.id != author_id:  # Don't notify the author
                subscriber_ids.add(user.id)

        # Create notifications
        notification_count = 0

        try:
            # 打印调试信息
            logger.debug(f"Creating notifications for {len(subscriber_ids)} subscribers")
            logger.debug(f"article_id type: {type(article_id)}, value: {article_id}")

            for user_id in subscriber_ids:
                try:
                    # 确保 article_id 是整数
                    article_id_int = int(article_id) if article_id is not None else None
                    logger.debug(f"Creating notification for user_id: {user_id}, article_id_int: {article_id_int}")

                    # 使用 NotificationCreate 模型创建通知
                    notification_data = NotificationCreate(
                        user_id=user_id,
                        title="新文章发布",
                        content=f"您关注的内容有新文章发布：'{title}'",
                        type="article",
                        reference_id=article_id_int
                    )

                    # 使用 create_notification 方法创建通知
                    NotificationService.create_notification(db, notification_data)
                    notification_count += 1
                except Exception as e:
                    logger.error(f"Error creating notification for user {user_id}: {str(e)}")
                    # 继续处理其他用户，不中断循环

            # 不需要在这里提交，因为 create_notification 方法已经包含了 db.commit()
            logger.debug(f"Successfully created {notification_count} notifications")
        except Exception as e:
            logger.error(f"Error in notification creation: {str(e)}")
            # 不抛出异常，继续处理邮件通知

        # 发送邮件通知
        email_count = 0
        try:
            # 调用邮件订阅服务发送邮件
            email_count = await EmailSubscriptionService.send_article_notification_emails(
                db=db,
                article_id=article_id,
                article_title=title,
                article_excerpt=excerpt,
                article_url=article_url,
                author_name=author_name,
                author_id=author_id,
                category_id=category_id,
                category_name=category_name
            )
        except Exception as e:
            logger.error(f"Failed to send email notifications: {str(e)}")

        return {
            "notification_count": notification_count,
            "email_count": email_count
        }

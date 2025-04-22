from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app import models
from app.schemas.subscription import NotificationCreate
from app.utils.logging import get_logger

logger = get_logger(__name__)

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
    def notify_subscribers_new_article(
        db: Session, 
        article_id: int, 
        title: str, 
        author_id: int,
        category_id: int
    ) -> int:
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
        for user_id in subscriber_ids:
            notification = models.Notification(
                user_id=user_id,
                title="New Article Published",
                content=f"A new article '{title}' has been published that you might be interested in.",
                type="article",
                reference_id=article_id
            )
            
            db.add(notification)
            notification_count += 1
        
        db.commit()
        
        return notification_count

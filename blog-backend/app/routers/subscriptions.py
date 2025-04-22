from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app import models
from app.core import security
from app.core.database import get_db
from app.schemas.subscription import (
    CategorySubscriptionCreate, AuthorSubscriptionCreate,
    NotificationResponse, SubscriptionResponse
)
from app.services.subscription_service import SubscriptionService, NotificationService
from app.utils.pagination import PaginationParams, PagedResponse

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def subscribe_to_category(
    subscription: CategorySubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Subscribe to a category.
    """
    success = SubscriptionService.subscribe_to_category(
        db=db,
        user_id=current_user.id,
        category_id=subscription.category_id
    )

    if not success:
        return {"message": "Already subscribed to this category"}

    return {"message": "Successfully subscribed to category"}

@router.delete("/categories/{category_id}")
async def unsubscribe_from_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Unsubscribe from a category.
    """
    success = SubscriptionService.unsubscribe_from_category(
        db=db,
        user_id=current_user.id,
        category_id=category_id
    )

    if not success:
        return {"message": "Not subscribed to this category"}

    return {"message": "Successfully unsubscribed from category"}

@router.post("/authors", status_code=status.HTTP_201_CREATED)
async def subscribe_to_author(
    subscription: AuthorSubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Subscribe to an author.
    """
    success = SubscriptionService.subscribe_to_author(
        db=db,
        subscriber_id=current_user.id,
        author_id=subscription.author_id
    )

    if not success:
        return {"message": "Already subscribed to this author"}

    return {"message": "Successfully subscribed to author"}

@router.delete("/authors/{author_id}")
async def unsubscribe_from_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Unsubscribe from an author.
    """
    success = SubscriptionService.unsubscribe_from_author(
        db=db,
        subscriber_id=current_user.id,
        author_id=author_id
    )

    if not success:
        return {"message": "Not subscribed to this author"}

    return {"message": "Successfully unsubscribed from author"}

@router.get("", response_model=SubscriptionResponse)
async def get_subscriptions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Get current user's subscriptions.
    """
    subscriptions = SubscriptionService.get_user_subscriptions(db=db, user_id=current_user.id)

    return {
        "user_id": current_user.id,
        "category_ids": subscriptions["category_ids"],
        "author_ids": subscriptions["author_ids"]
    }

# Notifications endpoints
@router.get("/notifications", response_model=PagedResponse[NotificationResponse])
async def get_notifications(
    unread_only: bool = Query(False, description="Get only unread notifications"),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Get current user's notifications.
    """
    notifications = NotificationService.get_user_notifications(
        db=db,
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.page_size,
        unread_only=unread_only
    )

    # Get total count
    total = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id
    )

    if unread_only:
        total = total.filter(models.Notification.is_read == False)

    total = total.count()

    return PagedResponse.create(notifications, total, pagination)

@router.put("/notifications/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Mark a notification as read.
    """
    notification = NotificationService.mark_notification_as_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )

    return {"message": "Notification marked as read"}

@router.put("/notifications/read-all")
async def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Mark all notifications as read.
    """
    count = NotificationService.mark_all_notifications_as_read(
        db=db,
        user_id=current_user.id
    )

    return {"message": f"{count} notifications marked as read"}

@router.delete("/notifications/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Delete a notification.
    """
    success = NotificationService.delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return {"message": "Notification deleted"}

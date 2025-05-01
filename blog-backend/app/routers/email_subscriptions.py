from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app import models
from app.core.database import get_db
from app.schemas.subscription import (
    EmailSubscriptionBase, EmailSubscriptionCreate, EmailSubscriptionResponse,
    EmailSubscriptionUpdate, EmailSubscriptionUnsubscribe
)
from app.models.subscription import SubscriptionType
from app.services.subscription_service import EmailSubscriptionService
from app.schemas.pagination import PaginatedResponse

router = APIRouter(prefix="/email-subscriptions", tags=["email-subscriptions"])

@router.post("", response_model=EmailSubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_email_subscription(
    subscription: EmailSubscriptionCreate,
    db: Session = Depends(get_db)
):
    """
    创建新的邮件订阅

    - **email**: 订阅者邮箱
    - **subscription_type**: 订阅类型 (author, category, all)
    - **reference_id**: 引用ID (作者ID或分类ID，对于all类型可为null)
    """
    db_subscription = EmailSubscriptionService.create_email_subscription(
        db=db,
        subscription=subscription
    )

    return db_subscription

@router.get("", response_model=PaginatedResponse[EmailSubscriptionResponse])
async def get_email_subscriptions(
    email: Optional[str] = Query(None, description="按邮箱筛选"),
    subscription_type: Optional[SubscriptionType] = Query(None, description="按订阅类型筛选"),
    reference_id: Optional[int] = Query(None, description="按引用ID筛选"),
    is_active: Optional[bool] = Query(None, description="按活跃状态筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取邮件订阅列表

    可选参数:
    - **email**: 按邮箱筛选
    - **subscription_type**: 按订阅类型筛选 (author, category, all)
    - **reference_id**: 按引用ID筛选
    - **is_active**: 按活跃状态筛选
    - **page**: 页码，默认为1
    - **page_size**: 每页数量，默认为10
    """
    # 计算跳过的记录数
    skip = (page - 1) * page_size

    result = EmailSubscriptionService.get_email_subscriptions(
        db=db,
        email=email,
        subscription_type=subscription_type,
        reference_id=reference_id,
        is_active=is_active,
        skip=skip,
        limit=page_size
    )

    return result

@router.post("/unsubscribe", status_code=status.HTTP_200_OK)
async def unsubscribe_by_token(
    unsubscribe_data: EmailSubscriptionUnsubscribe,
    db: Session = Depends(get_db)
):
    """
    通过令牌取消订阅

    - **token**: 订阅令牌
    """
    success = EmailSubscriptionService.unsubscribe_by_token(
        db=db,
        token=unsubscribe_data.token
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订阅不存在或已取消"
        )

    return {"message": "成功取消订阅"}

@router.post("/unsubscribe/email", status_code=status.HTTP_200_OK)
async def unsubscribe_by_email(
    email: str = Query(..., description="订阅邮箱"),
    subscription_type: Optional[SubscriptionType] = Query(None, description="订阅类型"),
    reference_id: Optional[int] = Query(None, description="引用ID"),
    db: Session = Depends(get_db)
):
    """
    通过邮箱取消订阅

    - **email**: 订阅邮箱
    - **subscription_type**: 订阅类型 (可选)
    - **reference_id**: 引用ID (可选)
    """
    count = EmailSubscriptionService.unsubscribe_by_email(
        db=db,
        email=email,
        subscription_type=subscription_type,
        reference_id=reference_id
    )

    return {"message": f"成功取消 {count} 个订阅"}

class SubscriptionStatusUpdate(BaseModel):
    """订阅状态更新模型"""
    is_active: bool

@router.patch("/{subscription_id}", response_model=EmailSubscriptionResponse)
async def update_subscription_status(
    subscription_id: int = Path(..., description="订阅ID"),
    status_update: SubscriptionStatusUpdate = None,
    db: Session = Depends(get_db)
):
    """
    更新订阅状态

    - **subscription_id**: 订阅ID
    - **is_active**: 是否活跃
    """
    subscription = EmailSubscriptionService.update_subscription_status(
        db=db,
        subscription_id=subscription_id,
        is_active=status_update.is_active
    )

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订阅不存在"
        )

    return subscription

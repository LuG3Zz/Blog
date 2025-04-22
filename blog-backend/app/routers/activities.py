from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from app import models
from app.core import security
from app.core.database import get_db
from app.core.cache import cache
from app.schemas.activity import ActivityResponse, EnhancedActivityResponse
from app.services.activity_service import ActivityService

router = APIRouter(prefix="/activities", tags=['activities'])

@router.get("/", response_model=List[EnhancedActivityResponse])
async def get_recent_activities(
    days: int = 30,
    user_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    获取最近的用户活动，包含详细的活动描述和相关信息。

    参数:
    - **days**: 返回最近多少天的活动，默认30天
    - **user_id**: 可选的用户ID筛选条件
    - **limit**: 返回的活动数量上限，默认50条

    返回增强的活动信息，包含格式化的描述、相对时间和目标详情。
    """
    # 计算开始日期
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    # 使用活动服务获取增强的活动信息
    activities = ActivityService.get_enhanced_activities(
        db=db,
        start_date=start_date,
        user_id=user_id,
        limit=limit
    )

    return activities

@router.get("/basic", response_model=List[ActivityResponse])
async def get_basic_activities(
    days: int = 30,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """获取基本活动信息（兼容旧版本）"""
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    query = db.query(models.Activity).filter(models.Activity.created_at >= start_date)

    if user_id:
        query = query.filter(models.Activity.user_id == user_id)

    activities = query.order_by(models.Activity.created_at.desc()).all()
    return activities

@router.get("/public", response_model=List[EnhancedActivityResponse])
@cache(ttl_seconds=300)  # 缓存5分钟
async def get_public_activities(
    days: int = Query(7, ge=1, le=30, description="返回最近几天的活动，默认7天"),
    limit: int = Query(10, ge=1, le=50, description="返回的活动数量，默认10条"),
    db: Session = Depends(get_db)
):
    """
    获取最近的公开活动，用于首页展示，不需要用户验证。
    只返回文章创建和评论创建的活动。

    参数:
    - **days**: 返回最近多少天的活动，默认7天，最大30天
    - **limit**: 返回的活动数量上限，默认10条，最大50条

    返回增强的活动信息，包含格式化的描述、相对时间和目标详情。
    """
    # 计算开始日期
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    # 使用活动服务获取公开的增强活动信息
    activities = ActivityService.get_enhanced_activities(
        db=db,
        start_date=start_date,
        limit=limit,
        public_only=True  # 只获取公开活动
    )

    return activities
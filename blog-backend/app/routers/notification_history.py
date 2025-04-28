"""
通知历史路由模块：提供通知历史相关的API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app import models
from app.core import security
from app.core.database import get_db
from app.schemas.notification_history import NotificationHistoryResponse, NotificationHistoryList
from app.utils.pagination import PaginationParams, PagedResponse
from app.services.notification_history_service import NotificationHistoryService

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    dependencies=[Depends(security.get_current_user)]
)

@router.get("/history", response_model=PagedResponse[NotificationHistoryResponse])
async def get_notification_history(
    level: str = Query(None, description="通知级别筛选"),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    获取通知历史列表

    参数:
    - **level**: 通知级别筛选，可选值：info, success, warning, error
    - **pagination**: 分页参数

    返回:
    - 通知历史列表
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看通知历史"
        )

    # 获取通知历史
    notifications, total = NotificationHistoryService.get_notification_history(
        db=db,
        skip=pagination.skip,
        limit=pagination.page_size,
        level=level
    )

    return PagedResponse.create(notifications, total, pagination)

@router.delete("/{notification_id}", status_code=status.HTTP_200_OK)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    删除通知

    参数:
    - **notification_id**: 通知ID

    返回:
    - 200 OK: 删除成功
    - 403 Forbidden: 没有权限删除
    - 404 Not Found: 通知不存在
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以删除通知"
        )

    # 删除通知
    success = NotificationHistoryService.delete_notification(
        db=db,
        notification_id=notification_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知不存在"
        )

    return {"message": "通知已删除"}

@router.delete("/all", status_code=status.HTTP_200_OK)
async def clear_notifications(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    清空所有通知

    返回:
    - 200 OK: 清空成功
    - 403 Forbidden: 没有权限清空
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以清空通知"
        )

    # 清空通知
    count = NotificationHistoryService.clear_notifications(db=db)

    return {"message": f"已清空 {count} 条通知"}

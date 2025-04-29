"""
访客记录路由模块：提供访客记录相关的API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone

from app import models
from app.core import security
from app.core.database import get_db
from app.core.cache import cache
from app.schemas.visitor import VisitorResponse, VisitorBatchDeleteRequest, VisitorStatistics
from app.utils.pagination import PaginationParams, PagedResponse
from app.services.visitor_service import VisitorService

router = APIRouter(
    prefix="/visitors",
    tags=["visitors"],
    dependencies=[Depends(security.get_current_user)]
)

@router.get("", response_model=PagedResponse[VisitorResponse])
async def get_visitors(
    pagination: PaginationParams = Depends(),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    ip_address: Optional[str] = Query(None, description="IP地址筛选"),
    path: Optional[str] = Query(None, description="访问路径筛选"),
    visitor_name: Optional[str] = Query(None, description="访问人员名称筛选"),
    user_id: Optional[str] = Query(None, description="用户ID筛选"),
    is_mobile: Optional[bool] = Query(None, description="是否为移动设备"),
    is_bot: Optional[bool] = Query(None, description="是否为爬虫"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    获取访客记录列表

    参数:
    - **pagination**: 分页参数
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    - **ip_address**: IP地址筛选
    - **path**: 访问路径筛选
    - **is_mobile**: 是否为移动设备
    - **is_bot**: 是否为爬虫

    返回:
    - 访客记录列表
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看访客记录"
        )

    # 获取访客记录
    visitors, total = VisitorService.get_visitors(
        db=db,
        skip=pagination.skip,
        limit=pagination.page_size,
        start_date=start_date,
        end_date=end_date,
        ip_address=ip_address,
        path=path,
        visitor_name=visitor_name,
        user_id=user_id,
        is_mobile=is_mobile,
        is_bot=is_bot
    )

    # 构建分页响应
    pages = (total + pagination.page_size - 1) // pagination.page_size if pagination.page_size > 0 else 0
    return PagedResponse(
        items=visitors,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=pages
    )

@router.get("/statistics", response_model=VisitorStatistics)
@cache(ttl_seconds=300)  # 缓存5分钟
async def get_visitor_statistics(
    days: int = Query(30, ge=1, le=365, description="统计天数，默认30天"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    获取访客统计信息

    参数:
    - **days**: 统计天数，默认30天

    返回:
    - 访客统计信息
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看访客统计信息"
        )

    # 获取访客统计信息
    statistics = VisitorService.get_visitor_statistics(
        db=db,
        days=days
    )

    return statistics

@router.delete("/{visitor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    删除访客记录

    参数:
    - **visitor_id**: 访客记录ID

    返回:
    - 204 No Content: 删除成功
    - 404 Not Found: 访客记录不存在
    - 403 Forbidden: 没有权限删除
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以删除访客记录"
        )

    # 删除访客记录
    success = VisitorService.delete_visitor(db=db, visitor_id=visitor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="访客记录不存在"
        )

@router.post("/batch-delete", status_code=status.HTTP_200_OK)
async def batch_delete_visitors(
    request: VisitorBatchDeleteRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    批量删除访客记录

    参数:
    - **visitor_ids**: 要删除的访客记录ID列表

    返回:
    - 200 OK: 删除成功，返回删除的数量
    - 403 Forbidden: 没有权限删除
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以删除访客记录"
        )

    if not request.visitor_ids:
        return {"deleted_count": 0, "message": "没有指定要删除的访客记录"}

    # 批量删除访客记录
    deleted_count = VisitorService.batch_delete_visitors(
        db=db,
        visitor_ids=request.visitor_ids
    )

    return {
        "deleted_count": deleted_count,
        "message": f"成功删除 {deleted_count} 条访客记录"
    }

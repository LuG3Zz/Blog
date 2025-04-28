"""
通知历史服务模块：提供通知历史相关的服务
"""
from sqlalchemy.orm import Session
from typing import List, Tuple, Optional
from datetime import datetime

from app import models
from app.schemas.notification_history import NotificationHistoryResponse

class NotificationHistoryService:
    """通知历史服务类"""

    @staticmethod
    def get_notification_history(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        level: Optional[str] = None
    ) -> Tuple[List[NotificationHistoryResponse], int]:
        """
        获取通知历史列表

        参数:
        - **db**: 数据库会话
        - **skip**: 跳过的记录数
        - **limit**: 返回的记录数
        - **level**: 通知级别筛选

        返回:
        - 通知历史列表和总记录数
        """
        # 构建查询
        query = db.query(models.NotificationHistory)

        # 应用筛选条件
        if level:
            query = query.filter(models.NotificationHistory.level == level)

        # 获取总记录数
        total = query.count()

        # 应用分页
        notifications = query.order_by(models.NotificationHistory.created_at.desc()) \
            .offset(skip).limit(limit).all()

        # 转换为响应模型
        result = []
        for notification in notifications:
            result.append(NotificationHistoryResponse(
                id=notification.id,
                title=notification.title,
                content=notification.content,
                level=notification.level,
                target_users=notification.target_users,
                created_at=notification.created_at,
                created_by=notification.created_by,
                created_by_username=notification.created_by_username
            ))

        return result, total

    @staticmethod
    def delete_notification(db: Session, notification_id: int) -> bool:
        """
        删除通知

        参数:
        - **db**: 数据库会话
        - **notification_id**: 通知ID

        返回:
        - 是否删除成功
        """
        notification = db.query(models.NotificationHistory).filter(
            models.NotificationHistory.id == notification_id
        ).first()

        if not notification:
            return False

        db.delete(notification)
        db.commit()
        return True

    @staticmethod
    def clear_notifications(db: Session) -> int:
        """
        清空所有通知

        参数:
        - **db**: 数据库会话

        返回:
        - 清空的通知数量
        """
        count = db.query(models.NotificationHistory).count()
        db.query(models.NotificationHistory).delete()
        db.commit()
        return count

    @staticmethod
    def create_notification(
        db: Session,
        title: str,
        content: str,
        level: str,
        target_users: Optional[List[int]],
        created_by: int,
        created_by_username: str
    ) -> models.NotificationHistory:
        """
        创建通知历史记录

        参数:
        - **db**: 数据库会话
        - **title**: 通知标题
        - **content**: 通知内容
        - **level**: 通知级别
        - **target_users**: 目标用户ID列表
        - **created_by**: 创建者ID
        - **created_by_username**: 创建者用户名

        返回:
        - 创建的通知历史记录
        """
        notification = models.NotificationHistory(
            title=title,
            content=content,
            level=level,
            target_users=target_users,
            created_at=datetime.now(),
            created_by=created_by,
            created_by_username=created_by_username
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

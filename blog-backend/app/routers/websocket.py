import json
import uuid
from typing import Optional, Dict, Any
from fastapi import APIRouter, WebSocket, Depends, HTTPException, Query, status
from starlette.websockets import WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from app.services.websocket_manager import manager
from app.schemas.websocket import (
    MessageType, WebSocketMessage, UserOnlineMessage, UserOfflineMessage,
    AdminNotificationMessage, SystemNotificationMessage, ErrorMessage,
    PingMessage, PongMessage, AdminNotificationRequest
)
from app.services.user_service import UserService
from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin_user
from app.models.user import User
from app.utils.logging import get_logger
from app.utils.ip_utils import get_client_ip
from app.services.ip_location_service import IPLocationService

logger = get_logger(__name__)
router = APIRouter(tags=["websocket"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.websocket("/ws", name="websocket")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    client_id: Optional[str] = Query(None)
):
    """WebSocket 连接端点"""
    # 生成客户端ID（如果未提供）
    if not client_id:
        client_id = str(uuid.uuid4())

    # 获取客户端 IP 地址
    client_ip = get_client_ip(websocket)

    # 验证用户身份（如果提供了token）
    user_id = None
    is_admin = False
    user = None

    if token:
        # 如果 token 包含 "bearer" 前缀，则去除它
        if token.lower().startswith("bearer "):
            token = token[7:]
        elif token.lower().startswith("bearer+"):
            token = token[7:]

        try:
            db = next(get_db())
            try:
                user = await get_current_user(token, db)
                if user:
                    user_id = str(user.id)
                    # 检查用户是否为管理员
                    user_info = db.query(User).filter(User.id == user_id).first()
                    if user_info:
                        is_admin = user_info.role == "admin"
            except Exception as e:
                logger.warning(f"Token验证失败: {str(e)}")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"获取数据库连接失败: {str(e)}")

    # 接受WebSocket连接，并检查是否是该 IP 的第一个连接
    is_first_connection = await manager.connect(websocket, client_id, user_id, is_admin, client_ip)

    # 发送连接成功消息
    welcome_message = {
        "type": MessageType.SYSTEM_NOTIFICATION,
        "data": {
            "message": "WebSocket连接已建立",
            "client_id": client_id,
            "user_id": user_id,
            "is_admin": is_admin,
            "ip_address": client_ip
        }
    }
    await manager.send_personal_message(welcome_message, client_id)

    # 获取 IP 属地信息
    ip_location = IPLocationService.get_location(client_ip)

    # 如果是已登录用户且是该用户在该 IP 上的第一个连接，广播用户上线消息
    if user and user_id and is_first_connection and not manager.is_user_ip_notified(user_id, client_ip):
        # 获取用户信息
        db = next(get_db())
        try:
            user_info = db.query(User).filter(User.id == user_id).first()
            if user_info:
                # 将用户名与 IP 属地信息拼接
                username_with_location = f"{user_info.username} 来自 {ip_location}"

                online_message = UserOnlineMessage(
                    data={
                        "user_id": user_id,
                        "username": username_with_location,
                        "original_username": user_info.username,
                        "ip_location": ip_location,
                        "avatar": user_info.avatar,
                        "is_admin": is_admin,
                        "is_anonymous": False
                    }
                )
                await manager.broadcast(online_message.model_dump(), exclude=client_id)

                # 标记该用户-IP 组合已发送过上线通知
                manager.mark_user_ip_notified(user_id, client_ip)
        finally:
            db.close()
    # 如果是匿名用户且是该 IP 的第一个连接，广播匿名用户上线消息
    elif not user_id and is_first_connection and not manager.is_anonymous_ip_notified(client_ip):
        # 创建匿名用户信息
        visitor_name = f"访客 来自 {ip_location}"

        online_message = UserOnlineMessage(
            data={
                "user_id": None,
                "username": visitor_name,
                "original_username": "访客",
                "ip_location": ip_location,
                "avatar": None,  # 匿名用户没有头像
                "is_admin": False,
                "is_anonymous": True
            }
        )
        await manager.broadcast(online_message.model_dump(), exclude=client_id)

        # 标记该 IP 地址已发送过上线通知
        manager.mark_anonymous_ip_notified(client_ip)

    try:
        # 消息处理循环
        while True:
            # 接收消息
            data = await websocket.receive_text()

            try:
                # 解析消息
                message_data = json.loads(data)
                message_type = message_data.get("type")

                # 处理不同类型的消息
                if message_type == MessageType.PING:
                    # 心跳检测
                    pong_message = PongMessage()
                    await manager.send_personal_message(pong_message.model_dump(), client_id)

                elif message_type == MessageType.ADMIN_NOTIFICATION and is_admin:
                    # 管理员通知
                    notification_data = message_data.get("data", {})

                    # 获取管理员信息
                    db = next(get_db())
                    admin_name = "管理员"
                    try:
                        user_info = db.query(User).filter(User.id == user_id).first()
                        if user_info:
                            admin_name = user_info.username
                    finally:
                        db.close()

                    notification = AdminNotificationMessage(
                        data={
                            "title": notification_data.get("title", "管理员通知"),
                            "content": notification_data.get("content", ""),
                            "level": notification_data.get("level", "info"),
                            "admin_id": user_id,
                            "admin_name": admin_name
                        }
                    )

                    # 发送给目标用户或广播
                    target_users = notification_data.get("target_users")
                    if target_users:
                        for target_user_id in target_users:
                            await manager.send_to_user(notification.model_dump(), target_user_id)
                    else:
                        await manager.broadcast(notification.model_dump())

                else:
                    # 未知或未授权的消息类型
                    error_message = ErrorMessage(
                        data={
                            "message": "未知或未授权的消息类型",
                            "received_type": message_type
                        }
                    )
                    await manager.send_personal_message(error_message.model_dump(), client_id)

            except json.JSONDecodeError:
                # JSON解析错误
                error_message = ErrorMessage(
                    data={
                        "message": "无效的JSON格式",
                        "received_data": data
                    }
                )
                await manager.send_personal_message(error_message.model_dump(), client_id)

            except ValidationError as e:
                # 消息验证错误
                error_message = ErrorMessage(
                    data={
                        "message": "消息格式验证失败",
                        "errors": str(e)
                    }
                )
                await manager.send_personal_message(error_message.model_dump(), client_id)

            except Exception as e:
                # 其他错误
                logger.error(f"处理WebSocket消息时出错: {str(e)}")
                error_message = ErrorMessage(
                    data={
                        "message": "服务器内部错误",
                        "error": str(e)
                    }
                )
                await manager.send_personal_message(error_message.model_dump(), client_id)

    except WebSocketDisconnect:
        # 处理WebSocket断开连接，检查是否是该用户在该 IP 上的最后一个连接
        result = manager.disconnect(client_id)

        # 如果有结果，处理下线通知
        if result:
            last_user_id, last_ip = result

            # 获取 IP 属地信息
            ip_location = IPLocationService.get_location(last_ip)

            # 如果是已登录用户
            if last_user_id:
                # 获取用户信息
                db = next(get_db())
                try:
                    user_info = db.query(User).filter(User.id == last_user_id).first()
                    if user_info:
                        # 将用户名与 IP 属地信息拼接
                        username_with_location = f"{user_info.username} 来自 {ip_location}"

                        offline_message = UserOfflineMessage(
                            data={
                                "user_id": last_user_id,
                                "username": username_with_location,
                                "original_username": user_info.username,
                                "ip_location": ip_location,
                                "avatar": user_info.avatar,
                                "is_admin": is_admin,
                                "is_anonymous": False
                            }
                        )
                        await manager.broadcast(offline_message.model_dump())
                finally:
                    db.close()
            # 如果是匿名用户
            else:
                # 创建匿名用户信息
                visitor_name = f"访客 来自 {ip_location}"

                offline_message = UserOfflineMessage(
                    data={
                        "user_id": None,
                        "username": visitor_name,
                        "original_username": "访客",
                        "ip_location": ip_location,
                        "avatar": None,  # 匿名用户没有头像
                        "is_admin": False,
                        "is_anonymous": True
                    }
                )
                await manager.broadcast(offline_message.model_dump())

    except Exception as e:
        # 处理其他异常
        logger.error(f"WebSocket连接异常: {str(e)}")
        manager.disconnect(client_id)

@router.post("/admin/notifications", response_model=Dict[str, Any])
async def send_admin_notification(
    notification: AdminNotificationRequest,
    current_user: User = Depends(get_current_admin_user)
):
    """管理员发送全站通知"""
    # 验证用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以发送全站通知"
        )

    # 创建通知消息
    notification_message = AdminNotificationMessage(
        data={
            "title": notification.title,
            "content": notification.content,
            "level": notification.level,
            "admin_id": str(current_user.id),
            "admin_name": current_user.username
        }
    )

    # 发送通知
    if notification.target_users:
        # 发送给特定用户
        sent_count = 0
        for user_id in notification.target_users:
            sent_count += await manager.send_to_user(notification_message.model_dump(), user_id)

        return {
            "success": True,
            "message": f"通知已发送给 {sent_count} 个连接",
            "target_type": "specific_users",
            "target_count": len(notification.target_users)
        }
    else:
        # 广播给所有用户
        sent_count = await manager.broadcast(notification_message.model_dump())

        return {
            "success": True,
            "message": f"通知已广播给 {sent_count} 个连接",
            "target_type": "all_users",
            "connections_count": manager.get_active_connections_count()
        }

@router.get("/ws/status", response_model=Dict[str, Any])
async def get_websocket_status(current_user: User = Depends(get_current_admin_user)):
    """获取WebSocket连接状态"""
    # 验证用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看WebSocket连接状态"
        )

    return manager.get_status()

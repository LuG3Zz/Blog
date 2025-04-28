import json
import uuid
import time
from typing import Optional, Dict, Any
from fastapi import APIRouter, WebSocket, Depends, HTTPException, Query, status
from starlette.websockets import WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

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
from app.services.unified_cache_service import UnifiedCacheService

logger = get_logger(__name__)
router = APIRouter(tags=["websocket"], prefix="/ws")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 用户信息缓存前缀
USER_CACHE_PREFIX = "ws_user_info:"
# 用户缓存过期时间（秒）
USER_CACHE_TTL = 3600  # 1小时

@router.websocket("", name="websocket")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    client_id: Optional[str] = Query(None)
):
    """WebSocket 连接端点"""
    # 开始计时
    start_time = time.time()

    # 首先接受WebSocket连接，确保客户端不会超时
    await websocket.accept()
    logger.debug(f"[性能] WebSocket初始接受耗时: {(time.time() - start_time) * 1000:.2f}ms")

    # 生成客户端ID（如果未提供）
    if not client_id:
        client_id = str(uuid.uuid4())

    # 获取客户端 IP 地址
    client_ip = get_client_ip(websocket)
    logger.debug(f"[性能] 获取客户端IP耗时: {(time.time() - start_time) * 1000:.2f}ms")

    # 发送初始连接确认消息
    try:
        initial_message = {
            "type": MessageType.SYSTEM_NOTIFICATION,
            "data": {
                "message": "WebSocket连接已初始化，正在处理...",
                "client_id": client_id,
                "status": "initializing"
            }
        }
        await websocket.send_text(json.dumps(initial_message))
    except Exception as e:
        logger.error(f"发送初始连接确认消息失败: {str(e)}")
        # 如果发送失败，可能是连接已断开，我们重新接受连接
        try:
            await websocket.accept()
            await websocket.send_text(json.dumps(initial_message))
            logger.info("重新接受连接并发送初始消息成功")
        except Exception as e2:
            logger.error(f"重新接受连接失败: {str(e2)}")
            # 如果重新接受连接也失败，我们记录错误并继续，后续操作可能会失败

    # 验证用户身份（如果提供了token）
    user_id = None
    is_admin = False
    user = None
    user_info = None

    auth_start_time = time.time()
    if token:
        # 如果 token 包含 "bearer" 前缀，则去除它
        if token.lower().startswith("bearer "):
            token = token[7:]
        elif token.lower().startswith("bearer+"):
            token = token[7:]

        # 尝试从缓存获取用户信息
        cache_key = f"{USER_CACHE_PREFIX}{token}"
        cached_user = UnifiedCacheService.get(cache_key)

        if cached_user:
            # 使用缓存的用户信息
            logger.debug(f"[性能] 使用缓存的用户信息")
            user_id = cached_user.get("id")
            is_admin = cached_user.get("is_admin", False)
            user_info = cached_user
        else:
            # 缓存未命中，从数据库获取
            try:
                db = next(get_db())
                db_start_time = time.time()
                try:
                    user = await get_current_user(token, db)
                    if user:
                        user_id = str(user.id)
                        # 检查用户是否为管理员
                        user_info = db.query(User).filter(User.id == user_id).first()
                        if user_info:
                            is_admin = user_info.role == "admin"

                            # 缓存用户信息
                            user_cache = {
                                "id": user_id,
                                "username": user_info.username,
                                "avatar": user_info.avatar,
                                "is_admin": is_admin
                            }
                            UnifiedCacheService.set(cache_key, user_cache, USER_CACHE_TTL)
                    logger.debug(f"[性能] 数据库查询用户信息耗时: {(time.time() - db_start_time) * 1000:.2f}ms")
                except Exception as e:
                    logger.warning(f"Token验证失败: {str(e)}")
                finally:
                    db.close()
            except Exception as e:
                logger.error(f"获取数据库连接失败: {str(e)}")

    logger.debug(f"[性能] 用户认证总耗时: {(time.time() - auth_start_time) * 1000:.2f}ms")

    # 将连接添加到管理器，并检查是否是该 IP 的第一个连接
    connect_start_time = time.time()
    is_first_connection = await manager.connect(websocket, client_id, user_id, is_admin, client_ip)
    logger.debug(f"[性能] WebSocket连接管理耗时: {(time.time() - connect_start_time) * 1000:.2f}ms")

    # 发送连接成功消息
    try:
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
    except Exception as e:
        logger.error(f"发送连接成功消息失败: {str(e)}")
        # 如果发送失败，我们记录错误并继续，不影响后续操作

    # 获取 IP 属地信息 (使用缓存)
    ip_start_time = time.time()
    ip_location = IPLocationService.get_location(client_ip)
    logger.debug(f"[性能] 获取IP属地信息耗时: {(time.time() - ip_start_time) * 1000:.2f}ms")

    # 记录总连接时间
    logger.info(f"[性能] WebSocket连接总耗时: {(time.time() - start_time) * 1000:.2f}ms")

    # 如果是已登录用户且是该用户在该 IP 上的第一个连接，广播用户上线消息
    if user_id and is_first_connection and not manager.is_user_ip_notified(user_id, client_ip):
        # 使用已经获取的用户信息，避免再次查询数据库
        notify_start_time = time.time()

        if user_info:
            # 将用户名与 IP 属地信息拼接
            # 根据user_info的类型获取用户名和头像
            if isinstance(user_info, dict):
                username = user_info.get("username", "用户")
                avatar = user_info.get("avatar")
            else:
                # 如果user_info是User对象
                username = getattr(user_info, "username", "用户")
                avatar = getattr(user_info, "avatar", None)

            username_with_location = f"{username} 来自 {ip_location}"

            online_message = UserOnlineMessage(
                data={
                    "user_id": user_id,
                    "username": username_with_location,
                    "original_username": username,
                    "ip_location": ip_location,
                    "avatar": avatar,
                    "is_admin": is_admin,
                    "is_anonymous": False
                }
            )
            await manager.broadcast(online_message.model_dump(), exclude=client_id)

            # 标记该用户-IP 组合已发送过上线通知
            manager.mark_user_ip_notified(user_id, client_ip)

            logger.debug(f"[性能] 发送用户上线通知耗时: {(time.time() - notify_start_time) * 1000:.2f}ms")

    # 如果是匿名用户且是该 IP 的第一个连接，广播匿名用户上线消息
    elif not user_id and is_first_connection and not manager.is_anonymous_ip_notified(client_ip):
        notify_start_time = time.time()

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

        logger.debug(f"[性能] 发送匿名用户上线通知耗时: {(time.time() - notify_start_time) * 1000:.2f}ms")

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
        disconnect_start_time = time.time()
        result = manager.disconnect(client_id)
        logger.debug(f"[性能] WebSocket断开连接处理耗时: {(time.time() - disconnect_start_time) * 1000:.2f}ms")

        # 如果有结果，处理下线通知
        if result:
            last_user_id, last_ip = result

            # 获取 IP 属地信息
            ip_location = IPLocationService.get_location(last_ip)

            # 如果是已登录用户
            if last_user_id:
                # 尝试从缓存获取用户信息
                cache_key = f"{USER_CACHE_PREFIX}user:{last_user_id}"
                cached_user = UnifiedCacheService.get(cache_key)

                if cached_user:
                    # 使用缓存的用户信息
                    username = cached_user.get("username", "用户")
                    avatar = cached_user.get("avatar")

                    # 将用户名与 IP 属地信息拼接
                    username_with_location = f"{username} 来自 {ip_location}"

                    offline_message = UserOfflineMessage(
                        data={
                            "user_id": last_user_id,
                            "username": username_with_location,
                            "original_username": username,
                            "ip_location": ip_location,
                            "avatar": avatar,
                            "is_admin": is_admin,
                            "is_anonymous": False
                        }
                    )
                    await manager.broadcast(offline_message.model_dump())
                else:
                    # 缓存未命中，从数据库获取
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

                            # 缓存用户信息
                            user_cache = {
                                "id": str(user_info.id),
                                "username": user_info.username,
                                "avatar": user_info.avatar,
                                "is_admin": user_info.role == "admin"
                            }
                            UnifiedCacheService.set(cache_key, user_cache, USER_CACHE_TTL)
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
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
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

    # 记录通知历史
    from app.services.notification_history_service import NotificationHistoryService
    NotificationHistoryService.create_notification(
        db=db,
        title=notification.title,
        content=notification.content,
        level=notification.level,
        target_users=notification.target_users,
        created_by=current_user.id,
        created_by_username=current_user.username
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

@router.get("/status", response_model=Dict[str, Any])
async def get_websocket_status(current_user: User = Depends(get_current_admin_user)):
    """获取WebSocket连接状态"""
    # 验证用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看WebSocket连接状态"
        )

    return manager.get_status()

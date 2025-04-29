import json
import uuid
import time
from datetime import datetime, timedelta, timezone
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
from app.core import security
from app.models.user import User
from app.models.visitor import Visitor
from app.utils.logging import get_logger
from app.utils.ip_utils import get_client_ip
from app.services.ip_location_service import IPLocationService
from app.services.unified_cache_service import UnifiedCacheService
from app.services.visitor_service import VisitorService
from app import models

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

    # 不再发送初始连接确认消息，只在日志中记录
    logger.debug(f"WebSocket连接已初始化，client_id={client_id}")

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
                    user = await security.get_current_user(token, db)
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

    # 不再发送连接成功消息，只在日志中记录
    logger.debug(f"WebSocket连接已建立，client_id={client_id}, user_id={user_id}, is_admin={is_admin}, ip_address={client_ip}")

    # 获取 IP 属地信息 (使用缓存)
    ip_start_time = time.time()
    ip_location = IPLocationService.get_location(client_ip)

    # 发送欢迎消息（显示给用户）
    try:
        # 根据用户是否登录设置不同的欢迎消息
        avatar = None
        username = None

        # 构建带有IP属地的欢迎消息
        welcome_content = f"欢迎来自{ip_location}的朋友访问我的博客"

        if user_id:
            # 根据user_info的类型获取用户名和头像
            if isinstance(user_info, dict):
                username = user_info.get("username", "用户")
                avatar = user_info.get("avatar")
                welcome_content = f"欢迎来自{ip_location}的{username}回来！"
            elif user_info:
                if hasattr(user_info, 'username'):
                    username = user_info.username
                    welcome_content = f"欢迎来自{ip_location}的{username}回来！"
                if hasattr(user_info, 'avatar'):
                    avatar = user_info.avatar
            else:
                welcome_content = f"欢迎来自{ip_location}的朋友回来！"

        welcome_message = {
            "type": "welcome",
            "data": {
                "title": "欢迎访问",
                "content": welcome_content,
                "ip_location": ip_location,
                "timestamp": datetime.now().isoformat(),
                "avatar": avatar,
                "username": username,
                "user_id": user_id
            }
        }
        await manager.send_personal_message(welcome_message, client_id)
        logger.info(f"已发送欢迎消息: client_id={client_id}, user_id={user_id}")
    except Exception as e:
        logger.error(f"发送欢迎消息失败: {str(e)}")
        # 如果发送失败，我们记录错误并继续，不影响后续操作

    # 记录IP属地信息获取性能
    logger.debug(f"[性能] 获取IP属地信息耗时: {(time.time() - ip_start_time) * 1000:.2f}ms")

    # 记录总连接时间
    logger.info(f"[性能] WebSocket连接总耗时: {(time.time() - start_time) * 1000:.2f}ms")

    # 记录访客信息（仅记录前端访问）
    try:
        # 获取请求头中的Referer和User-Agent
        headers = dict(websocket.headers)
        referer = headers.get("referer", "")
        user_agent = headers.get("user-agent", "")

        # 尝试获取用户信息（如果有）
        user_id = None
        user_info = None

        # 从查询参数中获取token
        token_param = websocket.query_params.get("token", "")
        logger.info(f"查询参数中的token: {token_param}")

        # 获取数据库连接
        db = next(get_db())
        try:
            if token_param and token_param.startswith("bearer "):
                token = token_param.replace("bearer ", "")
                logger.info(f"处理后的token: {token[:10]}...")
                try:
                    user_info = await security.get_current_user_optional(token, db)
                    logger.info(f"获取到的用户信息: {user_info}")
                    if user_info:
                        user_id = str(user_info.id)
                        logger.info(f"从查询参数获取到用户信息: user_id={user_id}, username={user_info.username}")
                    else:
                        logger.warning(f"未能从token获取用户信息: {token[:10]}...")
                except Exception as e:
                    logger.warning(f"解析查询参数中的用户令牌失败: {e}")
        finally:
            db.close()

        # 如果查询参数中没有token，尝试从header中获取
        if not user_info:
            auth_header = headers.get("authorization", "")
            logger.info(f"Header中的authorization: {auth_header}")

            # 获取数据库连接
            db = next(get_db())
            try:
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.replace("Bearer ", "")
                    logger.info(f"处理后的header token: {token[:10]}...")
                    try:
                        user_info = await security.get_current_user_optional(token, db)
                        logger.info(f"从header获取到的用户信息: {user_info}")
                        if user_info:
                            user_id = str(user_info.id)
                            logger.info(f"从header获取到用户信息: user_id={user_id}, username={user_info.username}")
                        else:
                            logger.warning(f"未能从header token获取用户信息: {token[:10]}...")
                    except Exception as e:
                        logger.warning(f"解析header中的用户令牌失败: {e}")
            finally:
                db.close()

        # 检查是否为前端访问（不是管理端）
        is_frontend = True
        if referer:
            # 如果referer包含admin或manage，则认为是管理端访问
            if "/admin" in referer or "/manage" in referer:
                is_frontend = False

        # 如果是前端访问，记录访客信息
        if is_frontend:
            # 从referer中提取访问路径
            path = "/"
            if referer:
                try:
                    from urllib.parse import urlparse
                    parsed_url = urlparse(referer)
                    path = parsed_url.path or "/"
                except Exception as e:
                    logger.error(f"解析Referer失败: {e}")

            # 记录访客信息
            db = next(get_db())
            try:
                # 检查是否已经记录过该IP的访问（30分钟内，不考虑路径）
                # 使用UTC时间，因为数据库中的时间戳是UTC时间
                recent_time = datetime.now(timezone.utc) - timedelta(minutes=30)

                # 查询最近的访问记录，考虑IP地址和client_id
                # 如果是已登录用户，则检查IP和用户ID的组合
                if user_id:
                    # 对于已登录用户，只检查IP和用户ID的组合，忽略client_id
                    recent_visit = db.query(models.Visitor).filter(
                        models.Visitor.ip_address == client_ip,
                        models.Visitor.user_id == user_id,
                        models.Visitor.visit_time >= recent_time
                        # 不再检查client_id，允许同一用户在30分钟内多次连接但只记录一次
                    ).first()
                    logger.info(f"检查已登录用户的最近访问记录: IP={client_ip}, user_id={user_id}, client_id={client_id}, 结果={recent_visit is not None}")
                else:
                    # 如果是匿名用户，则只检查IP，忽略client_id
                    recent_visit = db.query(models.Visitor).filter(
                        models.Visitor.ip_address == client_ip,
                        models.Visitor.user_id.is_(None),  # 确保是匿名用户的记录
                        models.Visitor.visit_time >= recent_time
                        # 不再检查client_id，允许同一IP在30分钟内多次连接但只记录一次
                    ).first()
                    logger.info(f"检查匿名用户的最近访问记录: IP={client_ip}, client_id={client_id}, 结果={recent_visit is not None}")

                # 添加额外的日志，帮助调试
                logger.info(f"访客记录检查结果: recent_visit={recent_visit}, user_id={user_id}, client_ip={client_ip}, client_id={client_id}")

                # 如果没有最近的访问记录，则创建新记录
                if not recent_visit:
                    # 获取用户信息
                    visitor_name = "访客"

                    # 记录用户认证信息
                    logger.info(f"WebSocket连接用户认证信息: user_id={user_id}, user_info={user_info}, client_id={client_id}")

                    # 如果已经获取到了用户信息，直接使用
                    if user_info:
                        if hasattr(user_info, 'username'):
                            visitor_name = user_info.username
                        elif isinstance(user_info, dict) and 'username' in user_info:
                            visitor_name = user_info['username']
                        logger.info(f"使用已获取的用户信息: user_id={user_id}, username={visitor_name}, client_id={client_id}")
                    # 如果只有user_id但没有user_info，从数据库获取
                    elif user_id:
                        try:
                            user_db = db.query(User).filter(User.id == user_id).first()
                            if user_db:
                                visitor_name = user_db.username
                                logger.info(f"从数据库获取用户信息: user_id={user_id}, username={visitor_name}, client_id={client_id}")
                            else:
                                logger.warning(f"未找到用户信息: user_id={user_id}, client_id={client_id}")
                        except Exception as e:
                            logger.error(f"获取用户信息失败: {e}, client_id={client_id}")

                    # 创建访客记录
                    visitor_record = VisitorService.create_visitor_record(
                        db=db,
                        ip_address=client_ip,
                        path=path,
                        user_agent_string=user_agent,
                        referer=referer,
                        visitor_name=visitor_name,
                        user_id=user_id,
                        client_id=client_id
                    )
                    logger.info(f"已记录WebSocket访客: IP={client_ip}, 用户={visitor_name}, IP属地={ip_location}, 记录ID={visitor_record.id}, client_id={client_id}")
                else:
                    logger.debug(f"跳过记录WebSocket访客（30分钟内已记录）: IP={client_ip}, 用户={recent_visit.visitor_name or '访客'}, client_id={client_id}, 最近记录ID={recent_visit.id}, 最近记录时间={recent_visit.visit_time}")
            finally:
                db.close()
    except Exception as e:
        logger.error(f"记录WebSocket访客失败: {e}", exc_info=True)

    # 如果是已登录用户且是该用户在该 IP 上的第一个连接，广播用户上线消息
    if user_id and is_first_connection and not manager.is_user_ip_notified(user_id, client_ip):
        # 使用已经获取的用户信息，避免再次查询数据库
        notify_start_time = time.time()
        logger.info(f"准备发送用户上线通知: user_id={user_id}, client_ip={client_ip}, is_first_connection={is_first_connection}")

        if user_info:
            # 将用户名与 IP 属地信息拼接
            # 根据user_info的类型获取用户名和头像
            if isinstance(user_info, dict):
                username = user_info.get("username", "用户")
                avatar = user_info.get("avatar")
                logger.info(f"用户信息(dict): username={username}, avatar={avatar}")
            else:
                # 如果user_info是User对象
                username = getattr(user_info, "username", "用户")
                avatar = getattr(user_info, "avatar", None)
                logger.info(f"用户信息(object): username={username}, avatar={avatar}")

            username_with_location = f"{username} 来自 {ip_location}"
            logger.info(f"用户上线: {username_with_location}")

            online_message = UserOnlineMessage(
                data={
                    "user_id": user_id,
                    "username": username_with_location,
                    "original_username": username,
                    "ip_location": ip_location,
                    "avatar": avatar,
                    "is_admin": is_admin,
                    "is_anonymous": False,
                    "timestamp": datetime.now().isoformat()
                }
            )

            # 记录要发送的消息
            logger.info(f"发送用户上线消息: {online_message.model_dump()}")

            # 广播消息
            sent_count = await manager.broadcast(online_message.model_dump(), exclude=client_id)
            logger.info(f"用户上线消息已发送给 {sent_count} 个连接")

            # 标记该用户-IP 组合已发送过上线通知
            manager.mark_user_ip_notified(user_id, client_ip)
            logger.info(f"已标记用户-IP组合已通知: {user_id}:{client_ip}")

            logger.debug(f"[性能] 发送用户上线通知耗时: {(time.time() - notify_start_time) * 1000:.2f}ms")

    # 如果是匿名用户且是该 IP 的第一个连接，广播匿名用户上线消息
    elif not user_id and is_first_connection:
        # 检查是否已经发送过上线通知
        is_notified = manager.is_anonymous_ip_notified(client_ip)
        logger.info(f"匿名用户连接检查: client_ip={client_ip}, is_first_connection={is_first_connection}, is_notified={is_notified}")

        if not is_notified:
            notify_start_time = time.time()
            logger.info(f"准备发送匿名用户上线通知: client_ip={client_ip}, is_first_connection={is_first_connection}")

            # 创建匿名用户信息
            visitor_name = f"访客 来自 {ip_location}"
            logger.info(f"匿名用户上线: {visitor_name}")

            online_message = UserOnlineMessage(
                data={
                    "user_id": None,
                    "username": visitor_name,
                    "original_username": "访客",
                    "ip_location": ip_location,
                    "avatar": None,  # 匿名用户没有头像
                    "is_admin": False,
                    "is_anonymous": True,
                    "timestamp": datetime.now().isoformat()
                }
            )

            # 记录要发送的消息
            logger.info(f"发送匿名用户上线消息: {online_message.model_dump()}")

            # 广播消息
            sent_count = await manager.broadcast(online_message.model_dump(), exclude=client_id)
            logger.info(f"匿名用户上线消息已发送给 {sent_count} 个连接")

            # 标记该 IP 地址已发送过上线通知
            manager.mark_anonymous_ip_notified(client_ip)
            logger.info(f"已标记匿名IP已通知: {client_ip}")

            logger.debug(f"[性能] 发送匿名用户上线通知耗时: {(time.time() - notify_start_time) * 1000:.2f}ms")
        else:
            logger.info(f"匿名用户已经发送过上线通知，跳过: client_ip={client_ip}")

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

                elif message_type == MessageType.USER_LEAVE:
                    # 用户离开（页面关闭）
                    logger.info(f"用户离开消息: user_id={user_id}, client_id={client_id}")
                    # 不需要特殊处理，WebSocket断开连接时会自动处理用户下线逻辑

                elif message_type == MessageType.ANONYMOUS_LEAVE:
                    # 匿名用户离开（页面关闭）
                    logger.info(f"匿名用户离开消息: client_id={client_id}")
                    # 不需要特殊处理，WebSocket断开连接时会自动处理用户下线逻辑

                elif message_type == MessageType.USER_LOGOUT:
                    # 用户登出
                    logger.info(f"用户登出消息: user_id={user_id}, client_id={client_id}")
                    # 不需要特殊处理，WebSocket断开连接时会自动处理用户下线逻辑

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
    current_user: User = Depends(security.get_current_admin_user),
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
async def get_websocket_status(current_user: User = Depends(security.get_current_admin_user)):
    """获取WebSocket连接状态"""
    # 验证用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看WebSocket连接状态"
        )

    return manager.get_status()

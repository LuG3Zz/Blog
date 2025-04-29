from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime

class MessageType(str, Enum):
    """WebSocket 消息类型"""
    USER_ONLINE = "user_online"  # 用户上线
    USER_OFFLINE = "user_offline"  # 用户下线
    ADMIN_NOTIFICATION = "admin_notification"  # 管理员通知
    SYSTEM_NOTIFICATION = "system_notification"  # 系统通知
    ERROR = "error"  # 错误消息
    PING = "ping"  # 心跳检测
    PONG = "pong"  # 心跳响应
    USER_LEAVE = "user_leave"  # 用户离开（页面关闭）
    ANONYMOUS_LEAVE = "anonymous_leave"  # 匿名用户离开（页面关闭）
    USER_LOGOUT = "user_logout"  # 用户登出

class WebSocketMessage(BaseModel):
    """WebSocket 消息模型"""
    type: MessageType
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class UserOnlineMessage(WebSocketMessage):
    """用户上线消息"""
    type: MessageType = MessageType.USER_ONLINE
    data: Dict[str, Any] = Field(...)

class UserOfflineMessage(WebSocketMessage):
    """用户下线消息"""
    type: MessageType = MessageType.USER_OFFLINE
    data: Dict[str, Any] = Field(...)

class AdminNotificationMessage(WebSocketMessage):
    """管理员通知消息"""
    type: MessageType = MessageType.ADMIN_NOTIFICATION
    data: Dict[str, Any] = Field(...)

class SystemNotificationMessage(WebSocketMessage):
    """系统通知消息"""
    type: MessageType = MessageType.SYSTEM_NOTIFICATION
    data: Dict[str, Any] = Field(...)

class ErrorMessage(WebSocketMessage):
    """错误消息"""
    type: MessageType = MessageType.ERROR
    data: Dict[str, Any] = Field(...)

class PingMessage(WebSocketMessage):
    """心跳检测消息"""
    type: MessageType = MessageType.PING
    data: Dict[str, Any] = Field(default_factory=dict)

class PongMessage(WebSocketMessage):
    """心跳响应消息"""
    type: MessageType = MessageType.PONG
    data: Dict[str, Any] = Field(default_factory=dict)

class AdminNotificationRequest(BaseModel):
    """管理员通知请求"""
    title: str
    content: str
    level: str = "info"  # info, warning, error
    target_users: Optional[List[str]] = None  # 如果为空，则发送给所有用户

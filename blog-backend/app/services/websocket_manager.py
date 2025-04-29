from typing import Dict, List, Any, Optional, Set
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime
from app.utils.logging import get_logger
from starlette.websockets import WebSocketDisconnect, WebSocketState

logger = get_logger(__name__)

class ConnectionManager:
    """管理 WebSocket 连接"""

    def __init__(self):
        # 活跃连接: {client_id: WebSocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # 用户连接映射: {user_id: [client_id1, client_id2, ...]}
        self.user_connections: Dict[str, List[str]] = {}
        # IP 地址映射: {ip_address: [client_id1, client_id2, ...]}
        self.ip_connections: Dict[str, List[str]] = {}
        # IP 地址用户映射: {ip_address: {user_id1, user_id2, ...}}
        self.ip_user_mapping: Dict[str, Set[str]] = {}
        # 用户-IP 映射: {(user_id, ip_address): [client_id1, client_id2, ...]}
        self.user_ip_connections: Dict[str, List[str]] = {}
        # 管理员连接: [client_id1, client_id2, ...]
        self.admin_connections: List[str] = []
        # 已通知的用户-IP 组合: {(user_id, ip_address)}
        self.notified_user_ips: Set[str] = set()
        # 已通知的匿名 IP 地址: {ip_address}
        self.notified_anonymous_ips: Set[str] = set()

    async def connect(self, websocket: WebSocket, client_id: str, user_id: Optional[str] = None,
                     is_admin: bool = False, ip_address: str = None) -> bool:
        """
        将WebSocket连接添加到管理器

        注意：此方法不再调用websocket.accept()，因为连接应该在调用此方法之前已经被接受
        """
        # 将连接添加到活跃连接映射
        self.active_connections[client_id] = websocket

        # 如果提供了用户ID，添加到用户连接映射
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(client_id)

        # 如果提供了 IP 地址，添加到 IP 连接映射
        is_first_connection = False
        if ip_address:
            # 检查是否是该 IP 的第一个连接
            is_first_ip = ip_address not in self.ip_connections

            # 添加到 IP 连接映射
            if is_first_ip:
                self.ip_connections[ip_address] = []
                # 对于匿名用户，如果是该 IP 的第一个连接，则标记为第一个连接
                if not user_id:
                    is_first_connection = True
                    logger.info(f"匿名用户的第一个IP连接: ip={ip_address}, client_id={client_id}")

            self.ip_connections[ip_address].append(client_id)

            # 如果有用户 ID，记录 IP 地址与用户的映射
            if user_id:
                # 创建用户-IP 组合的键
                user_ip_key = f"{user_id}:{ip_address}"

                # 检查是否是该用户在该 IP 上的第一个连接
                if user_ip_key not in self.user_ip_connections:
                    self.user_ip_connections[user_ip_key] = []
                    is_first_connection = True
                    logger.info(f"用户的第一个IP连接: user_id={user_id}, ip={ip_address}, client_id={client_id}")

                self.user_ip_connections[user_ip_key].append(client_id)

                # 更新 IP 地址用户映射
                if ip_address not in self.ip_user_mapping:
                    self.ip_user_mapping[ip_address] = set()
                self.ip_user_mapping[ip_address].add(user_id)

        # 如果是管理员，添加到管理员连接列表
        if is_admin:
            self.admin_connections.append(client_id)

        logger.info(f"WebSocket 连接已建立: client_id={client_id}, user_id={user_id}, is_admin={is_admin}, ip={ip_address}, is_first_connection={is_first_connection}")

        # 返回是否是第一个连接（对于已登录用户是该用户在该 IP 上的第一个连接，对于匿名用户是该 IP 的第一个连接）
        return is_first_connection

    def disconnect(self, client_id: str) -> Optional[tuple]:
        """断开 WebSocket 连接，返回 (user_id, ip_address) 元组或 (None, ip_address) 元组"""
        if client_id not in self.active_connections:
            return None

        # 从活跃连接中移除
        self.active_connections.pop(client_id)

        # 查找该客户端的用户 ID
        user_id = None
        for uid, connections in list(self.user_connections.items()):
            if client_id in connections:
                user_id = uid
                connections.remove(client_id)
                # 如果用户没有活跃连接，从映射中移除
                if not connections:
                    self.user_connections.pop(uid)
                break

        # 查找该客户端的 IP 地址
        ip_address = None
        is_last_ip_connection = False
        for ip, clients in list(self.ip_connections.items()):
            if client_id in clients:
                ip_address = ip
                clients.remove(client_id)
                # 如果该 IP 没有更多连接，从映射中移除
                if not clients:
                    self.ip_connections.pop(ip)
                    if ip in self.ip_user_mapping:
                        self.ip_user_mapping.pop(ip)
                    if ip in self.notified_anonymous_ips:
                        self.notified_anonymous_ips.remove(ip)
                    is_last_ip_connection = True
                break

        # 如果有用户 ID 和 IP 地址，处理用户-IP 映射
        is_last_user_ip_connection = False
        if user_id and ip_address:
            user_ip_key = f"{user_id}:{ip_address}"

            # 从用户-IP 连接映射中移除
            if user_ip_key in self.user_ip_connections:
                if client_id in self.user_ip_connections[user_ip_key]:
                    self.user_ip_connections[user_ip_key].remove(client_id)

                # 如果该用户在该 IP 上没有更多连接，从映射中移除
                if not self.user_ip_connections[user_ip_key]:
                    self.user_ip_connections.pop(user_ip_key)
                    is_last_user_ip_connection = True

                    # 从已通知的用户-IP 组合中移除
                    if user_ip_key in self.notified_user_ips:
                        self.notified_user_ips.remove(user_ip_key)

                    # 从 IP 地址用户映射中移除该用户
                    if ip_address in self.ip_user_mapping and user_id in self.ip_user_mapping[ip_address]:
                        self.ip_user_mapping[ip_address].remove(user_id)
                        if not self.ip_user_mapping[ip_address]:
                            self.ip_user_mapping.pop(ip_address)

        # 从管理员连接列表中移除
        if client_id in self.admin_connections:
            self.admin_connections.remove(client_id)

        logger.info(f"WebSocket 连接已断开: client_id={client_id}, user_id={user_id}, ip={ip_address}")

        # 如果是该用户在该 IP 上的最后一个连接，返回 (user_id, ip_address) 元组
        if is_last_user_ip_connection and user_id and ip_address:
            return (user_id, ip_address)
        # 如果是匿名用户且是该 IP 的最后一个连接，返回 (None, ip_address) 元组
        elif is_last_ip_connection and ip_address and not user_id:
            return (None, ip_address)
        return None

    def is_user_ip_notified(self, user_id: str, ip_address: str) -> bool:
        """检查用户-IP 组合是否已经发送过上线通知"""
        user_ip_key = f"{user_id}:{ip_address}"
        return user_ip_key in self.notified_user_ips

    def mark_user_ip_notified(self, user_id: str, ip_address: str) -> None:
        """标记用户-IP 组合已发送过上线通知"""
        user_ip_key = f"{user_id}:{ip_address}"
        self.notified_user_ips.add(user_ip_key)

    def is_anonymous_ip_notified(self, ip_address: str) -> bool:
        """检查匿名 IP 地址是否已经发送过上线通知"""
        is_notified = ip_address in self.notified_anonymous_ips
        logger.info(f"检查匿名IP是否已通知: ip={ip_address}, is_notified={is_notified}")
        return is_notified

    def mark_anonymous_ip_notified(self, ip_address: str) -> None:
        """标记匿名 IP 地址已发送过上线通知"""
        logger.info(f"标记匿名IP已通知: ip={ip_address}")
        self.notified_anonymous_ips.add(ip_address)
        logger.info(f"已通知的匿名IP数量: {len(self.notified_anonymous_ips)}")

    def get_users_by_ip(self, ip_address: str) -> Set[str]:
        """通过 IP 地址获取用户 ID 集合"""
        return self.ip_user_mapping.get(ip_address, set())

    async def send_personal_message(self, message: Any, client_id: str) -> bool:
        """向特定客户端发送消息"""
        try:
            if client_id not in self.active_connections:
                return False

            websocket = self.active_connections[client_id]
            if isinstance(message, dict):
                message = json.dumps(message, ensure_ascii=False)

            try:
                # 检查WebSocket连接状态
                if websocket.client_state == WebSocketState.DISCONNECTED:
                    logger.warning(f"WebSocket已断开连接: client_id={client_id}")
                    self.disconnect(client_id)
                    return False

                # 发送消息
                await websocket.send_text(message)
                return True
            except WebSocketDisconnect:
                logger.warning(f"WebSocket已断开连接: client_id={client_id}")
                self.disconnect(client_id)
                return False
            except Exception as e:
                logger.error(f"发送消息失败: client_id={client_id}, error={str(e)}")
                self.disconnect(client_id)
                return False

        except Exception as e:
            logger.error(f"发送个人消息时发生错误: {str(e)}")
            return False

    async def send_to_user(self, message: Any, user_id: str) -> int:
        """向特定用户的所有连接发送消息"""
        if user_id not in self.user_connections:
            return 0

        sent_count = 0
        for client_id in self.user_connections[user_id]:
            if await self.send_personal_message(message, client_id):
                sent_count += 1

        return sent_count

    async def broadcast(self, message: Any, exclude: Optional[str] = None) -> int:
        """向所有连接广播消息，可选择排除特定客户端"""
        sent_count = 0

        # 确保消息是字符串
        if isinstance(message, dict):
            message = json.dumps(message, ensure_ascii=False)

        # 广播给所有活跃连接
        for client_id, websocket in list(self.active_connections.items()):
            if exclude and client_id == exclude:
                continue

            try:
                # 检查WebSocket连接状态
                if websocket.client_state == WebSocketState.DISCONNECTED:
                    logger.warning(f"WebSocket已断开连接: client_id={client_id}")
                    self.disconnect(client_id)
                    continue

                # 发送消息
                await websocket.send_text(message)
                sent_count += 1
            except Exception as e:
                logger.error(f"向客户端 {client_id} 发送消息失败: {str(e)}")
                # 连接可能已断开，从活跃连接中移除
                self.disconnect(client_id)

        return sent_count

    async def broadcast_to_admins(self, message: Any) -> int:
        """向所有管理员广播消息"""
        sent_count = 0
        for client_id in list(self.admin_connections):
            if await self.send_personal_message(message, client_id):
                sent_count += 1

        return sent_count

    def get_active_connections_count(self) -> int:
        """获取活跃连接数量"""
        return len(self.active_connections)

    def get_active_users_count(self) -> int:
        """获取活跃用户数量"""
        return len(self.user_connections)

    def get_active_ips_count(self) -> int:
        """获取活跃 IP 地址数量"""
        return len(self.ip_connections)

    def get_active_admins_count(self) -> int:
        """获取活跃管理员数量"""
        return len(self.admin_connections)

    def get_status(self) -> Dict[str, Any]:
        """获取连接管理器状态"""
        return {
            "active_connections": len(self.active_connections),
            "active_users": len(self.user_connections),
            "active_ips": len(self.ip_connections),
            "active_admins": len(self.admin_connections),
            "timestamp": datetime.now().isoformat()
        }

# 全局连接管理器实例
manager = ConnectionManager()


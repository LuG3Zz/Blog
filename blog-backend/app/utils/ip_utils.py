from fastapi import Request, WebSocket
from typing import Optional, Union
from app.utils.logging import get_logger

logger = get_logger(__name__)

def get_client_ip(request_or_websocket: Union[Request, WebSocket]) -> str:
    """
    获取客户端真实 IP 地址。

    优先从各种代理头部获取，如果不存在则使用 client.host。
    X-Forwarded-For 格式通常为: client_ip, proxy1_ip, proxy2_ip, ...

    Args:
        request_or_websocket: FastAPI 请求对象或 WebSocket 对象

    Returns:
        客户端 IP 地址字符串
    """
    # 获取请求头和客户端信息
    headers = None
    client = None

    if isinstance(request_or_websocket, Request):
        headers = request_or_websocket.headers
        client = request_or_websocket.client
    else:  # WebSocket
        headers = request_or_websocket.headers
        client = request_or_websocket.client

    # 尝试从各种头部获取真实 IP
    x_client_ip = headers.get("X-Client-IP")
    x_real_ip = headers.get("X-Real-IP")
    x_forwarded_for = headers.get("X-Forwarded-For")
    forwarded = headers.get("Forwarded")

    # 按优先级获取真实 IP
    if x_client_ip:
        logger.debug(f"从 X-Client-IP 获取到 IP: {x_client_ip}")
        return x_client_ip
    elif x_real_ip:
        logger.debug(f"从 X-Real-IP 获取到 IP: {x_real_ip}")
        return x_real_ip
    elif x_forwarded_for:
        # X-Forwarded-For 可能包含多个 IP，取第一个
        client_ip = x_forwarded_for.split(',')[0].strip()
        logger.debug(f"从 X-Forwarded-For 获取到 IP: {client_ip} (完整值: {x_forwarded_for})")
        return client_ip
    elif forwarded:
        # 解析 Forwarded 头部
        for part in forwarded.split(';'):
            if part.lower().startswith('for='):
                real_ip = part[4:].strip()
                # 移除可能的引号和 IPv6 括号
                real_ip = real_ip.strip('"[]')
                logger.debug(f"从 Forwarded 获取到 IP: {real_ip}")
                return real_ip

    # 如果没有代理头部，使用直接连接的客户端 IP
    client_ip = client.host if client else "127.0.0.1"
    logger.debug(f"从 client.host 获取到 IP: {client_ip}")
    return client_ip

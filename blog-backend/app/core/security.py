from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import User
from app.services.unified_cache_service import UnifiedCacheService
from app.utils.logging import get_logger
from app.utils.password import verify_password, get_password_hash

logger = get_logger(__name__)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

# 缓存相关常量
USER_CACHE_PREFIX = "auth:user:"
TOKEN_CACHE_PREFIX = "auth:token:"
JWT_PAYLOAD_CACHE_PREFIX = "auth:jwt:"
# 缓存过期时间（秒）- 设置为比令牌过期时间短一些
USER_CACHE_TTL = min(settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 - 300, 3600)  # 令牌过期时间减5分钟或1小时，取较小值

def _get_token_cache_key(token: str) -> str:
    """生成令牌缓存键"""
    # 使用令牌的哈希值作为缓存键，避免将完整令牌存储在缓存键中
    import hashlib
    token_hash = hashlib.md5(token.encode()).hexdigest()
    return f"{TOKEN_CACHE_PREFIX}{token_hash}"

def _get_user_cache_key(username: str) -> str:
    """生成用户缓存键"""
    return f"{USER_CACHE_PREFIX}{username}"

def _get_jwt_payload_cache_key(token: str) -> str:
    """生成JWT负载缓存键"""
    import hashlib
    token_hash = hashlib.md5(token.encode()).hexdigest()
    return f"{JWT_PAYLOAD_CACHE_PREFIX}{token_hash}"

def _cache_user(username: str, user: User) -> None:
    """缓存用户信息"""
    if not user:
        return
    
    # 只缓存必要的用户信息，避免缓存敏感数据
    user_data = {
        "id": str(user.id),
        "username": user.username,
        "role": user.role,
        "avatar": user.avatar
    }
    
    cache_key = _get_user_cache_key(username)
    UnifiedCacheService.set(cache_key, user_data, USER_CACHE_TTL)
    logger.debug(f"用户信息已缓存: {username}")

def _cache_token_user_mapping(token: str, username: str) -> None:
    """缓存令牌到用户名的映射"""
    token_key = _get_token_cache_key(token)
    UnifiedCacheService.set(token_key, username, USER_CACHE_TTL)
    logger.debug(f"令牌到用户名映射已缓存")

def _cache_jwt_payload(token: str, payload: Dict[str, Any]) -> None:
    """缓存JWT负载"""
    payload_key = _get_jwt_payload_cache_key(token)
    UnifiedCacheService.set(payload_key, payload, USER_CACHE_TTL)
    logger.debug(f"JWT负载已缓存")

def _get_cached_user_by_token(token: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    """通过令牌获取缓存的用户信息"""
    # 1. 尝试从缓存获取令牌到用户名的映射
    token_key = _get_token_cache_key(token)
    username = UnifiedCacheService.get(token_key)
    
    if not username:
        logger.debug("令牌缓存未命中")
        return None
    
    # 2. 尝试从缓存获取用户信息
    user_key = _get_user_cache_key(username)
    user_data = UnifiedCacheService.get(user_key)
    
    if not user_data:
        logger.debug(f"用户缓存未命中: {username}")
        return None
    
    logger.debug(f"缓存命中: {username}")
    return username, user_data

def _get_cached_jwt_payload(token: str) -> Optional[Dict[str, Any]]:
    """获取缓存的JWT负载"""
    payload_key = _get_jwt_payload_cache_key(token)
    payload = UnifiedCacheService.get(payload_key)
    
    if not payload:
        logger.debug("JWT负载缓存未命中")
        return None
    
    logger.debug("JWT负载缓存命中")
    return payload

# 密码验证和哈希函数已移至 app.utils.password 模块

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    # 性能计时开始
    start_time = datetime.now()

    # 尝试从缓存获取用户信息
    cached_result = _get_cached_user_by_token(token)
    if cached_result:
        username, user_data = cached_result
        # 从缓存数据创建用户对象
        user = User(
            id=user_data["id"],
            username=user_data["username"],
            role=user_data["role"],
            avatar=user_data.get("avatar")
        )
        logger.debug(f"[性能] 从缓存获取用户信息耗时: {(datetime.now() - start_time).total_seconds() * 1000:.2f}ms")
        return user

    # 缓存未命中，从数据库获取
    jwt_start_time = datetime.now()
    try:
        # 尝试从缓存获取JWT负载
        payload = _get_cached_jwt_payload(token)
        if not payload:
            # 缓存未命中，解码JWT
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            # 缓存JWT负载
            _cache_jwt_payload(token, payload)

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        logger.debug(f"[性能] JWT解码耗时: {(datetime.now() - jwt_start_time).total_seconds() * 1000:.2f}ms")

        # 从数据库获取用户
        db_start_time = datetime.now()
        user = db.query(User).filter(User.username == username).first()
        logger.debug(f"[性能] 数据库查询用户耗时: {(datetime.now() - db_start_time).total_seconds() * 1000:.2f}ms")

        if user is None:
            raise credentials_exception

        # 缓存用户信息和令牌映射
        _cache_user(username, user)
        _cache_token_user_mapping(token, username)

        logger.debug(f"[性能] 获取用户总耗时: {(datetime.now() - start_time).total_seconds() * 1000:.2f}ms")
        return user

    except JWTError:
        logger.warning(f"JWT解码失败: {token[:10]}...")
        raise credentials_exception

async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get the current user if authenticated, or None for guest access."""
    if not token:
        return None

    # 性能计时开始
    start_time = datetime.now()

    # 尝试从缓存获取用户信息
    cached_result = _get_cached_user_by_token(token)
    if cached_result:
        username, user_data = cached_result
        # 从缓存数据创建用户对象
        user = User(
            id=user_data["id"],
            username=user_data["username"],
            role=user_data["role"],
            avatar=user_data.get("avatar")
        )
        logger.debug(f"[性能] 从缓存获取可选用户信息耗时: {(datetime.now() - start_time).total_seconds() * 1000:.2f}ms")
        return user

    try:
        # 尝试从缓存获取JWT负载
        payload = _get_cached_jwt_payload(token)
        if not payload:
            # 缓存未命中，解码JWT
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            # 缓存JWT负载
            _cache_jwt_payload(token, payload)
            
        username: str = payload.get("sub")
        if username is None:
            return None
        
        # 从数据库获取用户
        db_start_time = datetime.now()
        user = db.query(User).filter(User.username == username).first()
        logger.debug(f"[性能] 数据库查询可选用户耗时: {(datetime.now() - db_start_time).total_seconds() * 1000:.2f}ms")
        
        if user:
            # 缓存用户信息和令牌映射
            _cache_user(username, user)
            _cache_token_user_mapping(token, username)
        
        logger.debug(f"[性能] 获取可选用户总耗时: {(datetime.now() - start_time).total_seconds() * 1000:.2f}ms")
        return user

    except JWTError:
        logger.debug(f"JWT解码失败(可选用户): {token[:10]}...")
        return None

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get the current user and verify they are an admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

async def get_current_user_or_token(
    token: Optional[str] = Depends(oauth2_scheme),
    query_token: Optional[str] = None,
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current user from either the OAuth2 token or a query parameter token.
    This is useful for endpoints that need to be accessed both via API and directly (like image URLs).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 使用查询参数中的token（如果提供）
    if query_token:
        token_to_use = query_token
    else:
        token_to_use = token

    if not token_to_use:
        raise credentials_exception

    # 性能计时开始
    start_time = datetime.now()

    # 尝试从缓存获取用户信息
    cached_result = _get_cached_user_by_token(token_to_use)
    if cached_result:
        username, user_data = cached_result
        # 从缓存数据创建用户对象
        user = User(
            id=user_data["id"],
            username=user_data["username"],
            role=user_data["role"],
            avatar=user_data.get("avatar")
        )
        logger.debug(f"[性能] 从缓存获取token用户信息耗时: {(datetime.now() - start_time).total_seconds() * 1000:.2f}ms")
        return user

    # 缓存未命中，从数据库获取
    jwt_start_time = datetime.now()
    try:
        # 尝试从缓存获取JWT负载
        payload = _get_cached_jwt_payload(token_to_use)
        if not payload:
            # 缓存未命中，解码JWT
            payload = jwt.decode(
                token_to_use,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            # 缓存JWT负载
            _cache_jwt_payload(token_to_use, payload)

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        logger.debug(f"[性能] JWT解码耗时: {(datetime.now() - jwt_start_time).total_seconds() * 1000:.2f}ms")

        # 从数据库获取用户
        db_start_time = datetime.now()
        user = db.query(User).filter(User.username == username).first()
        logger.debug(f"[性能] 数据库查询token用户耗时: {(datetime.now() - db_start_time).total_seconds() * 1000:.2f}ms")

        if user is None:
            raise credentials_exception

        # 缓存用户信息和令牌映射
        _cache_user(username, user)
        _cache_token_user_mapping(token_to_use, username)

        logger.debug(f"[性能] 获取token用户总耗时: {(datetime.now() - start_time).total_seconds() * 1000:.2f}ms")
        return user

    except JWTError:
        logger.warning(f"JWT解码失败: {token_to_use[:10]}...")
        raise credentials_exception

def clear_user_cache(username: str = None, token: str = None) -> None:
    """
    清除用户缓存。
    
    可以通过用户名或令牌清除缓存。如果两者都提供，将同时清除两种缓存。
    如果都不提供，则不执行任何操作。
    
    Args:
        username: 用户名
        token: 令牌
    """
    if username:
        # 清除用户信息缓存
        user_key = _get_user_cache_key(username)
        UnifiedCacheService.delete(user_key)
        logger.debug(f"已清除用户缓存: {username}")
    
    if token:
        # 清除令牌到用户名的映射
        token_key = _get_token_cache_key(token)
        # 获取关联的用户名
        username_from_token = UnifiedCacheService.get(token_key)
        if username_from_token and not username:
            # 如果找到关联的用户名，且未通过参数提供用户名，则清除该用户的缓存
            user_key = _get_user_cache_key(username_from_token)
            UnifiedCacheService.delete(user_key)
            logger.debug(f"已清除用户缓存: {username_from_token} (通过令牌)")
        
        # 清除令牌映射
        UnifiedCacheService.delete(token_key)
        logger.debug(f"已清除令牌缓存: {token[:10]}...")
        
        # 清除JWT负载缓存
        payload_key = _get_jwt_payload_cache_key(token)
        UnifiedCacheService.delete(payload_key)
        logger.debug(f"已清除JWT负载缓存")

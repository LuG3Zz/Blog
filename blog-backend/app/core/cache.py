"""
缓存模块，用于缓存频繁请求的数据
"""
import time
import hashlib
import json
from functools import wraps
from typing import Dict, Any, Callable, Optional, List

from app.services.unified_cache_service import UnifiedCacheService
from app.utils.logging import get_logger

logger = get_logger(__name__)

# 兼容旧代码的内存缓存存储
_cache: Dict[str, Dict[str, Any]] = {}

def cache(ttl_seconds: int = 60, prefix: str = None):
    """
    缓存装饰器，用于缓存函数返回值

    Args:
        ttl_seconds: 缓存有效期（秒）
        prefix: 缓存键前缀，如果为 None，则使用函数名
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            key_prefix = prefix or func.__name__

            # 将参数转换为字符串
            args_str = json.dumps(args, sort_keys=True, default=str)
            kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)

            # 创建哈希
            key_hash = hashlib.md5(f"{key_prefix}:{args_str}:{kwargs_str}".encode()).hexdigest()
            cache_key = f"{key_prefix}:{key_hash}"

            # 尝试从缓存获取
            cached_result = UnifiedCacheService.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result

            # 执行原始函数
            logger.debug(f"Cache miss for {cache_key}")
            result = await func(*args, **kwargs)

            # 缓存结果
            UnifiedCacheService.set(cache_key, result, ttl_seconds)

            return result
        return wrapper
    return decorator

def clear_cache():
    """清除所有缓存"""
    # 清除内存缓存（兼容旧代码）
    global _cache
    _cache = {}

    # 清除统一缓存
    UnifiedCacheService.clear()

def clear_cache_by_prefix(prefix: str):
    """
    按前缀清除缓存

    Args:
        prefix: 缓存键前缀
    """
    # 清除内存缓存中的匹配项（兼容旧代码）
    keys_to_delete = [k for k in _cache.keys() if k.startswith(prefix)]
    for key in keys_to_delete:
        del _cache[key]

    # 清除统一缓存中的匹配项
    redis_keys = UnifiedCacheService.get_keys(f"{prefix}:*")
    for key in redis_keys:
        UnifiedCacheService.delete(key)

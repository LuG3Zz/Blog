import json
import hashlib
from typing import Any, Dict, Optional, Callable, TypeVar, cast, List
from functools import wraps

from app.core.config import settings
from app.services.cache_service import CacheService
from app.utils.logging import get_logger

# 定义缓存类型
T = TypeVar('T')

logger = get_logger(__name__)

# 根据配置导入适当的缓存服务
use_redis = False
try:
    use_redis = settings.USE_REDIS_CACHE
except Exception as e:
    logger.warning(f"Error reading Redis cache setting: {e}")

if use_redis:
    try:
        from app.services.redis_cache_service import RedisCacheService as ActiveCacheService
        logger.info("Using Redis cache service")
    except ImportError:
        logger.warning("Redis cache service not available, falling back to memory cache")
        ActiveCacheService = CacheService
else:
    ActiveCacheService = CacheService
    logger.info("Using memory cache service")

class UnifiedCacheService:
    """Unified cache service that delegates to the active cache service."""

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Get a value from cache if it exists."""
        return ActiveCacheService.get(key)

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300) -> None:
        """Set a value in cache with TTL in seconds."""
        ActiveCacheService.set(key, value, ttl)

    @classmethod
    def delete(cls, key: str) -> None:
        """Delete a value from cache."""
        ActiveCacheService.delete(key)

    @classmethod
    def clear(cls) -> None:
        """Clear all cache."""
        ActiveCacheService.clear()

    @classmethod
    def generate_key(cls, prefix: str, *args: Any, **kwargs: Any) -> str:
        """Generate a cache key from prefix and arguments."""
        return ActiveCacheService.generate_key(prefix, *args, **kwargs)

    @classmethod
    def get_keys(cls, pattern: str = "*") -> List[str]:
        """Get all keys matching pattern."""
        if hasattr(ActiveCacheService, "get_keys"):
            return ActiveCacheService.get_keys(pattern)
        # 内存缓存不支持模式匹配，返回所有键
        if ActiveCacheService == CacheService:
            return list(ActiveCacheService._cache.keys())
        return []

    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """Get cache statistics."""
        if hasattr(ActiveCacheService, "get_stats"):
            return ActiveCacheService.get_stats()
        # 内存缓存的简单统计
        if ActiveCacheService == CacheService:
            return {
                "keys_count": len(ActiveCacheService._cache),
                "type": "memory"
            }
        return {"type": "unknown"}

def cached(prefix: str, ttl: int = 300) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to cache function results."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # 生成缓存键
            cache_key = UnifiedCacheService.generate_key(prefix, *args, **kwargs)

            # 尝试从缓存获取
            cached_result = UnifiedCacheService.get(cache_key)
            if cached_result is not None:
                return cast(T, cached_result)

            # 执行原始函数
            result = func(*args, **kwargs)

            # 缓存结果
            UnifiedCacheService.set(cache_key, result, ttl)

            return result
        return wrapper
    return decorator

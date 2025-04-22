import time
import json
import hashlib
from typing import Any, Dict, Optional, Callable, TypeVar, cast
from functools import wraps

# 定义缓存类型
T = TypeVar('T')

class CacheService:
    """Simple in-memory cache service with TTL support."""
    
    # 内存缓存存储
    _cache: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Get a value from cache if it exists and is not expired."""
        if key not in cls._cache:
            return None
            
        cache_item = cls._cache[key]
        
        # 检查是否过期
        if 'expires_at' in cache_item and cache_item['expires_at'] < time.time():
            # 已过期，删除缓存项
            del cls._cache[key]
            return None
            
        return cache_item.get('value')
    
    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300) -> None:
        """Set a value in cache with TTL in seconds."""
        cls._cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl
        }
    
    @classmethod
    def delete(cls, key: str) -> None:
        """Delete a value from cache."""
        if key in cls._cache:
            del cls._cache[key]
    
    @classmethod
    def clear(cls) -> None:
        """Clear all cache."""
        cls._cache.clear()
    
    @classmethod
    def generate_key(cls, prefix: str, *args: Any, **kwargs: Any) -> str:
        """Generate a cache key from prefix and arguments."""
        # 将参数转换为字符串
        args_str = json.dumps(args, sort_keys=True, default=str)
        kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)
        
        # 创建哈希
        key_hash = hashlib.md5(f"{prefix}:{args_str}:{kwargs_str}".encode()).hexdigest()
        return f"{prefix}:{key_hash}"

def cached(prefix: str, ttl: int = 300) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to cache function results."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # 生成缓存键
            cache_key = CacheService.generate_key(prefix, *args, **kwargs)
            
            # 尝试从缓存获取
            cached_result = CacheService.get(cache_key)
            if cached_result is not None:
                return cast(T, cached_result)
            
            # 执行原始函数
            result = func(*args, **kwargs)
            
            # 缓存结果
            CacheService.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

import json
import time
import hashlib
from typing import Any, Dict, Optional, Callable, TypeVar, cast, List
from functools import wraps
import redis
from redis.client import Redis
from redis.connection import ConnectionPool

from app.core.config import settings
from app.utils.logging import get_logger

# 定义缓存类型
T = TypeVar('T')

logger = get_logger(__name__)

class RedisCacheService:
    """Redis-based cache service with TTL support."""
    
    _pool: Optional[ConnectionPool] = None
    _client: Optional[Redis] = None
    
    @classmethod
    def get_connection_pool(cls) -> ConnectionPool:
        """Get or create a Redis connection pool."""
        if cls._pool is None:
            # 创建连接参数
            connection_kwargs = {
                "host": settings.REDIS_HOST,
                "port": settings.REDIS_PORT,
                "db": settings.REDIS_DB,
                "decode_responses": True,  # 自动解码响应为字符串
            }
            
            # 添加可选的认证参数
            if settings.REDIS_PASSWORD:
                connection_kwargs["password"] = settings.REDIS_PASSWORD
            
            if settings.REDIS_USERNAME:
                connection_kwargs["username"] = settings.REDIS_USERNAME
                
            if settings.REDIS_USE_SSL:
                connection_kwargs["ssl"] = True
                connection_kwargs["ssl_cert_reqs"] = None  # 不验证证书
            
            # 创建连接池
            cls._pool = redis.ConnectionPool(**connection_kwargs)
            logger.info(f"Created Redis connection pool to {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            
        return cls._pool
    
    @classmethod
    def get_client(cls) -> Redis:
        """Get or create a Redis client."""
        if cls._client is None:
            pool = cls.get_connection_pool()
            cls._client = redis.Redis(connection_pool=pool)
            logger.info("Created Redis client")
            
        return cls._client
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Get a value from cache if it exists."""
        try:
            client = cls.get_client()
            value = client.get(key)
            
            if value is None:
                return None
                
            # 尝试解析 JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # 如果不是 JSON，则直接返回值
                return value
                
        except Exception as e:
            logger.error(f"Error getting value from Redis cache: {e}")
            return None
    
    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300) -> None:
        """Set a value in cache with TTL in seconds."""
        try:
            client = cls.get_client()
            
            # 如果值不是字符串，则转换为 JSON
            if not isinstance(value, (str, bytes)):
                value = json.dumps(value, default=str)
                
            client.set(key, value, ex=ttl)
        except Exception as e:
            logger.error(f"Error setting value in Redis cache: {e}")
    
    @classmethod
    def delete(cls, key: str) -> None:
        """Delete a value from cache."""
        try:
            client = cls.get_client()
            client.delete(key)
        except Exception as e:
            logger.error(f"Error deleting value from Redis cache: {e}")
    
    @classmethod
    def clear(cls) -> None:
        """Clear all cache."""
        try:
            client = cls.get_client()
            client.flushdb()
            logger.info("Redis cache cleared")
        except Exception as e:
            logger.error(f"Error clearing Redis cache: {e}")
    
    @classmethod
    def generate_key(cls, prefix: str, *args: Any, **kwargs: Any) -> str:
        """Generate a cache key from prefix and arguments."""
        # 将参数转换为字符串
        args_str = json.dumps(args, sort_keys=True, default=str)
        kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)
        
        # 创建哈希
        key_hash = hashlib.md5(f"{prefix}:{args_str}:{kwargs_str}".encode()).hexdigest()
        return f"{prefix}:{key_hash}"
    
    @classmethod
    def get_keys(cls, pattern: str = "*") -> List[str]:
        """Get all keys matching pattern."""
        try:
            client = cls.get_client()
            return client.keys(pattern)
        except Exception as e:
            logger.error(f"Error getting keys from Redis cache: {e}")
            return []
    
    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """Get cache statistics."""
        try:
            client = cls.get_client()
            info = client.info()
            stats = {
                "used_memory": info.get("used_memory_human", "N/A"),
                "used_memory_peak": info.get("used_memory_peak_human", "N/A"),
                "total_connections_received": info.get("total_connections_received", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0),
            }
            
            # 计算命中率
            hits = info.get("keyspace_hits", 0)
            misses = info.get("keyspace_misses", 0)
            total = hits + misses
            hit_rate = (hits / total) * 100 if total > 0 else 0
            stats["hit_rate"] = f"{hit_rate:.2f}%"
            
            return stats
        except Exception as e:
            logger.error(f"Error getting Redis cache stats: {e}")
            return {"error": str(e)}

def redis_cached(prefix: str, ttl: int = 300) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to cache function results in Redis."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # 如果未启用 Redis 缓存，则直接执行函数
            if not settings.USE_REDIS_CACHE:
                return func(*args, **kwargs)
                
            # 生成缓存键
            cache_key = RedisCacheService.generate_key(prefix, *args, **kwargs)
            
            # 尝试从缓存获取
            cached_result = RedisCacheService.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cast(T, cached_result)
            
            # 执行原始函数
            logger.debug(f"Cache miss for {cache_key}")
            result = func(*args, **kwargs)
            
            # 缓存结果
            RedisCacheService.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

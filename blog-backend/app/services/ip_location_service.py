import os
import json
import time
from ipregion import IP2Region
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from app.utils.logging import get_logger
from app.services.unified_cache_service import UnifiedCacheService

logger = get_logger(__name__)

class IPLocationService:
    """Service for resolving IP address locations."""

    _ip2region = None
    _cache_service = None
    _cache_prefix = "ip_location:"
    _cache_ttl = 86400 * 7  # 7 days in seconds

    @classmethod
    def init_app(cls):
        """Initialize the service when the application starts."""
        # 初始化 IP2Region 数据库
        cls.initialize()

        # 初始化缓存服务
        cls._cache_service = UnifiedCacheService()

        logger.info("IPLocationService initialized with cache")

    @classmethod
    def initialize(cls, db_path: Optional[str] = None):
        """Initialize the IP2Region database."""
        try:
            if not db_path:
                # 使用默认路径
                cur_path = os.path.abspath(os.path.dirname(__file__))
                # 使用 app/data 目录存放数据库文件
                data_dir = os.path.join(os.path.dirname(os.path.dirname(cur_path)), "app", "data")
                db_path = os.path.join(data_dir, "ipcache.db3")

                # 确保目录存在
                os.makedirs(data_dir, exist_ok=True)

            if os.path.exists(db_path):
                cls._ip2region = IP2Region(db_path=db_path)
                logger.info(f"Initialized IP2Region with database: {db_path}")
            else:
                # 如果数据库文件不存在，创建一个空数据库
                try:
                    # 创建一个空的 IP2Region 实例，它会自动创建数据库文件
                    cls._ip2region = IP2Region(db_path=db_path)
                    logger.info(f"Created new IP2Region database at: {db_path}")
                except Exception as e:
                    logger.error(f"Failed to create IP2Region database: {e}")
                    logger.error(f"IP2Region database not found at: {db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize IP2Region: {e}")

    @classmethod
    def _get_cache_key(cls, ip_address: str) -> str:
        """Generate a cache key for an IP address."""
        return f"{cls._cache_prefix}{ip_address}"

    @classmethod
    def _get_from_cache(cls, ip_address: str) -> Optional[str]:
        """Get location from cache."""
        if not cls._cache_service:
            return None

        try:
            cache_key = cls._get_cache_key(ip_address)
            cached_value = cls._cache_service.get(cache_key)

            if cached_value:
                logger.debug(f"Cache hit for IP: {ip_address}")
                return cached_value

            logger.debug(f"Cache miss for IP: {ip_address}")
            return None
        except Exception as e:
            logger.warning(f"Error getting IP location from cache: {e}")
            return None

    @classmethod
    def _save_to_cache(cls, ip_address: str, location: str) -> bool:
        """Save location to cache."""
        if not cls._cache_service or not location or location == "未知地区":
            return False

        try:
            cache_key = cls._get_cache_key(ip_address)
            cls._cache_service.set(cache_key, location, cls._cache_ttl)
            logger.debug(f"Cached IP location: {ip_address} -> {location}")
            return True
        except Exception as e:
            logger.warning(f"Error saving IP location to cache: {e}")
            return False

    @classmethod
    def get_location(cls, ip_address: str) -> str:
        """
        Get location information for an IP address.

        Args:
            ip_address: The IP address to resolve

        Returns:
            String containing location information or "未知地区" if not found
        """
        # 开始计时
        start_time = time.time()
        
        # 处理本地或内网IP
        if ip_address in ['127.0.0.1', 'localhost', '::1'] or ip_address.startswith('192.168.') or ip_address.startswith('10.') or ip_address.startswith('172.'):
            return "本地网络"

        # 先从缓存中获取
        cached_location = cls._get_from_cache(ip_address)
        if cached_location:
            logger.debug(f"[性能] IP属地缓存命中: {ip_address} -> {cached_location}")
            return cached_location

        # 如果缓存中没有，初始化 IP2Region
        if not cls._ip2region:
            cls.initialize()

        if not cls._ip2region:
            # 缓存未知地区结果，避免重复查询
            cls._save_to_cache(ip_address, "未知地区")
            return "未知地区"

        try:
            # 简化查询逻辑，直接使用 search 方法
            try:
                # 使用全局实例而不是创建新实例
                region = cls._ip2region.search(ip_address)
                logger.debug(f"[性能] IP地址解析耗时: {(time.time() - start_time) * 1000:.2f}ms")
            except Exception as e:
                logger.error(f"IP地址解析失败 ({ip_address}): {str(e)}")
                # 缓存未知地区结果，避免重复查询
                cls._save_to_cache(ip_address, "未知地区")
                return "未知地区"

            if region and isinstance(region, dict):
                # 从返回的字典中获取地区信息
                region_str = region.get('data', {}).get('region', '')
                
                if not region_str:
                    # 缓存未知地区结果，避免重复查询
                    cls._save_to_cache(ip_address, "未知地区")
                    return "未知地区"
                
                # 简化处理逻辑
                parts = region_str.split()
                
                # 移除"中国"前缀
                parts = [p for p in parts if p != '中国']
                
                # 简化地区名称处理
                if len(parts) >= 2:
                    # 对于直辖市，直接返回市名
                    if parts[0] in ['北京', '上海', '天津', '重庆']:
                        location = f"{parts[0]}市"
                    else:
                        # 对于其他地区，返回省市或前两部分
                        location = ' '.join(parts[:2])
                elif len(parts) == 1:
                    location = parts[0]
                else:
                    location = "未知地区"
                
                # 缓存结果
                cls._save_to_cache(ip_address, location)
                logger.debug(f"[性能] IP属地解析总耗时: {(time.time() - start_time) * 1000:.2f}ms")
                return location
            
            # 如果解析失败，返回未知地区
            logger.warning(f"Failed to resolve IP location for: {ip_address}")
            cls._save_to_cache(ip_address, "未知地区")
            return "未知地区"
        except Exception as e:
            logger.error(f"IP解析失败 ({ip_address}): {str(e)}")
            # 缓存未知地区结果，避免重复查询
            cls._save_to_cache(ip_address, "未知地区")
            return "未知地区"

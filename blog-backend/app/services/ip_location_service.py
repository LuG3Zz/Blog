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
        # 处理本地或内网IP
        if ip_address in ['127.0.0.1', 'localhost', '::1'] or ip_address.startswith('192.168.') or ip_address.startswith('10.') or ip_address.startswith('172.'):
            return "本地网络"

        # 先从缓存中获取
        cached_location = cls._get_from_cache(ip_address)
        if cached_location:
            return cached_location

        # 如果缓存中没有，初始化 IP2Region
        if not cls._ip2region:
            cls.initialize()

        if not cls._ip2region:
            return "未知地区"

        try:
            # 先尝试使用 searchWithFile 方法，这样可以获取更详细的地址信息
            try:
                # 创建一个新的 IP2Region 实例，避免缓存问题
                ip2region = IP2Region(ip=ip_address)
                region = ip2region.searchWithFile()
                logger.debug(f"IP地址解析结果 (searchWithFile): {region}")

                # 如果 searchWithFile 失败，尝试使用 search 方法
                if region.get('errno') != 0:
                    region = ip2region.search()
                    logger.debug(f"IP地址解析结果 (search): {region}")
            except Exception as e:
                logger.error(f"IP地址解析失败 ({ip_address}): {str(e)}")
                region = None

            if region and isinstance(region, dict):
                # 从返回的字典中获取地区信息
                region_str = region.get('data', {}).get('region', '')

                if region_str:
                    # 如果是 searchWithFile 返回的结果，格式可能是“中国 浙江省 杭州市 阿里云”
                    if ' ' in region_str and '中国' in region_str:
                        parts = region_str.split()
                        # 移除“中国”前缀
                        parts = [p for p in parts if p != '中国']

                        # 如果有省和市的信息，返回“省市”格式
                        if len(parts) >= 2:
                            # 判断是否是中国地区
                            is_china = any(p in ['中国', '大陆', '台湾', '香港', '澳门'] for p in region_str.split())

                            # 对于直辖市（北京、上海、天津、重庆），直接返回市名
                            if parts[0] in ['北京', '上海', '天津', '重庆']:
                                # 如果市名不以“市”结尾，添加“市”后缀
                                if not parts[0].endswith('市'):
                                    parts[0] += '市'
                                location = parts[0]
                            # 对于中国其他地区，返回“省市”格式
                            elif is_china:
                                # 如果省份不以“省”结尾，添加“省”后缀
                                if not parts[0].endswith('省') and not parts[0].endswith('市') and not parts[0].endswith('自治区') and not parts[0].endswith('特别行政区'):
                                    parts[0] += '省'

                                # 如果市不以“市”结尾，添加“市”后缀
                                if not parts[1].endswith('市') and not parts[1].endswith('县'):
                                    parts[1] += '市'

                                location = f"{parts[0]}{parts[1]}"
                            # 对于国外地区，保留更多详细信息
                            else:
                                # 如果有多个部分，保留前三个部分（国家、州/省、城市）
                                if len(parts) >= 3:
                                    location = ' '.join(parts[:3])
                                # 如果只有两个部分，保留两个部分（国家、州/省）
                                elif len(parts) == 2:
                                    location = ' '.join(parts)
                                # 如果只有一个部分，直接返回
                                else:
                                    location = parts[0]
                            cls._save_to_cache(ip_address, location)
                            return location
                        elif len(parts) == 1:
                            # 判断是否是中国地区
                            is_china = any(p in ['中国', '大陆', '台湾', '香港', '澳门'] for p in region_str.split())

                            # 如果只有省份信息
                            # 对于直辖市（北京、上海、天津、重庆），添加“市”后缀
                            if parts[0] in ['北京', '上海', '天津', '重庆'] and not parts[0].endswith('市'):
                                parts[0] += '市'
                            # 对于中国其他地区，添加“省”后缀
                            elif is_china and not parts[0].endswith('省') and not parts[0].endswith('市') and not parts[0].endswith('自治区') and not parts[0].endswith('特别行政区'):
                                parts[0] += '省'
                            # 对于国外地区，保持原样
                            location = parts[0]
                            cls._save_to_cache(ip_address, location)
                            return location

                    # 如果是中文地区名称，直接返回
                    elif any('\u4e00' <= char <= '\u9fff' for char in region_str):
                        # 判断是否是中国地区
                        is_china = any(p in ['中国', '大陆', '台湾', '香港', '澳门'] for p in region_str.split())

                        # 如果只有省份信息
                        if len(region_str) <= 3:
                            # 对于直辖市（北京、上海、天津、重庆），添加“市”后缀
                            if region_str in ['北京', '上海', '天津', '重庆'] and not region_str.endswith('市'):
                                region_str += '市'
                            # 对于中国其他地区，添加“省”后缀
                            elif is_china and not region_str.endswith('省') and not region_str.endswith('市') and not region_str.endswith('自治区') and not region_str.endswith('特别行政区'):
                                region_str += '省'
                        location = region_str
                        cls._save_to_cache(ip_address, location)
                        return location

                    # 如果是英文地区名称，返回更详细的信息
                    else:
                        parts = region_str.split()
                        # 如果有多个部分，保留前三个部分（国家、州/省、城市）
                        if len(parts) >= 3:
                            location = ' '.join(parts[:3])
                        # 如果只有两个部分，保留两个部分（国家、州/省）
                        elif len(parts) == 2:
                            location = ' '.join(parts)
                        # 如果只有一个部分，直接返回
                        else:
                            location = region_str
                        cls._save_to_cache(ip_address, location)
                        return location
            # 如果所有方法都失败，返回未知地区
            logger.warning(f"Failed to resolve IP location for: {ip_address}")
            return "未知地区"
        except Exception as e:
            logger.error(f"IP解析失败 ({ip_address}): {str(e)}")
            return "未知地区"

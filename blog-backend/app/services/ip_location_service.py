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

        # 处理IP地址中可能包含的端口号
        if ':' in ip_address:
            # 分离IP地址和端口号，只保留IP部分
            ip_address = ip_address.split(':')[0]
            logger.debug(f"从IP地址中移除端口号: {ip_address}")

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
                # 记录返回的region类型，便于调试
                logger.debug(f"IP2Region返回类型: {type(region)}, 值: {region}")
            except Exception as e:
                logger.error(f"IP地址解析失败 ({ip_address}): {str(e)}")
                # 缓存未知地区结果，避免重复查询
                cls._save_to_cache(ip_address, "未知地区")
                return "未知地区"

            # 处理不同类型的返回结果
            region_str = ""

            # 如果返回的是字典类型
            if region and isinstance(region, dict):
                # 从返回的字典中获取地区信息
                region_str = region.get('data', {}).get('region', '')
            # 如果返回的是字符串类型
            elif region and isinstance(region, str):
                region_str = region
            # 如果返回的是其他类型，尝试转换为字符串
            elif region:
                try:
                    region_str = str(region)
                except:
                    region_str = ""

            if not region_str:
                # 缓存未知地区结果，避免重复查询
                cls._save_to_cache(ip_address, "未知地区")
                return "未知地区"

            # 处理地区信息
            parts = region_str.split()

            # 移除"中国"前缀
            parts = [p for p in parts if p != '中国']

            # 定义国外地区列表
            foreign_countries = [
                '新加坡', '美国', '日本', '韩国', '英国', '法国', '德国', '加拿大', '澳大利亚',
                '俄罗斯', '印度', '巴西', '墨西哥', '南非', '阿联酋', '沙特', '泰国', '越南',
                '马来西亚', '印尼', '菲律宾', '荷兰', '比利时', '瑞士', '瑞典', '挪威', '芬兰',
                '丹麦', '意大利', '西班牙', '葡萄牙', '希腊', '土耳其', '以色列', '埃及'
            ]

            # 检查是否为国外IP
            is_foreign = False
            country_name = ""
            if parts and parts[0] in foreign_countries:
                is_foreign = True
                country_name = parts[0]
                logger.debug(f"检测到国外IP: {ip_address}, 国家: {country_name}, 原始数据: {region_str}")

            # 对国外IP进行特殊处理
            if is_foreign:
                # 只保留国家名称，或者国家+地区
                if len(parts) >= 2:
                    # 如果第二部分是方向词（东、南、西、北等）
                    if any(direction in parts[1] for direction in ['东', '南', '西', '北', '中']):
                        location = f"{country_name}"
                        logger.debug(f"国外IP处理: 检测到方向词，仅保留国家名称: {location}")
                    else:
                        # 否则保留第二部分作为地区
                        location = f"{country_name} {parts[1]}"
                        logger.debug(f"国外IP处理: 保留国家和地区: {location}")
                else:
                    location = country_name
                    logger.debug(f"国外IP处理: 仅有国家信息: {location}")
            # 中国IP地址处理
            elif len(parts) >= 3:  # 有省市区三级信息
                # 对于直辖市，格式为"北京市 xx区"
                if parts[0] in ['北京', '上海', '天津', '重庆']:
                    # 确保直辖市名称后面有"市"
                    city_name = parts[0] if parts[0].endswith('市') else f"{parts[0]}市"
                    # 组合直辖市的区县信息
                    location = f"{city_name} {parts[1]} {parts[2]}"
                else:
                    # 对于普通省份，格式为"xx省 xx市 xx区/县"
                    province = parts[0]
                    city = parts[1]
                    district = parts[2]

                    # 确保省份名称规范
                    if not (province.endswith('省') or province in ['内蒙古', '新疆', '西藏', '广西', '宁夏', '香港', '澳门', '台湾']):
                        if province not in ['内蒙古', '新疆', '西藏', '广西', '宁夏', '香港', '澳门', '台湾']:
                            province += '省'

                    # 确保城市名称规范
                    if not city.endswith(('市', '地区', '盟', '自治州')):
                        city += '市'

                    # 组合完整地址
                    location = f"{province} {city} {district}"

            elif len(parts) >= 2:  # 有省市两级信息
                # 对于直辖市，格式为"北京市 xx区"
                if parts[0] in ['北京', '上海', '天津', '重庆']:
                    # 确保直辖市名称后面有"市"
                    city_name = parts[0] if parts[0].endswith('市') else f"{parts[0]}市"
                    location = f"{city_name} {parts[1]}"
                else:
                    # 对于普通省份，格式为"xx省 xx市"
                    province = parts[0]
                    city = parts[1]

                    # 确保省份名称规范
                    if not (province.endswith('省') or province in ['内蒙古', '新疆', '西藏', '广西', '宁夏', '香港', '澳门', '台湾']):
                        if province not in ['内蒙古', '新疆', '西藏', '广西', '宁夏', '香港', '澳门', '台湾']:
                            province += '省'

                    # 确保城市名称规范
                    if not city.endswith(('市', '地区', '盟', '自治州')):
                        city += '市'

                    location = f"{province} {city}"

            elif len(parts) == 1:  # 只有省级信息
                # 对于直辖市，直接返回市名
                if parts[0] in ['北京', '上海', '天津', '重庆']:
                    location = f"{parts[0]}市"
                else:
                    # 对于其他地区，返回省级
                    province = parts[0]
                    # 确保省级名称规范
                    if not (province.endswith('省') or province in ['内蒙古', '新疆', '西藏', '广西', '宁夏', '香港', '澳门', '台湾']):
                        if province not in ['内蒙古', '新疆', '西藏', '广西', '宁夏', '香港', '澳门', '台湾']:
                            province += '省'
                    location = province
            else:
                location = "未知地区"

            # 记录解析结果
            logger.debug(f"IP地址 {ip_address} 解析结果: {location} (原始数据: {region_str})")

            # 缓存结果
            cls._save_to_cache(ip_address, location)
            logger.debug(f"[性能] IP属地解析总耗时: {(time.time() - start_time) * 1000:.2f}ms")
            return location
        except Exception as e:
            logger.error(f"IP解析失败 ({ip_address}): {str(e)}")
            # 缓存未知地区结果，避免重复查询
            cls._save_to_cache(ip_address, "未知地区")
            return "未知地区"

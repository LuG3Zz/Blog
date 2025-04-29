"""
访客记录服务模块：提供访客记录相关的业务逻辑
"""
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, extract
from datetime import datetime, timedelta, timezone
import re
import user_agents

from app import models
from app.schemas.visitor import VisitorCreate, VisitorResponse, VisitorStatistics
from app.utils.logging import get_logger
from app.utils.pagination import PaginationParams, PagedResponse
from app.services.ip_location_service import IPLocationService

logger = get_logger(__name__)

class VisitorService:
    """访客记录服务类"""

    @staticmethod
    def create_visitor_record(
        db: Session,
        ip_address: str,
        path: str,
        user_agent_string: Optional[str] = None,
        referer: Optional[str] = None,
        visitor_name: Optional[str] = "访客",
        user_id: Optional[str] = None,
        client_id: Optional[str] = None
    ) -> models.Visitor:
        """
        创建访客记录

        参数:
        - **db**: 数据库会话
        - **ip_address**: 访客IP地址
        - **path**: 访问路径
        - **user_agent_string**: 用户代理字符串
        - **referer**: 来源页面
        - **visitor_name**: 访客名称
        - **user_id**: 用户ID
        - **client_id**: WebSocket客户端ID

        返回:
        - 创建的访客记录
        """
        # 解析用户代理
        is_mobile = False
        is_bot = False

        if user_agent_string:
            try:
                user_agent = user_agents.parse(user_agent_string)
                is_mobile = user_agent.is_mobile
                is_bot = user_agent.is_bot
            except Exception as e:
                logger.error(f"解析用户代理失败: {e}")

                # 使用简单的正则表达式检测移动设备和爬虫
                is_mobile = bool(re.search(r'Mobile|Android|iPhone|iPad', user_agent_string))
                is_bot = bool(re.search(r'bot|crawl|spider|slurp|Baiduspider|Googlebot', user_agent_string, re.I))

        # 获取IP地址归属地
        ip_region = IPLocationService.get_location(ip_address)

        # 创建访客记录
        visitor = models.Visitor(
            ip_address=ip_address,
            ip_region=ip_region,
            user_agent=user_agent_string,
            referer=referer,
            path=path,
            visit_time=datetime.now(timezone.utc),
            is_mobile=is_mobile,
            is_bot=is_bot,
            visitor_name=visitor_name,
            user_id=user_id,
            client_id=client_id
        )

        db.add(visitor)
        db.commit()
        db.refresh(visitor)
        return visitor

    @staticmethod
    def get_visitors(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        ip_address: Optional[str] = None,
        path: Optional[str] = None,
        visitor_name: Optional[str] = None,
        user_id: Optional[str] = None,
        is_mobile: Optional[bool] = None,
        is_bot: Optional[bool] = None
    ) -> Tuple[List[models.Visitor], int]:
        """
        获取访客记录列表

        参数:
        - **db**: 数据库会话
        - **skip**: 跳过的记录数
        - **limit**: 返回的记录数
        - **start_date**: 开始日期
        - **end_date**: 结束日期
        - **ip_address**: IP地址筛选
        - **path**: 访问路径筛选
        - **is_mobile**: 是否为移动设备
        - **is_bot**: 是否为爬虫

        返回:
        - 访客记录列表和总记录数
        """
        # 构建查询
        query = db.query(models.Visitor)

        # 应用筛选条件
        if start_date:
            query = query.filter(models.Visitor.visit_time >= start_date)

        if end_date:
            query = query.filter(models.Visitor.visit_time <= end_date)

        if ip_address:
            query = query.filter(models.Visitor.ip_address.like(f"%{ip_address}%"))

        if path:
            query = query.filter(models.Visitor.path.like(f"%{path}%"))

        if visitor_name:
            query = query.filter(models.Visitor.visitor_name.like(f"%{visitor_name}%"))

        if user_id:
            query = query.filter(models.Visitor.user_id == user_id)

        if is_mobile is not None:
            query = query.filter(models.Visitor.is_mobile == is_mobile)

        if is_bot is not None:
            query = query.filter(models.Visitor.is_bot == is_bot)

        # 获取总记录数
        total = query.count()

        # 应用分页并按访问时间降序排序
        visitors = query.order_by(models.Visitor.visit_time.desc()) \
            .offset(skip).limit(limit).all()

        return visitors, total

    @staticmethod
    def get_visitor_by_id(db: Session, visitor_id: int) -> Optional[models.Visitor]:
        """
        根据ID获取访客记录

        参数:
        - **db**: 数据库会话
        - **visitor_id**: 访客记录ID

        返回:
        - 访客记录，如果不存在则返回None
        """
        return db.query(models.Visitor).filter(models.Visitor.id == visitor_id).first()

    @staticmethod
    def delete_visitor(db: Session, visitor_id: int) -> bool:
        """
        删除访客记录

        参数:
        - **db**: 数据库会话
        - **visitor_id**: 访客记录ID

        返回:
        - 是否删除成功
        """
        visitor = db.query(models.Visitor).filter(models.Visitor.id == visitor_id).first()
        if not visitor:
            return False

        db.delete(visitor)
        db.commit()
        return True

    @staticmethod
    def batch_delete_visitors(db: Session, visitor_ids: List[int]) -> int:
        """
        批量删除访客记录

        参数:
        - **db**: 数据库会话
        - **visitor_ids**: 访客记录ID列表

        返回:
        - 删除的记录数
        """
        if not visitor_ids:
            return 0

        # 查询并删除访客记录
        query = db.query(models.Visitor).filter(models.Visitor.id.in_(visitor_ids))
        visitors = query.all()

        if not visitors:
            return 0

        for visitor in visitors:
            db.delete(visitor)

        db.commit()
        return len(visitors)

    @staticmethod
    def get_visitor_statistics(
        db: Session,
        days: int = 30
    ) -> VisitorStatistics:
        """
        获取访客统计信息

        参数:
        - **db**: 数据库会话
        - **days**: 统计天数

        返回:
        - 访客统计信息
        """
        # 计算开始日期
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        # 查询总访问量
        total_visits = db.query(func.count(models.Visitor.id)) \
            .filter(models.Visitor.visit_time >= start_date) \
            .scalar() or 0

        # 查询独立访客数
        unique_visitors = db.query(func.count(func.distinct(models.Visitor.ip_address))) \
            .filter(models.Visitor.visit_time >= start_date) \
            .scalar() or 0

        # 查询移动设备访问量
        mobile_visits = db.query(func.count(models.Visitor.id)) \
            .filter(models.Visitor.visit_time >= start_date) \
            .filter(models.Visitor.is_mobile == True) \
            .scalar() or 0

        # 查询爬虫访问量
        bot_visits = db.query(func.count(models.Visitor.id)) \
            .filter(models.Visitor.visit_time >= start_date) \
            .filter(models.Visitor.is_bot == True) \
            .scalar() or 0

        # 查询访问量最高的页面
        top_pages_query = db.query(
            models.Visitor.path,
            func.count(models.Visitor.id).label('count')
        ) \
            .filter(models.Visitor.visit_time >= start_date) \
            .group_by(models.Visitor.path) \
            .order_by(desc('count')) \
            .limit(10)

        top_pages = [
            {"path": page.path, "count": page.count}
            for page in top_pages_query.all()
        ]

        # 查询访问量最高的地区
        top_regions_query = db.query(
            models.Visitor.ip_region,
            func.count(models.Visitor.id).label('count')
        ) \
            .filter(models.Visitor.visit_time >= start_date) \
            .filter(models.Visitor.ip_region != None) \
            .group_by(models.Visitor.ip_region) \
            .order_by(desc('count')) \
            .limit(10)

        top_regions = [
            {"region": region.ip_region or "未知地区", "count": region.count}
            for region in top_regions_query.all()
        ]

        # 查询最近访问趋势（按天统计）
        trend_query = db.query(
            func.date(models.Visitor.visit_time).label('date'),
            func.count(models.Visitor.id).label('count')
        ) \
            .filter(models.Visitor.visit_time >= start_date) \
            .group_by(func.date(models.Visitor.visit_time)) \
            .order_by('date')

        recent_trend = [
            {"date": trend.date.strftime('%Y-%m-%d'), "count": trend.count}
            for trend in trend_query.all()
        ]

        # 返回统计信息
        return VisitorStatistics(
            total_visits=total_visits,
            unique_visitors=unique_visitors,
            mobile_visits=mobile_visits,
            bot_visits=bot_visits,
            top_pages=top_pages,
            top_regions=top_regions,
            recent_trend=recent_trend
        )

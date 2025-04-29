"""
访客记录模式模块：定义访客记录相关的数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class VisitorBase(BaseModel):
    """访客记录基础模型"""
    ip_address: str = Field(..., description="访客IP地址")
    ip_region: Optional[str] = Field(None, description="IP地址归属地")
    user_agent: Optional[str] = Field(None, description="用户代理字符串")
    referer: Optional[str] = Field(None, description="来源页面")
    path: str = Field(..., description="访问路径")
    is_mobile: bool = Field(False, description="是否为移动设备")
    is_bot: bool = Field(False, description="是否为爬虫")
    visitor_name: Optional[str] = Field("访客", description="访客名称")
    user_id: Optional[str] = Field(None, description="用户ID")
    client_id: Optional[str] = Field(None, description="WebSocket客户端ID")

class VisitorCreate(VisitorBase):
    """创建访客记录模型"""
    pass

class VisitorResponse(VisitorBase):
    """访客记录响应模型"""
    id: int
    visit_time: datetime

    model_config = {
        "from_attributes": True
    }

class VisitorBatchDeleteRequest(BaseModel):
    """批量删除访客记录请求模型"""
    visitor_ids: List[int] = Field(..., description="要删除的访客记录ID列表")

class VisitorStatistics(BaseModel):
    """访客统计信息模型"""
    total_visits: int = Field(..., description="总访问量")
    unique_visitors: int = Field(..., description="独立访客数")
    mobile_visits: int = Field(..., description="移动设备访问量")
    bot_visits: int = Field(..., description="爬虫访问量")
    top_pages: List[Dict[str, Any]] = Field(..., description="访问量最高的页面")
    top_regions: List[Dict[str, Any]] = Field(..., description="访问量最高的地区")
    recent_trend: List[Dict[str, Any]] = Field(..., description="最近访问趋势")

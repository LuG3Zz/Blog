"""
通知历史模式模块：定义通知历史相关的数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class NotificationHistoryBase(BaseModel):
    """通知历史基础模型"""
    title: str = Field(..., description="通知标题")
    content: str = Field(..., description="通知内容")
    level: str = Field(..., description="通知级别")
    target_users: Optional[List[int]] = Field(None, description="目标用户ID列表")

class NotificationHistoryCreate(NotificationHistoryBase):
    """创建通知历史模型"""
    pass

class NotificationHistoryResponse(NotificationHistoryBase):
    """通知历史响应模型"""
    id: int = Field(..., description="通知ID")
    created_at: datetime = Field(..., description="创建时间")
    created_by: int = Field(..., description="创建者ID")
    created_by_username: str = Field(..., description="创建者用户名")

    model_config = {
        "from_attributes": True
    }

class NotificationHistoryList(BaseModel):
    """通知历史列表模型"""
    items: List[NotificationHistoryResponse]
    total: int
    page: int
    page_size: int
    pages: int

from pydantic import BaseModel
from typing import List
from datetime import date

class HeatmapItem(BaseModel):
    """单个热力图数据项"""
    date: str  # 格式为 'YYYY-MM-DD'
    count: int

class HeatmapResponse(BaseModel):
    """热力图响应模型"""
    values: List[HeatmapItem]

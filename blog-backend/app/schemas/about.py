"""
About页面相关的schema
"""
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class AboutPageBase(BaseModel):
    """About页面基础模型"""
    content: Dict[str, Any] = Field(..., description="页面内容，JSON格式")

class AboutPageCreate(AboutPageBase):
    """创建About页面模型"""
    pass

class AboutPageUpdate(BaseModel):
    """更新About页面模型"""
    content: Optional[Dict[str, Any]] = Field(None, description="页面内容，JSON格式")

class AboutPageResponse(AboutPageBase):
    """About页面响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

    def model_dump(self, *args, **kwargs):
        """确保所有字段都被正确序列化"""
        result = super().model_dump(*args, **kwargs)
        # 确保 content 字段包含 skills 字段
        if "content" in result and isinstance(result["content"], dict):
            if "skills" not in result["content"]:
                result["content"]["skills"] = []
        return result

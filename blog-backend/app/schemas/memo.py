from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.user import UserBriefNoSocial

class MemoBase(BaseModel):
    """备忘录基础模式，包含共同属性。"""
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = Field(default="")

class MemoCreate(MemoBase):
    """创建备忘录的模式。"""
    is_encrypted: bool = False
    password: Optional[str] = None  # 如果is_encrypted为True，则需要提供密码

class MemoUpdate(BaseModel):
    """更新备忘录的模式。"""
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None
    is_encrypted: Optional[bool] = None
    password: Optional[str] = None  # 如果要修改密码，提供新密码

class MemoResponse(MemoBase):
    """备忘录响应模式。"""
    id: int
    is_encrypted: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
    # 不返回密码哈希

    model_config = {
        "from_attributes": True
    }

class MemoWithoutContent(BaseModel):
    """备忘录列表响应模式，现在也包含内容字段。"""
    id: int
    title: Optional[str] = None
    content: Optional[str] = None  # 添加内容字段
    is_encrypted: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class MemoWithUser(MemoWithoutContent):
    """包含用户信息的备忘录响应模式。"""
    user: Optional[UserBriefNoSocial] = None

    model_config = {
        "from_attributes": True
    }

class MemoPasswordVerify(BaseModel):
    """验证备忘录密码的模式。"""
    password: str = Field(..., min_length=1)

class MemoPasswordVerifyResponse(BaseModel):
    """验证备忘录密码的响应模式。"""
    success: bool
    content: Optional[str] = None  # 验证成功时返回内容

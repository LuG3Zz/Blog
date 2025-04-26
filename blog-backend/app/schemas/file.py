from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class FileBase(BaseModel):
    """文件基础模式"""
    filename: str
    original_filename: str
    file_path: str
    file_type: str
    file_size: int
    mime_type: Optional[str] = None

class FileCreate(FileBase):
    """文件创建模式"""
    pass

class FileUpdate(BaseModel):
    """文件更新模式"""
    filename: Optional[str] = None
    file_path: Optional[str] = None

class FileInDB(FileBase):
    """数据库中的文件模式"""
    id: int
    uploaded_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class FileResponse(FileBase):
    """文件响应模式"""
    id: int
    uploaded_by: int
    created_at: datetime
    updated_at: datetime
    url: str  # 文件的访问URL

    model_config = {
        "from_attributes": True
    }

class FileListResponse(BaseModel):
    """文件列表响应模式"""
    items: List[FileResponse]
    total: int
    page: int
    page_size: int
    
    model_config = {
        "from_attributes": True
    }

class FileUploadResponse(BaseModel):
    """文件上传响应模式"""
    id: int
    filename: str
    url: str
    file_type: str
    file_size: int
    
    model_config = {
        "from_attributes": True
    }

class FileDeleteRequest(BaseModel):
    """文件删除请求模式"""
    file_id: int

class FileRenameRequest(BaseModel):
    """文件重命名请求模式"""
    file_id: int
    new_filename: str = Field(..., min_length=1, max_length=255)

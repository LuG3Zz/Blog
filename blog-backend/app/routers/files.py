from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from typing import Optional
import os
from pathlib import Path
from datetime import datetime, timezone
import uuid
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app import models
from app.core import security
from app.core.config import settings

router = APIRouter(prefix="/files", tags=['files'])

# 确保静态目录存在
UPLOAD_DIR = os.path.abspath(settings.IMAGES_DIR)
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

class DeleteImageRequest(BaseModel):
    image_path: str

@router.delete("/delete-image")
async def delete_image(
    request: DeleteImageRequest,
    current_user: models.User = Depends(security.get_current_user)
):
    # 解析路径并验证
    try:
        file_path = os.path.abspath(os.path.join(UPLOAD_DIR, os.path.basename(request.image_path)))
        if not file_path.startswith(UPLOAD_DIR):
            raise HTTPException(status_code=403, detail="非法文件路径")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="文件不存在")

        os.remove(file_path)
        return {"message": "文件删除成功"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件删除失败: {str(e)}")

@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(),
    current_user: models.User = Depends(security.get_current_user)
):
    # 打印请求信息以便调试
    print(f"Received file upload request: {file.filename if file and hasattr(file, 'filename') else 'No filename'}")
    print(f"Content type: {file.content_type if file and hasattr(file, 'content_type') else 'Unknown'}")
    print(f"User authenticated: {current_user.username if current_user else 'No user'}")

    try:
        # 检查文件是否存在
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided or filename is empty"
            )

        # 检查文件类型
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
        file_ext = file.filename.split(".")[-1].lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )

        # 生成唯一文件名
        unique_name = f"{uuid.uuid4().hex}.{file_ext}"

        # 确保目录存在
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # 保存文件
        save_path = os.path.join(UPLOAD_DIR, unique_name)
        content = await file.read()

        # 检查文件大小
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large. Maximum size is 10MB"
            )

        with open(save_path, "wb") as buffer:
            buffer.write(content)

        # 返回访问URL - 使用相对路径
        return JSONResponse({
            "url": f"/static/images/{unique_name}"
        })
    except HTTPException as e:
        # 重新抛出 HTTP 异常
        raise e
    except Exception as e:
        # 记录其他异常
        print(f"File upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {str(e)}"
        )
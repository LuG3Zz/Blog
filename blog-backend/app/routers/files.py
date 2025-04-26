from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status, Query
from typing import Optional, List
import os
import shutil
import mimetypes
from pathlib import Path
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from sqlalchemy import func

from app import models, schemas
from app.core import security
from app.core.database import get_db
from app.core.config import settings
from app.core.permissions import is_admin

router = APIRouter(prefix="/files", tags=['files'])

# 确保静态目录存在
IMAGES_DIR = os.path.abspath(settings.IMAGES_DIR)
FILES_DIR = os.path.abspath(settings.FILES_DIR)
Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)
Path(FILES_DIR).mkdir(parents=True, exist_ok=True)

class DeleteImageRequest(BaseModel):
    image_path: str

@router.delete("/delete-image")
async def delete_image(
    request: DeleteImageRequest,
    current_user: models.User = Depends(security.get_current_user)
):
    # 解析路径并验证
    try:
        file_path = os.path.abspath(os.path.join(IMAGES_DIR, os.path.basename(request.image_path)))
        if not file_path.startswith(IMAGES_DIR):
            raise HTTPException(status_code=403, detail="非法文件路径")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="文件不存在")

        os.remove(file_path)
        return {"message": "文件删除成功"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件删除失败: {str(e)}")

@router.post("/upload-image", response_model=dict)
async def upload_image(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
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
        os.makedirs(IMAGES_DIR, exist_ok=True)

        # 保存文件
        save_path = os.path.join(IMAGES_DIR, unique_name)
        content = await file.read()

        # 检查文件大小
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large. Maximum size is 10MB"
            )

        with open(save_path, "wb") as buffer:
            buffer.write(content)

        # 创建文件记录以便后续访问
        db_file = models.File(
            filename=unique_name,
            original_filename=file.filename,
            file_path=f"static/images/{unique_name}",
            file_type="image",
            file_size=len(content),
            mime_type=file.content_type,
            uploaded_by=current_user.id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        # 构建静态文件URL
        # 检查文件路径是否已经包含static前缀
        file_path = db_file.file_path
        if file_path.startswith("static/"):
            file_path = file_path[7:]  # 移除"static/"前缀
        file_url = f"/static/{file_path}"  # 使用相对路径，前端会自动添加base_url

        # 返回访问URL - 使用完整的API URL
        return JSONResponse({
            "url": file_url,
            "id": db_file.id
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

# 新增文件管理相关接口
@router.post("/upload", response_model=schemas.FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    上传文件
    """
    try:
        # 检查文件是否存在
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="未提供文件或文件名为空"
            )

        # 获取文件扩展名和类型
        original_filename = file.filename
        file_ext = original_filename.split(".")[-1].lower() if "." in original_filename else ""

        # 根据扩展名确定文件类型
        file_type = "unknown"
        # 图片类型
        if file_ext in ["jpg", "jpeg", "png", "gif", "webp", "svg", "bmp", "ico"]:
            file_type = "image"
        # 文档类型 - 确保PDF被正确归类为文档
        elif file_ext in ["doc", "docx", "pdf", "txt", "rtf", "odt", "md"]:
            file_type = "document"
        # 音频类型
        elif file_ext in ["mp3", "wav", "ogg", "flac", "aac"]:
            file_type = "audio"
        # 视频类型
        elif file_ext in ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm"]:
            file_type = "video"
        # 压缩文件类型
        elif file_ext in ["zip", "rar", "7z", "tar", "gz"]:
            file_type = "archive"

        # 检查文件类型是否允许
        if file_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件类型。允许的类型: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )

        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}" if file_ext else f"{uuid.uuid4().hex}"

        # 确保目录存在
        os.makedirs(FILES_DIR, exist_ok=True)

        # 保存文件
        file_path = os.path.join(FILES_DIR, unique_filename)
        content = await file.read()

        # 检查文件大小
        file_size = len(content)
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"文件太大。最大允许大小: {settings.MAX_FILE_SIZE / (1024 * 1024)}MB"
            )

        # 写入文件
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        # 获取MIME类型
        mime_type, _ = mimetypes.guess_type(file_path)

        # 创建文件记录
        db_file = models.File(
            filename=unique_filename,
            original_filename=original_filename,
            file_path=f"static/files/{unique_filename}",
            file_type=file_type,
            file_size=file_size,
            mime_type=mime_type,
            uploaded_by=current_user.id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        # 构建文件URL

        # 对于图片类型，直接使用静态文件URL
        if db_file.file_type == "image":
            # 检查文件路径是否已经包含static前缀
            file_path = db_file.file_path
            if file_path.startswith("static/"):
                file_path = file_path[7:]  # 移除"static/"前缀
            file_url = f"/static/{file_path}"  # 使用相对路径，前端会自动添加base_url
        else:
            # 非图片类型使用下载API
            file_url = f"{settings.API_V1_STR}/files/download/{db_file.id}"

        # 返回文件信息
        return {
            "id": db_file.id,
            "filename": db_file.filename,
            "url": file_url,  # 使用完整的API URL
            "file_type": db_file.file_type,
            "file_size": db_file.file_size
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"文件上传错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )

@router.get("/list", response_model=schemas.FileListResponse)
async def list_files(
    file_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    获取文件列表
    """
    try:
        # 构建查询
        query = db.query(models.File)

        # 按文件类型筛选
        if file_type:
            query = query.filter(models.File.file_type == file_type)

        # 如果不是管理员，只能查看自己上传的文件
        if not is_admin(current_user):
            query = query.filter(models.File.uploaded_by == current_user.id)

        # 计算总数
        total = query.count()

        # 分页
        files = query.order_by(models.File.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()

        # 构建响应
        items = []
        for file in files:
            # 构建文件URL

            # 对于图片类型，直接使用静态文件URL
            if file.file_type == "image":
                # 检查文件路径是否已经包含static前缀
                file_path = file.file_path
                if file_path.startswith("static/"):
                    file_path = file_path[7:]  # 移除"static/"前缀
                file_url = f"/static/{file_path}"  # 使用相对路径，前端会自动添加base_url
            else:
                # 非图片类型使用下载API
                file_url = f"{settings.API_V1_STR}/files/download/{file.id}"

            items.append({
                "id": file.id,
                "filename": file.filename,
                "original_filename": file.original_filename,
                "file_path": file.file_path,
                "file_type": file.file_type,
                "file_size": file.file_size,
                "mime_type": file.mime_type,
                "uploaded_by": file.uploaded_by,
                "created_at": file.created_at,
                "updated_at": file.updated_at,
                "url": file_url  # 使用完整的API URL
            })

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size
        }

    except Exception as e:
        print(f"获取文件列表错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文件列表失败: {str(e)}"
        )

@router.get("/download/{file_id}")
async def download_file(
    file_id: int,
    token: Optional[str] = Query(None, description="认证令牌，用于直接访问文件"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    下载文件
    """
    try:
        # 查询文件
        file = db.query(models.File).filter(models.File.id == file_id).first()

        # 检查文件是否存在
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )

        # 检查权限（只有管理员或文件上传者可以下载）
        if not is_admin(current_user) and file.uploaded_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限下载此文件"
            )

        # 构建文件路径
        file_path = os.path.join(settings.STATIC_FILES_DIR, "files", file.filename)

        # 检查文件是否存在于磁盘上
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在于服务器上"
            )

        # 返回文件
        return FileResponse(
            path=file_path,
            filename=file.original_filename,
            media_type=file.mime_type
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"文件下载错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件下载失败: {str(e)}"
        )

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    删除文件
    """
    try:
        # 查询文件
        file = db.query(models.File).filter(models.File.id == file_id).first()

        # 检查文件是否存在
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )

        # 检查权限（只有管理员或文件上传者可以删除）
        if not is_admin(current_user) and file.uploaded_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限删除此文件"
            )

        # 构建文件路径
        file_path = os.path.join(settings.STATIC_FILES_DIR, "files", file.filename)

        # 删除文件
        if os.path.exists(file_path):
            os.remove(file_path)

        # 删除数据库记录
        db.delete(file)
        db.commit()

        return {"message": "文件删除成功"}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"文件删除错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件删除失败: {str(e)}"
        )

@router.put("/rename/{file_id}")
async def rename_file(
    file_id: int,
    request: schemas.FileRenameRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    重命名文件
    """
    try:
        # 查询文件
        file = db.query(models.File).filter(models.File.id == file_id).first()

        # 检查文件是否存在
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )

        # 检查权限（只有管理员或文件上传者可以重命名）
        if not is_admin(current_user) and file.uploaded_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限重命名此文件"
            )

        # 更新文件名
        file.original_filename = request.new_filename
        file.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(file)

        return {"message": "文件重命名成功", "new_filename": file.original_filename}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"文件重命名错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件重命名失败: {str(e)}"
        )

@router.get("/stats", response_model=dict)
async def get_file_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """获取文件统计信息"""
    try:
        query = db.query(models.File)

        # 如果不是管理员，只统计自己的文件
        if not is_admin(current_user):
            query = query.filter(models.File.uploaded_by == current_user.id)

        total_files = query.count()
        total_size = db.query(func.sum(models.File.file_size)).scalar() or 0

        # 按类型统计
        type_stats = (
            query.with_entities(
                models.File.file_type,
                func.count(models.File.id).label('count'),
                func.sum(models.File.file_size).label('total_size')
            )
            .group_by(models.File.file_type)
            .all()
        )

        return {
            "total_files": total_files,
            "total_size": total_size,
            "type_stats": [
                {
                    "type": stat.file_type,
                    "count": stat.count,
                    "total_size": stat.total_size or 0
                }
                for stat in type_stats
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计信息失败: {str(e)}"
        )

class BatchDeleteRequest(BaseModel):
    file_ids: List[int]

@router.post("/batch-delete")
async def batch_delete_files(
    request: BatchDeleteRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """批量删除文件"""
    try:
        # 检查文件ID列表是否为空
        if not request.file_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件ID列表不能为空"
            )

        # 查询所有文件
        files = db.query(models.File).filter(models.File.id.in_(request.file_ids)).all()

        # 检查权限
        if not is_admin(current_user):
            # 非管理员只能删除自己的文件
            for file in files:
                if file.uploaded_by != current_user.id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"没有权限删除文件ID: {file.id}"
                    )

        # 删除文件
        deleted_count = 0
        for file in files:
            # 构建文件路径
            file_path = os.path.join(settings.STATIC_FILES_DIR, "files", file.filename)

            # 删除物理文件
            if os.path.exists(file_path):
                os.remove(file_path)

            # 删除数据库记录
            db.delete(file)
            deleted_count += 1

        # 提交事务
        db.commit()

        return {
            "message": f"成功删除 {deleted_count} 个文件",
            "deleted_count": deleted_count
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"批量删除文件错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量删除文件失败: {str(e)}"
        )

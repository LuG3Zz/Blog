from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from app import models
from app.core import security
from app.core.database import get_db
from app.core.cache import clear_cache_by_prefix
from app.schemas.tag import TagCreate, TagResponse, TagUpdate, TagWithCount, TagBatchDeleteRequest
from app.schemas.article import ArticleList
from app.services.tag_service import TagService

router = APIRouter(prefix="/tags", tags=["tags"])

@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Create a new tag.
    """
    return TagService.create_tag(db=db, tag=tag)

@router.get("", response_model=List[TagWithCount])
async def get_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all tags with article count.
    """
    return TagService.get_tags_with_count(db=db, skip=skip, limit=limit)

@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific tag by ID.
    """
    tag = TagService.get_tag_by_id(db=db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag: TagUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Update a tag.
    """
    return TagService.update_tag(db=db, tag_id=tag_id, tag_update=tag)

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Delete a tag.
    """
    success = TagService.delete_tag(db=db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return None

@router.post("/batch-delete", status_code=status.HTTP_200_OK)
async def batch_delete_tags(
    request: TagBatchDeleteRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    批量删除标签。

    参数:
    - **tag_ids**: 要删除的标签ID列表

    返回:
    - 200 OK: 删除成功，返回删除的数量
    - 403 Forbidden: 没有权限删除
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以批量删除标签"
        )

    if not request.tag_ids:
        return {"deleted_count": 0, "message": "没有指定要删除的标签"}

    # 查询并删除标签
    deleted_count = 0
    for tag_id in request.tag_ids:
        success = TagService.delete_tag(db=db, tag_id=tag_id)
        if success:
            deleted_count += 1

    # 清除相关缓存
    clear_cache_by_prefix("tags_")

    return {
        "deleted_count": deleted_count,
        "message": f"成功删除 {deleted_count} 个标签"
    }

@router.get("/by-name/{name}", response_model=TagResponse)
async def get_tag_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific tag by name.
    """
    tag = TagService.get_tag_by_name(db=db, name=name)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.get("/{tag_id}/articles", response_model=List[ArticleList])
async def get_articles_by_tag(
    tag_id: int = Path(..., title="The ID of the tag to get articles for"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all articles with a specific tag.
    """
    return TagService.get_articles_by_tag(db=db, tag_id=tag_id, skip=skip, limit=limit)

@router.post("/articles/{article_id}/tags")
async def add_tag_to_article(
    article_id: int = Path(..., title="The ID of the article to add the tag to"),
    tag_id: int = Query(..., title="The ID of the tag to add"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Add a tag to an article.
    """
    return {"success": TagService.add_tag_to_article(db=db, article_id=article_id, tag_id=tag_id)}

@router.delete("/articles/{article_id}/tags/{tag_id}")
async def remove_tag_from_article(
    article_id: int = Path(..., title="The ID of the article to remove the tag from"),
    tag_id: int = Path(..., title="The ID of the tag to remove"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Remove a tag from an article.
    """
    return {"success": TagService.remove_tag_from_article(db=db, article_id=article_id, tag_id=tag_id)}

@router.put("/articles/{article_id}/tags")
async def update_article_tags(
    article_id: int = Path(..., title="The ID of the article to update tags for"),
    tag_ids: List[int] = Query(..., title="The IDs of the tags to set"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Update all tags for an article.
    """
    tags = TagService.update_article_tags(db=db, article_id=article_id, tag_ids=tag_ids)
    return {"tags": [tag.name for tag in tags]}

@router.get("/articles/{article_id}/tags", response_model=List[TagResponse])
async def get_article_tags(
    article_id: int = Path(..., title="The ID of the article to get tags for"),
    db: Session = Depends(get_db)
):
    """
    Get all tags for an article.
    """
    return TagService.get_article_tags(db=db, article_id=article_id)

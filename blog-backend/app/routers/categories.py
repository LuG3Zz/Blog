from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from sqlalchemy.sql import func

from app import models
from app.core import security
from app.core.database import get_db
from app.core.cache import cache, clear_cache_by_prefix
from app.schemas.article import CategoryBase, CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithCount, CategoryBatchDeleteRequest

router = APIRouter(prefix="/categories", tags=['categories'])

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    # 检查分类名是否已存在
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    # 创建新分类
    db_category = models.Category(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    # 清除分类缓存
    clear_cache_by_prefix("get_categories")

    return db_category

@router.get("/", response_model=List[CategoryWithCount])
@cache(ttl_seconds=300)  # 缓存5分钟
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(
        models.Category,
        func.count(models.Article.id).label('articleCount')
    ).outerjoin(
        models.Article,
        models.Category.id == models.Article.category_id
    ).group_by(
        models.Category.id
    ).all()

    result = []
    for category, article_count in categories:
        category_dict = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "articleCount": article_count
        }
        result.append(category_dict)

    return result

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.name is not None:
        # 检查新名称是否已被使用
        existing_category = db.query(models.Category).filter(
            models.Category.name == category.name,
            models.Category.id != category_id
        ).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category name already exists")
        db_category.name = category.name

    if category.description is not None:
        db_category.description = category.description

    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    # 检查分类是否存在
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # 检查分类是否有关联的文章
    articles = db.query(models.Article).filter(models.Article.category_id == category_id).first()
    if articles:
        raise HTTPException(status_code=400, detail="Cannot delete category with associated articles")

    # 删除分类
    db.delete(category)
    db.commit()

    # 清除分类缓存
    clear_cache_by_prefix("get_categories")

    return {"message": "Category deleted successfully"}

@router.post("/batch-delete", status_code=status.HTTP_200_OK)
async def batch_delete_categories(
    request: CategoryBatchDeleteRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    批量删除分类。

    参数:
    - **category_ids**: 要删除的分类ID列表

    返回:
    - 200 OK: 删除成功，返回删除的数量
    - 403 Forbidden: 没有权限删除
    """
    # 检查用户是否为管理员
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以批量删除分类"
        )

    if not request.category_ids:
        return {"deleted_count": 0, "message": "没有指定要删除的分类"}

    # 查询并删除分类
    deleted_count = 0
    not_deleted = []

    for category_id in request.category_ids:
        # 检查分类是否存在
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not category:
            not_deleted.append({"id": category_id, "reason": "分类不存在"})
            continue

        # 检查分类是否有关联的文章
        articles = db.query(models.Article).filter(models.Article.category_id == category_id).first()
        if articles:
            not_deleted.append({"id": category_id, "reason": "分类下有关联文章"})
            continue

        # 删除分类
        db.delete(category)
        deleted_count += 1

    # 提交事务
    if deleted_count > 0:
        db.commit()
        # 清除分类缓存
        clear_cache_by_prefix("get_categories")

    result = {
        "deleted_count": deleted_count,
        "message": f"成功删除 {deleted_count} 个分类"
    }

    if not_deleted:
        result["not_deleted"] = not_deleted

    return result
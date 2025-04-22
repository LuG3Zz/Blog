from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from sqlalchemy.sql import func

from app import models
from app.core import security
from app.core.database import get_db
from app.core.cache import cache, clear_cache_by_prefix
from app.schemas.article import CategoryBase, CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithCount

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
    return {"message": "Category deleted successfully"}
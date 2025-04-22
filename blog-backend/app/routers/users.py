from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

from app import models
from app.core import security
from app.core.database import get_db
from app.core.config import settings
from app.services.user_service import UserService
from app.services.comment_service import CommentService
from app.utils.pagination import PaginationParams
from app.schemas.comment import CommentResponse
from app.schemas.user import UserCreate, UserInDB, UserLogin, UserUpdate, UserResponse, UserRole
from app.schemas.token import Token
from app.schemas.article import ArticleList
from app.schemas.activity import ActivityResponse

router = APIRouter(prefix="/users", tags=['users'])

@router.post("/", response_model=UserInDB)
@router.post("", response_model=UserInDB)  # 添加无尾部斜杠的路由
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token, summary="用户登录获取token")
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录并获取访问令牌

    - **username**: 用户名
    - **password**: 密码

    返回JWT令牌，可用于授权访问受保护的API端点
    """
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        user = None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserInDB)
async def read_users_me(
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    # 获取包含评论数和文章数的用户信息
    # 注意：UserService.get_user_by_id 已经处理了 social_media 字段的转换
    user = UserService.get_user_by_id(db, current_user.id, include_counts=True)
    return user

@router.get("/admin/info", response_model=UserResponse)
async def get_admin_info(db: Session = Depends(get_db)):
    """
    获取系统管理员信息

    此接口用于获取系统中唯一管理员的公开信息，供前端展示
    不需要认证即可访问
    """
    # 查询角色为admin的用户
    admin_user = db.query(models.User).filter(
        models.User.role == "admin"
    ).first()

    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No administrator found in the system"
        )

    # 获取包含评论数和文章数的用户信息
    admin_info = UserService.get_user_by_id(db, admin_user.id, include_counts=True)

    return admin_info

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    通过用户ID获取用户信息

    - **user_id**: 用户ID

    返回用户的基本信息，包含评论数和文章数，不包含敏感数据
    """
    user = UserService.get_user_by_id(db, user_id, include_counts=True)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 注意：UserService.get_user_by_id 已经处理了 social_media 字段的转换
    return user

@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")

    if user_update.password:
        current_user.hashed_password = security.get_password_hash(user_update.password)
    if user_update.email:
        current_user.email = user_update.email
    if user_update.avatar:
        current_user.avatar = user_update.avatar
    if user_update.bio:
        current_user.bio = user_update.bio
    if user_update.social_media is not None:
        # 将社交媒体字典转换为JSON字符串
        import json
        current_user.social_media = json.dumps(user_update.social_media, ensure_ascii=False)

    current_user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(current_user)

    # 在返回用户信息之前将 social_media 字段转换为字典
    if current_user.social_media:
        try:
            current_user.social_media = json.loads(current_user.social_media)
        except json.JSONDecodeError:
            current_user.social_media = None

    return current_user

@router.get("/{user_id}/articles", response_model=List[ArticleList])
async def get_user_articles(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    articles = db.query(models.Article).filter(
        models.Article.author_id == user_id
    ).offset(skip).limit(limit).all()

    # 处理文章作者的 social_media 字段
    for article in articles:
        if hasattr(article, 'author') and article.author and hasattr(article.author, 'social_media') and isinstance(article.author.social_media, str) and article.author.social_media:
            try:
                import json
                article.author.social_media = json.loads(article.author.social_media)
            except json.JSONDecodeError:
                article.author.social_media = None

    return articles

@router.get("/{user_id}/comments", response_model=List[CommentResponse])
async def get_user_comments(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user_optional)
):
    # 使用评论服务获取用户评论，确保处理社交媒体字段
    params = PaginationParams(page=skip // limit + 1, page_size=limit)
    comments_response = CommentService.get_all_comments(
        db=db,
        params=params,
        approved_only=True,
        user_id=user_id,
        sort_by="newest",
        current_user=current_user
    )
    return comments_response.items

@router.get("/{user_id}/activities", response_model=List[ActivityResponse])
async def get_user_activities(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    activities = db.query(models.Activity).filter(
        models.Activity.user_id == user_id
    ).order_by(models.Activity.created_at.desc()).offset(skip).limit(limit).all()
    return activities
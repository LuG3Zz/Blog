from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
import json

from app import models, schemas
# 避免循环导入
from app.utils.logging import get_logger
from app.utils.password import get_password_hash, verify_password

logger = get_logger(__name__)

class UserService:
    """Service for user-related operations."""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int, include_counts: bool = False) -> Optional[models.User]:
        """Get a user by ID with optional comment and article counts."""
        user = db.query(models.User).filter(models.User.id == user_id).first()

        if user:
            # 如果有社交媒体数据，将JSON字符串转换为字典
            if user.social_media:
                try:
                    user.social_media = json.loads(user.social_media)
                except json.JSONDecodeError:
                    user.social_media = {}

            if include_counts:
                # 获取用户评论数
                comment_count = db.query(func.count(models.Comment.id)).filter(
                    models.Comment.user_id == user_id
                ).scalar()

                # 获取用户文章数
                article_count = db.query(func.count(models.Article.id)).filter(
                    models.Article.author_id == user_id
                ).scalar()

                # 设置计数属性
                setattr(user, "comment_count", comment_count or 0)
                setattr(user, "article_count", article_count or 0)

        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
        """Get a user by username."""
        return db.query(models.User).filter(models.User.username == username).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
        """Get a user by email."""
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100, include_counts: bool = False) -> List[models.User]:
        """Get a list of users with optional comment and article counts."""
        users = db.query(models.User).offset(skip).limit(limit).all()

        if include_counts and users:
            # 获取所有用户ID
            user_ids = [user.id for user in users]

            # 批量获取评论数
            comment_counts = db.query(
                models.Comment.user_id,
                func.count(models.Comment.id).label('comment_count')
            ).filter(
                models.Comment.user_id.in_(user_ids)
            ).group_by(models.Comment.user_id).all()

            # 批量获取文章数
            article_counts = db.query(
                models.Article.author_id,
                func.count(models.Article.id).label('article_count')
            ).filter(
                models.Article.author_id.in_(user_ids)
            ).group_by(models.Article.author_id).all()

            # 创建计数字典
            comment_count_dict = {user_id: count for user_id, count in comment_counts}
            article_count_dict = {user_id: count for user_id, count in article_counts}

            # 设置每个用户的计数属性和处理社交媒体数据
            for user in users:
                # 如果有社交媒体数据，将JSON字符串转换为字典
                if user.social_media:
                    try:
                        user.social_media = json.loads(user.social_media)
                    except json.JSONDecodeError:
                        user.social_media = {}

                setattr(user, "comment_count", comment_count_dict.get(user.id, 0))
                setattr(user, "article_count", article_count_dict.get(user.id, 0))

        return users

    @staticmethod
    def create_user(db: Session, user_data) -> models.User:
        """Create a new user."""
        # 支持传入字典或Pydantic模型
        if hasattr(user_data, 'model_dump'):
            user_dict = user_data.model_dump()
        else:
            user_dict = user_data

        # Check if username already exists
        existing_user = UserService.get_user_by_username(db, user_dict['username'])
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email already exists
        existing_email = UserService.get_user_by_email(db, user_dict['email'])
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_dict['password'])

        # 准备用户数据
        user_create_data = {
            'username': user_dict['username'],
            'email': user_dict['email'],
            'hashed_password': hashed_password
        }

        # 如果提供了角色，则设置角色
        if 'role' in user_dict:
            user_create_data['role'] = user_dict['role']

        # 创建用户对象
        db_user = models.User(**user_create_data)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"Created new user: {db_user.username}")
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User:
        """Update a user."""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update user fields if provided
        update_data = user_update.model_dump(exclude_unset=True)
        logger.info(f"更新用户数据: {update_data}")

        # Hash password if provided
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        # Update user attributes
        for key, value in update_data.items():
            logger.info(f"设置属性 {key} = {value}")
            setattr(db_user, key, value)

        # 特别记录角色更新
        if "role" in update_data:
            logger.info(f"用户角色更新: {db_user.username} 的角色从 {db_user.role} 更改为 {update_data['role']}")

        db.commit()
        db.refresh(db_user)

        logger.info(f"Updated user: {db_user.username}")
        return db_user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
        """Authenticate a user."""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user."""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        db.delete(db_user)
        db.commit()

        logger.info(f"Deleted user: {db_user.username}")
        return True

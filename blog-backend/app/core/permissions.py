"""
权限检查模块：提供权限验证功能
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.models.user import UserRole

def check_article_permission(
    db: Session,
    article_id: int,
    user: models.User,
    action: str = "update"
) -> models.Article:
    """
    检查用户是否有权限操作指定文章

    Args:
        db: 数据库会话
        article_id: 文章ID
        user: 当前用户
        action: 操作类型，如 "update", "delete" 等

    Returns:
        文章对象，如果用户有权限

    Raises:
        HTTPException: 如果文章不存在或用户无权限
    """
    # 获取文章
    article = db.query(models.Article).filter(models.Article.id == article_id).first()

    # 检查文章是否存在
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # 检查权限
    # 1. 管理员可以执行任何操作
    # 2. 编辑可以更新任何文章，但只能删除自己的文章
    # 3. 作者只能操作自己的文章
    if user.role == UserRole.admin:
        return article

    if user.role == UserRole.editor:
        if action == "update":
            return article
        elif action == "delete" and article.author_id == user.id:
            return article

    if article.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: you don't have permission to {action} this article"
        )

    return article

def is_admin(user: models.User) -> bool:
    """检查用户是否为管理员"""
    return user.role == UserRole.admin

def is_super_admin(user: models.User) -> bool:
    """检查用户是否为超级管理员（与is_admin相同，但语义上更明确）"""
    return user.role == UserRole.admin

def is_editor_or_admin(user: models.User) -> bool:
    """检查用户是否为编辑或管理员"""
    return user.role in [UserRole.editor, UserRole.admin]

def can_manage_file(user: models.User, file_owner_id: int) -> bool:
    """
    检查用户是否可以管理文件

    Args:
        user: 用户对象
        file_owner_id: 文件所有者ID

    Returns:
        bool: 是否可以管理文件
    """
    if not user:
        return False
    # 管理员可以管理所有文件，普通用户只能管理自己的文件
    return is_admin(user) or user.id == file_owner_id

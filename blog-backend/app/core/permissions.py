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
    # 2. 编辑可以更新任何文章，但不能删除
    # 3. 作者只能操作自己的文章
    if user.role == UserRole.admin:
        return article

    if user.role == UserRole.editor and action == "update":
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

def is_editor_or_admin(user: models.User) -> bool:
    """检查用户是否为编辑或管理员"""
    return user.role in [UserRole.editor, UserRole.admin]

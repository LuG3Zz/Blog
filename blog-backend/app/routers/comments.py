from fastapi import APIRouter, Depends, HTTPException, Request, Header, status, Query
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import os
import json
import httpx
from ipregion import IP2Region
from dotenv import load_dotenv
from jose import jwt

from app.utils.ip_utils import get_client_ip

from app import models
from app.core import security
from app.core.database import get_db
from app.core.config import settings
from app.schemas.comment import (
    CommentBase, CommentCreate, CommentResponse, CommentUpdate,
    CommentWithReplies, CommentLike, CommentPaginationResponse
)
from app.services.comment_service import CommentService
from app.services.ip_location_service import IPLocationService
from app.utils.pagination import PaginationParams, PagedResponse

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/comments", tags=['comments'])

@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    request: Request,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """
    创建新评论

    请求体示例:
    ```json
    {
      "article_id": 6,
      "content": "测试评论",
      "parent_id": null,  // 可选，回复其他评论时提供
      "anonymous_name": "游客123"  // 可选，匿名用户的显示名称
    }
    ```

    - **article_id**: 文章ID（必需）
    - **content**: 评论内容（必需）
    - **parent_id**: 父评论ID（可选，用于回复其他评论）
    - **anonymous_name**: 匿名用户的显示名称（只在未登录时有效）

    注意：用户身份只能通过请求头中的 token 来识别，不能由用户直接传入。
    如果提供了有效的 token，则使用 token 中的用户身份；
    如果没有提供 token 或 token 无效，则作为匿名用户处理。

    评论审核规则:
    1. 已登录用户的评论自动通过审核
    2. 匿名评论先经过AI审核，通过则自动批准，不通过则拒绝
    3. 如果未配置AI审核密钥，匿名评论需要管理员手动审核

    返回创建的评论信息。
    """

    # 获取当前用户（如果已登录）
    current_user = None
    print(f"Authorization header: {authorization}")
    if authorization:
        try:
            # 处理 Bearer Token 格式
            token = authorization
            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")

            print(f"Token: {token}")

            # 解析 token
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            username = payload.get("sub")

            print(f"Username from token: {username}")

            if username:
                # 从数据库中获取用户
                current_user = db.query(models.User).filter(models.User.username == username).first()
                if current_user:
                    print(f"获取评论列表 - 用户已登录: {current_user.username}, ID: {current_user.id}, 角色: {current_user.role}")
        except Exception as e:
            # 记录错误但不中断流程，允许匿名评论
            print(f"Token 验证失败: {str(e)}")

    # article_id 现在直接从请求体中的 comment 对象获取

    # 获取评论者真实IP地址
    client_ip = get_client_ip(request)

    # 创建评论
    try:
        # 如果用户已登录，忽略匿名名称
        # 注意：用户ID只能从 token 中获取，不能由用户传入
        user_id = current_user.id if current_user else None
        anonymous_name = None if current_user else comment.anonymous_name

        print(f"创建评论: user_id={user_id}, anonymous_name={anonymous_name}")

        db_comment = await CommentService.create_comment(
            db=db,
            comment=comment,
            ip_address=client_ip,
            api_key=os.getenv('OPENROUTER_API_KEY'),
            user_id=user_id,
            anonymous_name=anonymous_name
        )

        # 如果是登录用户，记录活动
        if current_user:
            # 获取文章信息
            article = db.query(models.Article).filter(models.Article.id == db_comment.article_id).first()
            article_title = article.title if article else f"ID为{db_comment.article_id}的文章"

            # 获取文章作者信息
            if article:
                article_author = db.query(models.User).filter(models.User.id == article.author_id).first()
                author_name = article_author.username if article_author else "未知作者"
            else:
                author_name = "未知作者"

            # 生成评论预览
            comment_preview = db_comment.content[:50] + "..." if len(db_comment.content) > 50 else db_comment.content

            activity = models.Activity(
                action_type='comment',
                user_id=current_user.id,
                target_id=db_comment.id,
                description=f'用户 {current_user.username} 评论了 {author_name} 的文章 《{article_title}》: "{comment_preview}"',
                created_at=datetime.now(timezone.utc)
            )
            db.add(activity)
            db.commit()

        # 设置评论者名称
        comment_response = CommentResponse.model_validate(db_comment)
        if current_user:
            comment_response.commenter_name = current_user.username
        else:
            comment_response.commenter_name = comment.anonymous_name or "匿名用户"

        return comment_response
    except HTTPException as e:
        # 重新抛出服务层的异常
        raise e
    except Exception as e:
        # 记录并转换其他异常
        print(f"创建评论失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建评论失败: {str(e)}"
        )



@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """更新评论"""
    try:
        # 使用评论服务更新评论
        db_comment = CommentService.update_comment(
            db=db,
            comment_id=comment_id,
            comment_update=comment_update,
            user_id=current_user.id
        )

        # 获取文章信息
        article = db.query(models.Article).filter(models.Article.id == db_comment.article_id).first()
        article_title = article.title if article else f"ID为{db_comment.article_id}的文章"

        # 生成评论预览
        comment_preview = db_comment.content[:50] + "..." if len(db_comment.content) > 50 else db_comment.content

        # 记录活动
        activity = models.Activity(
            action_type='comment_update',
            user_id=current_user.id,
            target_id=db_comment.id,
            description=f'用户 {current_user.username} 更新了对文章 《{article_title}》 的评论: "{comment_preview}"',
            created_at=datetime.now(timezone.utc)
        )
        db.add(activity)
        db.commit()

        # 设置评论者名称
        comment_response = CommentResponse.model_validate(db_comment)
        comment_response.commenter_name = current_user.username
        return comment_response
    except HTTPException as e:
        # 重新抛出服务层的异常
        raise e
    except Exception as e:
        # 记录并转换其他异常
        print(f"更新评论失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新评论失败: {str(e)}"
        )

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """删除评论"""
    try:
        # 检查用户是否为管理员
        is_admin = current_user.role == "admin"

        # 使用评论服务删除评论
        CommentService.delete_comment(
            db=db,
            comment_id=comment_id,
            user_id=current_user.id,
            is_admin=is_admin
        )

        # 返回204状态码，无内容
        return None
    except HTTPException as e:
        # 重新抛出服务层的异常
        raise e
    except Exception as e:
        # 记录并转换其他异常
        print(f"删除评论失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除评论失败: {str(e)}"
        )

@router.post("/{comment_id}/like", response_model=CommentLike)
async def like_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """点赞或取消点赞评论"""
    try:
        # 使用评论服务点赞评论
        result = CommentService.like_comment(
            db=db,
            comment_id=comment_id,
            user_id=current_user.id
        )

        return result
    except HTTPException as e:
        # 重新抛出服务层的异常
        raise e
    except Exception as e:
        # 记录并转换其他异常
        print(f"点赞评论失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"点赞评论失败: {str(e)}"
        )

@router.get("/all", response_model=CommentPaginationResponse)
async def get_all_comments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    sort_by: str = Query("newest", description="排序方式: newest, oldest, most_liked"),
    approved_only: Optional[bool] = Query(None, description="审核状态筛选，True表示已审核，False表示未审核，None表示全部"),
    user_id: Optional[int] = Query(None, description="用户ID筛选"),
    parent_only: bool = Query(True, description="是否只返回顶层评论"),
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """
    获取所有评论（需要登录）

    参数:
    - **page**: 页码，从1开始
    - **page_size**: 每页数量，范围1-100
    - **sort_by**: 排序方式，可选值: newest(最新), oldest(最旧), most_liked(最多点赞)
    - **approved_only**: 审核状态筛选，True表示已审核，False表示未审核，None表示全部
    - **user_id**: 按用户ID筛选
    - **parent_only**: 是否只返回顶层评论，默认为True

    返回分页的评论列表。非管理员用户只能看到已审核的评论。
    """
    # 获取当前用户（如果已登录）
    current_user = None
    print(f"Authorization header: {authorization}")
    if authorization:
        try:
            # 处理 Bearer Token 格式
            token = authorization
            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")

            print(f"Token: {token}")

            # 解析 token
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            username = payload.get("sub")

            print(f"Username from token: {username}")

            if username:
                # 从数据库中获取用户
                current_user = db.query(models.User).filter(models.User.username == username).first()
                if current_user:
                    print(f"获取所有评论 - 用户已登录: {current_user.username}, ID: {current_user.id}, 角色: {current_user.role}")
        except Exception as e:
            # 记录错误但不中断流程
            print(f"Token 验证失败: {str(e)}")

    # 非管理员只能看到已审核的评论
    if not current_user or (current_user.role != "admin" and approved_only is not True):
        approved_only = True

    # 创建分页参数
    params = PaginationParams(page=page, page_size=page_size)

    # 获取评论列表
    comments = CommentService.get_all_comments(
        db=db,
        params=params,
        approved_only=approved_only,
        user_id=user_id,
        sort_by=sort_by,
        current_user=current_user,  # 传递当前用户信息
        parent_only=parent_only  # 是否只返回顶层评论
    )

    return comments

@router.get("/pending", response_model=CommentPaginationResponse)
async def get_pending_comments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    article_id: Optional[int] = Query(None, description="文章ID，用于编辑筛选自己文章的评论"),
    parent_only: bool = Query(True, description="是否只返回顶层评论"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    获取待审核评论列表（管理员可查看所有，编辑可查看自己文章的）

    参数:
    - **page**: 页码，从1开始
    - **page_size**: 每页数量，范围1-100
    - **article_id**: 文章ID，用于编辑筛选自己文章的评论
    - **parent_only**: 是否只返回顶层评论，默认为True
    """
    # 创建分页参数
    params = PaginationParams(page=page, page_size=page_size)

    # 检查用户角色
    is_admin = current_user.role == "admin"
    is_editor = current_user.role == "editor"

    # 如果是编辑但没有指定文章ID，则需要获取编辑的所有文章ID
    editor_article_ids = None
    if is_editor and not is_admin:
        if article_id:
            # 检查文章是否属于该编辑
            article = db.query(models.Article).filter(models.Article.id == article_id).first()
            if not article or article.author_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="您只能查看自己文章的待审核评论"
                )
            editor_article_ids = [article_id]
        else:
            # 获取编辑的所有文章ID
            editor_articles = db.query(models.Article).filter(models.Article.author_id == current_user.id).all()
            editor_article_ids = [article.id for article in editor_articles]
            if not editor_article_ids:
                # 如果编辑没有文章，返回空结果
                return CommentPaginationResponse(
                    items=[],
                    total=0,
                    page=page,
                    page_size=page_size,
                    total_pages=0
                )

    # 如果既不是管理员也不是编辑，则没有权限
    if not is_admin and not is_editor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员和编辑可以查看待审核评论"
        )

    # 获取待审核评论
    comments = CommentService.get_pending_comments(
        db=db,
        params=params,
        article_ids=editor_article_ids,  # 如果是编辑，只获取其文章的评论
        parent_only=parent_only  # 是否只返回顶层评论
    )

    return comments

@router.post("/approve/{comment_id}", response_model=CommentResponse)
async def approve_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """审核通过评论（管理员可审核所有，编辑可审核自己文章的）"""
    # 检查用户角色
    is_admin = current_user.role == "admin"
    is_editor = current_user.role == "editor"

    # 获取评论信息
    db_comment = CommentService.get_comment_by_id(db, comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 如果是编辑，检查评论是否属于自己的文章
    if is_editor and not is_admin:
        # 获取文章信息
        article = db.query(models.Article).filter(models.Article.id == db_comment.article_id).first()
        if not article or article.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您只能审核自己文章下的评论"
            )
    # 如果既不是管理员也不是编辑，则没有权限
    elif not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员和编辑可以审核评论"
        )

    try:
        # 审核通过评论
        db_comment = CommentService.approve_comment(db=db, comment_id=comment_id)

        # 获取评论信息
        comment_preview = db_comment.content[:50] + "..." if len(db_comment.content) > 50 else db_comment.content

        # 获取评论作者信息
        comment_author = None
        if db_comment.user_id:
            comment_author = db.query(models.User).filter(models.User.id == db_comment.user_id).first()
        comment_author_name = comment_author.username if comment_author else "匿名用户"

        # 获取文章信息
        article = db.query(models.Article).filter(models.Article.id == db_comment.article_id).first()
        article_title = article.title if article else f"ID为{db_comment.article_id}的文章"

        # 记录活动
        activity = models.Activity(
            action_type='comment_approve',
            user_id=current_user.id,
            target_id=comment_id,
            description=f'管理员 {current_user.username} 审核通过了 {comment_author_name} 对文章 《{article_title}》 的评论: "{comment_preview}"',
            created_at=datetime.now(timezone.utc)
        )
        db.add(activity)
        db.commit()

        # 设置评论者名称
        comment_response = CommentResponse.model_validate(db_comment)
        if db_comment.user_id:
            user = db.query(models.User).filter(models.User.id == db_comment.user_id).first()
            comment_response.commenter_name = user.username if user else "未知用户"
        else:
            comment_response.commenter_name = db_comment.anonymous_name or "匿名用户"

        return comment_response
    except HTTPException as e:
        # 重新抛出服务层的异常
        raise e
    except Exception as e:
        # 记录并转换其他异常
        print(f"审核评论失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"审核评论失败: {str(e)}"
        )

# 注意：这个路由必须放在最后，因为它会匹配所有的路径参数
@router.get("/{article_id}", response_model=CommentPaginationResponse)
async def get_comments(
    article_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    sort_by: str = Query("newest", description="排序方式: newest, oldest, most_liked"),
    parent_only: bool = Query(True, description="是否只返回顶层评论"),
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None, description="用户认证令牌，可选")
):
    """获取文章评论列表"""
    # 获取当前用户（如果已登录）
    current_user = None
    print(f"Authorization header: {authorization}")
    if authorization:
        try:
            # 处理 Bearer Token 格式
            token = authorization
            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")

            print(f"Token: {token}")

            # 解析 token
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            username = payload.get("sub")

            print(f"Username from token: {username}")

            if username:
                # 从数据库中获取用户
                current_user = db.query(models.User).filter(models.User.username == username).first()
                if current_user:
                    print(f"获取文章评论 - 用户已登录: {current_user.username}, ID: {current_user.id}, 角色: {current_user.role}")
        except Exception as e:
            # 记录错误但不中断流程
            print(f"Token 验证失败: {str(e)}")

    # 创建分页参数
    params = PaginationParams(page=page, page_size=page_size)

    # 获取评论列表
    comments = CommentService.get_comments_by_article(
        db=db,
        article_id=article_id,
        params=params,
        approved_only=True,
        sort_by=sort_by,
        parent_only=parent_only,
        current_user=current_user  # 传递当前用户信息
    )

    return comments
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models
from app.models.user import UserRole
from app.core import security
from app.core.database import get_db
from app.utils.logging import get_logger

# 初始化日志记录器
logger = get_logger(__name__)
from app.schemas.memo import (
    MemoCreate, MemoUpdate, MemoResponse, MemoWithoutContent, MemoWithUser,
    MemoPasswordVerify, MemoPasswordVerifyResponse
)
from app.services.memo_service import MemoService
from app.services.activity_service import ActivityService

router = APIRouter(prefix="/memos", tags=["memos"])

@router.post("/", response_model=MemoResponse)
async def create_memo(
    memo_data: MemoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    创建新备忘录。

    参数:
    - **title**: 备忘录标题
    - **content**: 备忘录内容
    - **is_encrypted**: 是否加密
    - **password**: 如果加密，提供密码

    返回创建的备忘录信息。
    """
    # 创建备忘录
    memo = MemoService.create_memo(db, memo_data, current_user.id)

    # 记录活动
    ActivityService.create_activity(
        db=db,
        action_type="memo_create",
        user_id=current_user.id,
        target_id=memo.id,
        description=f"用户 {current_user.username} 创建了备忘录 《{memo.title}》"
    )

    return memo

@router.get("/", response_model=List[MemoWithoutContent])
async def get_memos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    获取当前用户的备忘录列表。

    参数:
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数

    返回备忘录列表，包含内容（除非是加密的）。
    """
    memos = MemoService.get_memos_by_user(db, current_user.id, skip, limit)

    # 处理加密内容
    result_memos = []
    for memo in memos:
        # 如果备忘录加密，清空内容
        if memo.is_encrypted:
            # 创建一个新的备忘录对象，避免修改数据库中的对象
            memo_dict = {
                "id": memo.id,
                "title": memo.title,
                "content": "",  # 清空内容
                "is_encrypted": memo.is_encrypted,
                "user_id": memo.user_id,
                "created_at": memo.created_at,
                "updated_at": memo.updated_at
            }
            result_memos.append(memo_dict)
        else:
            result_memos.append(memo)

    return result_memos

@router.get("/public", response_model=List[MemoWithUser])
async def get_public_memos(
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    """
    获取所有公开的备忘录列表，无需登录。

    参数:
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数

    返回公开的备忘录列表，包含内容和用户信息（所有公开备忘录都是未加密的）。
    """
    # 获取所有公开的备忘录（未加密的）
    memos = MemoService.get_public_memos(db, skip, limit)

    # 添加用户信息
    result_memos = []
    for memo in memos:
        # 创建一个新的备忘录对象，包含用户信息
        memo_dict = {
            "id": memo.id,
            "title": memo.title,
            "content": memo.content,
            "is_encrypted": memo.is_encrypted,
            "user_id": memo.user_id,
            "created_at": memo.created_at,
            "updated_at": memo.updated_at,
            "user": memo.user  # 添加用户信息
        }
        result_memos.append(memo_dict)

    return result_memos

@router.get("/all", response_model=List[MemoWithUser])
async def get_all_memos(
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    """
    获取所有备忘录列表（包括加密的），无需登录。

    参数:
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数

    返回所有备忘录列表，包括加密的。对于加密备忘录，不返回内容。
    """
    # 获取所有备忘录（包括加密的）
    memos = MemoService.get_all_memos(db, skip, limit)

    # 处理加密内容
    result_memos = []
    for memo in memos:
        # 如果备忘录加密，清空内容
        if memo.is_encrypted:
            # 创建一个新的备忘录对象，避免修改数据库中的对象
            # 只加密内容，不加密标题
            memo_dict = {
                "id": memo.id,
                "title": memo.title,  # 保留标题
                "content": "",  # 清空内容
                "is_encrypted": memo.is_encrypted,
                "user_id": memo.user_id,
                "created_at": memo.created_at,
                "updated_at": memo.updated_at,
                "user": memo.user  # 添加用户信息
            }
            result_memos.append(memo_dict)
        else:
            # 创建一个新的备忘录对象，包含用户信息
            memo_dict = {
                "id": memo.id,
                "title": memo.title,
                "content": memo.content,
                "is_encrypted": memo.is_encrypted,
                "user_id": memo.user_id,
                "created_at": memo.created_at,
                "updated_at": memo.updated_at,
                "user": memo.user  # 添加用户信息
            }
            result_memos.append(memo_dict)

    return result_memos

@router.get("/search", response_model=List[MemoWithoutContent])
async def search_memos(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的记录数"),
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(security.get_current_user_optional)
):
    """
    搜索备忘录。

    参数:
    - **q**: 搜索关键词
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数

    返回符合搜索条件的备忘录列表。
    - 如果用户已登录，则搜索该用户的所有备忘录（包括加密的）和所有公开的备忘录
    - 如果用户未登录，则只搜索公开的备忘录
    """
    # 记录搜索请求
    user_id = current_user.id if current_user else None
    logger.info(f"用户 {user_id or '未登录'} 搜索备忘录，关键词: {q}")

    # 如果用户已登录，搜索该用户的所有备忘录和所有公开的备忘录
    if current_user:
        # 搜索用户自己的备忘录（包括加密的）
        user_memos = MemoService.search_memos(
            db=db,
            query=q,
            user_id=current_user.id,
            skip=0,
            limit=limit,
            include_encrypted=True
        )

        # 搜索其他用户的公开备忘录
        public_memos = MemoService.search_memos(
            db=db,
            query=q,
            user_id=None,
            skip=0,
            limit=limit,
            include_encrypted=False
        )

        # 合并结果并去重
        memo_ids = set()
        result_memos = []

        # 先添加用户自己的备忘录
        for memo in user_memos:
            if memo.id not in memo_ids:
                memo_ids.add(memo.id)
                # 如果是加密备忘录，清空内容
                if memo.is_encrypted:
                    memo_dict = {
                        "id": memo.id,
                        "title": memo.title,  # 保留标题
                        "content": "",  # 清空内容
                        "is_encrypted": memo.is_encrypted,
                        "user_id": memo.user_id,
                        "created_at": memo.created_at,
                        "updated_at": memo.updated_at,
                        "user": memo.user  # 添加用户信息
                    }
                    result_memos.append(memo_dict)
                else:
                    result_memos.append(memo)

        # 再添加其他用户的公开备忘录
        for memo in public_memos:
            if memo.id not in memo_ids and memo.user_id != current_user.id:
                memo_ids.add(memo.id)
                result_memos.append(memo)

        # 按创建时间排序
        result_memos.sort(key=lambda x: x["created_at"] if isinstance(x, dict) else x.created_at, reverse=True)

        # 应用分页
        start = skip
        end = skip + limit
        return result_memos[start:end]
    else:
        # 如果用户未登录，只搜索公开的备忘录
        memos = MemoService.search_memos(
            db=db,
            query=q,
            user_id=None,
            skip=skip,
            limit=limit,
            include_encrypted=False
        )
        return memos

@router.get("/public/{memo_id}", response_model=MemoResponse)
async def get_public_memo(
    memo_id: int,
    db: Session = Depends(get_db)
):
    """
    获取指定ID的公开备忘录，无需登录。

    参数:
    - **memo_id**: 备忘录ID

    返回备忘录信息。如果备忘录加密，则返回404错误。
    """
    # 获取备忘录
    memo = MemoService.get_memo_by_id(db, memo_id)
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="备忘录不存在"
        )

    # 检查是否是公开备忘录
    if memo.is_encrypted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="备忘录不存在或已加密"
        )

    return memo

@router.get("/{memo_id}", response_model=MemoResponse)
@router.get("/{memo_id}/", response_model=MemoResponse)  # 添加带斜杠的路由
async def get_memo(
    memo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    获取指定ID的备忘录。

    参数:
    - **memo_id**: 备忘录ID

    返回备忘录信息。如果备忘录加密，则不返回内容。
    """
    # 获取备忘录
    memo = MemoService.get_memo_by_id(db, memo_id)
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="备忘录不存在"
        )

    # 检查权限
    if memo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此备忘录"
        )

    # 如果备忘录加密，清空内容
    if memo.is_encrypted:
        # 创建一个新的备忘录对象，避免修改数据库中的对象
        # 只加密内容，不加密标题
        response_memo = MemoResponse(
            id=memo.id,
            title=memo.title,  # 保留标题
            content="",  # 清空内容
            is_encrypted=memo.is_encrypted,
            user_id=memo.user_id,
            created_at=memo.created_at,
            updated_at=memo.updated_at
        )
        return response_memo

    return memo

@router.post("/{memo_id}/verify", response_model=MemoPasswordVerifyResponse)
@router.post("/{memo_id}/verify/", response_model=MemoPasswordVerifyResponse)  # 添加带斜杠的路由
async def verify_memo_password(
    memo_id: int,
    password_data: MemoPasswordVerify,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    验证备忘录密码。

    参数:
    - **memo_id**: 备忘录ID
    - **password**: 密码

    返回验证结果和备忘录内容（如果验证成功）。
    任何已登录用户都可以尝试验证密码，只要密码正确就能查看内容。
    """
    # 获取备忘录
    memo = MemoService.get_memo_by_id(db, memo_id)
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="备忘录不存在"
        )

    # 不再检查用户是否是备忘录的创建者
    # 任何已登录用户都可以尝试验证密码
    # 密码验证成功与否由 verify_memo_password 函数决定

    # 记录尝试验证密码的用户信息
    logger.info(f"用户 {current_user.id} ({current_user.username}) 尝试验证备忘录 {memo_id} 的密码")

    # 验证密码
    verified_memo = MemoService.verify_memo_password(db, memo_id, password_data.password)
    if not verified_memo:
        logger.warning(f"用户 {current_user.id} 验证备忘录 {memo_id} 的密码失败")
        return MemoPasswordVerifyResponse(success=False)

    # 验证成功，返回内容
    logger.info(f"用户 {current_user.id} 成功验证备忘录 {memo_id} 的密码")
    return MemoPasswordVerifyResponse(
        success=True,
        content=verified_memo.content
    )

@router.put("/{memo_id}", response_model=MemoResponse)
@router.put("/{memo_id}/", response_model=MemoResponse)  # 添加带斜杠的路由
async def update_memo(
    memo_id: int,
    memo_data: MemoUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    更新备忘录。

    参数:
    - **memo_id**: 备忘录ID
    - **title**: 备忘录标题
    - **content**: 备忘录内容
    - **is_encrypted**: 是否加密
    - **password**: 如果加密，提供密码

    返回更新后的备忘录信息。
    """
    # 检查用户是否为管理员
    is_admin = current_user.role == UserRole.admin
    logger.info(f"用户 {current_user.id} ({current_user.username}) 尝试更新备忘录 {memo_id}, 角色: {current_user.role}, 是否管理员: {is_admin}")

    # 更新备忘录
    memo = MemoService.update_memo(db, memo_id, memo_data, current_user.id, is_admin)

    # 记录活动
    ActivityService.create_activity(
        db=db,
        action_type="memo_update",
        user_id=current_user.id,
        target_id=memo.id,
        description=f"用户 {current_user.username} 更新了备忘录 《{memo.title}》"
    )

    return memo

@router.delete("/{memo_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/{memo_id}/", status_code=status.HTTP_204_NO_CONTENT)  # 添加带斜杠的路由
async def delete_memo(
    memo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    删除备忘录。

    参数:
    - **memo_id**: 备忘录ID

    返回204 No Content。
    """
    # 添加调试日志
    logger.info(f"尝试删除备忘录 ID: {memo_id}, 当前用户 ID: {current_user.id}, 用户名: {current_user.username}, 角色: {current_user.role}")

    # 获取备忘录信息用于活动记录
    memo = MemoService.get_memo_by_id(db, memo_id)
    if not memo:
        logger.warning(f"备忘录不存在: {memo_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="备忘录不存在"
        )

    # 添加备忘录信息日志
    logger.info(f"找到备忘录: ID={memo.id}, 标题={memo.title}, 创建者ID={memo.user_id}")

    # 检查权限 - 允许管理员或创建者删除
    is_admin = current_user.role == "admin"
    is_owner = memo.user_id == current_user.id

    if not (is_admin or is_owner):
        logger.warning(f"权限拒绝: 用户 {current_user.id} 尝试删除备忘录 {memo_id}, 但该备忘录属于用户 {memo.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此备忘录"
        )

    # 记录活动
    ActivityService.create_activity(
        db=db,
        action_type="memo_delete",
        user_id=current_user.id,
        target_id=memo_id,
        description=f"用户 {current_user.username} 删除了备忘录 《{memo.title}》"
    )

    # 调用服务层方法删除备忘录，传递管理员状态
    is_admin = current_user.role == "admin"
    MemoService.delete_memo(db, memo_id, current_user.id, is_admin=is_admin)

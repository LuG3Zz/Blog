"""
管理员路由模块：提供管理员特有的功能
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app import models
from app.core import security
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserRole, UserUpdate
from app.core.permissions import is_admin
from app.services.user_service import UserService

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(security.get_current_user)]
)

@router.post("/users", response_model=UserResponse)
async def create_admin_user(
    user_data: UserCreate,
    role: UserRole,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    创建管理员或编辑用户

    只有管理员可以创建其他管理员或编辑用户
    """
    # 检查当前用户是否为管理员
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create admin or editor users"
        )

    # 创建用户
    try:
        # 设置用户角色
        user_dict = user_data.model_dump()
        user_dict["role"] = role

        # 创建用户
        new_user = UserService.create_user(db, user_dict)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/users", response_model=list[UserResponse])
async def list_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
    role: UserRole = None,
    skip: int = 0,
    limit: int = 100
):
    """
    获取用户列表

    只有管理员可以查看所有用户
    可以通过角色筛选用户
    """
    # 检查当前用户是否为管理员
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can view all users"
        )

    # 使用 UserService 获取用户列表，包含评论数和文章数
    users = UserService.get_users(db, skip=skip, limit=limit, include_counts=True)

    # 按角色筛选
    if role:
        users = [user for user in users if user.role == role]

    return users


@router.patch("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role_data: dict,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新用户角色（管理员专用）

    - **user_id**: 用户ID
    - **role_data**: 包含角色信息的JSON对象，格式为 {"role": "角色名称"}
      角色名称可以是: admin, editor, author, user

    返回更新后的用户信息
    """
    # 检查当前用户是否为管理员
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以修改用户角色"
        )

    # 检查用户是否存在
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 不允许修改自己的角色
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能修改自己的角色"
        )

    # 从请求体中获取角色
    role_value = role_data.get('role')
    if not role_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供角色参数"
        )

    try:
        # 将字符串转换为枚举值
        role_enum = UserRole(role_value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的角色值: {role_value}，有效值为: {[r.value for r in UserRole]}"
        )

    # 更新用户角色
    user_update = UserUpdate(role=role_enum)
    updated_user = UserService.update_user(db, user_id, user_update)

    return updated_user

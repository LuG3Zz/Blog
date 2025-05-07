from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from app import models
from app.schemas.memo import MemoCreate, MemoUpdate
from app.utils.password import verify_password, get_password_hash
from app.utils.logging import get_logger

logger = get_logger(__name__)

class MemoService:
    """备忘录服务，提供备忘录相关的业务逻辑。"""

    @staticmethod
    def get_memo_by_id(db: Session, memo_id: int) -> Optional[models.Memo]:
        """根据ID获取备忘录。"""
        return db.query(models.Memo).filter(models.Memo.id == memo_id).first()

    @staticmethod
    def get_memos_by_user(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Memo]:
        """获取用户的备忘录列表。"""
        return db.query(models.Memo)\
            .filter(models.Memo.user_id == user_id)\
            .order_by(models.Memo.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    def get_public_memos(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Memo]:
        """获取所有公开的备忘录列表（未加密的）。"""
        return db.query(models.Memo)\
            .filter(models.Memo.is_encrypted == False)\
            .order_by(models.Memo.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    def get_all_memos(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Memo]:
        """获取所有备忘录列表（包括加密的）。"""
        return db.query(models.Memo)\
            .order_by(models.Memo.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    def create_memo(
        db: Session,
        memo_data: MemoCreate,
        user_id: int
    ) -> models.Memo:
        """创建新备忘录。"""
        # 处理标题和内容
        title = memo_data.title
        content = memo_data.content or ""

        # 标题可以为空，不设置默认值
        # 如果标题是None，设置为空字符串以避免数据库问题
        if title is None:
            title = ""

        # 记录接收到的数据
        logger.info(f"创建备忘录，接收到的数据: title={title}, content_length={len(content)}, is_encrypted={memo_data.is_encrypted}")

        # 处理加密
        password_hash = None
        if memo_data.is_encrypted and memo_data.password:
            password_hash = get_password_hash(memo_data.password)
            logger.info("备忘录将被加密")
        elif memo_data.is_encrypted and not memo_data.password:
            logger.error("尝试创建加密备忘录但未提供密码")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="加密备忘录必须提供密码"
            )

        # 创建备忘录
        db_memo = models.Memo(
            title=title,
            content=content,
            is_encrypted=memo_data.is_encrypted,
            password_hash=password_hash,
            user_id=user_id
        )

        # 记录即将保存的数据
        logger.info(f"即将保存备忘录: title={db_memo.title}, content_length={len(db_memo.content) if db_memo.content else 0}, is_encrypted={db_memo.is_encrypted}")

        db.add(db_memo)
        db.commit()
        db.refresh(db_memo)

        # 记录保存后的数据
        logger.info(f"用户 {user_id} 创建了备忘录 {db_memo.id}, 保存后的content_length={len(db_memo.content) if db_memo.content else 0}")
        return db_memo

    @staticmethod
    def update_memo(
        db: Session,
        memo_id: int,
        memo_data: MemoUpdate,
        user_id: int,
        is_admin: bool = False
    ) -> models.Memo:
        """
        更新备忘录。

        参数:
        - db: 数据库会话
        - memo_id: 备忘录ID
        - memo_data: 更新数据
        - user_id: 用户ID
        - is_admin: 是否为管理员

        返回:
        - 更新后的备忘录
        """
        # 获取备忘录
        db_memo = MemoService.get_memo_by_id(db, memo_id)
        if not db_memo:
            logger.warning(f"尝试更新不存在的备忘录: {memo_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="备忘录不存在"
            )

        # 检查权限 - 允许管理员或创建者更新
        if not is_admin and db_memo.user_id != user_id:
            logger.warning(f"权限拒绝: 用户 {user_id} 尝试更新备忘录 {memo_id}, 但该备忘录属于用户 {db_memo.user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权修改此备忘录"
            )

        # 更新字段
        if memo_data.title is not None:
            db_memo.title = memo_data.title
        if memo_data.content is not None:
            db_memo.content = memo_data.content

        # 标题可以为空，不设置默认值
        # 如果标题是None，设置为空字符串以避免数据库问题
        if db_memo.title is None:
            db_memo.title = ""

        # 处理加密状态和密码
        if memo_data.is_encrypted is not None:
            # 如果从未加密变为加密，需要提供密码
            if memo_data.is_encrypted and not db_memo.is_encrypted:
                if not memo_data.password:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="加密备忘录必须提供密码"
                    )
                db_memo.password_hash = get_password_hash(memo_data.password)

            # 如果从加密变为未加密，清除密码哈希
            if not memo_data.is_encrypted and db_memo.is_encrypted:
                db_memo.password_hash = None

            db_memo.is_encrypted = memo_data.is_encrypted

        # 如果保持加密状态但更新密码
        if db_memo.is_encrypted and memo_data.password:
            db_memo.password_hash = get_password_hash(memo_data.password)

        db.commit()
        db.refresh(db_memo)

        logger.info(f"用户 {user_id} 更新了备忘录 {db_memo.id}")
        return db_memo

    @staticmethod
    def delete_memo(
        db: Session,
        memo_id: int,
        user_id: int,
        is_admin: bool = False
    ) -> bool:
        """
        删除备忘录。

        参数:
        - db: 数据库会话
        - memo_id: 备忘录ID
        - user_id: 用户ID
        - is_admin: 是否为管理员

        返回:
        - 是否删除成功
        """
        # 获取备忘录
        db_memo = MemoService.get_memo_by_id(db, memo_id)
        if not db_memo:
            logger.warning(f"尝试删除不存在的备忘录: {memo_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="备忘录不存在"
            )

        # 检查权限 - 允许管理员或创建者删除
        if not is_admin and db_memo.user_id != user_id:
            logger.warning(f"权限拒绝: 用户 {user_id} 尝试删除备忘录 {memo_id}, 但该备忘录属于用户 {db_memo.user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权删除此备忘录"
            )

        # 删除备忘录
        db.delete(db_memo)
        db.commit()

        logger.info(f"用户 {user_id} 删除了备忘录 {memo_id}")
        return True

    @staticmethod
    def verify_memo_password(
        db: Session,
        memo_id: int,
        password: str
    ) -> Optional[models.Memo]:
        """验证备忘录密码。"""
        # 获取备忘录
        db_memo = MemoService.get_memo_by_id(db, memo_id)
        if not db_memo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="备忘录不存在"
            )

        # 检查是否加密
        if not db_memo.is_encrypted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="此备忘录未加密"
            )

        # 验证密码
        if not verify_password(password, db_memo.password_hash):
            return None

        return db_memo

    @staticmethod
    def search_memos(
        db: Session,
        query: str,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        include_encrypted: bool = False
    ) -> List[models.Memo]:
        """
        搜索备忘录。

        参数:
        - db: 数据库会话
        - query: 搜索关键词
        - user_id: 用户ID，如果提供则只搜索该用户的备忘录
        - skip: 跳过的记录数
        - limit: 返回的记录数
        - include_encrypted: 是否包含加密的备忘录

        返回:
        - 符合条件的备忘录列表
        """
        # 构建基础查询
        search_query = db.query(models.Memo)

        # 添加搜索条件
        search_term = f"%{query}%"
        search_filter = or_(
            models.Memo.title.ilike(search_term),
            models.Memo.content.ilike(search_term)
        )
        search_query = search_query.filter(search_filter)

        # 如果指定了用户ID，只搜索该用户的备忘录
        if user_id:
            search_query = search_query.filter(models.Memo.user_id == user_id)

        # 如果不包含加密备忘录，则过滤掉加密的备忘录
        if not include_encrypted:
            search_query = search_query.filter(models.Memo.is_encrypted == False)

        # 按创建时间降序排序
        search_query = search_query.order_by(models.Memo.created_at.desc())

        # 应用分页
        search_query = search_query.offset(skip).limit(limit)

        # 执行查询并返回结果
        return search_query.all()

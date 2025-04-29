"""
添加访客名称和用户ID字段到访客表
"""
import logging
from sqlalchemy import Column, String, text
from app.core.database import engine

logger = logging.getLogger(__name__)

def run_migration():
    """
    添加访客名称和用户ID字段到访客表
    """
    logger.info("开始添加访客名称和用户ID字段到访客表...")

    # 检查字段是否已存在
    with engine.connect() as connection:
        # 检查visitor_name字段
        result = connection.execute(text(
            "SELECT COUNT(*) FROM information_schema.columns "
            "WHERE table_name = 'visitors' AND column_name = 'visitor_name'"
        ))
        visitor_name_exists = result.scalar() > 0

        # 检查user_id字段
        result = connection.execute(text(
            "SELECT COUNT(*) FROM information_schema.columns "
            "WHERE table_name = 'visitors' AND column_name = 'user_id'"
        ))
        user_id_exists = result.scalar() > 0

        # 添加visitor_name字段
        if not visitor_name_exists:
            logger.info("添加visitor_name字段...")
            connection.execute(text(
                "ALTER TABLE visitors "
                "ADD COLUMN visitor_name VARCHAR(100) DEFAULT '访客'"
            ))
            logger.info("visitor_name字段添加成功")
        else:
            logger.info("visitor_name字段已存在，跳过")

        # 添加user_id字段
        if not user_id_exists:
            logger.info("添加user_id字段...")
            connection.execute(text(
                "ALTER TABLE visitors "
                "ADD COLUMN user_id VARCHAR(50) DEFAULT NULL, "
                "ADD INDEX idx_visitors_user_id (user_id)"
            ))
            logger.info("user_id字段添加成功")
        else:
            logger.info("user_id字段已存在，跳过")

    logger.info("访客表字段添加完成")
    return True

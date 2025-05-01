"""
修复 users 表中缺少 email_verified 列的问题

此脚本用于确保 users 表中存在 email_verified 列，
解决部署环境中可能出现的 "Unknown column 'users.email_verified' in 'field list'" 错误。

使用方法：
python -m migrations.fix_email_verified_column
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 加载环境变量
load_dotenv()

# 获取数据库连接字符串
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("未找到数据库连接字符串，请确保 DATABASE_URL 环境变量已设置")
    sys.exit(1)

def run_migration():
    """执行数据库迁移，确保 users 表中存在 email_verified 列"""
    logger.info("开始执行数据库迁移，检查 email_verified 列...")

    # 创建数据库引擎
    engine = create_engine(DATABASE_URL)

    try:
        # 连接数据库
        with engine.connect() as connection:
            # 检查 users 表中是否已存在 email_verified 字段
            result = connection.execute(text("""
                SELECT COUNT(*)
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'users'
                AND COLUMN_NAME = 'email_verified'
            """))

            if result.scalar() == 0:
                # 添加 email_verified 字段到 users 表
                logger.info("向 users 表添加 email_verified 字段...")
                connection.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE
                """))
                logger.info("users 表更新完成")
            else:
                logger.info("users 表中 email_verified 字段已存在，跳过")

            # 提交事务
            connection.commit()

        logger.info("数据库迁移成功完成")

    except Exception as e:
        logger.error(f"数据库迁移失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()

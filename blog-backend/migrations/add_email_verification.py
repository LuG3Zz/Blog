"""
数据库迁移脚本：添加邮箱验证相关字段

此脚本用于向数据库添加邮箱验证相关的字段：
1. 在 users 表中添加 email_verified 字段
2. 在 site_settings 表中添加 require_email_verification 字段

使用方法：
python -m migrations.add_email_verification
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
    """执行数据库迁移"""
    logger.info("开始执行数据库迁移...")

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

            # 检查 site_settings 表是否存在
            result = connection.execute(text("""
                SELECT COUNT(*)
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'site_settings'
            """))

            if result.scalar() == 0:
                # 创建 site_settings 表
                logger.info("创建 site_settings 表...")
                connection.execute(text("""
                    CREATE TABLE site_settings (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        site_title VARCHAR(100) NOT NULL DEFAULT 'BrownLu的博客',
                        site_subtitle VARCHAR(200) DEFAULT '与你共享美好生活',
                        nav_text JSON,
                        banner_image VARCHAR(255),
                        footer_text VARCHAR(255),
                        logo_image VARCHAR(255),
                        favicon VARCHAR(255),
                        meta_description VARCHAR(500),
                        meta_keywords VARCHAR(255),
                        custom_css TEXT,
                        custom_js TEXT,
                        require_email_verification BOOLEAN NOT NULL DEFAULT FALSE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """))
                logger.info("site_settings 表创建完成")
            else:
                # 检查 site_settings 表中是否已存在 require_email_verification 字段
                result = connection.execute(text("""
                    SELECT COUNT(*)
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'site_settings'
                    AND COLUMN_NAME = 'require_email_verification'
                """))

                if result.scalar() == 0:
                    # 添加 require_email_verification 字段到 site_settings 表
                    logger.info("向 site_settings 表添加 require_email_verification 字段...")
                    connection.execute(text("""
                        ALTER TABLE site_settings
                        ADD COLUMN require_email_verification BOOLEAN NOT NULL DEFAULT FALSE
                    """))
                    logger.info("site_settings 表更新完成")
                else:
                    logger.info("site_settings 表中 require_email_verification 字段已存在，跳过")

            # 提交事务
            connection.commit()

        logger.info("数据库迁移成功完成")

    except Exception as e:
        logger.error(f"数据库迁移失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()

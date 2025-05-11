"""
数据库迁移脚本 - 添加邮件设置相关列
"""
import os
import sys
import logging
import traceback
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 直接打印到控制台
print("开始执行数据库迁移脚本 - 添加邮件设置相关列")

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入数据库配置
try:
    print("正在导入配置...")
    logger.info("正在导入配置...")
    from app.core.config import settings
    print(f"数据库URL: {settings.DATABASE_URL}")
    logger.info(f"数据库URL: {settings.DATABASE_URL}")
except Exception as e:
    print(f"导入配置失败: {e}")
    traceback.print_exc()
    logger.error(f"导入配置失败: {e}")
    sys.exit(1)

def run_migration():
    """执行数据库迁移"""
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)
        
        # 连接数据库
        with engine.connect() as connection:
            # 开始事务
            with connection.begin():
                # 检查列是否存在
                print("检查邮件设置相关列是否存在...")
                logger.info("检查邮件设置相关列是否存在...")
                
                # 检查email_enabled列
                result = connection.execute(text("""
                    SELECT COUNT(*) AS count FROM information_schema.columns 
                    WHERE table_schema = DATABASE() 
                    AND table_name = 'site_settings' 
                    AND column_name = 'email_enabled';
                """))
                
                if result.fetchone()[0] == 0:
                    print("添加email_enabled列...")
                    logger.info("添加email_enabled列...")
                    connection.execute(text("""
                        ALTER TABLE site_settings
                        ADD COLUMN email_enabled BOOLEAN DEFAULT FALSE AFTER comment_review_api_key;
                    """))
                else:
                    print("email_enabled列已存在")
                    logger.info("email_enabled列已存在")
                
                # 检查email_api_key列
                result = connection.execute(text("""
                    SELECT COUNT(*) AS count FROM information_schema.columns 
                    WHERE table_schema = DATABASE() 
                    AND table_name = 'site_settings' 
                    AND column_name = 'email_api_key';
                """))
                
                if result.fetchone()[0] == 0:
                    print("添加email_api_key列...")
                    logger.info("添加email_api_key列...")
                    connection.execute(text("""
                        ALTER TABLE site_settings
                        ADD COLUMN email_api_key VARCHAR(255) NULL AFTER email_enabled;
                    """))
                else:
                    print("email_api_key列已存在")
                    logger.info("email_api_key列已存在")
                
                # 更新现有记录
                print("更新现有记录...")
                logger.info("更新现有记录...")
                connection.execute(text("""
                    UPDATE site_settings
                    SET email_enabled = FALSE
                    WHERE email_enabled IS NULL;
                """))
                
        print("迁移成功完成！")
        logger.info("迁移成功完成！")
        return True
    except SQLAlchemyError as e:
        print(f"迁移失败: {e}")
        logger.error(f"迁移失败: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)

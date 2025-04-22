"""
数据库迁移脚本：从 articles 表中移除 tags 列
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """执行迁移：从 articles 表中移除 tags 列"""
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # 开始事务
        trans = conn.begin()
        try:
            # 检查 tags 列是否存在
            logger.info("检查 articles 表中的 tags 列是否存在...")
            result = conn.execute(text(
                "SELECT COUNT(*) FROM information_schema.columns "
                "WHERE table_name = 'articles' AND column_name = 'tags'"
            ))
            column_exists = result.scalar() > 0
            
            if column_exists:
                # 移除 tags 列
                logger.info("从 articles 表中移除 tags 列...")
                conn.execute(text("ALTER TABLE articles DROP COLUMN tags"))
                logger.info("成功移除 tags 列")
            else:
                logger.info("articles 表中不存在 tags 列，无需移除")
            
            # 提交事务
            trans.commit()
            logger.info("迁移完成")
            
        except Exception as e:
            # 回滚事务
            trans.rollback()
            logger.error(f"迁移失败: {e}")
            raise

if __name__ == "__main__":
    run_migration()

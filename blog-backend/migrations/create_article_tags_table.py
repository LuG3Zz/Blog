"""
数据库迁移脚本：创建文章-标签多对多关系表，并迁移现有标签数据
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """执行迁移：创建文章-标签多对多关系表，并迁移现有标签数据"""
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # 开始事务
        trans = conn.begin()
        try:
            # 检查article_tags表是否已存在
            result = conn.execute(text(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_name = 'article_tags'"
            ))
            table_exists = result.scalar() > 0
            
            if not table_exists:
                # 创建article_tags表
                logger.info("Creating article_tags table...")
                conn.execute(text("""
                    CREATE TABLE article_tags (
                        article_id INT NOT NULL,
                        tag_id INT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (article_id, tag_id),
                        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
                        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
                    )
                """))
                
                # 迁移现有标签数据
                logger.info("Migrating existing tag data...")
                
                # 获取所有文章
                articles = conn.execute(text("SELECT id, tags FROM articles WHERE tags IS NOT NULL AND tags != ''"))
                
                # 处理每篇文章的标签
                for article_id, tags_str in articles:
                    if tags_str:
                        # 分割标签字符串
                        tag_names = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                        
                        for tag_name in tag_names:
                            # 检查标签是否存在
                            tag_result = conn.execute(text(
                                "SELECT id FROM tags WHERE name = :name"
                            ), {"name": tag_name})
                            tag_row = tag_result.fetchone()
                            
                            # 如果标签不存在，创建它
                            if not tag_row:
                                logger.info(f"Creating new tag: {tag_name}")
                                tag_insert = conn.execute(text(
                                    "INSERT INTO tags (name) VALUES (:name)"
                                ), {"name": tag_name})
                                
                                # 获取新创建的标签ID
                                tag_id_result = conn.execute(text(
                                    "SELECT LAST_INSERT_ID()"
                                ))
                                tag_id = tag_id_result.scalar()
                            else:
                                tag_id = tag_row[0]
                            
                            # 创建文章-标签关联
                            try:
                                conn.execute(text(
                                    "INSERT INTO article_tags (article_id, tag_id) VALUES (:article_id, :tag_id)"
                                ), {"article_id": article_id, "tag_id": tag_id})
                                logger.info(f"Associated article {article_id} with tag {tag_name} (ID: {tag_id})")
                            except Exception as e:
                                # 可能已经存在，忽略错误
                                logger.warning(f"Error associating article {article_id} with tag {tag_id}: {e}")
                
                logger.info("Migration completed successfully")
            else:
                logger.info("article_tags table already exists, skipping migration")
            
            # 提交事务
            trans.commit()
            
        except Exception as e:
            # 回滚事务
            trans.rollback()
            logger.error(f"Migration failed: {e}")
            raise

if __name__ == "__main__":
    run_migration()

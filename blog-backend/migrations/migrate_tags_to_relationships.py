"""
数据库迁移脚本：将文章表中的 tags 字段数据迁移到 article_tags 多对多关系表中
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """执行迁移：将文章表中的 tags 字段数据迁移到 article_tags 多对多关系表中"""
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # 开始事务
        trans = conn.begin()
        try:
            # 获取所有文章及其标签
            logger.info("获取所有文章及其标签...")
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
                            logger.info(f"创建新标签: {tag_name}")
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
                        
                        # 检查关系是否已存在
                        relation_result = conn.execute(text(
                            "SELECT 1 FROM article_tags WHERE article_id = :article_id AND tag_id = :tag_id"
                        ), {"article_id": article_id, "tag_id": tag_id})
                        relation_exists = relation_result.fetchone() is not None
                        
                        # 如果关系不存在，创建它
                        if not relation_exists:
                            # 创建文章-标签关联
                            try:
                                now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                                conn.execute(text(
                                    "INSERT INTO article_tags (article_id, tag_id, created_at) VALUES (:article_id, :tag_id, :created_at)"
                                ), {"article_id": article_id, "tag_id": tag_id, "created_at": now})
                                logger.info(f"关联文章 {article_id} 与标签 {tag_name} (ID: {tag_id})")
                            except Exception as e:
                                # 可能已经存在，记录错误但继续执行
                                logger.warning(f"关联文章 {article_id} 与标签 {tag_id} 时出错: {e}")
            
            logger.info("迁移完成")
            
            # 提交事务
            trans.commit()
            
        except Exception as e:
            # 回滚事务
            trans.rollback()
            logger.error(f"迁移失败: {e}")
            raise

if __name__ == "__main__":
    run_migration()

from sqlalchemy import create_engine, text
from app.core.config import settings

def run_migration():
    """Add performance indexes to improve query speed."""
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={'charset': 'utf8mb4'}
    )

    with engine.connect() as connection:
        # 检查索引是否存在的函数
        def index_exists(table_name, index_name):
            result = connection.execute(text(
                "SELECT COUNT(*) FROM information_schema.statistics "
                "WHERE table_schema = DATABASE() "
                "AND table_name = :table_name "
                "AND index_name = :index_name"
            ), {"table_name": table_name, "index_name": index_name})
            return result.scalar() > 0

        # 创建索引的函数
        def create_index_if_not_exists(table_name, index_name, columns):
            if not index_exists(table_name, index_name):
                try:
                    connection.execute(text(
                        f"CREATE INDEX {index_name} ON {table_name} ({columns})"
                    ))
                    print(f"Created index {index_name} on {table_name}({columns})")
                except Exception as e:
                    print(f"Error creating index {index_name}: {str(e)}")
            else:
                print(f"Index {index_name} already exists on {table_name}")

        # 添加评论表索引
        create_index_if_not_exists("comments", "idx_comments_article_id", "article_id")
        create_index_if_not_exists("comments", "idx_comments_user_id", "user_id")
        create_index_if_not_exists("comments", "idx_comments_parent_id", "parent_id")
        create_index_if_not_exists("comments", "idx_comments_created_at", "created_at")
        create_index_if_not_exists("comments", "idx_comments_is_approved", "is_approved")

        # 添加文章表索引
        create_index_if_not_exists("articles", "idx_articles_author_id", "author_id")
        create_index_if_not_exists("articles", "idx_articles_category_id", "category_id")
        create_index_if_not_exists("articles", "idx_articles_created_at", "created_at")
        create_index_if_not_exists("articles", "idx_articles_is_featured", "is_featured")

        # 添加用户表索引
        create_index_if_not_exists("users", "idx_users_role", "role")

        # 添加活动表索引
        create_index_if_not_exists("activities", "idx_activities_user_id", "user_id")
        create_index_if_not_exists("activities", "idx_activities_action_type", "action_type")
        create_index_if_not_exists("activities", "idx_activities_created_at", "created_at")

        print("Migration successful: Added performance indexes")

if __name__ == "__main__":
    run_migration()

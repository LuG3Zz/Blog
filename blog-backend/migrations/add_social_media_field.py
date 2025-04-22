from sqlalchemy import create_engine, text
from app.core.config import settings

def run_migration():
    """Add social_media column to users table."""
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={'charset': 'utf8mb4'}
    )
    
    with engine.connect() as connection:
        # Check if the column already exists
        result = connection.execute(text(
            "SELECT COUNT(*) FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() "
            "AND TABLE_NAME = 'users' "
            "AND COLUMN_NAME = 'social_media'"
        ))
        column_exists = result.scalar() > 0
        
        if not column_exists:
            # Add the social_media column
            connection.execute(text(
                "ALTER TABLE users "
                "ADD COLUMN social_media TEXT NULL "
                "COMMENT '社交媒体链接，存储为JSON字符串'"
            ))
            print("Migration successful: Added social_media column to users table")
        else:
            print("Migration skipped: social_media column already exists")

if __name__ == "__main__":
    run_migration()

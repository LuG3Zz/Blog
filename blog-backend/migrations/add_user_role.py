"""
数据库迁移脚本：添加用户角色字段
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def run_migration():
    """执行迁移：添加用户角色字段"""
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)

    # 检查role列是否已存在
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT COUNT(*) FROM information_schema.columns "
            "WHERE table_name = 'users' AND column_name = 'role'"
        ))
        column_exists = result.scalar() > 0

    # 如果列不存在，则添加
    if not column_exists:
        with engine.connect() as conn:
            # 添加角色列，默认为'user'
            conn.execute(text(
                "ALTER TABLE users ADD COLUMN role ENUM('admin', 'editor', 'author', 'user') NOT NULL DEFAULT 'user'"
            ))

            # 将第一个用户设置为管理员
            conn.execute(text(
                "UPDATE users SET role = 'admin' WHERE id = 1"
            ))

            conn.commit()
            print("Migration completed: Added 'role' column to users table")
    else:
        print("Migration skipped: 'role' column already exists")

if __name__ == "__main__":
    run_migration()

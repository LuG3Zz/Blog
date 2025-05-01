"""
统一的数据库迁移脚本
用于运行所有数据库迁移和性能优化
"""
import sys
import importlib
from typing import List, Callable

# 所有迁移模块列表
MIGRATION_MODULES = [
    "migrations.add_user_role",
    "migrations.add_social_media_field",
    "migrations.add_performance_indexes",
    "migrations.update_emoji_support",
    "migrations.add_comment_review_fields",
    "migrations.create_article_tags_table",
    "migrations.migrate_tags_to_relationships",
    "migrations.remove_tags_column",
    "migrations.add_email_verification",
    "migrations.fix_email_verified_column"
]

def run_all_migrations():
    """运行所有迁移"""
    print("开始运行所有数据库迁移...")

    success_count = 0
    failed_migrations = []

    for module_name in MIGRATION_MODULES:
        try:
            print(f"\n正在运行迁移: {module_name}")
            # 动态导入模块
            module = importlib.import_module(module_name)
            # 运行迁移
            module.run_migration()
            success_count += 1
            print(f"✅ 迁移 {module_name} 成功完成")
        except Exception as e:
            print(f"❌ 迁移 {module_name} 失败: {str(e)}")
            failed_migrations.append((module_name, str(e)))

    # 打印迁移结果摘要
    print("\n" + "="*50)
    print(f"迁移完成: 成功 {success_count}/{len(MIGRATION_MODULES)}")

    if failed_migrations:
        print("\n失败的迁移:")
        for name, error in failed_migrations:
            print(f"- {name}: {error}")
        return False

    print("\n所有迁移成功完成!")
    return True

def run_specific_migration(module_name: str):
    """运行特定的迁移"""
    try:
        print(f"正在运行迁移: {module_name}")
        # 动态导入模块
        module = importlib.import_module(module_name)
        # 运行迁移
        module.run_migration()
        print(f"✅ 迁移 {module_name} 成功完成")
        return True
    except Exception as e:
        print(f"❌ 迁移 {module_name} 失败: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 如果提供了参数，运行特定的迁移
        migration_name = sys.argv[1]
        full_module_name = f"migrations.{migration_name}"
        success = run_specific_migration(full_module_name)
        sys.exit(0 if success else 1)
    else:
        # 否则运行所有迁移
        success = run_all_migrations()
        sys.exit(0 if success else 1)

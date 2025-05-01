# 部署修复指南

## 问题描述

在服务器部署时出现以下错误：

```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1054, "Unknown column 'users.email_verified' in 'field list'")
[SQL: SELECT users.id AS users_id, users.username AS users_username, users.email AS users_email, users.email_verified AS users_email_verified, users.hashed_password AS users_hashed_password, users.avatar AS users_avatar, users.bio AS users_bio, users.`role` AS users_role, users.social_media AS users_social_media, users.created_at AS users_created_at, users.updated_at AS users_updated_at
FROM users
WHERE users.id = %(id_1)s
 LIMIT %(param_1)s]
```

这个错误表明服务器上的数据库中 `users` 表缺少 `email_verified` 列，但代码中的 User 模型却在尝试查询这个列。

## 解决方案

我们创建了一个专门的数据库迁移脚本 `fix_email_verified_column.py` 来解决这个问题。这个脚本会检查 `users` 表中是否存在 `email_verified` 列，如果不存在则添加它。

### 在服务器上执行以下步骤：

1. 确保已经将最新的代码推送到服务器，包括新添加的迁移脚本 `migrations/fix_email_verified_column.py`

2. 在服务器上，进入项目目录并运行以下命令：

   ```bash
   # 如果使用 Docker 部署
   docker exec -it blog-api python -m migrations.fix_email_verified_column
   
   # 如果直接在服务器上部署
   cd /path/to/blog-backend
   python -m migrations.fix_email_verified_column
   ```

3. 如果上述命令成功执行，你应该会看到类似以下的输出：

   ```
   INFO - 开始执行数据库迁移，检查 email_verified 列...
   INFO - 向 users 表添加 email_verified 字段...
   INFO - users 表更新完成
   INFO - 数据库迁移成功完成
   ```

4. 重启应用服务：

   ```bash
   # 如果使用 Docker Compose
   docker-compose restart blog-api
   
   # 如果使用 systemd
   sudo systemctl restart blog-api
   ```

## 预防措施

为了避免将来出现类似问题，请确保：

1. 在本地开发环境中创建新的数据库模型字段后，始终创建相应的迁移脚本

2. 将所有迁移脚本添加到 `run_migrations.py` 的 `MIGRATION_MODULES` 列表中

3. 在部署新版本之前，先在测试环境中运行所有迁移脚本

4. 考虑使用自动化的数据库迁移工具，如 Alembic，来管理数据库架构变更

## 其他可能的问题

如果在修复此问题后仍然遇到其他数据库相关错误，可能是因为还有其他表或列缺失。请检查错误消息，并根据需要创建额外的迁移脚本。

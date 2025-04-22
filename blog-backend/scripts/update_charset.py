#!/usr/bin/env python
"""
数据库字符集迁移脚本
将数据库和表的字符集从 utf8mb3 更改为 utf8mb4，以支持 Emoji 字符
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取数据库连接信息
db_url = os.getenv("DATABASE_URL", "mysql+pymysql://user:pass@localhost:3306/dbname")

# 解析数据库连接信息
if "mysql+pymysql://" in db_url:
    # 从 SQLAlchemy URL 中提取连接信息
    db_url = db_url.replace("mysql+pymysql://", "")
    auth_part, db_part = db_url.split("@")
    
    if ":" in auth_part:
        user, password = auth_part.split(":")
    else:
        user = auth_part
        password = ""
    
    if "/" in db_part:
        host_port, db_name = db_part.split("/")
    else:
        host_port = db_part
        db_name = "blog"
    
    if ":" in host_port:
        host, port = host_port.split(":")
        port = int(port)
    else:
        host = host_port
        port = 3306
    
    # 移除查询参数
    if "?" in db_name:
        db_name = db_name.split("?")[0]
else:
    print("无法解析数据库连接 URL")
    sys.exit(1)

try:
    # 连接到数据库
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with connection.cursor() as cursor:
        # 修改数据库字符集
        print(f"正在修改数据库 {db_name} 的字符集为 utf8mb4...")
        cursor.execute(f"ALTER DATABASE `{db_name}` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;")
        
        # 切换到目标数据库
        cursor.execute(f"USE `{db_name}`;")
        
        # 获取所有表
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        # 修改每个表的字符集
        for table in tables:
            table_name = list(table.values())[0]
            print(f"正在修改表 {table_name} 的字符集为 utf8mb4...")
            cursor.execute(f"ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        
        # 特别处理 activities 表的 description 字段
        print("正在修改 activities 表的 description 字段...")
        cursor.execute("ALTER TABLE `activities` MODIFY `description` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        
        # 提交更改
        connection.commit()
        
        print("数据库字符集迁移完成！")
        
except Exception as e:
    print(f"迁移过程中出错: {e}")
    sys.exit(1)
finally:
    if 'connection' in locals():
        connection.close()

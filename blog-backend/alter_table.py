from app.core.database import engine
from sqlalchemy import text

def alter_table():
    with engine.connect() as conn:
        try:
            # 添加client_id列
            conn.execute(text('ALTER TABLE visitors ADD COLUMN client_id VARCHAR(50) NULL'))
            # 创建索引
            conn.execute(text('CREATE INDEX idx_client_id ON visitors (client_id)'))
            conn.commit()
            print("成功添加client_id列和索引")
        except Exception as e:
            print(f"执行SQL语句时出错: {e}")

if __name__ == "__main__":
    alter_table()

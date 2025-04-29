from app.core.database import get_db
from app.models.visitor import Visitor
from datetime import datetime, timedelta, timezone

def check_visitors():
    db = next(get_db())
    try:
        # 获取最近30分钟的访客记录
        recent_time = datetime.now() - timedelta(minutes=30)
        recent_visitors = db.query(Visitor).filter(
            Visitor.visit_time >= recent_time
        ).all()

        print(f"最近30分钟的访客记录数量: {len(recent_visitors)}")
        for visitor in recent_visitors:
            print(f"ID: {visitor.id}, IP: {visitor.ip_address}, 用户ID: {visitor.user_id}, 客户端ID: {visitor.client_id}, 时间: {visitor.visit_time}")

        # 获取最近的10条访客记录
        latest_visitors = db.query(Visitor).order_by(Visitor.visit_time.desc()).limit(10).all()

        print("\n最近的10条访客记录:")
        for visitor in latest_visitors:
            print(f"ID: {visitor.id}, IP: {visitor.ip_address}, 用户ID: {visitor.user_id}, 客户端ID: {visitor.client_id}, 时间: {visitor.visit_time}")
    finally:
        db.close()

if __name__ == "__main__":
    check_visitors()

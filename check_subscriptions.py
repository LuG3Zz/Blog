from app.core.database import get_db
from app.models.subscription import EmailSubscription
from app import models

def main():
    db = next(get_db())
    
    # 检查邮件订阅
    email_subscriptions = db.query(EmailSubscription).all()
    print(f"邮件订阅数量: {len(email_subscriptions)}")
    for sub in email_subscriptions:
        print(f"邮箱: {sub.email}, 类型: {sub.subscription_type}, 引用ID: {sub.reference_id}, 活跃: {sub.is_active}")
    
    # 检查用户订阅
    users = db.query(models.User).all()
    for user in users:
        print(f"用户 {user.username} (ID: {user.id}):")
        print(f"  订阅的分类: {[c.id for c in user.subscribed_categories]}")
        print(f"  订阅的作者: {[a.id for a in user.subscribed_authors]}")

if __name__ == "__main__":
    main()

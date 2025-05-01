from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from sqlalchemy import func, desc, extract
from datetime import datetime, timedelta, timezone, date

from app.core.database import get_db
from app.core.cache import cache
from app.models import Article, User, Comment, Category, Activity, EmailSubscription, SubscriptionType
from app.models.subscription import user_category_subscriptions, user_author_subscriptions
from app.schemas.heatmap import HeatmapResponse, HeatmapItem

router = APIRouter(prefix="/stats", tags=["statistics"])

@router.get("/overview")
@cache(ttl_seconds=300)  # 缓存5分钟
async def get_overview_stats(db: Session = Depends(get_db)):
    """
    Get overview statistics for the blog.
    """
    # Count total articles
    total_articles = db.query(func.count(Article.id)).scalar()

    # Count total users
    total_users = db.query(func.count(User.id)).scalar()

    # Count total comments
    total_comments = db.query(func.count(Comment.id)).scalar()

    # Count total categories
    total_categories = db.query(func.count(Category.id)).scalar()

    # Get total views
    total_views = db.query(func.sum(Article.view_count)).scalar() or 0

    # Get total likes
    total_likes = db.query(func.sum(Article.like_count)).scalar() or 0

    return {
        "total_articles": total_articles,
        "total_users": total_users,
        "total_comments": total_comments,
        "total_categories": total_categories,
        "total_views": total_views,
        "total_likes": total_likes
    }

@router.get("/popular-articles")
@cache(ttl_seconds=300)  # 缓存5分钟
async def get_popular_articles(
    limit: int = Query(5, ge=1, le=20),
    period: str = Query("all", regex="^(day|week|month|year|all)$"),
    db: Session = Depends(get_db)
):
    """
    Get the most popular articles based on view count.
    """
    query = db.query(
        Article.id,
        Article.title,
        Article.slug,
        Article.view_count,
        Article.like_count,
        Article.created_at,
        User.username.label("author_name")
    ).join(User, User.id == Article.author_id)

    # Apply time period filter
    if period != "all":
        now = datetime.now(timezone.utc)
        if period == "day":
            start_date = now - timedelta(days=1)
        elif period == "week":
            start_date = now - timedelta(weeks=1)
        elif period == "month":
            start_date = now - timedelta(days=30)
        elif period == "year":
            start_date = now - timedelta(days=365)

        query = query.filter(Article.created_at >= start_date)

    # Order by view count and get results
    popular_articles = query.order_by(desc(Article.view_count)).limit(limit).all()

    # Convert to list of dictionaries
    result = []
    for article in popular_articles:
        result.append({
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "view_count": article.view_count,
            "like_count": article.like_count,
            "created_at": article.created_at,
            "author_name": article.author_name
        })

    return result

@router.get("/activity-timeline")
@cache(ttl_seconds=600)  # 缓存10分钟
async def get_activity_timeline(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get activity timeline for the past specified days.
    """
    # Calculate start date
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Query for articles created per day
    articles_query = db.query(
        func.date(Article.created_at).label("date"),
        func.count(Article.id).label("count")
    ).filter(Article.created_at >= start_date)\
    .group_by(func.date(Article.created_at))

    # Query for comments created per day
    comments_query = db.query(
        func.date(Comment.created_at).label("date"),
        func.count(Comment.id).label("count")
    ).filter(Comment.created_at >= start_date)\
    .group_by(func.date(Comment.created_at))

    # Convert to dictionaries for easier processing
    articles_by_date = {str(row.date): row.count for row in articles_query.all()}
    comments_by_date = {str(row.date): row.count for row in comments_query.all()}

    # Generate a list of all dates in the range
    date_list = []
    current_date = start_date
    end_date = datetime.now(timezone.utc)

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        articles_count = articles_by_date.get(date_str, 0)
        comments_count = comments_by_date.get(date_str, 0)

        # 只有当文章数量或评论数量不为0时才添加到结果中
        if articles_count > 0 or comments_count > 0:
            date_list.append({
                "date": date_str,
                "articles": articles_count,
                "comments": comments_count
            })
        current_date += timedelta(days=1)

    return date_list

@router.get("/category-distribution")
@cache(ttl_seconds=1800)  # 缓存30分钟
async def get_category_distribution(db: Session = Depends(get_db)):
    """
    Get the distribution of articles across categories.
    """
    category_stats = db.query(
        Category.id,
        Category.name,
        func.count(Article.id).label("article_count")
    ).outerjoin(Article, Category.id == Article.category_id)\
    .group_by(Category.id, Category.name)\
    .order_by(desc("article_count"))\
    .all()

    result = []
    for stat in category_stats:
        result.append({
            "id": stat.id,
            "name": stat.name,
            "article_count": stat.article_count
        })

    return result

@router.get("/user-activity")
@cache(ttl_seconds=900)  # 缓存15分钟
async def get_user_activity(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get the most active users based on article and comment count.
    """
    # Query for users with article counts
    user_stats = db.query(
        User.id,
        User.username,
        User.avatar,
        func.count(Article.id).label("article_count")
    ).outerjoin(Article, User.id == Article.author_id)\
    .group_by(User.id, User.username, User.avatar)

    # Subquery for comment counts
    comment_counts = db.query(
        Comment.user_id,
        func.count(Comment.id).label("comment_count")
    ).filter(Comment.user_id != None)\
    .group_by(Comment.user_id)\
    .subquery()

    # Join with comment counts
    user_stats = user_stats.outerjoin(
        comment_counts,
        User.id == comment_counts.c.user_id
    ).add_columns(
        func.coalesce(comment_counts.c.comment_count, 0).label("comment_count")
    )

    # Calculate total activity and order by it
    user_stats = user_stats.add_column(
        (func.count(Article.id) + func.coalesce(comment_counts.c.comment_count, 0)).label("total_activity")
    ).order_by(desc("total_activity"))\
    .limit(limit)

    # Convert to list of dictionaries
    result = []
    for user in user_stats.all():
        result.append({
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar,
            "article_count": user.article_count,
            "comment_count": user.comment_count,
            "total_activity": user.total_activity
        })

    return result

@router.get("/activity-heatmap", response_model=HeatmapResponse)
@cache(ttl_seconds=3600)  # 缓存1小时
async def get_activity_heatmap(
    days: int = Query(365, ge=1, le=730),  # 默认显示一年的数据
    action_type: Optional[str] = Query(None, description="活动类型过滤，如 'article', 'comment', 'like' 等"),
    user_id: Optional[int] = Query(None, description="用户ID过滤"),
    db: Session = Depends(get_db)
):
    """
    获取活动热力图数据，返回格式为 [{ date: 'YYYY-MM-DD', count: N }, ...]
    用于前端渲染活动热力图。

    - **days**: 返回最近多少天的数据，默认365天
    - **action_type**: 可选的活动类型过滤，如 'article', 'comment', 'like' 等
    - **user_id**: 可选的用户ID过滤
    """
    # 计算开始日期
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    # 构建查询
    query = db.query(
        func.date(Activity.created_at).label("date"),
        func.count(Activity.id).label("count")
    ).filter(Activity.created_at >= start_date)

    # 添加可选的过滤条件
    if action_type:
        query = query.filter(Activity.action_type == action_type)

    if user_id:
        query = query.filter(Activity.user_id == user_id)

    # 执行查询
    activity_counts = query.group_by(func.date(Activity.created_at))\
    .order_by("date")\
    .all()

    # 将查询结果转换为所需格式
    heatmap_items = []

    # 创建一个字典来存储活动数据
    activity_dict = {}
    for activity_date, count in activity_counts:
        date_str = activity_date.strftime("%Y-%m-%d")
        activity_dict[date_str] = count

    # 生成日期范围内的所有日期
    current_date = datetime.now(timezone.utc).date()
    for day_offset in range(days):
        date_obj = current_date - timedelta(days=day_offset)
        date_str = date_obj.strftime("%Y-%m-%d")
        count = activity_dict.get(date_str, 0)  # 如果没有活动，设置为0
        heatmap_items.append(HeatmapItem(date=date_str, count=count))

    # 按日期排序
    heatmap_items.sort(key=lambda x: x.date)

    return {"values": heatmap_items}

@router.get("/subscriptions")
@cache(ttl_seconds=300)  # 缓存5分钟
async def get_subscription_stats(db: Session = Depends(get_db)):
    """
    获取订阅统计数据

    返回:
    - 总订阅数
    - 按类型（作者、分类、全站）统计的订阅数
    - 活跃订阅数和非活跃订阅数
    - 最近30天新增订阅数
    """
    # 计算开始日期（最近30天）
    start_date = datetime.now(timezone.utc) - timedelta(days=30)

    # 总订阅数
    total_subscriptions = db.query(func.count(EmailSubscription.id)).scalar() or 0

    # 活跃订阅数
    active_subscriptions = db.query(func.count(EmailSubscription.id))\
        .filter(EmailSubscription.is_active == True)\
        .scalar() or 0

    # 非活跃订阅数
    inactive_subscriptions = total_subscriptions - active_subscriptions

    # 按类型统计订阅数
    type_stats = db.query(
        EmailSubscription.subscription_type,
        func.count(EmailSubscription.id).label("count")
    )\
    .filter(EmailSubscription.is_active == True)\
    .group_by(EmailSubscription.subscription_type)\
    .all()

    # 转换为字典
    subscription_by_type = {
        "author": 0,
        "category": 0,
        "all": 0
    }

    for subscription_type, count in type_stats:
        subscription_by_type[subscription_type] = count

    # 最近30天新增订阅数
    recent_subscriptions = db.query(func.count(EmailSubscription.id))\
        .filter(EmailSubscription.created_at >= start_date)\
        .scalar() or 0

    # 用户订阅统计（通过关联表）
    user_category_count = db.query(func.count())\
        .select_from(user_category_subscriptions)\
        .scalar() or 0

    user_author_count = db.query(func.count())\
        .select_from(user_author_subscriptions)\
        .scalar() or 0

    # 返回统计结果
    return {
        "total_subscriptions": total_subscriptions,
        "active_subscriptions": active_subscriptions,
        "inactive_subscriptions": inactive_subscriptions,
        "subscription_by_type": subscription_by_type,
        "recent_subscriptions": recent_subscriptions,
        "user_category_subscriptions": user_category_count,
        "user_author_subscriptions": user_author_count
    }

from fastapi import APIRouter, Depends, HTTPException, status
import os
import json
import httpx
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
import re
from sqlalchemy import func, and_

from app import models
from app.core import security
from app.core.database import get_db
from app.core.config import settings
from app.core.cache import cache, clear_cache_by_prefix
from app.schemas.article import ArticleBase, ArticleCreate, ArticleUpdate, ArticleResponse, ArticleList, LikeResponse
from app.schemas.article_extended import ArticleWithContent, FeaturedArticle, HomeResponse
from app.schemas.ai_assist import AIAssistRequest, AIAssistResponse
from app.schemas.user import UserBriefResponse

# Load environment variables
load_dotenv()

# 获取 OpenRouter API 密钥
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Emoji 过滤函数
def remove_emoji(text):
    if not text:
        return ""
    # 移除 Emoji 字符
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

router = APIRouter(prefix="/articles", tags=['articles'])

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY

@router.post("/{article_id}/like", response_model=LikeResponse)
async def like_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    # 检查文章是否存在
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 检查用户是否已经点赞过
    existing_like = db.query(models.Activity).filter(
        and_(
            models.Activity.user_id == current_user.id,
            models.Activity.target_id == article_id,
            models.Activity.action_type == "like"
        )
    ).first()

    if existing_like:
        # 如果已点赞，则取消点赞
        db.delete(existing_like)
        article.like_count -= 1
        db.commit()
        db.refresh(article)
        return {
            "article_id": article_id,
            "like_count": article.like_count,
            "message": "取消点赞成功"
        }
    else:
        # 如果未点赞，则添加点赞
        article.like_count += 1
        # 获取文章作者信息
        article_author = db.query(models.User).filter(models.User.id == article.author_id).first()
        author_name = article_author.username if article_author else "未知作者"

        # 获取文章分类信息
        category = db.query(models.Category).filter(models.Category.id == article.category_id).first()
        category_name = category.name if category else "未分类"

        new_activity = models.Activity(
            action_type="like",
            user_id=current_user.id,
            target_id=article_id,
            description=f"用户 {current_user.username} 点赞了 {author_name} 的文章 《{article.title}》 [分类: {category_name}]",
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_activity)
        db.commit()
        db.refresh(article)
        return {
            "article_id": article_id,
            "like_count": article.like_count,
            "message": "点赞成功"
        }

@router.post("/ai-assist", response_model=AIAssistResponse)
async def ai_assist (
    request: AIAssistRequest,
    current_user: models.User = Depends(security.get_current_user)
):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured")

    try:
        # 使用 httpx 异步客户端
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/your-repo",
                    "X-Title": "Blog AI Assistant"
                },
                json={
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"请根据以下文章内容生成摘要（结合emoji，150字以内）和3-5个标签，用JSON格式返回:\n{request.content}"
                        }
                    ]
                }
            )
            response.raise_for_status()

            # 解析AI响应
            ai_response = response.json()
            print(ai_response)
            content = ai_response['choices'][0]['message']['content']

            # 提取JSON部分
            start = content.find('{')
            end = content.rfind('}') + 1
            json_data = json.loads(content[start:end])

            return {
                "excerpt": json_data.get("summary", ""),
                "tags": json_data.get("tags", [])
            }

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"AI service error: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"AI service returned error: {str(e)}")
    except (KeyError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {str(e)}")


def generate_slug(title: str) -> str:
    """从标题生成slug，添加时间戳确保唯一性"""
    # 转换为小写并替换空格为连字符
    slug = title.lower()
    # 移除特殊字符
    slug = re.sub(r'[^\w\s-]', '', slug)
    # 替换空格为连字符
    slug = re.sub(r'[\s]+', '-', slug)
    # 添加时间戳确保唯一性
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{slug}-{timestamp}"

@router.post("", response_model=ArticleResponse)
async def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    # 如果没有提供slug，则从标题生成
    if not article.slug:
        article.slug = generate_slug(article.title)

    # 检查slug是否已存在
    existing_article = db.query(models.Article).filter(models.Article.slug == article.slug).first()
    if existing_article:
        # 如果存在，添加数字后缀
        base_slug = article.slug
        counter = 1
        while existing_article:
            article.slug = f"{base_slug}-{counter}"
            counter += 1
            existing_article = db.query(models.Article).filter(models.Article.slug == article.slug).first()

    # 如果没有提供摘要，则从内容中提取
    if not article.excerpt and article.content:
        article.excerpt = article.content[:150] + "..." if len(article.content) > 150 else article.content

    # tags 字段已移除，使用 tags_relationship 多对多关系代替

    # 创建文章
    db_article = models.Article(
        title=article.title,
        slug=article.slug,
        content=article.content,
        excerpt=article.excerpt,
        category_id=article.category_id,  # 直接使用 category_id
        # tags 字段已移除
        cover_image=article.cover_image,
        author_id=current_user.id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # 先创建文章
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    # 处理标签关系
    if hasattr(article, 'tags') and article.tags:
        from app.models.article import article_tags

        # 处理每个标签
        for tag_name in article.tags:
            # 检查标签是否存在
            tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()

            # 如果标签不存在，创建它
            if not tag:
                tag = models.Tag(name=tag_name)
                db.add(tag)
                db.commit()  # 提交以获取标签 ID

            # 添加标签关系
            db.execute(
                article_tags.insert().values(
                    article_id=db_article.id,
                    tag_id=tag.id,
                    created_at=datetime.now(timezone.utc)
                )
            )
            db.commit()

    # 获取分类信息
    category = db.query(models.Category).filter(models.Category.id == db_article.category_id).first()
    category_name = category.name if category else "未分类"

    # 获取标签信息
    tags_info = ""
    if hasattr(article, 'tags') and article.tags:
        tags_info = f" [标签: {', '.join(article.tags)}]"

    # 生成文章预览
    content_preview = ""
    if db_article.excerpt:
        # 使用过滤函数移除 Emoji 字符
        excerpt = remove_emoji(db_article.excerpt)
        content_preview = f": \"{excerpt[:100]}...\""
    elif db_article.content:
        # 使用过滤函数移除 Emoji 字符
        content = remove_emoji(db_article.content)
        content_preview = f": \"{content[:100]}...\""

    # 记录活动
    # 使用过滤函数移除所有字段中的 Emoji 字符
    safe_username = remove_emoji(current_user.username)
    safe_title = remove_emoji(db_article.title)
    safe_category = remove_emoji(category_name)
    safe_tags = remove_emoji(tags_info)
    safe_preview = remove_emoji(content_preview)

    activity = models.Activity(
        action_type='article',
        user_id=current_user.id,
        target_id=db_article.id,
        description=f'用户 {safe_username} 创建了文章 《{safe_title}》 [分类: {safe_category}]{safe_tags}{safe_preview}',
        created_at=datetime.now(timezone.utc)
    )
    db.add(activity)
    db.commit()

    # 清除文章列表缓存
    clear_cache_by_prefix("read_articles")

    return db_article

@router.get("", response_model=List[ArticleList])
@cache(ttl_seconds=60)  # 缓存60秒
async def read_articles(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    is_featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    获取文章列表，支持分页、分类筛选、标签筛选和精选筛选。

    - **skip**: 跳过的记录数，用于分页
    - **limit**: 返回的最大记录数，用于分页
    - **category**: 按分类名称筛选
    - **tag**: 按标签名称筛选
    - **is_featured**: 是否只返回精选文章，True 表示只返回精选文章，False 表示只返回非精选文章，None 表示不筛选
    """

    # 使用join连接Category表，以便获取分类名称
    query = db.query(
        models.Article.id,
        models.Article.title,
        models.Article.slug,
        models.Article.content,
        models.Article.excerpt,
        models.Article.category_id,
        models.Article.cover_image,
        models.Article.author_id,
        models.Article.created_at,
        models.Article.updated_at,
        models.Article.view_count,
        models.Article.like_count,
        models.Article.is_featured,
        models.Category.name.label('category_name')
    ).join(models.Category, models.Article.category_id == models.Category.id, isouter=True)

    # 按分类筛选（修改为通过分类名称查询）
    if category:
        # 先获取分类ID
        category_obj = db.query(models.Category).filter(models.Category.name == category).first()
        if category_obj:
            query = query.filter(models.Article.category_id == category_obj.id)

    # 按标签筛选（使用多对多关系表）
    if tag:
        # 获取标签对象
        tag_obj = db.query(models.Tag).filter(models.Tag.name == tag).first()
        if tag_obj:
            # 使用多对多关系表进行查询
            from app.models.article import article_tags
            query = query.join(
                article_tags,
                models.Article.id == article_tags.c.article_id
            ).filter(article_tags.c.tag_id == tag_obj.id)
        else:
            # 如果标签不存在，返回空结果
            query = query.filter(models.Article.id == -1)  # 永远不会匹配的条件

    # 按是否精选筛选
    if is_featured is not None:
        query = query.filter(models.Article.is_featured == is_featured)

    # 按创建时间降序排序
    query = query.order_by(models.Article.created_at.desc())

    articles = query.offset(skip).limit(limit).all()

    # 将查询结果转换为字典列表
    result = []
    for article in articles:
        # 获取作者信息
        author_obj = db.query(models.User).filter(models.User.id == article.author_id).first()
        author = UserBriefResponse.model_validate(author_obj)

        # 获取分类信息
        category = None
        if article.category_id:
            category_obj = db.query(models.Category).filter(models.Category.id == article.category_id).first()
            if category_obj:
                category = {
                    "id": category_obj.id,
                    "name": category_obj.name
                }

        article_dict = {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "category_id": article.category_id,
            "tags_list": [],  # 将在下面填充
            "cover_image": article.cover_image,
            "author_id": article.author_id,
            "created_at": article.created_at,
            "updated_at": article.updated_at,
            "category_name": article.category_name,
            "view_count": article.view_count,
            "like_count": article.like_count,
            "is_featured": article.is_featured,
            "author": author,
            "category": category
        }

        # 获取文章的标签列表
        article_obj = db.query(models.Article).filter(models.Article.id == article.id).first()
        if article_obj and hasattr(article_obj, 'tags_relationship'):
            tags = [{
                "id": tag.id,
                "name": tag.name
            } for tag in article_obj.tags_relationship]
            article_dict["tags_list"] = tags
        result.append(article_dict)

    return result

# Move the /home route before the /{article_id} route
@router.get("/home", response_model=HomeResponse)
async def get_home_info(db: Session = Depends(get_db)):
    # 获取最新文章列表
    articles = db.query(models.Article).order_by(models.Article.created_at.desc()).limit(10).all()

    # 获取分类及其文章数量
    categories = (
        db.query(
            models.Category,
            func.count(models.Article.id).label('article_count')
        )
        .join(models.Article, models.Category.id == models.Article.category_id, isouter=True)
        .group_by(models.Category.id)
        .all()
    )

    # 获取精选/置顶文章
    featured_articles = db.query(models.Article).filter(models.Article.is_featured == True).limit(5).all()

    # 构建响应数据
    home_articles = []
    for article in articles:
        # 获取文章作者信息
        author_obj = db.query(models.User).filter(models.User.id == article.author_id).first()
        author = UserBriefResponse.model_validate(author_obj)

        # 获取文章分类信息
        category = None
        if article.category_id:
            category_obj = db.query(models.Category).filter(models.Category.id == article.category_id).first()
            if category_obj:
                category = {
                    "id": category_obj.id,
                    "name": category_obj.name
                }

        # 获取文章标签
        tags = []
        article_obj = db.query(models.Article).filter(models.Article.id == article.id).first()
        if article_obj and hasattr(article_obj, 'tags_relationship'):
            for tag in article_obj.tags_relationship:
                tags.append({"id": tag.id, "name": tag.name})

        # 获取评论数量
        comment_count = db.query(func.count(models.Comment.id)).filter(
            models.Comment.article_id == article.id
        ).scalar()

        home_articles.append({
            "id": article.id,
            "title": article.title,
            "excerpt": article.excerpt or "",  # 使用 excerpt 而不是 summary
            "cover_image": article.cover_image,
            "created_at": article.created_at,  # 使用 created_at 而不是 publishDate
            "author": author,
            "category": category,
            "tags": tags,
            "view_count": article.view_count or 0,
            "like_count": article.like_count or 0,
            "comment_count": comment_count or 0
        })

    # 构建分类列表
    category_list = [
        {
            "id": cat[0].id,
            "name": cat[0].name,
            "articleCount": cat[1]
        }
        for cat in categories
    ]

    # 构建精选文章列表
    featured_list = [
        {
            "id": art.id,
            "title": art.title,
            "coverImage": art.cover_image
        }
        for art in featured_articles
    ]

    return {
        "articles": home_articles,
        "categories": category_list,
        "featuredArticles": featured_list
    }

@router.get("/{article_id}", response_model=ArticleWithContent)
async def read_article(article_id: int, db: Session = Depends(get_db)):
    # 使用join连接Category表，以便获取分类名称
    article = db.query(
        models.Article.id,
        models.Article.title,
        models.Article.slug,
        models.Article.content,
        models.Article.excerpt,
        models.Article.category_id,
        models.Article.cover_image,
        models.Article.author_id,
        models.Article.created_at,
        models.Article.updated_at,
        models.Article.view_count,
        models.Article.like_count,
        models.Article.is_featured,
        models.Category.name.label('category_name')
    ).join(
        models.Category, models.Article.category_id == models.Category.id, isouter=True
    ).filter(models.Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 将查询结果转换为字典
    result = {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "content": article.content,
        "excerpt": article.excerpt,
        "category_id": article.category_id,
        "tags_list": [],  # 将在下面填充
        "cover_image": article.cover_image,
        "author_id": article.author_id,
        "created_at": article.created_at,
        "updated_at": article.updated_at,
        "category_name": article.category_name,
        "view_count": article.view_count,
        "like_count": article.like_count,
        "is_featured": article.is_featured
    }

    # 获取文章的标签列表
    article_obj = db.query(models.Article).filter(models.Article.id == article.id).first()
    if article_obj and hasattr(article_obj, 'tags_relationship'):
        tags = [{
            "id": tag.id,
            "name": tag.name
        } for tag in article_obj.tags_relationship]
        result["tags_list"] = tags

    return result

@router.get("/by-slug/{slug}", response_model=ArticleWithContent)
async def read_article_by_slug(slug: str, db: Session = Depends(get_db)):
    # 使用join连接Category表，以便获取分类名称
    article = db.query(
        models.Article.id,
        models.Article.title,
        models.Article.slug,
        models.Article.content,
        models.Article.excerpt,
        models.Article.category_id,
        models.Article.cover_image,
        models.Article.author_id,
        models.Article.created_at,
        models.Article.updated_at,
        models.Article.view_count,
        models.Article.like_count,
        models.Article.is_featured,
        models.Category.name.label('category_name')
    ).join(
        models.Category, models.Article.category_id == models.Category.id, isouter=True
    ).filter(models.Article.slug == slug).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 将查询结果转换为字典
    result = {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "content": article.content,
        "excerpt": article.excerpt,
        "category_id": article.category_id,
        "tags_list": [],  # 将在下面填充
        "cover_image": article.cover_image,
        "author_id": article.author_id,
        "created_at": article.created_at,
        "updated_at": article.updated_at,
        "category_name": article.category_name,
        "view_count": article.view_count,
        "like_count": article.like_count,
        "is_featured": article.is_featured
    }

    # 获取文章的标签列表
    article_obj = db.query(models.Article).filter(models.Article.id == article.id).first()
    if article_obj and hasattr(article_obj, 'tags_relationship'):
        tags = [{
            "id": tag.id,
            "name": tag.name
        } for tag in article_obj.tags_relationship]
        result["tags_list"] = tags

    return result

@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """更新文章

    需要身份验证，只有以下用户可以更新文章：
    - 文章作者
    - 编辑角色用户
    - 管理员角色用户
    """
    # 使用权限检查函数验证用户权限
    from app.core.permissions import check_article_permission
    db_article = check_article_permission(db, article_id, current_user, "update")

    # 更新提供的字段
    if article.title is not None:
        db_article.title = article.title
        # 如果更新了标题且没有提供新的slug，则重新生成slug
        if not hasattr(article, 'slug') or article.slug is None:
            # 直接使用generate_slug函数生成唯一slug（已包含时间戳）
            new_slug = generate_slug(article.title)
            db_article.slug = new_slug

    if hasattr(article, 'slug') and article.slug is not None:
        # 检查新slug是否已被其他文章使用
        existing = db.query(models.Article).filter(
            models.Article.slug == article.slug,
            models.Article.id != article_id
        ).first()
        if existing:
            # 如果存在，添加时间戳确保唯一性
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            article.slug = f"{article.slug}-{timestamp}"
        db_article.slug = article.slug

    if article.content is not None:
        db_article.content = article.content
        # 如果更新了内容且没有提供新的摘要，则重新生成摘要
        if article.excerpt is None:
            db_article.excerpt = article.content[:150] + "..." if len(article.content) > 150 else article.content

    if article.excerpt is not None:
        db_article.excerpt = article.excerpt

    if article.category_id is not None:
        db_article.category_id = article.category_id

    if hasattr(article, 'tags') and article.tags is not None:
        # tags 字段已移除，使用 tags_relationship 多对多关系代替

        # 更新标签关系
        if article.tags:
            # 手动删除现有的标签关系
            from app.models.article import article_tags
            db.execute(
                article_tags.delete().where(article_tags.c.article_id == article_id)
            )
            db.commit()

            # 获取所有需要的标签对象
            for tag_name in article.tags:
                # 检查标签是否存在
                tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()

                # 如果标签不存在，创建它
                if not tag:
                    tag = models.Tag(name=tag_name)
                    db.add(tag)
                    db.commit()  # 提交以获取标签 ID

                # 添加新的标签关系
                db.execute(
                    article_tags.insert().values(
                        article_id=article_id,
                        tag_id=tag.id,
                        created_at=datetime.now(timezone.utc)
                    )
                )

    if article.cover_image is not None:
        db_article.cover_image = article.cover_image

    if article.is_featured is not None:
        db_article.is_featured = article.is_featured

    # 更新修改时间
    db_article.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_article)

    # 获取分类信息
    category = db.query(models.Category).filter(models.Category.id == db_article.category_id).first()
    category_name = category.name if category else "未分类"

    # 获取标签信息
    tags = [tag.name for tag in db_article.tags_relationship] if hasattr(db_article, 'tags_relationship') else []
    tags_info = f" [标签: {', '.join(tags)}]" if tags else ""

    # 生成文章预览
    content_preview = ""
    if db_article.excerpt:
        content_preview = f": \"{db_article.excerpt[:100]}...\""
    elif db_article.content:
        content_preview = f": \"{db_article.content[:100]}...\""

    # 记录活动
    activity = models.Activity(
        action_type='article_update',
        user_id=current_user.id,
        target_id=db_article.id,
        description=f'用户 {current_user.username} 更新了文章 《{db_article.title}》 [分类: {category_name}]{tags_info}{content_preview}',
        created_at=datetime.now(timezone.utc)
    )
    db.add(activity)
    db.commit()

    # 获取作者信息，包括处理 social_media 字段
    author = db.query(models.User).filter(models.User.id == db_article.author_id).first()
    if author and author.social_media:
        try:
            import json
            author.social_media = json.loads(author.social_media)
        except json.JSONDecodeError:
            author.social_media = None

    # 将作者信息附加到文章对象
    setattr(db_article, 'author', author)

    return db_article

@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """删除文章

    需要身份验证，只有以下用户可以删除文章：
    - 文章作者
    - 管理员角色用户
    """
    # 使用权限检查函数验证用户权限
    from app.core.permissions import check_article_permission
    db_article = check_article_permission(db, article_id, current_user, "delete")

    db.delete(db_article)
    db.commit()
    return {"message": "Article deleted successfully"}


@router.get("/{article_id}/like-status")
async def get_like_status(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    like_exists = db.query(models.Activity).filter(
        models.Activity.user_id == current_user.id,
        models.Activity.target_id == article_id,
        models.Activity.action_type == "like"
    ).first() is not None

    return {"is_liked": like_exists}
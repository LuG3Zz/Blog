from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base

# 文章-标签多对多关系表
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc))
)

class Category(Base):
    """Category model for article categorization."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(200), nullable=True)

    # Relationships
    articles = relationship("Article", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"

class Tag(Base):
    """Tag model for article tagging."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(200), nullable=True)

    # 与文章的多对多关系
    articles = relationship("Article", secondary=article_tags, back_populates="tags_relationship")

    def __repr__(self):
        return f"<Tag {self.name}>"

class Article(Base):
    """Article model representing blog posts."""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255, collation='utf8mb4_unicode_ci'), nullable=False, info={'mysql_charset': 'utf8mb4'})
    slug = Column(String(255), unique=True, index=True)
    content = Column(Text(collation='utf8mb4_unicode_ci'), info={'mysql_charset': 'utf8mb4'})
    excerpt = Column(Text(collation='utf8mb4_unicode_ci'), nullable=True, info={'mysql_charset': 'utf8mb4'})
    cover_image = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    # tags 字段已移除，使用 tags_relationship 多对多关系代替
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)

    # Relationships
    author = relationship("User", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    comments = relationship("Comment", back_populates="article")
    tags_relationship = relationship("Tag", secondary=article_tags, back_populates="articles")

    def __repr__(self):
        return f"<Article {self.title}>"

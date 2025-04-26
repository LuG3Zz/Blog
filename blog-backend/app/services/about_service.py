"""
About页面服务
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.about import AboutPage

class AboutPageService:
    """About页面服务类"""

    @staticmethod
    def get_about_page(db: Session) -> Optional[AboutPage]:
        """
        获取About页面内容
        
        Args:
            db: 数据库会话
            
        Returns:
            AboutPage对象，如果不存在则返回None
        """
        return db.query(AboutPage).first()

    @staticmethod
    def create_about_page(db: Session, content: Dict[str, Any]) -> AboutPage:
        """
        创建About页面内容
        
        Args:
            db: 数据库会话
            content: 页面内容
            
        Returns:
            创建的AboutPage对象
        """
        # 检查是否已存在
        existing = AboutPageService.get_about_page(db)
        if existing:
            return AboutPageService.update_about_page(db, existing.id, content)
        
        # 创建新记录
        about_page = AboutPage(content=content)
        db.add(about_page)
        db.commit()
        db.refresh(about_page)
        return about_page

    @staticmethod
    def update_about_page(db: Session, about_id: int, content: Dict[str, Any]) -> Optional[AboutPage]:
        """
        更新About页面内容
        
        Args:
            db: 数据库会话
            about_id: About页面ID
            content: 更新的内容
            
        Returns:
            更新后的AboutPage对象，如果不存在则返回None
        """
        about_page = db.query(AboutPage).filter(AboutPage.id == about_id).first()
        if not about_page:
            return None
        
        about_page.content = content
        db.commit()
        db.refresh(about_page)
        return about_page

    @staticmethod
    def delete_about_page(db: Session, about_id: int) -> bool:
        """
        删除About页面
        
        Args:
            db: 数据库会话
            about_id: About页面ID
            
        Returns:
            是否删除成功
        """
        about_page = db.query(AboutPage).filter(AboutPage.id == about_id).first()
        if not about_page:
            return False
        
        db.delete(about_page)
        db.commit()
        return True

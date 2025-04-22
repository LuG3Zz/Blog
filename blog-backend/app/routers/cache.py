from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List

from app.core import security
from app.services.unified_cache_service import UnifiedCacheService
from app.core.config import settings

router = APIRouter(
    prefix="/cache",
    tags=["cache"],
    dependencies=[Depends(security.get_current_admin_user)]  # 只有管理员可以访问
)

@router.get("/stats", response_model=Dict[str, Any])
async def get_cache_stats():
    """获取缓存统计信息"""
    return UnifiedCacheService.get_stats()

@router.get("/keys", response_model=List[str])
async def get_cache_keys(pattern: str = "*"):
    """获取缓存键列表"""
    return UnifiedCacheService.get_keys(pattern)

@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cache():
    """清除所有缓存"""
    UnifiedCacheService.clear()
    return {"message": "Cache cleared"}

@router.delete("/keys/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cache_key(key: str):
    """删除指定的缓存键"""
    UnifiedCacheService.delete(key)
    return {"message": f"Key {key} deleted"}

@router.get("/info", response_model=Dict[str, Any])
async def get_cache_info():
    """获取缓存配置信息"""
    return {
        "type": "redis" if settings.USE_REDIS_CACHE else "memory",
        "redis_host": settings.REDIS_HOST if settings.USE_REDIS_CACHE else None,
        "redis_port": settings.REDIS_PORT if settings.USE_REDIS_CACHE else None,
    }

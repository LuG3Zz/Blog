import re
import os
import json
import httpx
from typing import Dict, List, Tuple, Optional
from fastapi import HTTPException, status
from app.utils.logging import get_logger

logger = get_logger(__name__)

class ContentFilterService:
    """Service for filtering and moderating content."""
    
    # 默认敏感词列表
    _default_sensitive_words = [
        "广告", "推广", "优惠", "折扣", "促销", "代理", "微信", "电话", "联系方式",
        "赌博", "博彩", "菠菜", "威尼斯", "澳门", "赌场", "彩票", "时时彩",
        "色情", "做爱", "约炮", "一夜情", "嫖娼", "妓女", "援交",
        "毒品", "大麻", "冰毒", "摇头丸", "海洛因", "可卡因",
        "诈骗", "骗子", "传销", "资金盘", "非法集资",
        "反动", "政治", "敏感", "共产党", "民主", "自由", "独立", "抗议", "示威"
    ]
    
    # 敏感词列表
    _sensitive_words = []
    
    @classmethod
    def load_sensitive_words(cls, file_path: Optional[str] = None):
        """Load sensitive words from file or use default list."""
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    cls._sensitive_words = json.load(f)
                logger.info(f"Loaded {len(cls._sensitive_words)} sensitive words from {file_path}")
            except Exception as e:
                logger.error(f"Failed to load sensitive words from {file_path}: {e}")
                cls._sensitive_words = cls._default_sensitive_words
        else:
            cls._sensitive_words = cls._default_sensitive_words
            logger.info(f"Using default sensitive words list with {len(cls._sensitive_words)} words")
    
    @classmethod
    def contains_sensitive_words(cls, content: str) -> Tuple[bool, List[str]]:
        """
        Check if content contains sensitive words.
        
        Returns:
            Tuple containing:
                - Boolean indicating if sensitive words were found
                - List of found sensitive words
        """
        if not cls._sensitive_words:
            cls.load_sensitive_words()
        
        found_words = []
        for word in cls._sensitive_words:
            if word in content:
                found_words.append(word)
        
        return len(found_words) > 0, found_words
    
    @classmethod
    async def moderate_with_ai(cls, content: str, api_key: str) -> Tuple[bool, str]:
        """
        Moderate content using AI API.
        
        Returns:
            Tuple containing:
                - Boolean indicating if content is approved
                - Reason for rejection if not approved
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "deepseek/deepseek-chat-v3-0324:free",
                        "messages": [{
                            "role": "user",
                            "content": "请严格审核以下评论内容，直接返回JSON格式不要markdown {approved:布尔值, reason:字符串}\n"
                                      "审核要求：\n1. 包含敏感词/广告/违法内容返回false\n"
                                      "2. 内容友善且符合社区规范返回true\n"
                                      f"评论内容：{content}"
                        }]
                    },
                    timeout=10.0  # 设置超时时间
                )
                
                response.raise_for_status()
                result = response.json()
                
                # 解析AI响应
                ai_content = result['choices'][0]['message']['content'].strip()
                
                # 移除可能存在的Markdown标记
                if ai_content.startswith('```json'):
                    ai_content = ai_content[7:]
                if ai_content.endswith('```'):
                    ai_content = ai_content[:-3]
                ai_content = ai_content.strip()
                
                # 解析JSON
                try:
                    ai_response = json.loads(ai_content)
                    is_approved = ai_response.get('approved', False)
                    reason = ai_response.get('reason', '内容不符合社区规范')
                    return is_approved, reason
                except json.JSONDecodeError:
                    logger.error(f"AI响应JSON解析失败: {ai_content}")
                    return False, "AI审核解析失败"
                
        except httpx.TimeoutException:
            logger.error("AI审核API调用超时")
            return False, "AI审核超时"
        except Exception as e:
            logger.error(f"AI审核API调用失败: {e}")
            return False, f"AI审核失败: {str(e)}"
    
    @classmethod
    async def moderate_content(cls, content: str, api_key: Optional[str] = None) -> Tuple[bool, str]:
        """
        Moderate content using local filter and optionally AI API.
        
        Returns:
            Tuple containing:
                - Boolean indicating if content is approved
                - Reason for rejection if not approved
        """
        # 首先进行本地敏感词过滤
        has_sensitive_words, found_words = cls.contains_sensitive_words(content)
        
        if has_sensitive_words:
            return False, f"内容包含敏感词: {', '.join(found_words)}"
        
        # 如果提供了API密钥，则进行AI审核
        if api_key:
            return await cls.moderate_with_ai(content, api_key)
        
        # 如果没有API密钥，则只依赖本地过滤
        return True, ""

import os
import random
import string
import logging
from typing import Dict, Optional, Tuple
import httpx
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from app.core.config import settings
from app.services.unified_cache_service import UnifiedCacheService
from app.services.site_settings_service import SiteSettingsService

# 配置日志
logger = logging.getLogger(__name__)

# 验证码缓存前缀
EMAIL_VERIFICATION_CODE_PREFIX = "email_verification_code:"
# 验证码有效期（分钟）
VERIFICATION_CODE_EXPIRY_MINUTES = 10

class EmailService:
    """邮件服务，用于发送各类邮件"""

    @staticmethod
    async def send_email(
        to_email: str,
        subject: str,
        html_content: str,
        from_name: str = None,
        from_email: str = None,
        db = None
    ) -> Dict:
        """
        使用Resend API发送邮件

        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            html_content: 邮件HTML内容
            from_name: 发件人名称，默认使用网站名称
            from_email: 发件人邮箱，默认使用配置的邮箱
            db: 数据库会话，用于获取系统设置

        Returns:
            Dict: 包含发送结果的字典
        """
        # 获取API密钥
        api_key = None

        # 如果提供了数据库会话，尝试从系统设置中获取API密钥
        if db:
            site_settings = SiteSettingsService.get_settings(db)
            if site_settings and site_settings.email_enabled and site_settings.email_api_key:
                api_key = site_settings.email_api_key
                logger.info("使用系统设置中的Resend API密钥")

        # 如果系统设置中没有API密钥，尝试从环境变量中获取
        if not api_key:
            api_key = os.getenv("RESEND_API_KEY", settings.RESEND_API_KEY)
            logger.info("使用环境变量中的Resend API密钥")

        if not api_key:
            logger.error("未配置Resend API密钥")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="邮件服务未正确配置"
            )

        # 设置默认发件人
        if not from_name:
            from_name = settings.SITE_NAME
        if not from_email:
            from_email = settings.EMAIL_FROM

        # 构建发件人
        from_address = f"{from_name} <{from_email}>"

        # 构建请求数据
        email_data = {
            "from": from_address,
            "to": [to_email],
            "subject": subject,
            "html": html_content
        }

        try:
            # 发送请求
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json=email_data
                )

                # 检查响应
                response_data = response.json()
                if response.status_code != 200:
                    logger.error(f"发送邮件失败: {response_data}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"发送邮件失败: {response_data.get('message', '未知错误')}"
                    )

                logger.info(f"邮件发送成功: {response_data}")
                return response_data

        except Exception as e:
            logger.exception(f"发送邮件时发生异常: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"发送邮件失败: {str(e)}"
            )

    @staticmethod
    def generate_verification_code(length: int = 6) -> str:
        """
        生成数字验证码

        Args:
            length: 验证码长度，默认6位

        Returns:
            str: 生成的验证码
        """
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    async def send_verification_email(email: str, db = None) -> str:
        """
        发送验证码邮件

        Args:
            email: 收件人邮箱
            db: 数据库会话，用于获取系统设置

        Returns:
            str: 生成的验证码
        """
        # 生成验证码
        code = EmailService.generate_verification_code()

        # 构建邮件内容
        subject = f"【{settings.SITE_NAME}】您的注册验证码"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
            <h2 style="color: #333; text-align: center;">验证您的邮箱</h2>
            <p>您好，</p>
            <p>感谢您注册{settings.SITE_NAME}。请使用以下验证码完成注册：</p>
            <div style="background-color: #f5f5f5; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; margin: 20px 0;">
                {code}
            </div>
            <p>此验证码将在 {VERIFICATION_CODE_EXPIRY_MINUTES} 分钟后失效。</p>
            <p>如果您没有请求此验证码，请忽略此邮件。</p>
            <p style="margin-top: 30px; font-size: 12px; color: #999; text-align: center;">
                此邮件由系统自动发送，请勿回复。
            </p>
        </div>
        """

        # 发送邮件
        await EmailService.send_email(
            to_email=email,
            subject=subject,
            html_content=html_content,
            db=db
        )

        # 将验证码存入缓存
        cache_key = f"{EMAIL_VERIFICATION_CODE_PREFIX}{email}"
        UnifiedCacheService.set(
            cache_key,
            code,
            VERIFICATION_CODE_EXPIRY_MINUTES * 60
        )

        logger.info(f"已向 {email} 发送验证码: {code}")
        return code

    @staticmethod
    def verify_code(email: str, code: str) -> bool:
        """
        验证邮箱验证码

        Args:
            email: 邮箱
            code: 用户提供的验证码

        Returns:
            bool: 验证是否成功
        """
        # 从缓存获取验证码
        cache_key = f"{EMAIL_VERIFICATION_CODE_PREFIX}{email}"
        stored_code = UnifiedCacheService.get(cache_key)

        if not stored_code:
            logger.warning(f"验证码不存在或已过期: {email}")
            return False

        # 确保验证码是字符串类型
        stored_code_str = str(stored_code).strip()
        code_str = str(code).strip()

        # 验证码比对
        is_valid = stored_code_str == code_str

        # 如果验证成功，删除缓存中的验证码
        if is_valid:
            UnifiedCacheService.delete(cache_key)
            logger.info(f"验证码验证成功: {email}")
        else:
            logger.warning(f"验证码不匹配: {email}, 提供: {code_str}, 存储: {stored_code_str}, 类型: {type(code)}/{type(stored_code)}")

        return is_valid

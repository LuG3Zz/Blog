from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.services.email_service import EmailService
from app.services.site_settings_service import SiteSettingsService
from app.schemas.user import EmailVerification, VerifyEmailCode
from app.models.user import User

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["email"])

@router.post("/send-verification", summary="发送邮箱验证码")
async def send_verification_code(
    email_data: EmailVerification,
    db: Session = Depends(get_db)
):
    """
    发送邮箱验证码
    
    - **email**: 邮箱地址
    
    返回发送结果
    """
    # 检查系统设置是否启用了邮箱验证
    settings = SiteSettingsService.get_settings(db)
    if not settings or not settings.require_email_verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="系统未启用邮箱验证功能"
        )
    
    # 检查邮箱是否已被注册
    existing_user = db.query(User).filter(User.email == email_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    try:
        # 发送验证码
        await EmailService.send_verification_email(email_data.email)
        return {"message": "验证码已发送，请查收邮件"}
    except Exception as e:
        logger.exception(f"发送验证码失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送验证码失败: {str(e)}"
        )

@router.post("/verify-code", summary="验证邮箱验证码")
def verify_email_code(
    verification_data: VerifyEmailCode,
    db: Session = Depends(get_db)
):
    """
    验证邮箱验证码
    
    - **email**: 邮箱地址
    - **code**: 验证码
    
    返回验证结果
    """
    # 检查系统设置是否启用了邮箱验证
    settings = SiteSettingsService.get_settings(db)
    if not settings or not settings.require_email_verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="系统未启用邮箱验证功能"
        )
    
    # 验证验证码
    is_valid = EmailService.verify_code(
        verification_data.email,
        verification_data.code
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码无效或已过期"
        )
    
    return {"message": "验证码验证成功"}

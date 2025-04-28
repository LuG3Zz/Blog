"""
密码处理工具模块，用于密码哈希和验证。
将这些功能从security.py中分离出来，避免循环导入问题。
"""
from passlib.context import CryptContext

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配哈希值。"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希值。"""
    return pwd_context.hash(password)

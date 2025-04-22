import os
import sys
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 获取当前环境模式
def get_environment():
    # 默认为开发环境
    env = os.getenv("ENVIRONMENT", "development")
    # 从命令行参数中获取环境变量
    for arg in sys.argv:
        if arg.startswith("--env="):
            env = arg.split("=")[1]
            break
    return env

# 当前环境
ENVIRONMENT = get_environment()

# 加载对应环境的配置文件
env_file = f".env.{ENVIRONMENT}"
if os.path.exists(env_file):
    print(f"加载环境配置: {env_file}")
    load_dotenv(env_file)
else:
    print(f"未找到环境配置文件 {env_file}，尝试加载默认的 .env 文件")
    # 如果没有找到环境特定的配置文件，则加载默认的 .env 文件
    load_dotenv()

class Settings(BaseSettings):
    """Application settings"""

    # 环境设置
    ENVIRONMENT: str = ENVIRONMENT
    IS_DEVELOPMENT: bool = ENVIRONMENT == "development"
    IS_PRODUCTION: bool = ENVIRONMENT == "production"

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Blog API"
    PROJECT_DESCRIPTION: str = "博客系统API接口文档，包含用户、文章和评论管理"
    PROJECT_VERSION: str = "1.0.0"

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://user:pass@localhost:3306/dbname?charset=utf8mb4")

    # External API settings
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    # File storage settings
    STATIC_FILES_DIR: str = "static"
    IMAGES_DIR: str = "static/images"
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

    # Cache settings
    VIEW_COUNT_CACHE_SECONDS: int = 300  # 5 minutes

    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_USERNAME: Optional[str] = os.getenv("REDIS_USERNAME")
    REDIS_USE_SSL: bool = os.getenv("REDIS_USE_SSL", "False").lower() == "true"
    USE_REDIS_CACHE: bool = os.getenv("USE_REDIS_CACHE", "True").lower() == "true"

    model_config = {
        "case_sensitive": True
    }

# Create global settings object
settings = Settings()

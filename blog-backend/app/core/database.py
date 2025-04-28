from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # Enable connection pool ping
    pool_recycle=600,        # Recycle connections every 10 minutes
    pool_size=20,            # Increase connection pool size
    max_overflow=30,         # Increase max additional connections
    pool_timeout=10,         # Connection timeout in seconds
    connect_args={'charset': 'utf8mb4'},  # Support for Emoji characters
    echo=settings.SQL_ECHO,  # Log SQL queries in development mode
    echo_pool=settings.SQL_ECHO_POOL  # Log connection pool events in development mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

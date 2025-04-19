from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

sync_engine = create_engine(settings.DATABASE_URL.replace('+asyncpg', ''), echo=True)
SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)

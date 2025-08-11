from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

logger = logging.getLogger(__name__)

# PostgreSQL veritabanı bağlantısı - .env dosyasından al
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

try:
    engine = create_engine(
        DATABASE_URL,
        echo=False  # SQL loglarını kapat
    )
    logger.info(f"PostgreSQL database engine created successfully for: {DATABASE_URL}")
except Exception as e:
    logger.error(f"Error creating PostgreSQL database engine: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
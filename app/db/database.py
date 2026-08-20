from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from app.core.config import settings

DATA_URL = settings.DATABASE_URL

engine = create_engine(DATA_URL)

Base = declarative_base()

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
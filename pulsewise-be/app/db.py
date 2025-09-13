from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://pulsewise:pulsewise@db:5432/pulsewise")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

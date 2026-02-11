from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.model import Base

DB_URL = "sqlite:///./db/database.db"

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

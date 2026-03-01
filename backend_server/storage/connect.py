import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.model import Base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "database.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


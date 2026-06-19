import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Use Supabase PostgreSQL URL from .env file
# For local testing without Supabase, SQLite is used automatically
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./pharmacy_local.db"
    print("NOTE: Using local SQLite for testing. Set DATABASE_URL in .env for Supabase.")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Give each API request its own database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

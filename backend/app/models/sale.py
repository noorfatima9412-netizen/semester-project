from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database.database import Base

class Sale(Base):
    __tablename__ = "sales"

  
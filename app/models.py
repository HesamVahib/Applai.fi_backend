from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, func #, Text (for long texts like description)
from app.database import Base

class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String, index=True)
    company = Column(String)
    link = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    fi_lang = Column(String)
    en_lang = Column(String)

## unique constraints
    __table_args__ = (
        UniqueConstraint('link'),
    )

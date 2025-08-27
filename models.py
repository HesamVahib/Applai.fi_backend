from sqlalchemy import Column, Integer, String #, Text (for long texts like description)
from database import Base

class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String, index=True)
    company = Column(String)
    created_at = Column(String)
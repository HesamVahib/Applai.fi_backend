from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class JobCreate(BaseModel):
    title: str
    location: Optional[str] = None
    category: Optional[str] = None
    company: Optional[str] = None
    link: str
    fi_lang: Optional[str] = None
    en_lang: Optional[str] = None

class JobResponse(JobCreate):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PaginationJobsResponse(BaseModel):
    total_jobs: int
    jobs: List[JobResponse]
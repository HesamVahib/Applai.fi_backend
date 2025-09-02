from pydantic import BaseModel
from typing import List


class JobCreate(BaseModel):
    title: str
    location: str
    company: str = None
    link: str
    fi_lang: str = None
    en_lang: str = None

class JobResponse(JobCreate):
    id: int

    class Config:
        orm_mode = True

class PaginationJobsResponse(BaseModel):
    total_jobs: int
    jobs: List[JobResponse]
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

## Job Schemas

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

## User Schemas

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PaginationUsersResponse(BaseModel):
    total_users: int
    users: List[UserResponse]

class UserEdit(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

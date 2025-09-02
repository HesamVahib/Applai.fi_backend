from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Jobs
from app.database import get_db
from app.schemas.schemas import JobCreate, JobResponse, PaginationJobsResponse
from app.api_key import get_api_key

router = APIRouter(prefix="/jobs", tags=["jobs"])


# get all jobs
@router.get("/", response_model=PaginationJobsResponse, status_code=status.HTTP_200_OK)
async def get_jobs(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    ):

    total_number = await db.execute(select(func.count()).select_from(Jobs))
    total_jobs = total_number.scalar()

    result = await db.execute(select(Jobs).offset(skip).limit(limit))
    jobs = result.scalars().all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found")
    return {"total_jobs": total_jobs, "jobs": jobs}


# get job by id
@router.get("/{job_id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
async def get_job_id(job_id: int, db: AsyncSession = Depends(get_db)) -> JobResponse:
    result = await db.execute(select(Jobs).where(Jobs.id == job_id))
    job = result.scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job by id {job_id} not found")
    return job


# create job
@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_api_key)])
async def create_job(job: JobCreate, db: AsyncSession = Depends(get_db)) -> JobResponse:

    new_job = Jobs(
        title=job.title,
        location=job.location,
        company=job.company,
        link=job.link,
        fi_lang=job.fi_lang,
        en_lang=job.en_lang,
    )

    try:
        db.add(new_job)
        await db.commit()
        await db.refresh(new_job)
        return new_job
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# delete job
@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
async def delete_job(job_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Jobs).where(Jobs.id == job_id))
    job = result.scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job by id {job_id} not found")
    await db.delete(job)
    await db.commit()
from fastapi import APIRouter, HTTPException, status
from app.storage import load_data, save_data
from app.schemas import JobCreate, JobOut, JobUpdate
import uuid

# A prefix lets you add a string before all the routes created in this module
router = APIRouter(prefix="/app/jobs", tags=["jobs"])

@router.get("/", response_model=list[JobOut])
def get_jobs():
    jobs = load_data()
    return jobs

@router.post("/", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate):
    jobs = load_data()
    new_job = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "type": payload.type,
        "description": payload.description,
        "location": payload.location,
        "salary": payload.salary,
        "company": payload.company.model_dump(),
    }
    jobs.append(new_job)
    save_data(jobs)
    return new_job

@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: str):
    jobs = load_data()
    for job in jobs:
        if job["id"] == job_id:
            return job
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

@router.put("/{job_id}", response_model=JobOut)
def update_job(job_id: str, payload: JobUpdate):
    jobs = load_data()
    for job in jobs:
        if job["id"] == job_id:
            if payload.title is not None:
                job["title"] = payload.title
            if payload.type is not None:
                job["type"] = payload.type
            if payload.description is not None:
                job["description"] = payload.description
            if payload.location is not None:
                job["location"] = payload.location
            if payload.salary is not None:
                job["salary"] = payload.salary
            if payload.company is not None:
                job["company"] = payload.company.model_dump()
            save_data(jobs)
            return job
    # if no job is found for update, raise this exception
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Job not found"
    )

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: str):
    """Delete a job by ID."""
    jobs = load_data()

    for i, job in enumerate(jobs):
        if job["id"] == job_id:
            jobs.pop(i)
            save_data(jobs)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Job not found"
    )

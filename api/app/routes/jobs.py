from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import Company, JobCreate, JobOut, JobUpdate

# A prefix lets you add a string before all the routes created in this module
router = APIRouter(prefix="/app/jobs", tags=["jobs"])


def get_or_create_company(db: Session, company_data: Company) -> models.Company:
    company = db.query(models.Company).filter_by(name=company_data.name).first()
    if company is None:
        company = models.Company(
            name=company_data.name,
            description=company_data.description,
            contactEmail=company_data.contactEmail,
            contactPhone=company_data.contactPhone,
        )
        db.add(company)
        db.flush()
    return company


@router.get("/", response_model=list[JobOut])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()


@router.post("/", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    company = get_or_create_company(db, payload.company)
    new_job = models.Job(
        title=payload.title,
        type=payload.type,
        description=payload.description,
        location=payload.location,
        salary=payload.salary,
        company_id=company.id,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobOut)
def update_job(job_id: int, payload: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    if payload.title is not None:
        job.title = payload.title
    if payload.type is not None:
        job.type = payload.type
    if payload.description is not None:
        job.description = payload.description
    if payload.location is not None:
        job.location = payload.location
    if payload.salary is not None:
        job.salary = payload.salary
    if payload.company is not None:
        job.company_id = get_or_create_company(db, payload.company).id

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(job)
    db.commit()

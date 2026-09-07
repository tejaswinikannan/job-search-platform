import json
from pathlib import Path

from app.database import SessionLocal
from app import models

db = SessionLocal()

data = json.loads(Path("data/jobs.json").read_text())

for job in data["jobs"]:
    company_data = job["company"]

    company = db.query(models.Company).filter_by(name=company_data["name"]).first()
    if company is None:
        company = models.Company(
            name=company_data["name"],
            description=company_data["description"],
            contactEmail=company_data["contactEmail"],
            contactPhone=company_data["contactPhone"],
        )
        db.add(company)
        db.flush()  # sends the INSERT so company.id gets populated, without ending the transaction

    new_job = models.Job(
        title=job["title"],
        type=job["type"],
        description=job["description"],
        location=job["location"],
        salary=job["salary"],
        company_id=company.id,
    )
    db.add(new_job)

db.commit()
db.close()

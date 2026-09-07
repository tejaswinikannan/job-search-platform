from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    contactEmail = Column("contact_email", String, nullable=False)
    contactPhone = Column("contact_phone", String, nullable=False)

    jobs = relationship("Job", back_populates="company")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    salary = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    company = relationship("Company", back_populates="jobs")

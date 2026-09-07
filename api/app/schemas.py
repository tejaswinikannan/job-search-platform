from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class JobType(str, Enum):
    full_time = "Full-Time"
    part_time = "Part-Time"
    remote = "Remote"
    internship = "Internship"


class Company(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    contactEmail: EmailStr
    contactPhone: str


class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    type: JobType
    description: str = Field(min_length=5, max_length=2000)
    location: str = Field(min_length=1, max_length=100)
    salary: str
    company: Company


class JobUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=100)
    type: Optional[JobType] = None
    description: Optional[str] = Field(default=None, max_length=2000)
    location: Optional[str] = Field(default=None, max_length=100)
    salary: Optional[str] = None
    company: Optional[Company] = None


class JobOut(BaseModel):
    id: str
    title: str
    type: JobType
    description: str
    location: str
    salary: str
    company: Company

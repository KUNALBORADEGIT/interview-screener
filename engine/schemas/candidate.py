# engine/schemas/candidate.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    resume_url: Optional[str] = None


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    resume_url: Optional[str] = None


class CandidateResponse(CandidateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

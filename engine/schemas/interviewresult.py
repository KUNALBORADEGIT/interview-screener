from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InterviewResultBase(BaseModel):
    transcript: Optional[str] = None
    audio_url: Optional[str] = None
    score: Optional[float] = None


class InterviewResultCreate(InterviewResultBase):
    candidate_id: int
    question_id: int


class InterviewResultResponse(InterviewResultBase):
    id: int
    candidate_id: int
    question_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

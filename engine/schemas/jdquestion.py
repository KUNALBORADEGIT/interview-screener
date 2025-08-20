from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JDQuestionBase(BaseModel):
    jd_text: str
    question_text: str


class JDQuestionCreate(JDQuestionBase):
    candidate_id: int


class JDQuestionResponse(JDQuestionBase):
    id: int
    candidate_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

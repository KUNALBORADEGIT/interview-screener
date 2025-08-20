from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FinalRecommendationBase(BaseModel):
    overall_score: Optional[float] = None
    recommendation: Optional[str] = None  # "hire", "no_hire", "maybe"


class FinalRecommendationCreate(FinalRecommendationBase):
    candidate_id: int


class FinalRecommendationResponse(FinalRecommendationBase):
    id: int
    candidate_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

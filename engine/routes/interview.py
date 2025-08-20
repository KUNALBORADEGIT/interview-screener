# engine/routes/interview.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from engine.services.interview_service import InterviewService

router = APIRouter()


class InterviewRequest(BaseModel):
    candidate_id: int
    jd_id: int


@router.post("/trigger")
async def trigger_interview(request: InterviewRequest):
    service = InterviewService()
    try:
        result = await service.start_interview(
            candidate_id=request.candidate_id, jd_id=request.jd_id
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

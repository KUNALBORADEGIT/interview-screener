# engine/routes/candidate.py
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os, shutil, uuid

from engine.db.session import get_db
from engine.models import Candidate, Recommendation, Interview
from engine.services.resume_parser import ResumeParser

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from engine.db.session import SessionLocal


router = APIRouter()


@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a candidate resume (PDF/DOCX),
    parse info using LLM,
    and save candidate with extracted fields.
    """

    # Only allow PDF/DOCX
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in [".pdf", ".docx"]:
        return {"error": "Only PDF and DOCX resumes supported"}

    # Save file
    save_dir = "uploads/resumes"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(save_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse resume with LLM
    parser = ResumeParser()
    parsed_data = await parser.parse(file_path)

    if "error" in parsed_data:
        # fallback to placeholder values if LLM fails
        candidate = Candidate(
            name="Unknown",
            email=f"auto-{uuid.uuid4()}@placeholder.com",
            phone=f"+10000000000",
            resume_url=file_path,
        )
    else:
        candidate = Candidate(
            name=parsed_data.get("name", "Unknown"),
            email=parsed_data.get("email", f"auto-{uuid.uuid4()}@placeholder.com"),
            phone=parsed_data.get("phone", f"+10000000000"),
            resume_url=file_path,
        )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {
        "message": "Candidate created with resume",
        "candidate_id": candidate.id,
        "resume_url": candidate.resume_url,
        "parsed_data": parsed_data,  # optional, helps debugging
    }


@router.get("/result")
async def result(candidate_id: int):
    """
    Fetch candidate interview results, scores, and recommendation.
    """
    db = SessionLocal()
    try:
        # Fetch all interview entries for candidate
        interviews = (
            db.query(Interview).filter(Interview.candidate_id == candidate_id).all()
        )
        if not interviews:
            raise HTTPException(
                status_code=404, detail="No interviews found for this candidate"
            )

        # Collect each question answer and score
        interview_results = [
            {
                "question_id": i.question_id,
                "transcript": i.transcript,
                "audio_url": i.audio_url,
                "score": i.score,
            }
            for i in interviews
        ]

        # Fetch recommendation if exists
        recommendation = (
            db.query(Recommendation)
            .filter(Recommendation.candidate_id == candidate_id)
            .first()
        )
        rec_data = None
        if recommendation:
            rec_data = {
                "overall_score": recommendation.overall_score,
                "recommendation": recommendation.recommendation,
            }

        return JSONResponse(
            {
                "candidate_id": candidate_id,
                "interviews": interview_results,
                "recommendation": rec_data,
            }
        )
    finally:
        db.close()

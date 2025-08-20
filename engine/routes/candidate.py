# engine/routes/candidate.py
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os, shutil, uuid

from engine.db.session import get_db
from engine.models.candidate import Candidate
from engine.services.resume_parser import ResumeParser

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

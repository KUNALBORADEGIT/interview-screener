from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from engine.db.session import get_db
from engine.models import JobDescription, Question, JDToQS
from engine.services.llm_client import LLMClient

router = APIRouter()


@router.post("/upload")
async def upload_jobdescription(
    file: UploadFile = File(None),
    text: str = Form(None),
    db: Session = Depends(get_db),
):
    """
    Upload a Job Description (txt or raw text),
    generate 5–7 interview questions using LLM,
    and store JD + Questions + JD_to_QS mappings.
    """

    # 1️⃣ Extract JD content
    if text:
        jd_content = text
    elif file:
        if file.filename.endswith(".txt"):
            jd_content = (await file.read()).decode("utf-8")
        else:
            return {"error": "Only .txt files supported for now"}
    else:
        return {"error": "Provide either JD text or JD file"}

    # 2️⃣ Save JD in table
    job = JobDescription(jobdescription=jd_content)
    db.add(job)
    db.commit()
    db.refresh(job)  # ✅ get job.id

    # 3️⃣ Ask LLM to generate 5–7 questions
    client = LLMClient()
    prompt = f"Generate 5 to 7 concise interview questions from this job description:\n\n{jd_content}"
    questions = await client.ask(prompt)

    if isinstance(questions, str):
        questions = [q.strip() for q in questions.split("\n") if q.strip()]
    questions = questions[:7]  # max 7
    if len(questions) < 5:
        return {"error": "LLM did not return enough questions"}

    # 4️⃣ Insert questions + mapping
    saved_questions = []
    for q in questions:
        question_obj = Question(question=q)
        db.add(question_obj)
        db.commit()
        db.refresh(question_obj)

        mapping = JDToQS(jd_id=job.id, qs_id=question_obj.id)
        db.add(mapping)
        db.commit()

        saved_questions.append({"id": question_obj.id, "text": q})

    # 5️⃣ Return response
    return {
        "jobdescription": {"id": job.id, "text": job.jobdescription[:200]},
        "questions": saved_questions,
    }

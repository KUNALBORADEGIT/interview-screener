# engine/routes/twiml.py
from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
from engine.core.logger import logger
from engine.core.config import settings
from engine.db.session import SessionLocal
from engine.models import Candidate, Interview, Question, JDToQS
from pathlib import Path

router = APIRouter()


@router.api_route("/interview", methods=["GET", "POST"])
async def twiml_interview(request: Request):
    """
    Twilio endpoint to play one question at a time and record response.
    """
    logger.info("############### Received TwiML request for interview #############")

    candidate_id = int(request.query_params.get("candidate_id"))
    question_ids_param = request.query_params.get("question_ids", "")
    question_ids = (
        [int(qid) for qid in question_ids_param.split(",")]
        if question_ids_param
        else []
    )

    question_idx = int(request.query_params.get("question_idx", 0))

    response = VoiceResponse()

    if question_idx < len(question_ids):
        # Fetch question text from DB for this question_id
        db = SessionLocal()
        try:
            question = (
                db.query(Question).filter_by(id=question_ids[question_idx]).first()
            )
            if not question:
                response.say("Question not found.")
                return Response(content=str(response), media_type="application/xml")
            question_text = question.question
        finally:
            db.close()

        # Speak the question
        response.say(question_text, voice="alice")

        # Record response, increment question_idx in callback URL
        response.record(
            timeout=5,
            max_length=120,
            play_beep=True,
            action=(
                f"/twiml/record_callback?"
                f"candidate_id={candidate_id}&"
                f"question_idx={question_idx}&"
                f"question_ids={question_ids_param}"
            ),
        )
    else:
        response.say("Thank you! Interview complete.")

    return Response(content=str(response), media_type="application/xml")


@router.post("/record_callback")
async def record_callback(request: Request):
    """
    Twilio record callback: save recording and move to next question.
    """
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    call_sid = form.get("CallSid")
    candidate_id = int(request.query_params.get("candidate_id"))
    question_idx = int(request.query_params.get("question_idx", 0))
    question_ids_param = request.query_params.get("question_ids", "")
    question_ids = (
        [int(qid) for qid in question_ids_param.split(",")]
        if question_ids_param
        else []
    )

    # Save recording to DB
    if question_idx < len(question_ids):
        db = SessionLocal()
        try:
            interview = Interview(
                candidate_id=candidate_id,
                question_id=question_ids[question_idx],
                recording_url=recording_url,
            )
            db.add(interview)
            db.commit()
            logger.info(
                f"Recording saved: {recording_url} "
                f"(Call SID: {call_sid}, Question ID: {question_ids[question_idx]})"
            )
        finally:
            db.close()

    # Prepare next question
    next_idx = question_idx + 1
    response = VoiceResponse()

    if next_idx < len(question_ids):
        response.redirect(
            f"/twiml/interview?"
            f"candidate_id={candidate_id}&"
            f"question_ids={question_ids_param}&"
            f"question_idx={next_idx}"
        )
    else:
        response.say("Thank you! Interview complete.")

    return Response(content=str(response), media_type="application/xml")

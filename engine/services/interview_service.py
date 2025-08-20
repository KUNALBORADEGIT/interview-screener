from typing import Dict
from pathlib import Path
from engine.services.twilio_client import TwilioClient
from engine.services.stt_service import STTService
from engine.services.tts_service import TTSService
from engine.core.config import settings  # Import settings

from engine.db.session import SessionLocal
from engine.models import Candidate, Interview, Question, JDToQS


class InterviewService:
    def __init__(self):
        self.twilio = TwilioClient()
        self.stt = STTService()
        self.tts = TTSService()

    def start_interview(self, candidate_id: int, jd_id: int) -> Dict:

        # Open DB session
        db = SessionLocal()
        try:
            # 1️⃣ Fetch candidate
            candidate = db.query(Candidate).filter_by(id=candidate_id).first()
            if not candidate:
                raise ValueError("Candidate not found")

            # 2️⃣ Fetch all questions for the JD
            question_ids = (
                db.query(Question.id)
                .join(JDToQS, Question.id == JDToQS.qs_id)
                .filter(JDToQS.jd_id == jd_id)
                .all()
            )
            if not question_ids:
                raise ValueError("No questions found for this JD")

            question_ids = [qid for (qid,) in question_ids]

            call_sid = self.twilio.call_and_play_questions(
                candidate_phone=candidate.phone,
                candidate_id=candidate.id,
                question_ids=question_ids,
            )

            return {
                "candidate": candidate.name,
                "phone": candidate.phone,
                "question_ids": question_ids,
                "status": "in-progress",
                "call_sid": call_sid,
            }
        finally:
            db.close()

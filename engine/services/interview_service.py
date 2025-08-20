# engine/services/interview.py
from typing import Dict
from engine.services.twilio_client import TwilioClient
from engine.services.stt_service import STTService
from engine.services.tts_service import TTSService

from engine.db.session import SessionLocal
from engine.models import Candidate, Interview, Question, JDToQS


class InterviewService:
    def __init__(self):
        self.twilio = TwilioClient()
        self.stt = STTService()
        self.tts = TTSService()

    async def start_interview(self, candidate_id: int, jd_id: int) -> Dict:
        with SessionLocal() as db:
            # 1️⃣ Fetch candidate
            candidate = db.query(Candidate).filter_by(id=candidate_id).first()
            if not candidate:
                raise ValueError("Candidate not found")

            # 2️⃣ Fetch all questions for the JD via JDToQS
            questions = (
                db.query(Question)
                .join(JDToQS, Question.id == JDToQS.qs_id)
                .filter(JDToQS.jd_id == jd_id)
                .all()
            )
            if not questions:
                raise ValueError("No questions found for this JD")

            question_texts = [q.question for q in questions]

            # 3️⃣ Generate TTS audios (placeholder)
            question_audios = [self.tts.text_to_speech(q) for q in question_texts]

            # 4️⃣ Trigger Twilio call (placeholder)
            call_sid = self.twilio.call_and_play_audios(
                candidate.phone, question_audios
            )

            # 5️⃣ Create interview record
            interview = Interview(candidate_id=candidate.id)
            db.add(interview)
            db.commit()
            db.refresh(interview)

            # 6️⃣ Return initial response
            return {
                "interview_id": interview.id,
                "candidate": candidate.name,
                "phone": candidate.phone,
                "questions": question_texts,
                "status": "in-progress",
                "call_sid": call_sid,
            }

        # # 2. Trigger phone call
        # call_sid = self.twilio.call_and_ask_questions(
        #     to=candidate.phone,
        #     questions=questions,
        # )

        # # 3. Placeholder for answers
        # interview = Interview(candidate_id=candidate.id, jd_id=jd.id, call_sid=call_sid)
        # db.add(interview)
        # db.commit()
        # db.refresh(interview)

        # return {
        #     "interview_id": interview.id,
        #     "candidate": candidate.name,
        #     "phone": candidate.phone,
        #     "questions": questions,
        #     "status": "in-progress",
        # }

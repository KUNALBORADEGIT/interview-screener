# engine/services/interview.py
from typing import Dict
from pathlib import Path
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

            # Prepare candidate folders
            base_dir = Path("static") / str(candidate_id)
            q_dir = base_dir / "questions"
            a_dir = base_dir / "answers"
            q_dir.mkdir(parents=True, exist_ok=True)
            a_dir.mkdir(parents=True, exist_ok=True)

            question_audios = []
            for q in questions:
                audio_path = q_dir / f"{q.id}.mp3"
                self.tts.text_to_speech(q.question, str(audio_path))
                question_audios.append(str(audio_path))

            # 3️⃣ Trigger Twilio call
            call_sid = self.twilio.call_and_play_audios(
                candidate.id, candidate.phone, question_audios
            )

            for q in questions:
                interview = Interview(candidate_id=candidate.id, question_id=q.id)
                db.add(interview)
            db.commit()

            return {
                "candidate": candidate.name,
                "phone": candidate.phone,
                "questions": [q.question for q in questions],
                "status": "in-progress",
                "call_sid": call_sid,
            }

            # # 3️⃣ Generate TTS audios (placeholder)
            # question_audios = [self.tts.text_to_speech(q) for q in question_texts]

            # # 4️⃣ Trigger Twilio call (placeholder)
            # call_sid = self.twilio.call_and_play_audios(
            #     candidate.phone, question_audios
            # )

            # # 5️⃣ Create interview record
            # interview = Interview(candidate_id=candidate.id)
            # db.add(interview)
            # db.commit()
            # db.refresh(interview)

            # # 6️⃣ Return initial response
            # return {
            #     "interview_id": interview.id,
            #     "candidate": candidate.name,
            #     "phone": candidate.phone,
            #     "questions": question_texts,
            #     "status": "in-progress",
            #     "call_sid": call_sid,
            # }

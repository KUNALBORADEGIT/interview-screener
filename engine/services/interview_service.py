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

    async def start_interview(self, candidate_id: int, jd_id: int) -> Dict:
        with SessionLocal() as db:
            # 1️⃣ Fetch candidate
            candidate = db.query(Candidate).filter_by(id=candidate_id).first()
            if not candidate:
                raise ValueError("Candidate not found")

            # 2️⃣ Fetch all questions for the JD
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

            # Generate audio files and their public URLs
            public_urls = []
            for idx, q in enumerate(questions):
                file_name = f"tts_{idx}.mp3"
                audio_path = q_dir / file_name
                self.tts.text_to_speech(q.question, str(audio_path))

                # Construct the full public URL here
                public_url = f"{settings.SERVICE_URL}/static/{candidate_id}/questions/{file_name}"
                public_urls.append(public_url)

            # 3️⃣ Trigger Twilio call with the public URLs
            call_sid = self.twilio.call_and_play_audios(
                candidate_phone=candidate.phone, public_urls=public_urls
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

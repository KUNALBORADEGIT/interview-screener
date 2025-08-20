# engine/services/twilio_client.py
from twilio.rest import Client
from pathlib import Path
import os
from engine.core.config import settings
from engine.core.logger import logger


class TwilioClient:
    def __init__(self):
        self.from_phone = settings.TWILIO_PHONE_NUMBER
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.client = Client(self.account_sid, self.auth_token)

        # Base folders
        self.static_dir = Path("static")
        os.makedirs(self.static_dir, exist_ok=True)

    def call_and_play_audios(
        self, candidate_phone: str, candidate_id: int, audio_files: list[str]
    ) -> str:
        """
        Makes a call, plays questions (audio files), and records answers.
        Returns the Twilio Call SID.
        """

        logger(
            f"Calling {candidate_phone} and playing {len(audio_files)} audio files..."
        )

        # Ensure candidate question folder exists
        question_folder = self.static_dir / str(candidate_id) / "questions"
        os.makedirs(question_folder, exist_ok=True)

        # Ensure candidate answers folder exists
        answers_folder = self.static_dir / str(candidate_id) / "answers"
        os.makedirs(answers_folder, exist_ok=True)

        # Move TTS files to candidate question folder and construct public URLs
        public_urls = []
        for idx, file_path in enumerate(audio_files):
            file_name = f"tts_{idx}.mp3"
            dest_path = question_folder / file_name
            os.replace(file_path, dest_path)  # move file
            public_url = (
                f"{settings.SERVICE_URL}/static/{candidate_id}/questions/{file_name}"
            )
            public_urls.append(public_url)

        # Join URLs for TwiML
        files_param = ",".join(public_urls)

        try:
            call = self.client.calls.create(
                to=candidate_phone,
                from_=self.from_phone,
                url=f"{settings.SERVICE_URL}/twiml/interview?files={files_param}",
            )
            return call.sid
        except Exception as e:
            logger(f"Twilio call failed: {e}")
            raise

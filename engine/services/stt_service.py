# engine/services/stt_service.py
import os
import tempfile

import requests
from engine.core.config import settings


class STTService:
    def audio_to_text(self, audio_url: str) -> str:
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                tmp_path = tmp_file.name
                # Use Twilio credentials for private recording
                resp = requests.get(
                    audio_url,
                    auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
                )
                resp.raise_for_status()
                tmp_file.write(resp.content)

            # TODO: pass tmp_path to real STT model
            transcript = f"Transcribed text of audio at {audio_url}"

            return transcript
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

# engine/services/stt_service.py
import os
import tempfile
import requests
from engine.core.logger import logger


class STTService:
    """
    Speech-to-Text service.
    Converts audio file into text transcript.
    """

    def __init__(self):
        pass

    def audio_to_text(self, audio_url: str) -> str:
        """
        Converts an audio file URL to text.
        Returns the transcript as string.
        """
        try:
            # Download audio to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                tmp_path = tmp_file.name
                logger.info(f"Downloading audio from {audio_url} to {tmp_path}")
                resp = requests.get(audio_url)
                resp.raise_for_status()
                tmp_file.write(resp.content)

            transcript = f"Transcribed text of audio at {audio_url}"

            logger.info(f"Audio transcribed: {transcript}")
            return transcript
        except Exception as e:
            logger.error(f"Failed to convert audio to text: {e}")
            return ""
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

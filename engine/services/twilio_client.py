# engine/services/twilio_client.py
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Play, Record
import os
from engine.core.config import settings


class TwilioClient:
    def __init__(self):
        self.from_phone = settings.TWILIO_PHONE_NUMBER
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.client = Client(self.account_sid, self.auth_token)
        self.recordings_dir = "engine/temp_recordings"
        os.makedirs(self.recordings_dir, exist_ok=True)

    def call_and_play_audios(self, to: str, audio_files: list[str]) -> str:
        """
        Makes a call, plays questions (audio files), and records answers.
        Returns the Twilio Call SID.
        """
        print(
            f"@@@@@@@@@@@@@@@@ Calling {to} and playing {len(audio_files)} audio files... @@@@@@@@@@@@@@@@"
        )
        try:
            files_param = ",".join(audio_files)  # must be public URLs
            call = self.client.calls.create(
                to=to,
                from_=self.from_phone,
                url=f"https://{settings.SERVICE_URL}/twiml/interview?files={files_param}",
            )
            return call.sid
        except Exception as e:
            print(f"Twilio call failed: {e}")
            raise

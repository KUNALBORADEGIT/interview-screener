from twilio.rest import Client
from engine.core.config import settings
from engine.core.logger import logger
from urllib.parse import quote


class TwilioClient:
    def __init__(self):
        self.from_phone = settings.TWILIO_PHONE_NUMBER
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.client = Client(self.account_sid, self.auth_token)

    def call_and_play_audios(self, candidate_phone: str, public_urls: list[str]) -> str:
        """
        Makes a call and plays a sequence of audio files from public URLs.
        Returns the Twilio Call SID.
        """
        logger.info(
            f"Calling {candidate_phone} and playing {len(public_urls)} audio files..."
        )

        # URL-encode each file URL for safety
        encoded_files = [quote(url, safe="") for url in public_urls]
        files_param = ",".join(encoded_files)

        try:
            call = self.client.calls.create(
                to=candidate_phone,
                from_=self.from_phone,
                url=f"{settings.SERVICE_URL}/twiml/interview?files={files_param}",
                method="POST",  # Ensure Twilio POSTs
            )
            return call.sid
        except Exception as e:
            logger.error(f"Twilio call failed: {e}")
            raise

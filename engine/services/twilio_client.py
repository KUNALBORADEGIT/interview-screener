from twilio.rest import Client
from engine.core.config import settings
from engine.core.logger import logger
from urllib.parse import quote
from typing import List


class TwilioClient:
    def __init__(self):
        self.from_phone = settings.TWILIO_PHONE_NUMBER
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.client = Client(self.account_sid, self.auth_token)

    def call_and_play_questions(
        self,
        candidate_phone: str,
        candidate_id: int,
        question_ids: List[int],
    ) -> str:
        """
        Makes a call and passes question IDs to the TwiML endpoint.
        The TwiML endpoint will fetch the actual questions from the DB.
        Returns the Twilio Call SID.
        """
        logger.info(
            f"Calling {candidate_phone} with {len(question_ids)} questions (candidate_id={candidate_id})"
        )

        # Encode IDs for URL safety
        encoded_ids = [quote(str(qid), safe="") for qid in question_ids]
        questions_param = ",".join(encoded_ids)

        # Construct TwiML URL
        twiml_url = (
            f"{settings.SERVICE_URL}/twiml/interview?"
            f"candidate_id={candidate_id}&question_ids={questions_param}"
        )

        try:
            call = self.client.calls.create(
                to=candidate_phone,
                from_=self.from_phone,
                url=twiml_url,
                method="POST",  # Ensure Twilio POSTs
            )
            return call.sid
        except Exception as e:
            logger.error(f"Twilio call failed: {e}")
            raise

from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
from engine.core.logger import logger

router = APIRouter()


@router.api_route("/interview", methods=["GET", "POST"])
async def twiml_interview(request: Request):
    logger.info("############### Received TwiML request for interview #############")
    files_param = request.query_params.get("files", "")
    files = files_param.split(",") if files_param else []

    response = VoiceResponse()

    for idx, file_url in enumerate(files):
        response.play(file_url)
        # Include question index in record action
        response.record(
            timeout=5,
            max_length=120,
            play_beep=True,
            action=f"/twiml/record_callback?question_id={idx}",
        )

    return Response(content=str(response), media_type="application/xml")


@router.post("/record_callback")
async def record_callback(request: Request):
    logger.info("######### Received TwiML record callback #################")
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    call_sid = form.get("CallSid")
    question_id = request.query_params.get("question_id")

    if recording_url and call_sid:
        # TODO: Save recording_url to DB with call_sid & question_id
        logger.info(
            f"Recording saved: {recording_url} (Call SID: {call_sid}, Question ID: {question_id})"
        )
    else:
        logger.warning(
            f"Record callback missing data: form={form}, query={request.query_params}"
        )

    return Response(content="<Response></Response>", media_type="application/xml")

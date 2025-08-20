from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse

router = APIRouter()


@router.get("/interview")
async def twiml_interview(request: Request):
    print(
        "###################### Received TwiML request for interview ######################"
    )
    files_param = request.query_params.get("files", "")
    files = files_param.split(",")

    response = VoiceResponse()

    for file_url in files:
        response.play(file_url)
        response.record(
            timeout=5,
            max_length=120,
            play_beep=True,
            action="/twiml/record_callback",
        )

    return Response(content=str(response), media_type="application/xml")


@router.post("/record_callback")
async def record_callback(request: Request):
    print(
        "###################### Received TwiML record callback ######################"
    )
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    call_sid = form.get("CallSid")
    question_id = request.query_params.get("question_id")

    # TODO: Save recording_url to DB with call_sid & question_id
    print(
        f"Recording saved: {recording_url} (Call SID: {call_sid}, Question ID: {question_id})"
    )

    return Response(content="<Response></Response>", media_type="application/xml")

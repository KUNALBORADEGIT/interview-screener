from fastapi import APIRouter, Depends
from engine.services.llm_client import LLMClient

router = APIRouter(prefix="/llm", tags=["LLM"])


@router.get("/ask")
async def ask_llm(q: str):
    client = LLMClient()
    response = await client.ask(q)
    return {"question": q, "answer": response}

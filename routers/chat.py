# routers/chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import handle_chat

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    bank_button: bool = False


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Foydalanuvchi xabarini qabul qiladi va
    chat_service.py dagi AI logikasiga yuboradi.
    """
    result = await handle_chat(request.message)

    return ChatResponse(
        reply=result["reply"],
        bank_button=result["bank_button"]
    )

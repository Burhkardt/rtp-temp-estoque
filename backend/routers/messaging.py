from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from modules.messaging.whatsapp import send_whatsapp_message

router = APIRouter(prefix="/messaging", tags=["messaging"])

class MessagePayload(BaseModel):
    to_number: str
    message: str

@router.post("/whatsapp/send")
def send_whatsapp(payload: MessagePayload):
    try:
        response = send_whatsapp_message(payload.to_number, payload.message)
        return {"success": True, "details": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from config import settings

# Exemplo usando API do Twilio ou API direta do WhatsApp
TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER

def send_whatsapp_message(to_number: str, message: str) -> dict:
    """Simula o envio de uma mensagem de WhatsApp"""
    
    # Exemplo de payload
    payload = {
        "to": to_number,
        "message": message,
        "status": "success"
    }
    
    # Na implementação real com Twilio seria algo como:
    # from twilio.rest import Client
    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # msg = client.messages.create(
    #     from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
    #     body=message,
    #     to=f"whatsapp:{to_number}"
    # )
    # payload['sid'] = msg.sid
    
    print(f"Mensagem enviada para {to_number}: {message}")
    
    return payload

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests
import os

telegram_bp = Blueprint('telegram', __name__)

#dados necessários para envio
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  


#Auxiliar para envio de mensagem
def send_to_channel(text: str, parse_mode: str = "Markdown") -> dict:
    response = requests.post(f"{TELEGRAM_API}/sendMessage", json={
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": parse_mode
    })
    return response.json()


#Envia a mensagem para o canal do telegram
@telegram_bp.route("/send", methods=["POST"])
def send_message():

    data = request.get_json()
    message = data.get("message")
    parse_mode = data.get("parse_mode", "Markdown")

    if not message:
        return jsonify({"error": "O campo 'message' é obrigatório"}), 400

    result = send_to_channel(message, parse_mode)

    if result.get("ok"):
        return jsonify({"success": True, "message_id": result["result"]["message_id"]}), 200
    
    return jsonify({"success": False, "error": result.get("description")}), 500


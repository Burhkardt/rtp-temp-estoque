from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests
import os
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from database.generic_queries import repository
from utils.barcode import id_to_barcode

telegram_bp = Blueprint('telegram', __name__)

# Dados necessários para envio
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


# Auxiliar para envio de mensagem de texto
def send_to_channel(text: str, parse_mode: str = "Markdown") -> dict:
    response = requests.post(f"{TELEGRAM_API}/sendMessage", json={
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": parse_mode
    })
    return response.json()


# Auxiliar para envio de foto (barcode)
def send_photo_to_channel(photo_bytes, caption: str, parse_mode: str = "Markdown") -> dict:
    files = {'photo': ('barcode.png', photo_bytes, 'image/png')}
    data = {
        "chat_id": CHANNEL_ID,
        "caption": caption,
        "parse_mode": parse_mode
    }
    response = requests.post(f"{TELEGRAM_API}/sendPhoto", data=data, files=files)
    return response.json()


# Envia a mensagem de texto para o canal
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


# Nova rota integrada: Gera Barcode + Envia para Telegram
# Suporta dados MOKADOS para teste sem banco de dados
@telegram_bp.route("/send-product-tag/<int:product_id>", methods=["POST"])
def send_product_tag(product_id):
    try:
        # Flag para forçar mock enquanto não tem acesso ao banco
        use_mock = request.args.get("mock", "true").lower() == "true"

        if use_mock:
            # DADOS MOKADOS PARA TESTE
            product_name = "PRODUTO TESTE MOKADO"
            stock = 99
            print(f"Usando dados MOKADOS para o produto {product_id}")
        else:
            # BUSCA REAL NO BANCO (Ativar quando estiver na rede)
            product = repository.select_product_by_id(product_id)
            if not product:
                return jsonify({"error": "Produto não encontrado no banco."}), 404
            product_name = product[0]
            stock = product[1]

        # 1. Gerar valor do barcode (ex: 1000000001)
        barcode_value = id_to_barcode(product_id)

        # 2. Gerar imagem do barcode em memória (BytesIO)
        buffer = BytesIO()
        barcode.get("code128", barcode_value, writer=ImageWriter()).write(buffer)
        buffer.seek(0)

        # 3. Montar a legenda (Caption)
        caption = (
            f"📦 *Etiqueta de Patrimônio*\n\n"
            f"🔹 *ID:* `{product_id}`\n"
            f"🔹 *Produto:* {product_name}\n"
            f"🔹 *Estoque:* {stock}\n"
            f"🔹 *Código:* `{barcode_value}`"
        )

        # 4. Enviar Foto + Legenda para o Telegram
        result = send_photo_to_channel(buffer, caption)

        if result.get("ok"):
            return jsonify({
                "success": True, 
                "mode": "mock" if use_mock else "database",
                "message_id": result["result"]["message_id"]
            }), 200
        
        return jsonify({"success": False, "error": result.get("description")}), 500

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500



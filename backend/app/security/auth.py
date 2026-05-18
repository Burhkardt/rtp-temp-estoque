import jwt

from functools import wraps
from flask import request, jsonify

SECRET_KEY = "segredo-super-seguro"


# =========================
# GERAR TOKEN
# =========================
def generate_token(user_id):

    payload = {
        "user_id": user_id
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


# =========================
# VALIDAR TOKEN
# =========================
def validate_token(token):

    try:

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return decoded

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


# =========================
# PROTEGER ENDPOINTS
# =========================
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:

            return jsonify({
                "error": "Token não informado"
            }), 401

        try:

            token = auth_header.split(" ")[1]

        except:
            return jsonify({
                "error": "Token inválido"
            }), 401

        decoded = validate_token(token)

        if not decoded:

            return jsonify({
                "error": "Token inválido ou expirado"
            }), 401

        return f(*args, **kwargs)

    return decorated
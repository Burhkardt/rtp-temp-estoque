import jwt

from functools import wraps

from flask import request, jsonify

SECRET_KEY = "segredo-super-seguro"


# =====================================
# GERAR TOKEN
# =====================================

def create_access_token(data):

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


# =====================================
# VALIDAR TOKEN
# =====================================

def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except:

        return None


# =====================================
# PROTEGER ROTAS
# =====================================

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

        payload = verify_token(token)

        if not payload:

            return jsonify({
                "error": "Token inválido ou expirado"
            }), 401

        return f(*args, **kwargs)

    return decorated
from flask import Blueprint, request, jsonify

from app.auth.jwt_handler import create_access_token

auth_bp = Blueprint(
    "auth",
    __name__
)

# =====================================
# LOGIN
# =====================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # LOGIN FAKE PARA TESTE
    if username == "admin" and password == "123":

        token = create_access_token({
            "user_id": 1
        })

        return jsonify({
            "access_token": token
        })

    return jsonify({
        "error": "Usuário ou senha inválidos"
    }), 401
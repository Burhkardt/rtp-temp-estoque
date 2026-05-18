from flask import Blueprint, jsonify, request

from app.security.auth import generate_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # LOGIN FAKE APENAS PARA TESTE
    if username == "admin" and password == "123":

        token = generate_token(1)

        return jsonify({
            "token": token
        })

    return jsonify({
        "error": "Usuário ou senha inválidos"
    }), 401
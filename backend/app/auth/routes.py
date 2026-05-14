from flask import Blueprint, request, jsonify

# Cria blueprint de autenticação
auth_bp = Blueprint(
    "auth_bp",
    __name__,
    url_prefix="/auth"
)

# =========================================
# LOGIN
# =========================================
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    # Verifica se veio JSON
    if not data:

        return jsonify({
            "erro": "JSON inválido"
        }), 400

    cpf = data.get("cpf")
    senha = data.get("senha")

    # Validação simples
    if not cpf or not senha:

        return jsonify({
            "erro": "CPF e senha obrigatórios"
        }), 400

    # Usuário fake para testes
    if cpf != "12345678910" or senha != "123456":

        return jsonify({
            "erro": "Credenciais inválidas"
        }), 401

    # Resposta simulando login
    return jsonify({

        "access_token": "token_fake",

        "token_type": "bearer",

        "nome": "Administrador",

        "perfil": "admin"

    }), 200
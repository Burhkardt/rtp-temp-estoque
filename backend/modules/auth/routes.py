from flask import Blueprint, request, jsonify
import json
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

# Usuários mockados para autenticação sem banco de dados
USUARIOS_MOCK = [
    {
        "email": "teste@email.com",
        "password": "123456",
        "name": "Usuário Teste"
    }
]


@auth_bp.route('/login', methods=['POST'])
def login():

    dados = request.get_json(force=True, silent=True)
    if isinstance(dados, str):
        try:
            dados = json.loads(dados)
        except:
            dados = {}
    if not dados or not isinstance(dados, dict):
        dados = {}

    usuario = dados.get('username')
    senha = dados.get('password')

    if not usuario or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios."}), 400

    usuario_valido = next(
        (user for user in USUARIOS_MOCK if user["email"] == usuario and user["password"] == senha),
        None
    )

    if not usuario_valido:
        return jsonify({"erro": "Usuário ou senha incorretos"}), 401

    token_acesso = create_access_token(identity=usuario_valido["email"])
    return jsonify({"token": token_acesso}), 200

# ==========================================
# 🌟 NOVA ROTA PROTEGIDA (A SALA VIP)
# ==========================================

@auth_bp.route('/estoque-vip', methods=['GET'])
@jwt_required() 
def acessar_estoque_vip():

    usuario_atual = get_jwt_identity()
    
    # Devolvemos uma mensagem de sucesso
    return jsonify({
        "mensagem": f"Sucesso! Bem-vindo ao estoque, {usuario_atual}. Seu crachá é válido!"
    }), 200
import os
from flask import Flask, redirect
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
from database.connection import Database
from flask_jwt_extended import JWTManager
from core.register import register_routes
from modules.auth.routes import auth_bp 

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-inseguro")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]

    JWTManager(app)
    register_routes(app)
    
    # 🌟 NOVO AQUI: Avisamos o sistema que a rota de login existe!
    # O url_prefix='/api/auth' fazer login, 
    # o frontend vai acessar: seudominio.com/api/auth/login
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    app.config["SWAGGER"] = {
        "title": "API RTP Estoque",
        "uiversion": 3,
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API RTP Estoque",
            "description": "Documentação interativa da API do sistema de leitura de código de barra para estoque.",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "⚠️ **AVISO IMPORTANTE:**\\nVocê **DEVE** digitar a palavra `Bearer` seguida de um espaço antes do seu token!\\n\\n**Exemplo correto:** `Bearer eyJhbGciOiJIUzI1NiIs...`"
            }
        },
    }
    Swagger(app, template=swagger_template)

    @app.route('/')
    def index():
        return redirect('/apidocs/')

    try:
        Database.initialize()
        print("Banco de dados carregado.")

    except Exception as e:
        print(f"Erro ao iniciar: {e}")

    return app


if __name__ == "__main__":
    app = create_app()
    # Foi adicionado o host='0.0.0.0' para ele abrir as portas para fora do Docker!
    app.run(host="0.0.0.0", port=5000, debug=True)

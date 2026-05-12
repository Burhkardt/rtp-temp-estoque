import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
from database.connection import Database
from flask_jwt_extended import JWTManager

def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-inseguro")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]

    JWTManager(app)

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API RTP Patrimônio",
            "description": "Documentação interativa da API do sistema de Patrimônio.",
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

    Database().initialize()

    #register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
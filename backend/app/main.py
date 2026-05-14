from flask import Flask
from flask_cors import CORS

# Importa blueprint de autenticação
from app.auth.routes import auth_bp

# Importa blueprint de produtos
from app.routes.products import products_bp

# Cria aplicação Flask
app = Flask(__name__)

# =========================================
# CONFIGURAÇÃO CORS
# =========================================
CORS(
    app,

    resources={
        r"/*": {
            "origins": [
                "http://127.0.0.1:5500",
                "http://localhost:5500"
            ]
        }
    },

    supports_credentials=True
)

# =========================================
# REGISTRO DOS BLUEPRINTS
# =========================================

# Rotas de autenticação
app.register_blueprint(auth_bp)

# Rotas de produtos
app.register_blueprint(products_bp)

# =========================================
# ROTA PRINCIPAL
# =========================================
@app.route("/")
def home():

    return {
        "message": "Projeto 3 Online"
    }

# =========================================
# INICIALIZAÇÃO DA APLICAÇÃO
# =========================================
if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
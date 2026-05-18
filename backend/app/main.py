from flask import Flask
from flask_cors import CORS

from app.routes.products import products_bp
from app.auth.routes import auth_bp

app = Flask(__name__)

# =====================================
# CORS
# =====================================

CORS(
    app,

    resources={
        r"/*": {
            "origins": [
                "http://127.0.0.1:5500",
                "http://localhost:5500"
            ]
        }
    }
)

# =====================================
# BLUEPRINTS
# =====================================

app.register_blueprint(products_bp)
app.register_blueprint(auth_bp)

# =====================================
# ROOT
# =====================================

@app.route("/")
def root():

    return {
        "message": "Projeto 3 Online"
    }

# =====================================
# START
# =====================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
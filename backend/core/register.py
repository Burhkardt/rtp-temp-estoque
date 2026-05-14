from modules.product.product_routes import product_bp
from modules.send_message.telegram_routes import telegram_bp

def register_routes(app):
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(telegram_bp, url_prefix='/telegram')
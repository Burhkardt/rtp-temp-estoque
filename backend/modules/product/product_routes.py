import barcode
from barcode.writer import ImageWriter
from flask import Blueprint, jsonify, send_file
from flask_jwt_extended import jwt_required
from io import BytesIO
from database.generic_queries import repository
from utils.barcode import barcode_to_id, id_to_barcode
from flasgger import swag_from

product_bp = Blueprint("products", __name__)


@product_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from("../../docs/get_all_products.yml")
def get_all_products():
    """
    Get all products
    """
    try:
        products = repository.select_all_products()
        return jsonify({"data": products, "total": len(products)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Retorna o produto ao ler o código de barra
@product_bp.route("/barcode/<string:barcode>", methods=["GET"])
@jwt_required()
@swag_from("../../docs/get_product_by_barcode.yml")
def get_product_by_barcode(barcode):
    """
    Get product by barcode
    """
    try:
        if len(barcode) < 2:
            return jsonify({"error": "Código de barras inválido."}), 400

        product = repository.select_product_by_id(barcode_to_id(barcode))

        if not product:
            return jsonify({"error": "Produto não encontrado."}), 404

        return jsonify({"data": product}), 200

    except ValueError:
        return jsonify({"error": "Formato de código de barras inválido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Retorna um código de barra para um determinado produto
@product_bp.route("/<int:product_id>/barcode", methods=["GET"])
@jwt_required()
@swag_from("../../docs/get_barcode_by_product.yml")
def get_barcode_by_product(product_id):
    """
    Get barcode image for a product
    """
    try:
        product = repository.select_product_by_id(product_id)

        if not product:
            return jsonify({"error": "Produto não encontrado."}), 404

        barcode_value = id_to_barcode(product_id)

        buffer = BytesIO()
        barcode.get("code128", barcode_value, writer=ImageWriter()).write(buffer)
        buffer.seek(0)

        return send_file(buffer, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
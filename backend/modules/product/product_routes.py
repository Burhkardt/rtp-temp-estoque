from flask import Blueprint, jsonify, request
from database.generic_queries import repository

product_bp = Blueprint("products", __name__)


#GET All
@product_bp.route("/", methods=["GET"])
def get_all_products():

    try:
        produtos = repository.select_all_products()
        return jsonify({"data": produtos, "total": len(produtos)}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar produtos: {str(e)}"}), 500


#GET ONE
# @product_bp.route("/<int:id_produto>", methods=["GET"])
# def get_product_by_id(id_produto):
#     try:
#         produto = repository.select_product_by_id(id_produto)

#         if not produto:
#             return jsonify({"error": f"Produto com ID {id_produto} não encontrado."}), 404

#         return jsonify({"data": produto}), 200
#     except Exception as e:
#         return jsonify({"error": f"Erro ao buscar produto: {str(e)}"}), 500
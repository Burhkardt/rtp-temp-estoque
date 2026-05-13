from flask import Blueprint, jsonify, request
from database.generic_queries import repository

product_bp = Blueprint("products", __name__)


#GET ONE
@product_bp.route("/", methods=["GET"])
def get_all_products():
    """
    Retorna todos os produtos cadastrados.
    ---
    tags:
      - Produtos
    responses:
      200:
        description: Lista de produtos
      500:
        description: Erro interno
    """
    try:
        produtos = repository.select_all_products()
        return jsonify({"data": produtos, "total": len(produtos)}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar produtos: {str(e)}"}), 500


#GET ALL
# @product_bp.route("/<int:id_produto>", methods=["GET"])
# def get_product_by_id(id_produto):
#     """
#     Retorna um produto pelo ID.
#     ---
#     tags:
#       - Produtos
#     parameters:
#       - name: id_produto
#         in: path
#         type: integer
#         required: true
#         description: ID do produto
#     responses:
#       200:
#         description: Produto encontrado
#       404:
#         description: Produto não encontrado
#       500:
#         description: Erro interno
#     """
#     try:
#         produto = repository.select_product_by_id(id_produto)

#         if not produto:
#             return jsonify({"error": f"Produto com ID {id_produto} não encontrado."}), 404

#         return jsonify({"data": produto}), 200
#     except Exception as e:
#         return jsonify({"error": f"Erro ao buscar produto: {str(e)}"}), 500
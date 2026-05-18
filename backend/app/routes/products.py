from flask import Blueprint, jsonify

from app.repositories.product_repository import repository

from app.auth.jwt_handler import token_required

products_bp = Blueprint(
    "products",
    __name__
)

# =====================================
# TODOS OS PRODUTOS
# =====================================

@products_bp.route("/products", methods=["GET"])
@token_required
def get_products():

    products = repository.select_all_products()

    return jsonify(products)


# =====================================
# UM PRODUTO
# =====================================

@products_bp.route("/products/<int:id>", methods=["GET"])
@token_required
def get_one_product(id):

    product = repository.select_one_product(id)

    return jsonify(product)


# =====================================
# ESTOQUES DE UM PRODUTO
# =====================================

@products_bp.route("/products/<int:id>/stocks", methods=["GET"])
@token_required
def get_stocks_of_product(id):

    stocks = repository.select_all_stocks_of_one_product(id)

    return jsonify(stocks)


# =====================================
# PRODUTOS DE UM ESTOQUE
# =====================================

@products_bp.route("/products/stock/<int:id>", methods=["GET"])
@token_required
def get_products_of_stock(id):

    products = repository.select_all_products_of_one_stock(id)

    return jsonify(products)
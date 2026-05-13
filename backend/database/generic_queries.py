from .connection import Database

class GenericRepository:

    def select_all_products(self):
        query = "SELECT DS_PRODUTO FROM PRODUTO"
        return Database.execute(query)

    # def select_product_by_id(self, id):
    #     # Em Oracle Python, usamos :nome para binds, igual ao Node
    #     query = """
    #         SELECT 
    #         A.DS_PRODUTO, 
    #         B.QT_ESTOQUE_ATUAL 
    #         FROM PRODUTO A 
    #         JOIN EST_PRO B 
    #         ON A.CD_PRODUTO = B.CD_PRODUTO
    #     WHERE A.CD_PRODUTO = :id
    #     """
    #     binds = {"id": id}
    #     result = Database.execute(query, binds)
    #     return result[0] if result else None
    
    # def select_product_by_name(self, name):

    #     #Porcentagens para permitir busca com termo parcial
    #     name_search = f"%{name}%"

    #     query = """
    #         SELECT
    #             P.CD_PRODUTo,
    #             P.DS_PRODUTO,
    #             E.QT_ESTOQUE_ATUAL
    #         FROM PRODUTO P JOIN EST_PRO E 
    #         ON P.CD_PRODUTO = E.CD_PRODUTO 
    #         WHERE DS_PRODUTO LIKE :name
    #         """

    #     binds = {"name": name_search}

    #     return Database.execute(query, binds)

# Exporta uma instância (Singleton)
repository = GenericRepository()
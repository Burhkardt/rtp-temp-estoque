from .connection import Database

class GenericRepository:

    def select_all_products(self):
        query = "SELECT DS_PRODUTO FROM PRODUTO"
        return Database.execute(query)

    def select_product_by_id(self, id):
        # Em Oracle Python, usamos :nome para binds, igual ao Node
        query = """
            SELECT 
            A.DS_PRODUTO, 
            B.QT_ESTOQUE_ATUAL 
            FROM PRODUTO A 
            JOIN EST_PRO B 
            ON A.CD_PRODUTO = B.CD_PRODUTO
        WHERE A.CD_PRODUTO = :id
        """
        binds = {"id": id}
        result = Database.execute(query, binds)
        # Transforma os dados em uma lista para facilitar o acesso (DS_PRODUTO, QT_ESTOQUE_ATUAL)
        if result:
            return [result[0]['ds_produto'], result[0]['qt_estoque_atual']]
        return None
    
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
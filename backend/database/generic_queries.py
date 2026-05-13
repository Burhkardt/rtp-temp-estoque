from connection import Database

class GenericRepository:

    def select_all_products(self):
        query = "SELECT DS_PRODUTO FROM PRODUTO"
        return Database.execute(query)
    
    def select_all_stocks_of_one_product(self, id_produto):
        query = """
            SELECT 
                p.CD_PRODUTO,
                p.DS_PRODUTO,
                e.CD_ESTOQUE,
                e.CD_LOCALIZACAO,
                e.QT_ESTOQUE_ATUAL,
                e.DS_LOCALIZACAO_PRATELEIRA,
                e.DT_ULTIMA_MOVIMENTACAO
            FROM PRODUTO p
            JOIN EST_PRO e ON p.CD_PRODUTO = e. CD_PRODUTO
            WHERE p.CD_PRODUTO = :id
        """
        binds = {"id": id_produto}

        return Database.execute(query, binds)
    
    def select_all_products_of_one_stock(self, id_estoque):
        query = """
        SELECT 
            p.CD_PRODUTO,
            p.DS_PRODUTO,
            e.QT_ESTOQUE_ATUAL,
            e.DS_LOCALIZACAO_PRATELEIRA
        FROM EST_PRO e
        JOIN PRODUTO p ON e.CD_PRODUTO = p.CD_PRODUTO
        WHERE e.CD_ESTOQUE = :id
        ORDER BY p.DS_PRODUTO
    """
        binds = {"id": id_estoque}
        return Database.execute(query, binds)

    def select_product_by_id(self, id):
        # Em Oracle Python, usamos :nome para binds, igual ao Node
        query = """
            SELECT
                CD_PRODUTo,
                DS_PRODUTO,
                QT_ESTOQUE_ATUAL,
                SN_MEDICAMENTO,
                TP_STATUS_UNIFICADO
            FROM PRODUTO WHERE id = :id
        """
        binds = {"id": id}
        result = Database.execute(query, binds)
        return result[0] if result else None
    
    def select_product_by_name(self, name):

        #Porcentagens para permitir busca com termo parcial
        name_search = f"%{name}%"

        query = """
            SELECT
                CD_PRODUTo,
                DS_PRODUTO,
                QT_ESTOQUE_ATUAL,
                SN_MEDICAMENTO,
                TP_STATUS_UNIFICADO
            FROM PRODUTO WHERE DS_PRODUTO LIKE :name"""

        binds = {"name": name_search}

        return Database.execute(query, binds)

# Exporta uma instância (Singleton)
repository = GenericRepository()
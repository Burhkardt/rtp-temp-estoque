from app.database.connection import Database

class ProductRepository:

    # =========================
    # LISTAR TODOS OS PRODUTOS
    # =========================
    def select_all_products(self):

        conn = Database.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                CD_PRODUTO,
                DS_PRODUTO,
                QT_ESTOQUE_ATUAL,
                SN_MEDICAMENTO,
                TP_STATUS_UNIFICADO
            FROM PRODUTO
        """)

        rows = cursor.fetchall()

        conn.close()

        products = []

        for row in rows:
            products.append({
                "cd_produto": row[0],
                "ds_produto": row[1],
                "qt_estoque_atual": row[2],
                "sn_medicamento": row[3],
                "tp_status_unificado": row[4]
            })

        return products

    # =========================
    # BUSCAR PRODUTO POR ID
    # =========================
    def select_one_product(self, id):

        conn = Database.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                CD_PRODUTO,
                DS_PRODUTO,
                QT_ESTOQUE_ATUAL,
                SN_MEDICAMENTO,
                TP_STATUS_UNIFICADO
            FROM PRODUTO
            WHERE CD_PRODUTO = ?
        """, (id,))

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return {
            "cd_produto": row[0],
            "ds_produto": row[1],
            "qt_estoque_atual": row[2],
            "sn_medicamento": row[3],
            "tp_status_unificado": row[4]
        }

    # =========================
    # ESTOQUES DE UM PRODUTO
    # =========================
    def select_all_stocks_of_one_product(self, product_id):

        conn = Database.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                ID,
                CD_ESTOQUE,
                CD_LOCALIZACAO,
                QT_ESTOQUE_ATUAL,
                DS_LOCALIZACAO_PRATELEIRA,
                DT_ULTIMA_MOVIMENTACAO
            FROM EST_PRO
            WHERE CD_PRODUTO = ?
        """, (product_id,))

        rows = cursor.fetchall()

        conn.close()

        stocks = []

        for row in rows:
            stocks.append({
                "id": row[0],
                "cd_estoque": row[1],
                "cd_localizacao": row[2],
                "qt_estoque_atual": row[3],
                "ds_localizacao_prateleira": row[4],
                "dt_ultima_movimentacao": row[5]
            })

        return stocks

    # =========================
    # PRODUTOS DE UM ESTOQUE
    # =========================
    def select_all_products_of_one_stock(self, stock_id):

        conn = Database.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.CD_PRODUTO,
                p.DS_PRODUTO,
                e.QT_ESTOQUE_ATUAL,
                e.CD_LOCALIZACAO,
                e.DS_LOCALIZACAO_PRATELEIRA,
                e.DT_ULTIMA_MOVIMENTACAO
            FROM EST_PRO e
            INNER JOIN PRODUTO p
                ON p.CD_PRODUTO = e.CD_PRODUTO
            WHERE e.CD_ESTOQUE = ?
        """, (stock_id,))

        rows = cursor.fetchall()

        conn.close()

        products = []

        for row in rows:
            products.append({
                "cd_produto": row[0],
                "ds_produto": row[1],
                "qt_estoque_atual": row[2],
                "cd_localizacao": row[3],
                "ds_localizacao_prateleira": row[4],
                "dt_ultima_movimentacao": row[5]
            })

        return products


repository = ProductRepository()
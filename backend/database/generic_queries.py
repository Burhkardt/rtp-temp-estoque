from connection import Database

class GenericRepository:
    def __init__(self):
        self.allowed_tables = ['produto', 'est_pro']

    #Verificador de segurança para que apenas tabelas permitidas sejam pesquisadas
    def _check_table(self, table):
        if table.lower() not in self.allowed_tables:
            raise ValueError(f"Acesso negado ou nome errado: {table}")

    def select_all(self, table):
        self._check_table(table)
        query = f"SELECT * FROM {table}"
        return Database.execute(query)

    def select_by_id(self, table, record_id):
        self._check_table(table)
        # Em Oracle Python, usamos :nome para binds, igual ao Node
        query = f"SELECT * FROM {table} WHERE id = :id"
        binds = {"id": record_id}
        result = Database.execute(query, binds)
        return result[0] if result else None
    
    def select_by_name(self, table, name):
        self._check_table(table)

        #Porcentagens para permitir busca com termo parcial
        name_search = f"%{name}%"

        query = f"SELECT * FROM {table} WHERE DS_PRODUTO LIKE :name"

        binds = {"name": name_search}

        return Database.execute(query, binds)

# Exporta uma instância (Singleton)
repository = GenericRepository()
from ..config.settings import *
import oracledb

#Função que garante 
def init_session(connection, requested_tag):
    with connection.cursor() as cursor:
        cursor.execute("ALTER SESSION SET NLS_COMP = 'LINGUISTIC'")
        cursor.execute("ALTER SESSION SET NLS_SORT = 'BINARY_AI'")

class Database:
    _pool = None

    @classmethod
    def initialize(cls):
        #Inicializa os acessos ao banco
        if cls._pool is None:
            cls._pool = oracledb.create_pool(
                user=DB_USER,
                password=DB_PASS,
                dsn=DB_DSN,
                min=2,
                max=20,
                increment=2,
                session_callback=init_session
            )
    @classmethod
    def execute(cls, sql, binds=None):
        if cls._pool is None:
            cls.initialize()

        with cls._pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.rowfactory = lambda *args: dict(zip([d[0].lower() for d in cursor.description], args))

                cursor.execute(sql, binds or {})

                if sql.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
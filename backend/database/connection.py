from ..config.settings import *
import oracledb

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
                increment=2
            )
    @classmethod
    def execute(cls, sql, binds=None):
        if cls._pool is None:
            cls.initialize

        with cls._pool.acquire() as conn:
            with conn.cursor() as cursor:
                
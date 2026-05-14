import sqlite3
import os

# Caminho absoluto da pasta atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho do banco
DATABASE_NAME = os.path.join(BASE_DIR, "database.db")


class Database:

    @staticmethod
    def connect():
        return sqlite3.connect(DATABASE_NAME)

    @staticmethod
    def execute(query, binds=None):

        conn = Database.connect()
        cursor = conn.cursor()

        if binds:
            cursor.execute(query, binds)
        else:
            cursor.execute(query)

        columns = [column[0] for column in cursor.description] if cursor.description else []

        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        conn.commit()
        conn.close()

        return results
from app.database.connection import Database

conn = Database.connect()
cursor = conn.cursor()

# =========================
# PRODUTOS
# =========================

produtos = [
    (1, "Luva Cirúrgica", 150, "S", "ATIVO"),
    (2, "Seringa 10ml", 300, "N", "ATIVO"),
    (3, "Máscara Descartável", 500, "N", "ATIVO")
]

cursor.executemany("""
INSERT INTO PRODUTO (
    CD_PRODUTO,
    DS_PRODUTO,
    QT_ESTOQUE_ATUAL,
    SN_MEDICAMENTO,
    TP_STATUS_UNIFICADO
)
VALUES (?, ?, ?, ?, ?)
""", produtos)

# =========================
# ESTOQUES
# =========================

estoques = [
    (1, 1, 101, 150, "Prateleira A1", "2026-05-13"),
    (2, 1, 102, 50, "Prateleira B1", "2026-05-13"),
    (2, 2, 201, 300, "Prateleira C2", "2026-05-12"),
    (3, 3, 301, 500, "Prateleira D4", "2026-05-10")
]

cursor.executemany("""
INSERT INTO EST_PRO (
    CD_PRODUTO,
    CD_ESTOQUE,
    CD_LOCALIZACAO,
    QT_ESTOQUE_ATUAL,
    DS_LOCALIZACAO_PRATELEIRA,
    DT_ULTIMA_MOVIMENTACAO
)
VALUES (?, ?, ?, ?, ?, ?)
""", estoques)

conn.commit()
conn.close()

print("Banco populado com sucesso!")
import sqlite3

db_path = r"c:\Users\Service Desk\Documents\GitHub\ecommerce_loja_flex\ecommerce.db"

con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cur.fetchall()

print("Tabelas existentes no banco:")
for tabela in tabelas:
    print("-", tabela[0])

con.close()

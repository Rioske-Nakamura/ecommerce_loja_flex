import sqlite3

with open('criar_banco.sql', 'r', encoding='utf-8') as f:
    script_sql = f.read()

con = sqlite3.connect('ecommerce.db')
con.executescript(script_sql)
con.commit()
con.close()

print("Banco de dados criado com sucesso ✅")

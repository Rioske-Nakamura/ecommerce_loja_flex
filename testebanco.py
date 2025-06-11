import sqlite3

conn = sqlite3.connect('c:/Users/Service Desk/Documents/GitHub/ecommerce_loja_flex/ecommerce.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos';")
table_exists = cursor.fetchone()

if table_exists:
    print("A tabela 'produtos' existe.")
else:
    print("A tabela 'produtos' não existe.")

conn.close()

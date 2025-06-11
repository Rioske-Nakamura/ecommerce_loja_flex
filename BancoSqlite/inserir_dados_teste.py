import sqlite3

CAMINHO_DB = "ecommerce.db"

conn = sqlite3.connect(CAMINHO_DB)
cur = conn.cursor()

# Inserir usuário ADM
cur.execute("""
    INSERT INTO usuarios (nome, email, senha, tipo)
    VALUES (?, ?, ?, ?)
""", ("Administrador", "admin@teste.com", "1234", "adm"))

# Inserir loja
cur.execute("""
    INSERT INTO lojas (nome)
    VALUES (?)
""", ("Loja Teste",))

loja_id = cur.lastrowid

# Vincular usuário à loja como vendedor
cur.execute("""
    INSERT INTO loja_vendedor (loja_id, usuario_id)
    VALUES (?, ?)
""", (loja_id, 1))  # 1 = ID do primeiro usuário (ADM recém-criado)

# Inserir produtos
produtos = [
    ("Produto 1", "Descrição do produto 1", 19.90, "https://via.placeholder.com/150", loja_id),
    ("Produto 2", "Descrição do produto 2", 29.90, "https://via.placeholder.com/150", loja_id),
    ("Produto 3", "Descrição do produto 3", 9.99, "https://via.placeholder.com/150", loja_id)
]

cur.executemany("""
    INSERT INTO produtos (nome, descricao, preco, imagem, loja_id)
    VALUES (?, ?, ?, ?, ?)
""", produtos)

conn.commit()
conn.close()

print("Dados de teste inseridos com sucesso.")

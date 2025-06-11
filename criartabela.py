import sqlite3

conn = sqlite3.connect('ecommerce.db')
cur = conn.cursor()

# Criar tabela de usuários
cur.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
)
''')

# Criar tabela de lojas
cur.execute('''
CREATE TABLE IF NOT EXISTS lojas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

# Criar tabela de produtos
cur.execute('''
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    descricao TEXT,
    preco REAL,
    imagem TEXT,
    loja_id INTEGER,
    status TEXT
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS loja_vendedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loja_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (loja_id) REFERENCES lojas (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
)
''')

# Criar tabela do carrinho (opcional)
cur.execute('''
CREATE TABLE IF NOT EXISTS carrinho (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
''')

conn.commit()
conn.close()

print("Banco de dados inicializado com sucesso.")

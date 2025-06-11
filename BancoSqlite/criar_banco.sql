-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('cliente', 'vendedor', 'adm')) NOT NULL
);

-- Tabela de lojas
CREATE TABLE IF NOT EXISTS lojas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

-- Ligação entre vendedores e lojas
CREATE TABLE IF NOT EXISTS loja_vendedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    loja_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (loja_id) REFERENCES lojas(id)
);

-- Tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    imagem TEXT,
    loja_id INTEGER,
    status TEXT CHECK(status IN ('ativo', 'inativo')) NOT NULL DEFAULT 'ativo',
    FOREIGN KEY (loja_id) REFERENCES lojas(id)
);

-- Tabela de compras
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER,
    status TEXT CHECK(status IN ('pendente', 'pago', 'cancelado')) NOT NULL DEFAULT 'pendente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

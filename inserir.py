from banco import Session, Usuario, Loja, Produto, Pedido

session = Session()

# Inserir usuários
usuario1 = Usuario(nome="Alice", email="alice@email.com", senha="123", tipo="cliente")
usuario2 = Usuario(nome="Bob", email="bob@email.com", senha="123", tipo="vendedor")
usuario3 = Usuario(nome="Carol", email="carol@email.com", senha="123", tipo="adm")
session.add_all([usuario1, usuario2, usuario3])
session.commit()

# Inserir loja para Bob
loja1 = Loja(nome="Loja do Bob", dono_id=usuario2.id, CNPJ="12345678900001", descricao="Loja de eletrônicos", ramo="Eletrônicos")
session.add(loja1)
session.commit()

# Inserir produtos
produto1 = Produto(nome="Celular", descricao="Smartphone XYZ", preco=1200.0, loja_id=loja1.id)
produto2 = Produto(nome="Notebook", descricao="Notebook ABC", preco=3500.0, loja_id=loja1.id)
produto3 = Produto(nome="Fone de ouvido", descricao="Fone Bluetooth", preco=250.0, loja_id=loja1.id)
session.add_all([produto1, produto2, produto3])
session.commit()

# Inserir pedidos no carrinho da Alice
pedido1 = Pedido(cliente_id=usuario1.id, produto_id=produto1.id, carrinho=True)
pedido2 = Pedido(cliente_id=usuario1.id, produto_id=produto2.id, carrinho=True)
session.add_all([pedido1, pedido2])
session.commit()

# Inserir pedido já finalizado
pedido3 = Pedido(cliente_id=usuario1.id, produto_id=produto3.id, carrinho=False, status="pago")
session.add(pedido3)
session.commit()

session.close()

print("Dados inseridos com sucesso.")

# banco.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, scoped_session

# Configuração do banco
engine = create_engine("sqlite:///banco.db", echo=False)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# Modelos

class Loja(Base):
    __tablename__ = "lojas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, unique=True)
    CNPJ = Column(String, unique=True, nullable=True)
    descricao = Column(String, nullable=True)
    ramo = Column(String, nullable=True)
    dono_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    produtos = relationship("Produto", backref="loja", cascade="all, delete-orphan")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    ativo = Column(Boolean, default=True)
    tipo = Column(String)

    lojas = relationship("Loja", backref="dono", cascade="all, delete-orphan")
    pedidos = relationship("Pedido", backref="cliente", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
            "ativo": self.ativo
        }

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(String)
    preco = Column(Float)
    imagem = Column(String, nullable=True)
    status = Column(String, default="ativo")
    loja_id = Column(Integer, ForeignKey("lojas.id"))
    pedidos = relationship("Pedido", backref="produto", cascade="all, delete-orphan")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    status = Column(String, default="pendente")  # pendente, pago, expirado
    carrinho = Column(Boolean, default=True)  # se True está no carrinho, se False foi finalizado

# Cria tabelas
Base.metadata.create_all(bind=engine)

# Funções utilitárias

def criar_usuario(nome, email, senha, tipo="cliente", ativo=True):
    session = Session()
    novo = Usuario(nome=nome, email=email, senha=senha, tipo=tipo, ativo=ativo)
    session.add(novo)
    session.commit()
    session.close()

def autenticar_usuario(email, senha):
    session = Session()
    usuario = session.query(Usuario).filter_by(email=email, senha=senha).first()
    session.close()
    return usuario

def criar_loja(nome, dono_id, CNPJ=None, descricao=None, ramo=None):
    session = Session()
    nova = Loja(nome=nome, dono_id=dono_id, CNPJ=CNPJ, descricao=descricao, ramo=ramo)
    session.add(nova)
    session.commit()
    session.close()

def listar_lojas(dono_id=None):
    session = Session()
    if dono_id:
        lojas = session.query(Loja).filter_by(dono_id=dono_id).all()
    else:
        lojas = session.query(Loja).all()
    session.close()
    return lojas

def criar_produto(nome, descricao, preco, loja_id, imagem=None, status="ativo"):
    session = Session()
    novo = Produto(nome=nome, descricao=descricao, preco=preco, loja_id=loja_id, imagem=imagem, status=status)
    session.add(novo)
    session.commit()
    session.close()

def listar_produtos(ativos=True):
    session = Session()
    if ativos:
        produtos = session.query(Produto).filter_by(status="ativo").all()
    else:
        produtos = session.query(Produto).all()
    session.close()
    return produtos

def excluir_produto(produto_id, usuario):
    session = Session()
    produto = session.query(Produto).get(produto_id)
    if produto and (usuario.tipo == 'adm' or produto.loja.dono_id == usuario.id):
        session.delete(produto)
        session.commit()
    session.close()

def editar_produto(produto_id, usuario, **kwargs):
    session = Session()
    produto = session.query(Produto).get(produto_id)
    if produto and (usuario.tipo == 'adm' or produto.loja.dono_id == usuario.id):
        for key, value in kwargs.items():
            setattr(produto, key, value)
        session.commit()
    session.close()

def excluir_loja(loja_id, usuario):
    session = Session()
    loja = session.query(Loja).get(loja_id)
    if loja and (usuario.tipo == 'adm' or loja.dono_id == usuario.id):
        session.delete(loja)
        session.commit()
    session.close()

def editar_loja(loja_id, usuario, **kwargs):
    session = Session()
    loja = session.query(Loja).get(loja_id)
    if loja and (usuario.tipo == 'adm' or loja.dono_id == usuario.id):
        for key, value in kwargs.items():
            setattr(loja, key, value)
        session.commit()
    session.close()

def listar_usuarios():
    session = Session()
    usuarios = session.query(Usuario).all()
    session.close()
    return usuarios

def excluir_usuario(usuario_id, solicitante):
    session = Session()
    if solicitante.tipo == 'adm':
        usuario = session.query(Usuario).get(usuario_id)
        if usuario:
            session.delete(usuario)
            session.commit()
    session.close()

def editar_usuario(usuario_id, solicitante, **kwargs):
    session = Session()
    if solicitante.tipo == 'adm':
        usuario = session.query(Usuario).get(usuario_id)
        if usuario:
            for key, value in kwargs.items():
                setattr(usuario, key, value)
            session.commit()
    session.close()

def adicionar_ao_carrinho(cliente_id, produto_id):
    session = Session()
    carrinho_item = Pedido(cliente_id=cliente_id, produto_id=produto_id, carrinho=True, status="pendente")
    session.add(carrinho_item)
    session.commit()
    session.close()

def listar_carrinho(cliente_id):
    session = Session()
    itens = session.query(Pedido).filter_by(cliente_id=cliente_id, carrinho=True).all()
    session.close()
    return itens

def finalizar_compra(cliente_id):
    session = Session()
    itens = session.query(Pedido).filter_by(cliente_id=cliente_id, carrinho=True).all()
    for item in itens:
        item.carrinho = False
    session.commit()
    session.close()

def alterar_status_pedido(pedido_id, usuario, novo_status):
    session = Session()
    pedido = session.query(Pedido).get(pedido_id)
    if pedido and usuario.tipo in ['vendedor', 'adm']:
        if usuario.tipo == 'adm' or pedido.produto.loja.dono_id == usuario.id:
            pedido.status = novo_status
            session.commit()
    session.close()


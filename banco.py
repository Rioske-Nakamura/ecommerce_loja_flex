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

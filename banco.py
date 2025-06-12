from sqlalchemy import Column, Integer, String, DateTime, Float,create_engine,  Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

db =  create_engine("sqlite:///banco.db")
Session =   sessionmaker(bind=db)
session =  Session()

Base  = declarative_base()

class Loja(Base):
    __tablename__ = "lojas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome =  Column(String, unique=True )
    CNPJ = Column(String, unique=True )
    descricao =  Column(String )
    ramo = Column(String)

    def __init__ ( self, nome,CNPJ, descricao, ramo) :
        
        self.nome = nome
        self.CNPJ = CNPJ
        self.descricao = descricao
        self.ramo = ramo



class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, unique=True)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    tipo = Column("tipo", String)

    def __init__(self, nome, email, senha, tipo, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.tipo = tipo

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
            "ativo": self.ativo
        }

    def __repr__(self):
        return str(self.to_dict())


class Produto(Base):
    __tablename__ = "produtos"
    id =  Column('id', Integer, primary_key=True,autoincrement=True)
    nome = Column("nome",String)
    descricao = Column("descricao",String)
    preco = Column("preco", Float)
    dono = Column("dono", ForeignKey("lojas.id"))

    def __init__(self, nome,descricao, preco, dono):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.dono =  dono 

Base.metadata.create_all(bind=db)


#cria
#usuarios =  Usuario(nome="Felipe", email="sql@gmail.com", senha="1234", tipo="")
#session.add(usuarios)
#session.commit()


#puxa 
lista_user = session.query(Usuario).all()
print(lista_user)
#lista_user = session.query(Usuario).all().filter_by()
#lista_user = session.query(Usuario).all().first
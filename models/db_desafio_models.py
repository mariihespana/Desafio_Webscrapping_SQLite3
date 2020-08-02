from sqlalchemy import create_engine, Column, Integer, String, Sequence, Numeric, ForeignKey, desc
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.base_desafio import Base

def configurar_banco_de_dados():

    # Para criar um banco de dados SQLite3
    engine = create_engine('sqlite:///produtos.db', echo = True)
    Base.metadata.drop_all(bind = engine) # Usa-se essa linha caso queira recriar todas as tabelas
    Base.metadata.create_all(bind = engine) # Verifica se vc ja possui um banco de dados e se alguma das informações ja foi criada, ele pula a informação e não recria a tabela

    # Criando uma conexao
    Conexao = sessionmaker(bind=engine)
    conexao = Conexao()
    conexao: sessionmaker
    return conexao

def criar_produto(conexao, nome, descricao, preco):
    novo_produto = Produtos()
    novo_produto.nome = nome
    novo_produto.descricao = descricao
    novo_produto.preco = preco
    conexao.add(novo_produto)
    conexao.commit()

class Produtos(Base):
    __tablename__ = 'produtos'
    produto_id = Column(Integer, Sequence(
        'artista_id_auto_incremento', start = 1), primary_key = True)
    nome = Column(String)
    descricao = Column(String)
    preco = Column(Numeric)

def buscar_todos_produtos(conexao):
    for item in conexao.query(Produtos).all(): # nome da classe
        print(item.nome, item.descricao, item.preco)
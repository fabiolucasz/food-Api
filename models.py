from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    preco = Column(Float)
    descricao = Column(String)
    imagem = Column(String)
    categoria = Column(String)
    qnt_estoque = Column(Integer)
    disponibilidade = Column(Boolean, default=True)

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from database import SessionLocal, engine
from models import Produto, Base
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema de validação para a entrada de dados
class ProdutoSchema(BaseModel):
    id: Optional[int]
    nome: str
    preco: float
    descricao: str
    imagem: str
    categoria: str
    qnt_estoque: int
    disponibilidade: bool

    class Config:
        from_attributes = True  # Habilita o suporte para conversão de ORM para JSON

# Rota para criar um produto
@app.post("/admin/cadastrar/", response_model=ProdutoSchema)
def criar_produto(produto: ProdutoSchema, db: Session = Depends(get_db)):
    novo_produto = Produto(

        nome=produto.nome,
        preco=produto.preco,
        descricao=produto.descricao,
        imagem=produto.imagem,
        categoria=produto.categoria,
        qnt_estoque=produto.qnt_estoque,
        disponibilidade=produto.disponibilidade
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return jsonable_encoder(novo_produto)  # Retorna o produto criado em JSON

# Rota para listar todos os produtos
@app.get("/admin/produtos", response_model=List[ProdutoSchema])
def listar_produtos_admin(db: Session = Depends(get_db)) -> list:
    produtos = db.query(Produto).all()
    return jsonable_encoder(produtos)  # Retorna a lista de produtos em JSON

# Rota para listar produto por ID
@app.get("/admin/produtos/{produto_id}", response_model=ProdutoSchema)
def listar_produto_por_id(produto_id: int, db: Session = Depends(get_db)) -> dict:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return jsonable_encoder(produto)  # Retorna o produto em JSON

# Rota para listar produtos por categoria
@app.get("/admin/produtos/categoria/{categoria}", response_model=List[ProdutoSchema])
def listar_produtos_por_categoria(categoria: str, db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.categoria == categoria).all()
    if not produtos:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado para essa categoria")
    return jsonable_encoder(produtos)  # Retorna a lista de produtos em JSON

@app.put("/admin/produtos/{id}/")
async def update_product(id: int, produto: ProdutoSchema, db: Session = Depends(get_db)):
    produto_existente = db.query(Produto).filter(Produto.id == id).first()
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in produto.dict().items():
        setattr(produto_existente, key, value)
    db.commit()
    db.refresh(produto_existente)
    return produto_existente

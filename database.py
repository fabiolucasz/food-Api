from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão ao PostgreSQL (altere conforme necessário)
DATABASE_URL = "postgresql://postgres:1234@localhost/fastfood"

# Configuração do engine para PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

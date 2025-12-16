# app/database.py
from sqlalchemy import create_engine # para criar a engine do banco de dados
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # carrega .env na inicialização do módulo

# Exemplo de valor esperado em .env:
# DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/biblioteca
DATABASE_URL = os.getenv( "DATABASE_URL")

# create_engine: future=True ativa comportamentos compatíveis com SQLAlchemy 2.0
engine = create_engine(DATABASE_URL, echo=False, future=True)

# SessionLocal: instâncias ligadas à engine
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    future=True
)

# Base declarativa para seus models
Base = declarative_base()




# def init_db(create_tables: bool = True) -> None:
#     """
#     Inicializa o banco localmente (cria tabelas via metadata).
#     Se você usa Alembic, não é recomendado chamar init_db() automaticamente em produção.
#     """
#     if create_tables:
#         # importe os módulos que registram os models antes de criar as tabelas
#         # Exemplo: from app.models import livro, usuario, emprestimo, reserva, multa
#         # Import dinâmico para evitar import cycles na carga inicial do pacote
#         try:
#             # importa todos os modules que registrem classes no Base
#             import importlib
#             importlib.import_module("app.models.livro")
#             importlib.import_module("app.models.usuario")
#             importlib.import_module("app.models.emprestimo")
#             importlib.import_module("app.models.reserva")
#             importlib.import_module("app.models.multa")
#         except Exception:
#             # Se você estiver usando um layout diferente de nomes, ajuste aqui.
#             pass

#         Base.metadata.create_all(bind=engine)

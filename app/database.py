from sqlalchemy import create_engine # para criar a engine do banco de dados
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # carrega .env na inicialização do módulo

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


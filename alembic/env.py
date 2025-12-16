# alembic/env.py
from logging.config import fileConfig
import os
import sys
from sqlalchemy import pool
from sqlalchemy import engine_from_config
from alembic import context # cerebro do alembic
from dotenv import load_dotenv

# carrega .env (se existir)
load_dotenv()

# adiciona raiz do projeto ao path para importar app.*
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# carrega o alembic config
config = context.config
fileConfig(config.config_file_name)

# pegar DATABASE_URL do ambiente (.env) — fallback vazio
DATABASE_URL = os.getenv("DATABASE_URL", "")

# importa metadata da app (certifique-se que app.models registra todas as classes no Base)
from app.database import Base
target_metadata = Base.metadata
from app.models import livro, usuario, emprestimo, multa, reserva


def run_migrations_offline():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL não definida. Defina no .env ou em variável de ambiente.")
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL não definida. Defina no .env ou em variável de ambiente.")

    # PASSO CORRIGIDO: engine_from_config espera uma chave 'url' quando prefix="".
    # Usamos {"url": DATABASE_URL} e future=True para compatibilidade SQLAlchemy 2.x.
    connectable = engine_from_config(
        {"url": DATABASE_URL},
        prefix="",
        poolclass=pool.NullPool, #evita conexões zumbis, úteis em scripts de migração
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,          #detecta mudanças de tipo
            compare_server_default=True, #detecta default no banco
        )
        with context.begin_transaction(): #Transação, Ou tudo aplica, ou nada aplica. Banco gosta disso.
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# app/deps.py (síncrono)
from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal

def get_db() -> Generator[Session, None, None]: #essa função vai gerar um Session, não recebe nada no send, e não retorna valor final.
    """
    Dependência FastAPI que fornece uma sessão por requisição.
    Uso típico:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_db
from app import models

def get_current_user(db: Session = Depends(get_db)):
    """
    TEMPORÁRIO:
    Retorna um usuário qualquer do banco.
    Depois isso vira JWT.
    """
    usuario = db.query(models.Usuario).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado."
        )

    return usuario

from fastapi import Depends, HTTPException, status
from app.models import Usuario
from app.security import get_current_user  # JWT, sessão etc.

def usuario_logado(
    usuario: Usuario = Depends(get_current_user)
):
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado."
        )
    return usuario

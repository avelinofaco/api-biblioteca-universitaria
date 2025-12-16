from fastapi import Depends, HTTPException, status
from app.dependencies.auth import usuario_logado
from app.models import Usuario


#recebe um usuário real
#valida o papel
#barra corretamente
def exigir_roles(*roles):
    def checker(usuario: Usuario = Depends(usuario_logado)):
        role_usuario = usuario.role.value if hasattr(usuario.role, "value") else usuario.role

        if role_usuario not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente para essa ação."
            )
        return usuario
    return checker


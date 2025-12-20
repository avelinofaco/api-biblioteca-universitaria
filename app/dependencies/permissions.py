from fastapi import Depends, HTTPException, status
from app.deps import get_current_user

#recebe um usuário real
#valida o papel
#barra corretamente
def exigir_roles(*roles):
    def role_checker(
        current_user = Depends(get_current_user)
    ):
        if current_user.role.value not in roles: #controle de acesso no nível da rota
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente"
            )
        return current_user
    return role_checker

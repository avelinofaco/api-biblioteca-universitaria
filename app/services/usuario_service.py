from sqlalchemy.orm import Session
from app.crud import usuario as usuario_crud
from app.services.exceptions import NotFoundError

def criar_usuario_service(db: Session, payload):
    return usuario_crud.create(db, payload)


def listar_usuarios_service(db: Session, skip: int = 0, limit: int = 50):
    items = usuario_crud.get_all(db, skip, limit)
    total = usuario_crud.count(db)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


def recuperar_usuario_service(db: Session, usuario_id: int):
    usuario = usuario_crud.get_by_id(db, usuario_id)
    if not usuario:
        raise NotFoundError("Usuário não encontrado.")
    return usuario


def atualizar_usuario_service(db: Session, usuario_id: int, payload):
    usuario = usuario_crud.update(db, usuario_id, payload)
    if not usuario:
        raise NotFoundError("Usuário não encontrado.")
    return usuario


def remover_usuario_service(db: Session, usuario_id: int):
    ok = usuario_crud.delete(db, usuario_id)
    if not ok:
        raise NotFoundError("Usuário não encontrado.")


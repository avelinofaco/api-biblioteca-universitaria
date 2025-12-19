from sqlalchemy.orm import Session
from app.crud import multa as multa_crud
from app.schemas import PageMulta
from app.services.exceptions import NotFoundError, BusinessRuleError


def listar_multas_service(db: Session, skip: int, limit: int):
    total = multa_crud.contar(db)
    multas = multa_crud.listar(db, skip, limit)

    return PageMulta(
        total=total,
        skip=skip,
        limit=limit,
        items=multas
    )


def listar_multas_usuario_service(
    db: Session,
    usuario_id: int,
    skip: int,
    limit: int
):
    total = multa_crud.contar_por_usuario(db, usuario_id)
    multas = multa_crud.listar_por_usuario(db, usuario_id, skip, limit)

    return PageMulta(
        total=total,
        skip=skip,
        limit=limit,
        items=multas
    )


def listar_minhas_multas_service(
    db: Session,
    usuario_id: int,
    skip: int,
    limit: int
):
    return listar_multas_usuario_service(
        db=db,
        usuario_id=usuario_id,
        skip=skip,
        limit=limit
    )

def recuperar_multa_service(db: Session, multa_id: int):
    multa = multa_crud.get_by_id(db, multa_id)
    if not multa:
        raise NotFoundError("Multa não encontrada.")
    return multa


def pagar_multa_service(
    db: Session,
    multa_id: int,
    usuario_id: int
):
    multa = multa_crud.get_by_id(db, multa_id)

    if not multa:
        raise NotFoundError("Multa não encontrada.")

    if multa.usuario_id != usuario_id:
        raise BusinessRuleError("Você não pode pagar a multa de outro usuário.")

    if multa.paga:
        raise BusinessRuleError("Esta multa já foi paga.")

    return multa_crud.pagar_multa(db, multa_id)

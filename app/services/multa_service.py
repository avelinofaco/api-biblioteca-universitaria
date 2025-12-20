from sqlalchemy.orm import Session
from app.crud import multa as multa_crud
from app.schemas import PageMulta
from app.services import historico_service
from app.services.exceptions import NotFoundError, BusinessRuleError


# =========================
# LISTAGENS
# =========================

def listar_multas_service(db: Session, skip: int, limit: int):
    total = multa_crud.contar(db)
    items = multa_crud.listar(db, skip, limit)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


def listar_multas_usuario_service(
    db: Session,
    usuario_id: int,
    skip: int,
    limit: int
):
    total = multa_crud.contar_por_usuario(db, usuario_id)
    items = multa_crud.listar_por_usuario(db, usuario_id, skip, limit)
     
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


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


# =========================
# PAGAMENTO
# =========================

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

    if multa.paga_em is not None:
        raise BusinessRuleError("Esta multa já foi paga.")

    return multa_crud.marcar_como_paga(db, multa)

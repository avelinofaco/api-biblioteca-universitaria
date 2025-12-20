from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app import models, schemas


# =========================
# CONSULTAS
# =========================

def listar(db: Session, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Multa)
        .offset(skip)
        .limit(limit)
        .all()
    )


def listar_por_usuario(
    db: Session,
    usuario_id: int,
    skip: int = 0,
    limit: int = 50
):
    return (
        db.query(models.Multa)
        .filter(models.Multa.usuario_id == usuario_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def contar(db: Session) -> int:
    return db.query(models.Multa).count()


def contar_por_usuario(db: Session, usuario_id: int) -> int:
    return (
        db.query(models.Multa)
        .filter(models.Multa.usuario_id == usuario_id)
        .count()
    )

def get_by_id(db: Session, multa_id: int):
    return (
        db.query(models.Multa)
        .filter(models.Multa.id == multa_id)
        .first()
    )


def marcar_como_paga(db: Session, multa: models.Multa) -> models.Multa:
    """
    Marca a multa como paga.
    NÃO valida regra de negócio.
    NÃO verifica permissão.
    """
    multa.paga_em = datetime.now(timezone.utc)

    if hasattr(models.MultaStatus, "paga"):
        multa.status = models.MultaStatus.paga

    db.commit()
    db.refresh(multa)
    return multa


def update(db: Session, multa_id: int, multa: schemas.MultaUpdate):
    db_multa = get_by_id(db, multa_id)
    if not db_multa:
        return None

    for key, value in multa.model_dump(exclude_unset=True).items():
        setattr(db_multa, key, value)

    db.commit()
    db.refresh(db_multa)
    return db_multa


def delete(db: Session, multa_id: int) -> bool:
    db_multa = get_by_id(db, multa_id)
    if not db_multa:
        return False

    db.delete(db_multa)
    db.commit()
    return True

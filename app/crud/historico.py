from sqlalchemy.orm import Session
from app import models

def create(db: Session, historico: models.HistoricoComportamento):
    db.add(historico)
    db.flush()
    db.refresh(historico)
    return historico


def listar_por_usuario(
    db: Session,
    usuario_id: int,
    skip: int = 0,
    limit: int = 50
):
    return (
        db.query(models.HistoricoComportamento)
        .filter(models.HistoricoComportamento.usuario_id == usuario_id)
        .order_by(models.HistoricoComportamento.devolvido_em.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def listar_todos(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(models.HistoricoComportamento)
        .order_by(models.HistoricoComportamento.devolvido_em.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def contar_todos(db: Session) -> int:
    return db.query(models.HistoricoComportamento).count()


def contar_por_usuario(db: Session, usuario_id: int) -> int:
    return (
        db.query(models.HistoricoComportamento)
        .filter(models.HistoricoComportamento.usuario_id == usuario_id)
        .count()
    )

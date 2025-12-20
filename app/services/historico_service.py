from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from app import models
from app.crud import historico as historico_crud


def registrar_historico_devolucao(
    db: Session,
    *,
    usuario_id: int,
    emprestimo_id: int,
    devolvido_em: datetime,
    dias_atraso: int,
    multa_gerada: Decimal
) -> models.HistoricoComportamento:
    """
    Registra o histórico de comportamento referente à devolução de um empréstimo.
    Este método NÃO faz commit. A transação é controlada pelo service chamador.
    """

    if dias_atraso < 0:
        raise ValueError("dias_atraso não pode ser negativo.")
    
    print("🔥 REGISTRANDO HISTÓRICO 🔥", usuario_id, emprestimo_id)
    historico = models.HistoricoComportamento(
        usuario_id=usuario_id,
        emprestimo_id=emprestimo_id,
        devolvido_em=devolvido_em,
        estava_atrasado=dias_atraso > 0,
        dias_atraso=dias_atraso,
        multa_gerada=multa_gerada
    )

    return historico_crud.create(db, historico)

def listar_historico_usuario_service(
    db: Session,
    *,
    usuario_id: int,
    skip: int = 0,
    limit: int = 50
):
    total = historico_crud.contar_por_usuario(db, usuario_id)
    items = historico_crud.listar_por_usuario(
        db,
        usuario_id=usuario_id,
        skip=skip,
        limit=limit
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }

def listar_historico_geral_service(
    db: Session,
    skip: int,
    limit: int
):
    total = historico_crud.contar_todos(db)
    items = historico_crud.listar_todos(db, skip, limit)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


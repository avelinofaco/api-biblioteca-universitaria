from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app import models, schemas

def get_all(db: Session):
    return db.query(models.Multa).all()

def get_by_id(db: Session, multa_id: int):
    return db.query(models.Multa).filter(models.Multa.id == multa_id).first()

def get_by_usuario(db: Session, usuario_id: int):
    return db.query(models.Multa).filter(models.Multa.usuario_id == usuario_id).all()

def pagar_multa(db: Session, multa_id: int):
    """
    Marca a multa como paga:
     - define `paga_em` com o timestamp atual (autoridade de pagamento)
     - tenta também atualizar `status` para `MultaStatus.paga` se esse membro existir
    Retorna a multa atualizada ou None se já paga/nao existente.
    """
    multa = get_by_id(db, multa_id)
    if not multa:
        return None

    # se já tiver data de pagamento, considerar como já paga
    if getattr(multa, "paga_em", None) is not None:
        return None

    # marca como paga
    multa.paga_em = datetime.now(timezone.utc)

    # tenta atualizar o enum status para um valor "pago" se o enum definir isso.
    # fazemos em try/except para não quebrar caso o enum tenha outro nome.
    try:
        MultaStatus = getattr(models, "MultaStatus", None)
        if MultaStatus is not None and hasattr(MultaStatus, "paga"):
            multa.status = MultaStatus.paga
        # alternativa comum: "pago" em PT — checar essa opção também
        elif MultaStatus is not None and hasattr(MultaStatus, "pago"):
            multa.status = MultaStatus.pago
    except Exception:
        # não crucificar: se não for possível setar o enum, deixamos só a paga_em
        pass

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

def delete(db: Session, multa_id: int):
    db_multa = get_by_id(db, multa_id)
    if not db_multa:
        return None
    db.delete(db_multa)
    db.commit()
    return True

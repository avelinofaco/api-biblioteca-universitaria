from sqlalchemy.orm import Session
from app import models, schemas

def create(db: Session, reserva: schemas.ReservaCreate):
    db_res = models.Reserva(**reserva.model_dump())
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

def get_all(db: Session):
    return db.query(models.Reserva).all()

def get_by_id(db: Session, reserva_id: int):
    return db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()

def update(db: Session, reserva_id: int, reserva: schemas.ReservaUpdate):
    db_res = get_by_id(db, reserva_id)
    if not db_res:
        return None

    for key, value in reserva.model_dump(exclude_unset=True).items():
        setattr(db_res, key, value)

    db.commit()
    db.refresh(db_res)
    return db_res

def delete(db: Session, reserva_id: int):
    db_res = get_by_id(db, reserva_id)
    if not db_res:
        return None
    db.delete(db_res)
    db.commit()
    return True

def cancelar_reserva(db: Session, reserva_id: int):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not reserva or reserva.status == models.ReservaStatus.cancelada:
        return None  # o router trata como 404

    reserva.status = models.ReservaStatus.cancelada
    db.commit()
    db.refresh(reserva)
    return reserva  # <<< retornar o objeto, não True


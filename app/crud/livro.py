from sqlalchemy.orm import Session
from app import models, schemas

def create(db: Session, livro: schemas.LivroCreate):
    db_livro = models.Livro(**livro.model_dump())
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

def get_all(db: Session):
    return db.query(models.Livro).all()

def get_by_id(db: Session, livro_id: int):
    return db.query(models.Livro).filter(models.Livro.id == livro_id).first()

def update(db: Session, livro_id: int, livro: schemas.LivroUpdate):
    db_livro = get_by_id(db, livro_id)
    if not db_livro:
        return None

    for key, value in livro.model_dump(exclude_unset=True).items():
        setattr(db_livro, key, value)

    db.commit()
    db.refresh(db_livro)
    return db_livro

def delete(db: Session, livro_id: int):
    db_livro = get_by_id(db, livro_id)
    if not db_livro:
        return None
    db.delete(db_livro)
    db.commit()
    return True

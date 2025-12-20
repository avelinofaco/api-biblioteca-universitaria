from sqlalchemy.orm import Session
from app import models

def create(db: Session, data: dict) -> models.Livro:
    livro = models.Livro(**data)
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro

def existe_emprestimo_ativo_por_livro(db: Session, livro_id: int) -> bool:
    return (
        db.query(models.Emprestimo)
        .filter(
            models.Emprestimo.livro_id == livro_id,
            models.Emprestimo.status == models.EmprestimoStatus.ativo
        )
        .first()
        is not None
    )
 
def get_by_isbn(db: Session, isbn: str):
    return (
        db.query(models.Livro)
        .filter(models.Livro.isbn == isbn)
        .first()
    ) 

def get_all(db: Session, skip: int = 0, limit: int = 50) -> list[models.Livro]:
    return (
        db.query(models.Livro)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_by_id(db: Session, livro_id: int) -> models.Livro | None:
    return (
        db.query(models.Livro)
        .filter(models.Livro.id == livro_id)
        .first()
    )

def get_livro(db: Session, livro_id: int):
    return (db.query(models.Livro)
        .filter(models.Livro.id == livro_id)
        .first()
    )


def update(db: Session, livro_id: int, data: dict):
    db_livro = get_by_id(db, livro_id)
    if not db_livro:
        return None

    for key, value in data.items():
        setattr(db_livro, key, value)

    db.commit()
    db.refresh(db_livro)
    return db_livro


def delete(db: Session, livro):
    db.delete(livro)
    db.commit()


def count(db: Session) -> int:
    return db.query(models.Livro).count()

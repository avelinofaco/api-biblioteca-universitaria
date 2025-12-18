from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password

def create(db: Session, usuario: schemas.UsuarioCreate):
    dados = usuario.model_dump()
    dados["password"] = hash_password(dados["password"])

    db_usuario = models.Usuario(**dados)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
def get_all(db: Session):
    return db.query(models.Usuario).all()

def get_by_id(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def update(db: Session, usuario_id: int, usuario: schemas.UsuarioUpdate):
    db_usuario = get_by_id(db, usuario_id)
    if not db_usuario:
        return None

    for key, value in usuario.model_dump(exclude_unset=True).items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete(db: Session, usuario_id: int):
    db_usuario = get_by_id(db, usuario_id)
    if not db_usuario:
        return None
    db.delete(db_usuario)
    db.commit()
    return True


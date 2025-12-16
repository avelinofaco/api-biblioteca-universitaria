from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app import crud, schemas
from app.dependencies.permissions import exigir_roles
from app.deps import get_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED, description="So quem pode criar usuarios é o admin")
def criar_usuario(payload: schemas.UsuarioCreate, 
                db: Session = Depends(get_db),
                adim = Depends(exigir_roles("admin"))):
     return crud.usuario.create(db, payload)

@router.get("/", response_model=List[schemas.UsuarioOut])
def listar_usuarios(skip: int = 0, limit: int = 50, 
                    db: Session = Depends(get_db),
                    _ = Depends(exigir_roles("admin"))):
    usuarios = db.execute(select(crud.Usuario).offset(skip).limit(limit)).scalars().all()
    return usuarios

@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
def recuperar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    u = crud.get_usuario(db, usuario_id=usuario_id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return u


@router.put("/{usuario_id}", response_model=schemas.UsuarioOut, description="So quem pode atualizar usuarios é o admin ou bibliotecario")
def atualizar_usuario(usuario_id: int, payload: schemas.UsuarioUpdate, db: Session = Depends(get_db), _ = Depends(exigir_roles("admin","bibliotecario"))):
    u = crud.get_usuario(db, usuario_id=usuario_id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(u, field, value)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, description="So quem pode remover usuarios é o admin")
def remover_usuario(usuario_id: int, db: Session = Depends(get_db), _ = Depends(exigir_roles("admin"))):
    u = crud.get_usuario(db, usuario_id=usuario_id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(u)
    db.commit()
    return None


@router.get("/{usuario_id}/multas", response_model=list[schemas.MultaOut], description="Proprio usuario pode ver suas multas,ou admin e bibliotecario podem ver as multas de um usuario")
def multas_do_usuario(usuario_id: int, db: Session = Depends(get_db), _ = Depends(exigir_roles("aluno","admin","bibliotecario"))):
    multas = crud.listar_multas_usuario(db, usuario_id=usuario_id)
    return multas

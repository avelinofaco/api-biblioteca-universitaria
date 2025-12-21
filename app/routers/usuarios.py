from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app import crud, schemas
from app.dependencies.permissions import exigir_roles
from app.services import usuario_service
from app.deps import get_db
from app.services.exceptions import NotFoundError

router = APIRouter(prefix="/usuarios",tags=["usuarios"],dependencies=[Depends(exigir_roles("admin", "bibliotecario"))])


@router.post("/", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED, description="Somente admin ou bibliotecario podem criar usuarios")
def criar_usuario(payload: schemas.UsuarioCreate, 
                db: Session = Depends(get_db)):
     return crud.usuario.create(db, payload)


@router.get("/", response_model=schemas.PageUsuario, description="Somente admin ou bibliotecario podem listar usuarios")
def listar_usuarios(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    return usuario_service.listar_usuarios_service(db, skip, limit)


@router.get("/{usuario_id}", response_model=schemas.UsuarioOut, description="Somente admin ou bibliotecario podem recuperar usuarios")
def recuperar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return usuario_service.recuperar_usuario_service(db, usuario_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.put("/{usuario_id}", response_model=schemas.UsuarioOut, description="Somente admin ou bibliotecario podem atualizar usuarios")
def atualizar_usuario(
    usuario_id: int,
    payload: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
):
    try:
        return usuario_service.atualizar_usuario_service(db, usuario_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, description="Somente admin ou bibliotecario podem remover usuarios")
def remover_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        usuario_service.remover_usuario_service(db, usuario_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select

from app.crud import reserva as reserva_crud
from app import models, schemas
from app.deps import get_db
from app.dependencies.permissions import exigir_roles


router = APIRouter(prefix="/reservas", tags=["reservas"])

# Criar nova reserva
@router.post("/", response_model=schemas.ReservaOut, status_code=status.HTTP_201_CREATED, description= "aluno e bibliotecario podem criar reservas")
def criar_reserva(payload: schemas.ReservaCreate, db: Session = Depends(get_db), _ = Depends(exigir_roles("aluno", "bibliotecario"))):
    reserva = reserva_crud.create(db, payload)
    return reserva

# Cancelar reserva
@router.post("/{reserva_id}/cancelar", response_model=schemas.ReservaOut, description= "aluno, bibliotecario e admin podem cancelar reservas")
def cancelar_reserva(reserva_id: int, db: Session = Depends(get_db), _ = Depends(exigir_roles("aluno", "bibliotecario", "admin"))):
    reserva = reserva_crud.cancelar_reserva(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada ou já cancelada")
    return reserva

# Listar todas as reservas com paginação
@router.get("/", response_model=List[schemas.ReservaOut], description= "bibliotecario e admin podem listar reservas")
def listar_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _ = Depends(exigir_roles("bibliotecario", "admin"))):
    reservas = db.execute(
        select(models.Reserva).offset(skip).limit(limit)
    ).scalars().all()
    return reservas


# Listar reservas por livro
@router.get("/livro/{livro_id}", response_model=List[schemas.ReservaOut], description= "bibliotecario e admin podem listar reservas por livro")
def reservas_por_livro(livro_id: int, db: Session = Depends(get_db), _ = Depends(exigir_roles("bibliotecario", "admin"))):
    reservas = db.execute(
        select(models.Reserva)
        .where(models.Reserva.livro_id == livro_id)
        .order_by(models.Reserva.created_at)
    ).scalars().all()
    return reservas


# Buscar reserva por ID
@router.get("/{reserva_id}", response_model=schemas.ReservaOut, description= "bibliotecario, admin e aluno podem buscar reservas por ID")
def get_reserva(reserva_id: int, db: Session = Depends(get_db), _ = Depends(exigir_roles("bibliotecario", "admin", "aluno"))):
    reserva = reserva_crud.get_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva

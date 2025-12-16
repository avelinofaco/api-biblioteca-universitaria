from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select

from app.crud import reserva as reserva_crud
from app import models, schemas
from app.deps import get_db

router = APIRouter(prefix="/reservas", tags=["reservas"])

# Criar nova reserva
@router.post("/", response_model=schemas.ReservaOut, status_code=status.HTTP_201_CREATED)
def criar_reserva(payload: schemas.ReservaCreate, db: Session = Depends(get_db)):
    reserva = reserva_crud.create(db, payload)
    return reserva

# Cancelar reserva
@router.post("/{reserva_id}/cancelar", response_model=schemas.ReservaOut)
def cancelar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = reserva_crud.cancelar_reserva(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada ou já cancelada")
    return reserva

# Listar todas as reservas com paginação
@router.get("/", response_model=List[schemas.ReservaOut])
def listar_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservas = db.execute(
        select(models.Reserva).offset(skip).limit(limit)
    ).scalars().all()
    return reservas

# Listar reservas por livro
@router.get("/livro/{livro_id}", response_model=List[schemas.ReservaOut])
def reservas_por_livro(livro_id: int, db: Session = Depends(get_db)):
    reservas = db.execute(
        select(models.Reserva)
        .where(models.Reserva.livro_id == livro_id)
        .order_by(models.Reserva.created_at)
    ).scalars().all()
    return reservas

# Buscar reserva por ID
@router.get("/{reserva_id}", response_model=schemas.ReservaOut)
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = reserva_crud.get_by_id(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva

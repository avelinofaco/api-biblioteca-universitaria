from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select

from app.crud import multa as multa_crud
from app import models, schemas
from app.deps import get_db

router = APIRouter(prefix="/multas", tags=["multas"])

# Listar todas as multas
@router.get("/", response_model=List[schemas.MultaOut])
def listar_multas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    multas = db.execute(
        select(models.Multa).offset(skip).limit(limit)
    ).scalars().all()
    return multas

# Listar multas por usuário
@router.get("/usuario/{usuario_id}", response_model=List[schemas.MultaOut])
def multas_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    multas = db.execute(
        select(models.Multa)
        .where(models.Multa.usuario_id == usuario_id)
    ).scalars().all()
    return multas

# Pagar multa
@router.post("/{multa_id}/pagar", response_model=schemas.MultaOut)
def pagar_multa(multa_id: int, db: Session = Depends(get_db)):
    multa = multa_crud.pagar_multa(db, multa_id)
    if not multa:
        raise HTTPException(status_code=404, detail="Multa não encontrada ou já paga")
    return multa

# Buscar multa por ID
@router.get("/{multa_id}", response_model=schemas.MultaOut)
def get_multa(multa_id: int, db: Session = Depends(get_db)):
    multa = multa_crud.get_by_id(db, multa_id)
    if not multa:
        raise HTTPException(status_code=404, detail="Multa não encontrada")
    return multa

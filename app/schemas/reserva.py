# app/schemas/reserva.py (adicionar)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReservaCreate(BaseModel):
    usuario_id: int
    livro_id: int

class ReservaUpdate(BaseModel):
    posicao: Optional[int] = None
    status: Optional[str] = None

class ReservaOut(BaseModel):
    id: int
    usuario_id: int
    livro_id: int
    created_at: datetime
    posicao: int
    status: str

    class Config:
        orm_mode = True

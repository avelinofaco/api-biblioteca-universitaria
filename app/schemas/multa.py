# app/schemas/multa.py (adicionar)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List

class MultaCreate(BaseModel):
    emprestimo_id: int
    usuario_id: int
    valor: Decimal
    descricao: Optional[str] = None

class MultaUpdate(BaseModel):
    valor: Optional[Decimal] = None
    descricao: Optional[str] = None
    status: Optional[str] = None
    paga_em: Optional[datetime] = None

class MultaOut(BaseModel):
    id: int
    emprestimo_id: int
    usuario_id: int
    valor: Decimal
    descricao: Optional[str] = None
    status: str
    gerada_em: datetime
    paga_em: Optional[datetime] = None

class PageMulta(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[MultaOut]
    class Config:
        orm_mode = True

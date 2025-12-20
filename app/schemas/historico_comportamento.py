from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import List


class HistoricoComportamentoOut(BaseModel):
    id: int
    usuario_id: int
    emprestimo_id: int
    devolvido_em: datetime
    estava_atrasado: bool
    dias_atraso: int
    multa_gerada: Decimal

class PageHistoricoOut(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[HistoricoComportamentoOut]
    
    class Config:
        from_attributes = True


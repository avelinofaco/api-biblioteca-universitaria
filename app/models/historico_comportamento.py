from sqlalchemy import (Column, Integer, DateTime, Boolean, ForeignKey, Numeric)
from sqlalchemy.orm import relationship
from app.database import Base


class HistoricoComportamento(Base):
    __tablename__ = "historico_comportamento"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    emprestimo_id = Column(Integer, ForeignKey("emprestimos.id", ondelete="CASCADE"), nullable=False, index=True)
    devolvido_em = Column(DateTime(timezone=True), nullable=False)
    estava_atrasado = Column(Boolean, nullable=False)
    dias_atraso = Column(Integer, nullable=False, default=0)
    multa_gerada = Column(Numeric(10, 2), nullable=False, default=0)

    usuario = relationship("Usuario")
    emprestimo = relationship("Emprestimo")

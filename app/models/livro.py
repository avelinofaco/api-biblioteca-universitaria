from sqlalchemy import Column, Integer, String, DateTime, func, CheckConstraint, Index
from sqlalchemy.orm import relationship
from . import Base

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False, index=True)
    autor = Column(String(255), nullable=True)
    isbn = Column(String(32), unique=True, nullable=True, index=True)
    quantidade_total = Column(Integer, nullable=False, default=1)
    quantidade_disponivel = Column(Integer, nullable=False, default=1)
    area = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # relacionamentos
    emprestimos = relationship("Emprestimo", back_populates="livro", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="livro", cascade="all, delete-orphan")

    #Regras de integridade
    __table_args__ = (
        CheckConstraint("quantidade_total >= 0", name="chk_livro_quantidade_total_nonneg"), #A quantidade total nunca pode ser negativa.
        CheckConstraint("quantidade_disponivel >= 0", name="chk_livro_quantidade_disponivel_nonneg"),
        Index("ix_livro_titulo_autor", "titulo", "autor"), # Índice composto para buscas frequentes por título e autor
    )

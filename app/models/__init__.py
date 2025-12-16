# Importa o Base "único" definido em app.database para evitar múltiplos declarative_base()
from app.database import Base

# Importa módulos que registram as classes no Base
from .livro import Livro
from .usuario import Usuario, UsuarioRole
from .emprestimo import Emprestimo, EmprestimoStatus
from .reserva import Reserva, ReservaStatus
from .multa import Multa, MultaStatus

__all__ = [
    "Base",
    "Livro",
    "Usuario",
    "UsuarioRole",
    "Emprestimo",
    "EmprestimoStatus",
    "Reserva",
    "ReservaStatus",
    "Multa",
    "MultaStatus",
]

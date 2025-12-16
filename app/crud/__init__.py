# app/crud/__init__.py
# "Facade" para unificar a API do pacote crud com os routers existentes.

from app import models

# import dos submódulos
from . import usuario as usuario_mod
from . import livro as livro_mod
from . import emprestimo as emprestimo_mod
from . import reserva as reserva_mod
from . import multa as multa_mod

# --- funções em português esperadas pelos routers ---
# Usuarios
def criar_usuario(db, nome: str, email: str, role: str = "aluno"):
    # chama a implementação em crud/usuario.py (create)
    payload = {"nome": nome, "email": email, "role": role}
    # construir um pydantic-like dict se o módulo espera schemas; mas nosso crud/usuario.create aceita um schema.
    # para simplicidade, vamos delegar construindo um objeto compatível:
    from app.schemas import UsuarioCreate
    return usuario_mod.create(db, UsuarioCreate(**payload))

def listar_usuarios(db):
    return usuario_mod.get_all(db)

def get_usuario(db, usuario_id: int):
    return usuario_mod.get_by_id(db, usuario_id)

def atualizar_usuario(db, usuario_id: int, usuario_payload):
    # usuario_payload deve ser um pydantic model (UsuarioUpdate) vindo do router
    return usuario_mod.update(db, usuario_id, usuario_payload)

def deletar_usuario(db, usuario_id: int):
    return usuario_mod.delete(db, usuario_id)

# Livros
def criar_livro(db, titulo: str, autor: str = None, isbn: str = None, quantidade_total: int = 1, area: str = None):
    from app.schemas import LivroCreate
    payload = {"titulo": titulo, "autor": autor, "isbn": isbn, "quantidade_total": quantidade_total, "area": area}
    return livro_mod.create(db, LivroCreate(**payload))

def listar_livros(db):
    return livro_mod.get_all(db)

def get_livro(db, livro_id: int):
    return livro_mod.get_by_id(db, livro_id)

def atualizar_livro(db, livro_id: int, livro_payload):
    return livro_mod.update(db, livro_id, livro_payload)

def deletar_livro(db, livro_id: int):
    return livro_mod.delete(db, livro_id)

# Emprestimos (mapeia para funções básicas do módulo emprestimo)
def criar_emprestimo(db, usuario_id: int, livro_id: int, dias: int = 14):
    from app.schemas import EmprestimoCreate
    return emprestimo_mod.create(db, EmprestimoCreate(usuario_id=usuario_id, livro_id=livro_id, dias=dias))

def listar_emprestimos(db):
    return emprestimo_mod.get_all(db)

def get_emprestimo(db, emprestimo_id: int):
    return emprestimo_mod.get_by_id(db, emprestimo_id)

def atualizar_emprestimo(db, emprestimo_id: int, payload):
    return emprestimo_mod.update(db, emprestimo_id, payload)

def deletar_emprestimo(db, emprestimo_id: int):
    return emprestimo_mod.delete(db, emprestimo_id)

# Reservas
def criar_reserva(db, usuario_id: int, livro_id: int):
    from app.schemas import ReservaCreate
    return reserva_mod.create(db, ReservaCreate(usuario_id=usuario_id, livro_id=livro_id))

def listar_reservas(db):
    return reserva_mod.get_all(db)

def get_reserva(db, reserva_id: int):
    return reserva_mod.get_by_id(db, reserva_id)

def cancelar_reserva(db, reserva_id: int):
    # use update/delete conforme a implementação do seu módulo
    return reserva_mod.delete(db, reserva_id)

# Multas
def criar_multa(db, emprestimo_id: int, usuario_id: int, valor, descricao: str = None):
    from app.schemas import MultaCreate
    return multa_mod.create(db, MultaCreate(emprestimo_id=emprestimo_id, usuario_id=usuario_id, valor=valor, descricao=descricao))

def listar_multas(db):
    return multa_mod.get_all(db)

def listar_multas_usuario(db, usuario_id: int):
    """
    Retorna lista de Multa para um dado usuario_id.
    Implementação rápida no 'facade' para manter compatibilidade com routers.
    """
    return db.query(models.Multa).filter(models.Multa.usuario_id == usuario_id).all()

def get_multa(db, multa_id: int):
    return multa_mod.get_by_id(db, multa_id)

def atualizar_multa(db, multa_id: int, payload):
    return multa_mod.update(db, multa_id, payload)

def deletar_multa(db, multa_id: int):
    return multa_mod.delete(db, multa_id)

# --- Expor models e enums que alguns routers usam diretamente (ex.: select(crud.Livro)) ---
Livro = models.Livro
Usuario = models.Usuario
Emprestimo = models.Emprestimo
Reserva = models.Reserva
Multa = models.Multa

# Expor status/enums se o código os referir
try:
    EmprestimoStatus = models.EmprestimoStatus
    ReservaStatus = models.ReservaStatus
    MultaStatus = models.MultaStatus
except Exception:
    # se enums estiverem definidos nos próprios modelos de CRUD ou noutro lugar, ignore
    pass

# Nota: se algum router usar nomes diferentes, você pode adicionar aqui as funções correspondentes.

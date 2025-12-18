from sqlalchemy.orm import Session
from app.crud import livro as livro_crud
from app.crud import emprestimo as emprestimo_crud
from app.schemas import LivroCreate, LivroUpdate
from app.services.exceptions import BusinessRuleError, NotFoundError


def criar_livro_service(db: Session, livro_in: LivroCreate):
    existente = livro_crud.get_by_isbn(db, livro_in.isbn)
    if existente:
        raise BusinessRuleError("Já existe um livro com este ISBN.")

    return livro_crud.create(db, livro_in.model_dump())

def listar_livros_service(db: Session, skip: int = 0, limit: int = 50):
    items = livro_crud.get_all(db, skip=skip, limit=limit)
    total = livro_crud.count(db)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }


def recuperar_livro_service(db: Session, livro_id: int):
    livro = livro_crud.get_by_id(db, livro_id)
    if not livro:
        raise NotFoundError("Livro não encontrado.")

    return livro


def atualizar_livro_service(db: Session, livro_id: int, data: dict):
    atualizado = livro_crud.update(db, livro_id, data)
    if not atualizado:
        raise NotFoundError("Livro não encontrado.")

    return atualizado

def remover_livro_service(db: Session, livro_id: int):
    livro = livro_crud.get_livro(db, livro_id)
    if not livro:
        raise NotFoundError("Livro não encontrado.")

    if emprestimo_crud.existe_emprestimo_ativo_por_livro(db, livro_id):
        raise BusinessRuleError(
            "Livro não pode ser removido pois possui empréstimo ativo."
        )

    livro_crud.delete(db, livro)

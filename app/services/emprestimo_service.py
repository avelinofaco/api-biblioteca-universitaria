
#“Tradutor entre o mundo do negócio e o mundo da aplicação”.
from sqlalchemy.orm import Session
from app.crud import emprestimo as emprestimo_crud
from app.domain.exceptions import DomainError
from app.services.exceptions import BusinessRuleError, NotFoundError
from app import schemas

# Serviço para criar um empréstimo
def criar_emprestimo_sevice(db: Session, payload: schemas.EmprestimoCreate):
    try:
        return emprestimo_crud.create(db, payload)

    except DomainError as e:
        raise BusinessRuleError(str(e))

# service decide o significado do erro, o router decide como isso vira HTTP, o CRUD continua focado em persistência
def devolver_emprestimo_service(db: Session, emprestimo_id: int):
    res = emprestimo_crud.devolver_emprestimo(db, emprestimo_id)

    if not res:
        raise NotFoundError(
            "Empréstimo não encontrado ou não está em estado passível de devolução."
        )
    return {
        "emprestimo": res["emprestimo"],
        "multa": res["multa"]
    }

def renovar_emprestimo_service(db: Session, emprestimo_id: int, payload: schemas.RenovacaoEmprestimo):
    emp = emprestimo_crud.renovar_emprestimo(db=db, emprestimo_id=emprestimo_id, dias=payload.dias)
    if not emp:
        raise BusinessRuleError(
            "Empréstimo não encontrado ou não está ativo."
        )
    return emp


def listar_emprestimos_service(db: Session,skip: int,limit: int):
    items = emprestimo_crud.get_all(db, skip, limit)
    total = emprestimo_crud.count(db)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }

def listar_ativos_service(db: Session, skip: int, limit: int):
    total = emprestimo_crud.count_ativos(db)
    items = emprestimo_crud.get_ativos(db, skip, limit)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }

 
def deletar_emprestimo_service(db: Session, emprestimo_id: int):
    res = emprestimo_crud.delete(db, emprestimo_id)

    if not res:
        raise NotFoundError("Empréstimo não encontrado.")

    return None

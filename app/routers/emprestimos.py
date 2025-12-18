from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session #representa a conexão ativa com o banco. Permite executar queries e transações
from typing import List #Usado para tipar respostas que retornam listas.

from app.crud import emprestimo as emprestimo_crud #Importa o módulo de regras de persistência e negócio de empréstimo.(o router não acessa o banco diretamente — isso é responsabilidade do CRUD)
from app.services.emprestimo_service import criar_emprestimo_sevice, devolver_emprestimo_service
from app.services.exceptions import BusinessRuleError, NotFoundError
from app import schemas  #Importa os contratos de entrada e saída da API (Pydantic).
from app.deps import get_current_user 
from app.dependencies.permissions import exigir_roles
from app.deps import get_db #Função que fornece uma sessão do banco de dados via injeção de dependência.

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])

# Endpoint para criar um novo empréstimo
@router.post("/", response_model=schemas.EmprestimoOut, status_code=status.HTTP_201_CREATED,
        summary="Criar um novo empréstimo",
        description="""Admin, bibliotecario ou usuario pode criar um novo empréstimo.""")
def criar_emprestimo(payload: schemas.EmprestimoCreate, 
                     db: Session = Depends(get_db), 
                     usuario = Depends(get_current_user),
                     _ = Depends(exigir_roles("aluno","bibliotecario","admin"))):#payload: corpo da requisição, validado pelo Pydantic, db: sessão do banco via injeção de dependência
    try:
        return criar_emprestimo_sevice(db, payload)
    # Recurso não encontrado
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))  
    # Conflito de regras de negócio
    except BusinessRuleError as e:
        raise HTTPException(status_code=409, detail=str(e))

# Endpoint para devolver um empréstimo
@router.post("/{emprestimo_id}/devolver", response_model=schemas.EmprestimoDevolucaoOut, description="Devolve um empréstimo ativo e calcula multa se houver atraso.   Só admin e bibliotecario podem fazer isso.")
def devolver_emprestimo(emprestimo_id: int, db: Session = Depends(get_db),
                        usuario = Depends(get_current_user),
                        _ = Depends(exigir_roles("bibliotecario","admin"))):
    try:
        return devolver_emprestimo_service(db=db,emprestimo_id=emprestimo_id)
    # Recurso não encontrado
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    # Conflito de regras de negócio
    except BusinessRuleError as e:
        raise HTTPException(status_code=409, detail=str(e))

# Endpoint para renovar um empréstimo
@router.post("/{emprestimo_id}/renovar", response_model=schemas.EmprestimoOut, 
             description="adicional de dias (padrão 7 dias).")
def renovar_emprestimo(emprestimo_id: int, dias: int = 7, 
                       db: Session = Depends(get_db),
                       usuario = Depends(get_current_user),
                       _ = Depends(exigir_roles("aluno","bibliotecario"))):
    emp = emprestimo_crud.renovar_emprestimo(db, emprestimo_id, dias)
    if not emp:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou não ativo")
    return emp


# Endpoint para listar todos os empréstimos
@router.get("/", response_model=List[schemas.EmprestimoOut], description="Lista todos os empréstimos com paginação.  Bibliotecario ou aluno podem fazer isso.")
def listar_emprestimos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _ = Depends(exigir_roles("bibliotecario","aluno"))):
    return emprestimo_crud.get_all(db, skip, limit)


# Endpoint para listar apenas os empréstimos ativos
@router.get("/ativos", response_model=List[schemas.EmprestimoOut], description="Lista apenas os empréstimos ativos. Bibliotecario ou admin podem fazer isso.")
def listar_ativos(db: Session = Depends(get_db), _ = Depends(exigir_roles("bibliotecario","admin"))):
    return emprestimo_crud.get_ativos(db)


# Endpoint para deletar um empréstimo
@router.delete("/{emprestimo_id}", response_model=dict, description="Só admin e bibliotecario podem fazer isso.")
def deletar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db), _ = Depends(exigir_roles("bibliotecario","admin"))):
    res = emprestimo_crud.delete(db, emprestimo_id)
    if not res:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return res
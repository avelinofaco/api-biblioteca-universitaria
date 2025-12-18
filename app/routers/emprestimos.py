from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session #representa a conexão ativa com o banco. Permite executar queries e transações
from typing import List #Usado para tipar respostas que retornam listas.

from app.services.emprestimo_service import criar_emprestimo_sevice, devolver_emprestimo_service, renovar_emprestimo_service, listar_emprestimos_service, listar_ativos_service, deletar_emprestimo_service
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
                     _ = Depends(get_current_user),
                     _r = Depends(exigir_roles("aluno","bibliotecario","admin"))):#payload: corpo da requisição, validado pelo Pydantic, db: sessão do banco via injeção de dependência
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
             description="adicional de dias (padrão 7 dias). Só aluno e bibliotecario podem fazer isso.")
def renovar_emprestimo(emprestimo_id: int, payload: schemas.RenovacaoEmprestimo, 
                       db: Session = Depends(get_db),
                       _ = Depends(get_current_user),
                       _r = Depends(exigir_roles("aluno","bibliotecario"))):
    try:
        return renovar_emprestimo_service(db, emprestimo_id, payload)
    except BusinessRuleError as e:
        raise HTTPException(status_code=409, detail=str(e))


# Endpoint para listar todos os empréstimos
@router.get("/", response_model=schemas.PageEmprestimo,
            summary="Listar todos os empréstimos", 
            description="Lista todos os empréstimos com paginação.  Bibliotecario e admin vai fazer isso.")
def listar_emprestimos(skip: int = 0, limit: int = 2, db: Session = Depends(get_db),
                       _ = Depends(get_current_user),
                      _r = Depends(exigir_roles("bibliotecario", "admin"))):
    return listar_emprestimos_service(db, skip, limit)


# Endpoint para listar apenas os empréstimos ativos
@router.get("/ativos", response_model=schemas.PageEmprestimo, 
            summary="Listar empréstimos ativos",
            description="Bibliotecário ou admin podem listar empréstimos ativos com paginação.")
def listar_ativos(skip: int = 0, limit: int = 10,
        db: Session = Depends(get_db),
        _r = Depends(exigir_roles("bibliotecario", "admin"))):
    return listar_ativos_service(db, skip, limit)

# Endpoint para deletar um empréstimo
@router.delete("/{emprestimo_id}", status_code=status.HTTP_204_NO_CONTENT, 
               summary="Deletar um empréstimo", 
               description="Só admin e bibliotecario podem fazer isso.")
def deletar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db), _r = Depends(exigir_roles("bibliotecario","admin"))):
    try:
        deletar_emprestimo_service(db, emprestimo_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    return None
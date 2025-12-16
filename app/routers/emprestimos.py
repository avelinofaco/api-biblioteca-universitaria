from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session #representa a conexão ativa com o banco. Permite executar queries e transações
from typing import List #Usado para tipar respostas que retornam listas.

from app.crud import emprestimo as emprestimo_crud #Importa o módulo de regras de persistência e negócio de empréstimo.(o router não acessa o banco diretamente — isso é responsabilidade do CRUD)
from app.services.emprestimo_service import criar_emprestimo_sevice, devolver_emprestimo_service
from app.services.exceptions import BusinessRuleError, NotFoundError
from app import schemas  #Importa os contratos de entrada e saída da API (Pydantic).
from app.dependencies.auth import usuario_logado #Funções de dependência para autenticação e autorização.
from app.dependencies.permissions import exigir_roles
from app.deps import get_db #Função que fornece uma sessão do banco de dados via injeção de dependência.

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])

# Endpoint para criar um novo empréstimo
@router.post("/", response_model=schemas.EmprestimoOut, status_code=status.HTTP_201_CREATED,
        summary="Criar um novo empréstimo",
        description="""
        Este endpoint cria um novo empréstimo para um usuário.
        - `usuario_id`: ID do usuário que está pegando o livro.
        - `livro_id`: ID do livro que será emprestado.
        - `dias` (opcional): quantidade de dias para devolução, padrão 14 dias.
        """
        )
def criar_emprestimo(payload: schemas.EmprestimoCreate, 
                     db: Session = Depends(get_db), 
                     usuario = Depends(usuario_logado),
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
@router.post("/{emprestimo_id}/devolver", response_model=schemas.EmprestimoDevolucaoOut, description="Devolve um empréstimo ativo e calcula multa se houver atraso.")
def devolver_emprestimo(emprestimo_id: int, db: Session = Depends(get_db),
                        usuario = Depends(usuario_logado),
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
             description="Renova um empréstimo ativo por um número adicional de dias (padrão 7 dias).")
def renovar_emprestimo(emprestimo_id: int, dias: int = 7, 
                       db: Session = Depends(get_db),
                       usuario = Depends(usuario_logado),
                       _ = Depends(exigir_roles("aluno","bibliotecario"))):
    emp = emprestimo_crud.renovar_emprestimo(db, emprestimo_id, dias)
    if not emp:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou não ativo")
    return emp


# Endpoint para listar todos os empréstimos
@router.get("/", response_model=List[schemas.EmprestimoOut], description="Lista todos os empréstimos com paginação.")
def listar_emprestimos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return emprestimo_crud.get_all(db, skip, limit)


# Endpoint para listar apenas os empréstimos ativos
@router.get("/ativos", response_model=List[schemas.EmprestimoOut])
def listar_ativos(db: Session = Depends(get_db)):
    return emprestimo_crud.get_ativos(db)


# Endpoint para deletar um empréstimo
@router.delete("/{emprestimo_id}", response_model=dict)
def deletar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    res = emprestimo_crud.delete(db, emprestimo_id)
    if not res:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return res
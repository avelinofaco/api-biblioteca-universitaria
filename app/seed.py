# app/seed.py
"""
Script de população (seed) idempotente para a API da Biblioteca.
Rode a partir da raiz do projeto:
    python -m app.seed
ou
    python app/seed.py
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional
import json
import os
from pathlib import Path

from app.database import SessionLocal, init_db
from app.models import (
    Usuario, UsuarioRole,
    Livro,
    Emprestimo, EmprestimoStatus,
    Reserva, ReservaStatus,
    Multa, MultaStatus,
)

MULTA_POR_DIA = Decimal("1.00")
PADRAO_DIAS = 14

# Dados de exemplo pequenos (usuarios)
USUARIOS = [
    {"nome": "Alice Silva", "email": "alice@uni.edu", "role": UsuarioRole.aluno},
    {"nome": "Bruno Souza", "email": "bruno@uni.edu", "role": UsuarioRole.aluno},
    {"nome": "Carla Pereira", "email": "carla@uni.edu", "role": UsuarioRole.bibliotecario},
]

# Mantive uma pequena lista local para compatibilidade, mas os 100 livros virão do JSON.
LIVROS = [
    {"titulo": "Introdução à Programação", "autor": "J. Doe", "isbn": "978-1", "quantidade_total": 3, "area": "Computação"},
    {"titulo": "Banco de Dados Avançado", "autor": "A. Smith", "isbn": "978-2", "quantidade_total": 2, "area": "Computação"},
    {"titulo": "Algoritmos em Ação", "autor": "B. Lee", "isbn": "978-3", "quantidade_total": 1, "area": "Computação"},
]


def get_or_create_usuario(db, nome: str, email: str, role: UsuarioRole):
    u = db.query(Usuario).filter(Usuario.email == email).first()
    if u:
        return u
    u = Usuario(nome=nome, email=email, role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def get_or_create_livro(db, titulo: str, autor: Optional[str], isbn: Optional[str], quantidade_total: int, area: Optional[str]):
    """
    Busca por ISBN (quando fornecido). Se não encontrado, busca por titulo+autor.
    Se não existir, cria o registro e configura quantidade_disponivel igual a quantidade_total.
    """
    l = None
    if isbn:
        l = db.query(Livro).filter(Livro.isbn == isbn).first()
    if not l:
        l = db.query(Livro).filter(Livro.titulo == titulo, Livro.autor == autor).first()
    if l:
        return l
    l = Livro(
        titulo=titulo,
        autor=autor,
        isbn=isbn,
        quantidade_total=quantidade_total,
        quantidade_disponivel=quantidade_total,
        area=area,
    )
    db.add(l)
    db.commit()
    db.refresh(l)
    return l


def criar_emprestimo_manual(
    db,
    usuario_id: int,
    livro_id: int,
    data_emprestimo: datetime,
    data_prevista: datetime,
    status=EmprestimoStatus.ativo,
    renovacoes=0,
    data_devolucao=None,
):
    # evita duplicatas idempotentes: considera um empréstimo igual se mesmo usuário, livro, data_emprestimo
    exist = (
        db.query(Emprestimo)
        .filter(
            Emprestimo.usuario_id == usuario_id,
            Emprestimo.livro_id == livro_id,
            Emprestimo.data_emprestimo == data_emprestimo,
        )
        .first()
    )
    if exist:
        return exist

    emp = Emprestimo(
        usuario_id=usuario_id,
        livro_id=livro_id,
        data_emprestimo=data_emprestimo,
        data_prevista_devolucao=data_prevista,
        data_devolucao=data_devolucao,
        renovacoes=renovacoes,
        status=status,
    )
    # ajustar disponibilidade se empréstimo estiver ativo/atrasado
    if status in (EmprestimoStatus.ativo, EmprestimoStatus.atrasado):
        livro = db.get(Livro, livro_id)
        if livro:
            if livro.quantidade_disponivel > 0:
                livro.quantidade_disponivel -= 1
                db.add(livro)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


def criar_reserva_manual(db, usuario_id: int, livro_id: int):
    # evita duplicatas
    exist = (
        db.query(Reserva)
        .filter(
            Reserva.usuario_id == usuario_id,
            Reserva.livro_id == livro_id,
            Reserva.status == ReservaStatus.ativa,
        )
        .first()
    )
    if exist:
        return exist
    # calcular posicao
    qtd = db.query(Reserva).filter(Reserva.livro_id == livro_id, Reserva.status == ReservaStatus.ativa).count()
    pos = qtd + 1
    r = Reserva(usuario_id=usuario_id, livro_id=livro_id, posicao=pos, status=ReservaStatus.ativa)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def criar_multa_para_emprestimo(db, emprestimo: Emprestimo):
    # se já existir multa para esse empréstimo, retorna
    exist = db.query(Multa).filter(Multa.emprestimo_id == emprestimo.id).first()
    if exist:
        return exist
    if not emprestimo.data_prevista_devolucao:
        return None
    # considera data de referência: se emprestimo.data_devolucao existe, usa ela; senão usa agora UTC
    referencia = emprestimo.data_devolucao or datetime.utcnow()
    dias_atraso = (referencia.date() - emprestimo.data_prevista_devolucao.date()).days
    if dias_atraso <= 0:
        return None
    valor = MULTA_POR_DIA * Decimal(dias_atraso)
    desc = f"Multa por {dias_atraso} dia(s) de atraso"
    multa = Multa(
        emprestimo_id=emprestimo.id,
        usuario_id=emprestimo.usuario_id,
        valor=valor,
        descricao=desc,
        status=MultaStatus.pendente,
    )
    db.add(multa)
    db.commit()
    db.refresh(multa)
    return multa


# ---------------- JSON seeding ----------------
def seed_livros_from_json(db, json_path: str):
    p = Path(json_path)
    if not p.exists():
        print(f"[seed] arquivo de livros não encontrado em: {json_path}")
        return 0
    with p.open("r", encoding="utf-8") as f:
        livros = json.load(f)
    created = 0
    for item in livros:
        titulo = item.get("titulo")
        autor = item.get("autor")
        isbn = item.get("isbn")
        quantidade_total = int(item.get("quantidade_total", 1))
        area = item.get("area", "TI")
        l = get_or_create_livro(db, titulo, autor, isbn, quantidade_total, area)
        if l:
            created += 1
    return created


def run():
    print("Inicializando DB (cria tabelas se necessário)...")
    init_db(create_tables=True)

    db = SessionLocal()
    try:
        # criar usuários
        usuarios_created = []
        for u in USUARIOS:
            usuario = get_or_create_usuario(db, u["nome"], u["email"], u["role"])
            usuarios_created.append(usuario)
        print(f"Usuários garantidos: {len(usuarios_created)}")

        # ---------- popula livros do JSON (arquivo em app/data/books_ti_100.json) ----------
        json_file = os.path.join(os.path.dirname(__file__), "data", "books_ti_100.json")
        added = seed_livros_from_json(db, json_file)
        print(f"Livros adicionados (ou garantidos) a partir do JSON: {added}")

        # --- Mantemos também a inserção manual pequena (compatibilidade) ---
        livros_created = []
        for l in LIVROS:
            livro = get_or_create_livro(db, l["titulo"], l.get("autor"), l.get("isbn"), l.get("quantidade_total", 1), l.get("area"))
            livros_created.append(livro)
        print(f"Livros (manuais) garantidos: {len(livros_created)}")

        # criar alguns empréstimos:
        # 1) empréstimo ativo recente (Alice pega "Introdução à Programação")
        alice = db.query(Usuario).filter(Usuario.email == "alice@uni.edu").one()
        livro1 = db.query(Livro).filter(Livro.isbn == "978-1").one()
        data_emp = datetime.utcnow() - timedelta(days=2)
        data_prev = data_emp + timedelta(days=PADRAO_DIAS)
        criar_emprestimo_manual(db, alice.id, livro1.id, data_emp, data_prev, status=EmprestimoStatus.ativo)

        # 2) empréstimo atrasado (Bruno pegou "Banco de Dados Avançado" há 30 dias)
        bruno = db.query(Usuario).filter(Usuario.email == "bruno@uni.edu").one()
        livro2 = db.query(Livro).filter(Livro.isbn == "978-2").one()
        data_emp2 = datetime.utcnow() - timedelta(days=30)
        data_prev2 = data_emp2 + timedelta(days=PADRAO_DIAS)  # vencido há 16 dias
        emp_atrasado = criar_emprestimo_manual(db, bruno.id, livro2.id, data_emp2, data_prev2, status=EmprestimoStatus.atrasado)

        # gerar multa para o empréstimo atrasado
        multa = criar_multa_para_emprestimo(db, emp_atrasado)
        if multa:
            print(f"Multa criada: id={multa.id}, valor={multa.valor}")

        # 3) reserva (Alice reserva "Banco de Dados Avançado")
        reserva = criar_reserva_manual(db, alice.id, livro2.id)
        print(f"Reserva criada (ou existente): id={reserva.id}, posicao={reserva.posicao}")

        # 4) emprestimo já devolvido (ex.: livro 3 devolvido em dia)
        livro3 = db.query(Livro).filter(Livro.isbn == "978-3").one()
        data_emp3 = datetime.utcnow() - timedelta(days=20)
        data_prev3 = data_emp3 + timedelta(days=PADRAO_DIAS)
        data_dev3 = data_emp3 + timedelta(days=PADRAO_DIAS - 1)  # devolvido 1 dia antes do prazo
        criar_emprestimo_manual(db, alice.id, livro3.id, data_emp3, data_prev3, status=EmprestimoStatus.devolvido, data_devolucao=data_dev3)

        # resumo
        total_usuarios = db.query(Usuario).count()
        total_livros = db.query(Livro).count()
        total_emprestimos = db.query(Emprestimo).count()
        total_reservas = db.query(Reserva).count()
        total_multas = db.query(Multa).count()

        print("=== Resumo após seed ===")
        print(f"Usuários: {total_usuarios}")
        print(f"Livros: {total_livros}")
        print(f"Empréstimos: {total_emprestimos}")
        print(f"Reservas: {total_reservas}")
        print(f"Multas: {total_multas}")

    finally:
        db.close()


if __name__ == "__main__":
    run()

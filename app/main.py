from fastapi import FastAPI
from app.routers import login, livros, usuarios, emprestimos, reservas, multas, historico_comportamento



app = FastAPI(title="API Biblioteca Universitária")

# Inicializa o banco de dados (cria as tabelas se não existirem)
# init_db()

app.include_router(login.router)
app.include_router(livros.router)
app.include_router(usuarios.router)
app.include_router(emprestimos.router)
app.include_router(reservas.router)
app.include_router(multas.router)
app.include_router(historico_comportamento.router)


@app.get("/")
def root():
    return {"msg": "API Biblioteca — Bem-vindo à API da Biblioteca Universitária!"}

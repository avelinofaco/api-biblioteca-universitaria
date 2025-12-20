📚 API de Biblioteca — Backend
Visão Geral

Esta é uma API REST para gerenciamento de uma biblioteca, desenvolvida com foco em aprendizado de backend, modelagem de domínio e implementação de regras de negócio reais.

O projeto vai além de um CRUD simples, buscando representar de forma coerente o funcionamento lógico de uma biblioteca: controle de usuários, livros, empréstimos, devoluções e aplicação automática de multas.

Trata-se de um projeto em evolução, utilizado como laboratório prático para boas práticas de backend.

🏗️ Tecnologias Utilizadas

Python

FastAPI

SQLAlchemy

PostgreSQL

Alembic (migrations)

JWT (autenticação e autorização)

Pydantic

📦 Domínio do Sistema
👤 Usuário

Pode realizar empréstimos

Pode possuir multas pendentes

Está sujeito a regras antes de realizar novos empréstimos

Possui papéis (roles) para controle de acesso

📘 Livro

Representa o acervo da biblioteca

Possui controle de disponibilidade

Não pode ser emprestado se já estiver em uso

🔄 Empréstimo

Entidade central do sistema

Relaciona usuário e livro

Controla datas, status e devolução

Responsável pela geração de multas em caso de atraso

💸 Multa

Gerada automaticamente em devoluções atrasadas

Associada a um empréstimo e a um usuário

Bloqueia novos empréstimos enquanto estiver pendente

📜 Principais Regras de Negócio

Usuários devem estar cadastrados para realizar empréstimos

Usuários com multas pendentes não podem realizar novos empréstimos

Existe um limite configurável de empréstimos ativos por usuário

Um livro não pode ter mais de um empréstimo ativo

Empréstimos atrasados geram multa automaticamente no momento da devolução

Essas regras são aplicadas na camada de services, não nos endpoints.

⚙️ Arquitetura do Projeto

O projeto segue uma separação clara de responsabilidades:

Models: definição das entidades e estrutura do banco de dados

Schemas: validação de dados e contratos da API

CRUD: operações básicas de persistência

Services: implementação das regras de negócio

Routers: definição dos endpoints HTTP

Essa abordagem facilita manutenção, testes e futuras evoluções.

🔐 Autenticação e Autorização

A API utiliza JWT (JSON Web Token) para autenticação.

Endpoints sensíveis são protegidos

Controle de acesso baseado em papéis (roles)

O backend é responsável por validar permissões, não o frontend

▶️ Como Executar o Projeto
Pré-requisitos

Python 3.10+

PostgreSQL

Virtualenv (recomendado)

1️⃣ Clone o repositório
git clone https://github.com/avelinofaco/api-biblioteca-universitaria
cd seu-repositorio

2️⃣ Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3️⃣ Instale as dependências
pip install -r requirements.txt

4️⃣ Configure as variáveis de ambiente

Crie um arquivo .env com as configurações do banco de dados e JWT, por exemplo:

DATABASE_URL=postgresql://usuario:senha@localhost:5432/biblioteca
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

5️⃣ Execute as migrations
alembic upgrade head

6️⃣ Inicie a aplicação
uvicorn app.main:app --reload


A API estará disponível em:

http://localhost:8000


Documentação automática (Swagger):

http://localhost:8000/docs

📖 Documentação Complementar

Detalhes sobre decisões arquiteturais, fluxo de empréstimos, regras internas e aprendizados estão descritos no arquivo:

📄 DOCUMENTACAO.md

🚀 Objetivo do Projeto

Consolidar conhecimentos em backend com Python

Praticar modelagem de domínio

Implementar regras de negócio realistas

Criar um projeto de portfólio preparado para integração com frontend

📌 Observações Finais

Este projeto está em constante evolução e serve como base para estudos mais avançados, incluindo testes automatizados, frontend integrado e melhorias de performance e segurança.
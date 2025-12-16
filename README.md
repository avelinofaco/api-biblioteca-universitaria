# 📚 API de Biblioteca

## Visão Geral

Esta é uma **API de Biblioteca** desenvolvida com foco em aprendizado de backend, modelagem de domínio e aplicação de regras de negócio reais. O projeto vai além de um CRUD simples, representando de forma coerente o funcionamento lógico de uma biblioteca.

---

## 🏗️ Tecnologias Utilizadas

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT (autenticação)
* Pydantic

---

## 📦 Entidades do Sistema

### 👤 Usuário

* Pode realizar empréstimos
* Pode possuir multas
* Está sujeito a regras antes de novos empréstimos

### 📘 Livro

* Item do acervo da biblioteca
* Pode estar disponível ou indisponível

### 🔄 Empréstimo

* Conecta usuário e livro
* Possui datas e status
* É o núcleo do domínio

### 💸 Multa

* Gerada automaticamente em atrasos
* Associada a usuário e empréstimo
* Bloqueia novos empréstimos enquanto pendente

---

## 📜 Regras de Negócio (Resumo)

* Usuário deve estar cadastrado
* Usuário com multa pendente não pode emprestar
* Existe limite de empréstimos ativos por usuário
* Livro não pode estar em empréstimo ativo
* Atrasos geram multa automaticamente

---

## ⚙️ Arquitetura

O projeto segue separação clara de responsabilidades:

* **Models**: estrutura do banco de dados
* **Schemas**: validação e contratos
* **CRUD**: operações simples
* **Services**: regras de negócio
* **Routers**: endpoints HTTP

---

## 🔐 Autenticação

A API utiliza autenticação via **JWT**, protegendo endpoints sensíveis e garantindo controle de acesso.

---

## 📖 Documentação Técnica

Detalhes aprofundados sobre domínio, decisões arquiteturais, fluxos internos e aprendizados estão descritos no arquivo:

📄 **DOCUMENTACAO.md**

---

## 🚀 Objetivo do Projeto

* Consolidar conhecimentos em backend Python
* Praticar modelagem de domínio
* Aplicar regras de negócio reais
* Servir como projeto de estudo e portfólio

---

## 📌 Observação Final

Este projeto foi desenvolvido como um laboratório de aprendizado contínuo e está preparado para evoluções futuras.

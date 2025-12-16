# 📖 Documentação Técnica – API de Biblioteca

Este documento complementa o README principal. Aqui estão concentrados os **detalhes técnicos, decisões arquiteturais e aprendizados**, funcionando como um caderno de estudo e referência futura.

---

## 🎯 Propósito da Documentação

Este arquivo existe para:

* Registrar decisões de arquitetura
* Explicar regras de negócio em profundidade
* Servir como material de revisão e estudo
* Facilitar manutenção futura do projeto

Enquanto o README apresenta o projeto, **esta documentação explica o porquê das escolhas**.

---

## 🧠 Visão de Domínio

A API modela o funcionamento real de uma biblioteca. O domínio foi pensado antes da implementação, garantindo coerência entre regras e código.

### Conceitos centrais

* **Usuário**: agente que realiza empréstimos
* **Livro**: recurso limitado do acervo
* **Empréstimo**: vínculo temporal entre usuário e livro
* **Multa**: consequência de atraso

O domínio é orientado a eventos: emprestar, devolver, atrasar.

---

## 🧱 Decisões de Modelagem

### Por que Multa é uma entidade?

A multa não é apenas um cálculo momentâneo. Ela:

* Possui identidade própria
* Está associada a um empréstimo
* Pode bloquear novas ações do usuário
* Pode evoluir (pagamento, histórico)

Por isso, foi modelada como entidade persistente.

---

### Ciclo de vida do Empréstimo

O empréstimo possui estados bem definidos:

* **Ativo**: livro emprestado e dentro do prazo
* **Devolvido**: livro retornado
* **Atrasado**: devolução fora do prazo

O estado do empréstimo guia a criação de multas e a disponibilidade do livro.

---

## 📜 Regras de Negócio em Detalhe

### Validações antes de criar um empréstimo

Antes de um empréstimo ser criado, o sistema verifica:

* Usuário existe
* Usuário não possui multas pendentes
* Usuário não ultrapassou o limite de empréstimos ativos
* Livro está disponível

Essas regras vivem na **camada de service**, não nos endpoints.

---

### Devolução de Empréstimo

Ao devolver um livro:

1. O status do empréstimo é atualizado
2. A data real de devolução é registrada
3. O sistema calcula atraso
4. Se houver atraso, uma multa é criada automaticamente

O valor da multa é calculado com base em dias de atraso e valor diário configurável.

---

## 🔁 Fluxo Técnico (Request → Banco)

Exemplo: criação de empréstimo

```
Request HTTP
   ↓
Router (FastAPI)
   ↓
Service (regras de negócio)
   ↓
CRUD
   ↓
SQLAlchemy ORM
   ↓
Banco de Dados
   ↓
Response HTTP
```

Essa separação garante clareza, testabilidade e manutenção.

---

## 🧪 Estratégia de Testes (Planejada)

O projeto foi estruturado para permitir testes como:

* Usuário com multa não consegue emprestar
* Usuário atinge limite de empréstimos
* Devolução em atraso gera multa
* Devolução em dia não gera multa

Os testes validam regras, não apenas respostas HTTP.

---

## 📚 Aprendizados Consolidados

Este projeto reforçou conceitos essenciais:

* Backend é sobre regras, não apenas endpoints
* Domínio bem definido reduz bugs
* Separação de camadas aumenta clareza
* Documentação é parte do código

---

## 🧭 Evoluções Futuras

Possíveis extensões do sistema:

* Pagamento de multas
* Relatórios de empréstimos
* Histórico detalhado por usuário
* Dashboard administrativo
* Soft delete

Essas evoluções foram consideradas desde a modelagem inicial.

---

## 🧩 Observação Final

Este documento não é estático. Ele evolui junto com o projeto e serve como memória técnica do sistema.

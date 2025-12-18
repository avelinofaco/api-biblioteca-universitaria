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



<!-- Próximo passo estratégico: Pensar como produto

Depois disso, você pode evoluir o sistema de verdade:

Histórico de empréstimos do usuário

Relatório de multas

Livros mais emprestados

Status do acervo

Pagamento ou quitação de multa

Soft delete vs hard delete

Aqui o projeto deixa de ser “API de estudo” e vira case de portfólio.  


Router vira maestro.
Service vira cérebro.
CRUD vira músculo.
-->

Registro de estudo do dia 18/12

Evoluções realizadas (Experiência do consumidor da API)
1. Separação clara de responsabilidades (Router → Service → CRUD)

Foi consolidada a arquitetura em três camadas bem definidas:

Routers
Responsáveis apenas por:

receber requisições

validar permissões (roles)

delegar a execução para os services

Services
Responsáveis por:

aplicar regras de negócio

validar estados do domínio

orquestrar chamadas ao CRUD

CRUD
Responsável exclusivamente por:

acesso ao banco de dados

operações simples (create, read, update, delete)

nenhuma regra de negócio

Essa separação evita duplicação de lógica, facilita testes e reduz regressões.

2. Padronização de paginação nos endpoints

Os endpoints de listagem passaram a oferecer paginação explícita, melhorando a experiência de quem consome a API (Swagger, front-end, integrações).

Parâmetros adotados:

skip: deslocamento inicial

limit: quantidade de registros por página

Os retornos de listagem agora seguem um padrão consistente:

{
  "total": 120,
  "skip": 0,
  "limit": 10,
  "items": []
}


Isso permite que o consumidor navegue facilmente entre páginas, inclusive via Swagger.

3. Refatoração dos endpoints de Livro

Os endpoints de livros foram ajustados para:

Delegar lógica ao livro_service

Centralizar regras de negócio

Evitar lógica duplicada nos routers

Garantir respostas HTTP coerentes (404, 204, etc.)

O router agora atua apenas como ponto de entrada, e não como camada decisória.

4. Correção do fluxo de atualização (PATCH)

Foi corrigido o erro onde o service tentava usar model_dump() em um dict.

A responsabilidade ficou clara:

O router recebe o schema

O service trabalha com dict de dados já tratados

O CRUD aplica as alterações no modelo persistido

Isso eliminou erros 500 e tornou o fluxo mais previsível.

5. Regra de negócio: livro não pode ser removido se estiver emprestado

Foi implementada uma regra fundamental do domínio:

Um livro não pode ser removido se existir empréstimo ativo associado a ele.

Implementação:

Criada função específica no emprestimo_crud para verificar existência de empréstimo ativo por livro

A verificação acontece no service, antes do delete

O CRUD permanece simples e sem regras

Exemplo de validação aplicada:

Se houver empréstimo ativo → erro de regra de negócio

Se o livro não existir → 404

Se estiver disponível → remoção permitida

Essa mudança impede inconsistências no sistema e reflete corretamente o mundo real.

6. Correção de erros críticos de delete

Foram corrigidos erros comuns de SQLAlchemy, como:

tentativa de delete() passando id em vez de instância

tentativa de deletar listas ou tipos primitivos

Agora:

o CRUD recebe sempre a instância mapeada

o delete ocorre de forma segura e previsível

7. Ajustes de autorização e roles

Foi validado e corrigido o uso de permissões:

admin e bibliotecario conseguem acessar endpoints restritos

erros 403 foram corrigidos com uso adequado do Depends(exigir_roles(...))
            DOCUMENTAÇÃO DE VISÃO API BIBLIOTECA UNIVERSITÁRIA

1. Visão Geral
A API de Biblioteca é um sistema backend desenvolvido para gerenciar o acervo, os usuários e os empréstimos de uma biblioteca, aplicando regras de negócio próximas da realidade operacional desse tipo de instituição. O projeto tem como foco principal o aprendizado prático de desenvolvimento backend, modelagem de domínio e aplicação consistente de regras de negócio, indo além de um CRUD simples.
A API foi construída para servir como base para futuras integrações com aplicações frontend, sistemas administrativos ou aplicações acadêmicas, mantendo uma separação clara entre regras de negócio e camada de apresentação.
2. Problema a Ser Resolvido
Muitos sistemas de estudo ou projetos iniciais de backend se limitam a operações básicas de criação, leitura, atualização e exclusão de dados, sem considerar restrições reais do domínio. Em bibliotecas reais, existem regras claras sobre quem pode pegar livros, quando um empréstimo é permitido e quais condições impedem novas operações.
Este projeto busca resolver esse problema ao modelar um sistema que:
Controle o fluxo de empréstimos de livros
Garanta a consistência das regras de negócio
Evite estados inválidos do sistema (ex.: livro emprestado duas vezes simultaneamente)
3. Objetivos do Sistema
3.1 Objetivo Geral
Desenvolver uma API robusta e coerente para gestão de bibliotecas, aplicando boas práticas de backend, organização de código e modelagem de domínio.
3.2 Objetivos Específicos
Permitir o cadastro e gerenciamento de usuários
Permitir o cadastro e gerenciamento de livros do acervo
Controlar empréstimos e devoluções de livros
Aplicar regras de negócio relacionadas a multas, limites e disponibilidade
Garantir autenticação e segurança no acesso aos endpoints
4. Público-Alvo
Desenvolvedores backend em processo de aprendizado
Estudantes de tecnologia da informação
Avaliadores técnicos e recrutadores
Aplicações frontend que necessitem consumir uma API de biblioteca
5. Escopo do Sistema
5.1 Funcionalidades Incluídas
Cadastro, edição, consulta e remoção de usuários
Cadastro, edição, consulta e remoção de livros
Registro de empréstimos de livros
Registro de devoluções
Verificação de disponibilidade de livros
Aplicação de regras de negócio antes da realização de empréstimos
Autenticação de usuários via JWT
5.2 Funcionalidades Fora do Escopo
Interface gráfica (frontend)
Integração com sistemas externos
Notificações por e-mail ou SMS
Controle financeiro avançado de multas
6. Premissas
O sistema será consumido via requisições HTTP
Todas as regras de negócio são aplicadas no backend
A persistência de dados é feita em banco relacional
A API segue princípios REST
7. Restrições
O projeto utiliza tecnologias específicas definidas previamente (FastAPI, SQLAlchemy, PostgreSQL)
O sistema depende de autenticação para operações sensíveis
As regras de negócio devem ser respeitadas independentemente do cliente que consome a API
8. Benefícios Esperados
Aprendizado aprofundado de backend além de CRUD
Demonstração clara de raciocínio de negócio aplicado ao código
Base sólida para expansão futura do sistema
Facilidade de manutenção e evolução do projeto
9. Visão de Evolução Futura
Como possíveis evoluções do sistema, podem ser consideradas:
Criação de uma interface web ou mobile
Relatórios de empréstimos e usuários
Sistema de reservas de livros
Integração com serviços externos

            REQUISITOS DO SISTEMA

1. Introdução
Este documento descreve os requisitos funcionais e não funcionais da API de Biblioteca, derivados diretamente do Documento de Visão e da implementação do sistema. Os requisitos aqui apresentados definem o comportamento esperado da aplicação e as restrições técnicas e de qualidade que devem ser atendidas.
2. Requisitos Funcionais
RF-01 – Cadastro de Usuário
O sistema deve permitir o cadastro de usuários com informações básicas necessárias para identificação e controle de empréstimos.
RF-02 – Consulta de Usuário
O sistema deve permitir a consulta de usuários cadastrados por identificador único.
RF-03 – Atualização de Usuário
O sistema deve permitir a atualização dos dados cadastrais de um usuário.
RF-04 – Remoção de Usuário
O sistema deve permitir a remoção de usuários, respeitando as restrições de integridade do sistema.
RF-05 – Cadastro de Livro
O sistema deve permitir o cadastro de livros no acervo da biblioteca.
RF-06 – Consulta de Livro
O sistema deve permitir a consulta de livros cadastrados e sua disponibilidade.
RF-07 – Atualização de Livro
O sistema deve permitir a atualização das informações de um livro.
RF-08 – Remoção de Livro
O sistema deve permitir a remoção de livros do acervo, respeitando as regras de negócio.
RF-09 – Registro de Empréstimo
O sistema deve permitir o registro de empréstimos de livros para usuários cadastrados.
RF-10 – Registro de Devolução
O sistema deve permitir o registro da devolução de livros emprestados.
RF-11 – Verificação de Disponibilidade
O sistema deve verificar automaticamente a disponibilidade do livro antes de permitir um empréstimo.
RF-12 – Aplicação de Regras de Negócio
O sistema deve aplicar todas as regras de negócio relacionadas a empréstimos, limites e multas antes de concluir uma operação.
RF-13 – Autenticação
O sistema deve permitir autenticação de usuários e controle de acesso aos endpoints protegidos.
3. Requisitos Não Funcionais
RNF-01 – Segurança
O sistema deve garantir autenticação e autorização utilizando JWT para proteger endpoints sensíveis.
RNF-02 – Consistência de Dados
O sistema deve garantir que os dados persistidos não entrem em estados inválidos.
RNF-03 – Desempenho
O sistema deve responder às requisições em tempo adequado para uso em aplicações cliente.
RNF-04 – Escalabilidade
O sistema deve permitir evolução futura sem necessidade de reescrita completa da aplicação.
RNF-05 – Manutenibilidade
O código-fonte deve ser organizado de forma clara, modular e de fácil manutenção.
RNF-06 – Portabilidade
O sistema deve poder ser executado em diferentes ambientes de desenvolvimento e produção.
RNF-07 – Padronização
A API deve seguir padrões REST e convenções claras de nomenclatura.

               MODELO DE DOMÍNIO

1. Visão Geral do Domínio
O Modelo de Domínio da API de Biblioteca representa os principais conceitos do problema que o sistema se propõe a resolver, bem como as relações entre esses conceitos. O objetivo deste modelo é refletir fielmente as regras e restrições do mundo real de uma biblioteca, servindo como base para a implementação das regras de negócio e da persistência de dados.
O sistema foi modelado com foco em clareza, consistência e separação de responsabilidades, evitando dependências desnecessárias entre entidades.
2. Entidades Principais
2.1 Usuário
Representa uma pessoa cadastrada no sistema que pode realizar empréstimos de livros.
Responsabilidades:
Identificar o usuário no sistema
Armazenar informações necessárias para controle de empréstimos
Manter o estado relacionado a multas e restrições
Atributos principais:
Identificador único
Dados cadastrais básicos
Indicador de situação regular ou com pendências
2.2 Livro
Representa um item do acervo da biblioteca disponível para empréstimo.
Responsabilidades:
Identificar um exemplar do acervo
Armazenar informações bibliográficas
Indicar se o livro está disponível ou indisponível para empréstimo
Atributos principais:
Identificador único
Título
Autor
Status de disponibilidade
2.3 Empréstimo
Representa o vínculo temporário entre um usuário e um livro.
Responsabilidades:
Registrar a data de empréstimo
Registrar a data de devolução
Controlar o estado do empréstimo (ativo ou finalizado)
Atributos principais:
Identificador único
Data de empréstimo
Data prevista de devolução
Data de devolução efetiva
Status do empréstimo
3. Relacionamentos
Um Usuário pode possuir vários Empréstimos ao longo do tempo (relação 1:N).
Um Livro pode estar associado a vários Empréstimos, porém apenas um empréstimo ativo por vez.
Um Empréstimo está obrigatoriamente associado a um único Usuário e a um único Livro.
Esses relacionamentos garantem que o sistema represente corretamente o fluxo de empréstimos e devoluções.
4. Invariantes do Domínio
As seguintes regras devem ser sempre verdadeiras no sistema:
Um livro não pode possuir mais de um empréstimo ativo simultaneamente.
Um empréstimo ativo deve sempre estar associado a um usuário válido.
Um empréstimo finalizado não pode ser reativado.
A disponibilidade de um livro é derivada do estado de seus empréstimos.
5. Considerações de Modelagem
O modelo foi desenhado para:
Evitar duplicação de informações
Centralizar regras críticas no domínio
Facilitar a aplicação das regras de negócio
Permitir evolução futura, como reservas ou histórico avançado
Este Modelo de Domínio serve como base para a definição detalhada das regras de negócio e para a estruturação da camada de persistência do sistema.

                        REGRAS DE NEGÓCIO 

RN-01 — Cadastro obrigatório de usuário
 Somente usuários previamente cadastrados no sistema podem realizar empréstimos de livros.
RN-02 — Autenticação para operações sensíveis
 Operações que alteram o estado do sistema (cadastro, atualização, empréstimo e devolução) exigem autenticação válida.
RN-03 — Usuário com pendências não pode emprestar
 Usuários que possuam multas ou pendências ativas não podem realizar novos empréstimos até a regularização da situação.
RN-04 — Limite máximo de empréstimos ativos por usuário
 Um usuário não pode ultrapassar o número máximo de empréstimos ativos permitidos pelo sistema.
 Esse limite é configurável e validado no momento da solicitação do empréstimo.
RN-05 — Livro deve estar disponível para empréstimo
 Um livro só pode ser emprestado se não existir nenhum empréstimo ativo associado a ele.
RN-06 — Um livro não pode ter mais de um empréstimo ativo
 O sistema deve impedir a criação de múltiplos empréstimos ativos para o mesmo livro.
RN-07 — Criação de empréstimo condicionada às regras
 A criação de um empréstimo só é permitida quando todas as regras relacionadas a usuário, livro e limites forem satisfeitas.
RN-08 — Registro obrigatório de devolução
 A devolução de um livro deve ser registrada explicitamente no sistema para finalizar o empréstimo.
RN-09 — Devolução finaliza o empréstimo
 Ao registrar a devolução, o empréstimo passa para o estado “finalizado” e não pode mais ser alterado.
RN-10 — Livro torna-se disponível após devolução
 Um livro só volta a ficar disponível para novos empréstimos após a finalização do empréstimo ativo.
RN-11 — Empréstimos possuem estado controlado
 Um empréstimo pode assumir apenas estados válidos definidos pelo sistema (ex.: ativo ou finalizado).
RN-12 — Empréstimos finalizados são imutáveis
 Empréstimos finalizados não podem ser reativados, alterados ou excluídos.
RN-13 — Integridade entre usuário, livro e empréstimo
 Todo empréstimo deve estar obrigatoriamente associado a um usuário válido e a um livro válido.
RN-14 — Exclusão de entidades respeita integridade
 Usuários ou livros não podem ser removidos do sistema caso existam empréstimos ativos ou vínculos que comprometam a integridade dos dados.
RN-15 — Regras de negócio aplicadas no backend
 Todas as regras de negócio são validadas exclusivamente no backend, independentemente do cliente consumidor da API.
RN-16 — Consistência do estado do sistema
 O sistema deve impedir qualquer operação que gere estados inválidos, como livros disponíveis com empréstimos ativos ou usuários ultrapassando limites.

         DOCUMENTAÇÃO DA API


1. Visão Geral
A API de Biblioteca é uma API REST desenvolvida para gerenciamento de usuários, livros e empréstimos de uma biblioteca. Seu objetivo é fornecer endpoints consistentes, seguros e alinhados às regras de negócio do domínio, permitindo integração com aplicações frontend, sistemas administrativos ou ferramentas de teste.
Todas as requisições e respostas utilizam o formato JSON.
2. Base URL
/
(O caminho base pode variar conforme o ambiente de execução.)
3. Autenticação
A API utiliza autenticação baseada em JWT (JSON Web Token).
O token deve ser enviado no header:
Authorization: Bearer <token>
Endpoints protegidos exigem um token válido.
Tokens inválidos ou ausentes resultam em erro de autenticação.


4. Recursos da API
4.1 Usuários
Criar usuário
POST /usuarios
Cria um novo usuário no sistema.
Listar usuários
GET /usuarios
Retorna todos os usuários cadastrados.
Buscar usuário por ID
GET /usuarios/{id}
Retorna os dados de um usuário específico.
Atualizar usuário
PUT /usuarios/{id}
Atualiza os dados de um usuário existente.
Remover usuário
DELETE /usuarios/{id}
Remove um usuário do sistema, respeitando as regras de integridade (ex.: empréstimos ativos).

4.2 Livros
Criar livro
POST /livros
Cadastra um novo livro no acervo da biblioteca.
Listar livros
GET /livros
Retorna a lista de livros cadastrados.
Buscar livro por ID
GET /livros/{id}
Retorna os dados de um livro específico, incluindo seu status de disponibilidade.
Atualizar livro
PUT /livros/{id}
Atualiza as informações de um livro existente.
Remover livro
DELETE /livros/{id}
Remove um livro do sistema, respeitando as regras de negócio (ex.: livro emprestado).

4.3 Empréstimos
Criar empréstimo
POST /emprestimos
Registra um novo empréstimo de um livro para um usuário.
A criação do empréstimo está sujeita às regras de negócio:
usuário deve estar regular
livro deve estar disponível
limite de empréstimos deve ser respeitado


Listar empréstimos
GET /emprestimos
Retorna a lista de todos os empréstimos registrados no sistema.
Buscar empréstimo por ID
GET /emprestimos/{id}
Retorna os dados de um empréstimo específico.
Registrar devolução
POST /emprestimos/{id}/devolucao
Registra a devolução de um livro, finalizando o empréstimo e tornando o livro disponível novamente.

5. Códigos de Resposta HTTP


Código
Descrição
200 OK
Requisição realizada com sucesso
201 created
Recurso criado com sucesso
400 Bad Request
Dados inválidos ou violação de regra de negócio
401 Unauthorized
Falha de autenticação
404 Not Found
Recurso não encontrado
409 Conflict
Conflito de estado no sistema


6. Tratamento de Erros
Erros retornam mensagens claras indicando:
motivo da falha
regra de negócio violada (quando aplicável)
Isso facilita o tratamento por aplicações consumidoras da API.
7. Documentação Automatizada
A API disponibiliza documentação interativa gerada automaticamente pelo FastAPI, utilizando OpenAPI/Swagger, permitindo:
visualização dos endpoints
teste direto das requisições
inspeção de schemas de entrada e saída


# Roadmap de Maturidade (MPS.BR - Nível G)

Para adequar o projeto aos critérios estipulados pelo Nível G do MPS.BR em um ciclo de 90 dias, a equipe propõe as seguintes ações operacionais:

## Ação 1: Institucionalização da Gerência de Projetos (GPR)
* **Objetivo:** Estabelecer controle, rastreabilidade de tarefas e mitigar a dependência técnica.
* **Execução:** Implementação do quadro de acompanhamento visual via GitHub Projects para definir cadências previsíveis. Adicionalmente, implementar uma política de rotação de mantenedores com permissões de merge compartilhadas para dissolver o anti-padrão de herói único. Criação de um registro formal de riscos técnicos no repositório.
* **Prioridade:** Crítica.

## Ação 2: Formalização da Gerência de Requisitos (GRE)
* **Objetivo:** Evitar expansões de escopo indocumentadas e garantir a bidirecionalidade dos requisitos.
* **Execução:** Configuração de Issue Templates com a obrigatoriedade de preenchimento de Critérios de Aceitação. Adoção de ADRs (Architecture Decision Records) para documentar permanentemente qualquer escolha estrutural que afete o sistema.
* **Prioridade:** Alta.

## Ação 3: Garantia da Qualidade do Produto (QPR)
* **Objetivo:** Evitar regressões e impedir a introdução de falhas de segurança durante a evolução do código.
* **Execução:** Instituir uma regra rígida de Definition of Done (DoD), onde os PRs dependam da aprovação de testes unitários automatizados. Adição de uma etapa de Análise Estática de Segurança (SAST) integrada ao pipeline de CI/CD para bloqueio autônomo de padrões inseguros de SQL.
* **Prioridade:** Alta.
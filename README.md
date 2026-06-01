# Auditoria Forense e Plano de Resgate Técnico: Vanna AI

Este repositório contém os artefatos, diagnósticos e diagramas desenvolvidos para a Atividade 2 da disciplina de Engenharia de Software (COMP0503). O trabalho foca na análise do código, identificação de dívidas técnicas e sugestão de melhorias baseadas no modelo MPS.BR para o projeto Vanna AI.

## Defesa da Auditoria Técnica

**(link)**

*(Apresentação com a fundamentação teórica dos achados e a inspeção no código-fonte)*

## Composição da Equipe

* Bruno Henrique Carneiro da Silva
* Diego Carvalho Cavalcante
* Fábio Henrique Lisboa de Souza
* Flávio Henrique de Jesus Cruz
* Guilherme Sollano Andrade dos Santos
* José Weverton de Oliveira Vilar
* Leonardo Caricchio do Nascimento
* Matheus Henrique Silva de Melo

---

## Diagnóstico e Evidências

### Avaliação de Gestão e Processos (Eixo A - MPS.BR: GPR)

Analisando o histórico do repositório, com foco na Issue `#659` e no Pull Request `#660`, notamos problemas na documentação de requisitos e na rastreabilidade. Algumas funcionalidades foram adicionadas sem testes prévios, e ocorreram mudanças de escopo que não foram registradas durante a correção de bugs. Isso indica um risco médio-alto para a manutenção do software a longo prazo.

Sobre o gerenciamento de riscos técnicos, o projeto acerta ao evitar o *vendor lock-in*, isolando as integrações na pasta `integrations/` e centralizando o tratamento de erros no módulo `core/recovery`. Por outro lado, a falta de comentários padronizados, como `TODO` ou `FIXME`, dificulta a visualização de pendências por parte da equipe, o que consideramos um risco médio.

Em relação ao ritmo de trabalho, o gráfico de contribuições mostra um padrão de centralização. Um único desenvolvedor concentra quase seis vezes mais *commits* que o segundo colaborador mais ativo. As entregas acontecem em picos irregulares (*crunch time*), e as revisões de código (PRs) parecem focar mais em fazer a funcionalidade rodar do que em discutir o design do código. Esse cenário traz um risco alto, pois o projeto depende muito de uma só pessoa.

### Anatomia do Código e Dívida Técnica (Eixo B - SOLID e DRY)

O código apresenta pontos positivos e negativos. Um acerto claro é o respeito ao Princípio da Inversão de Dependência (DIP) na integração com os modelos de IA. O agente principal depende apenas da interface `LlmService`, o que facilita trocar o provedor de IA sem precisar alterar a lógica central do sistema.

Por outro lado, encontramos uma violação direta do Princípio da Responsabilidade Única (SRP) na classe `VannaBase` (da versão *legacy*). Com 2.125 linhas e 65 métodos, essa classe concentra responsabilidades demais: ela gera *queries* SQL, conecta ao banco de dados, chama o LLM e lida com *embeddings* ao mesmo tempo.

Também notamos repetição de código, o que quebra o princípio DRY (*Don't Repeat Yourself*), na parte dos provedores de linguagem. A lógica de tratar parâmetros e interpretar *tool_calls* — visível no método `_extract_tool_calls_from_message` do `OpenAILlmService` — aparece copiada em outras classes. Esse trecho poderia ser facilmente isolado em uma função utilitária.

### Mapeamento de Padrões de Projeto (Eixo C - GoF)

Durante a análise, verificamos como o sistema aplica os padrões de projeto (GoF):

* **Padrões Criacionais:** Faltou o uso do padrão *Singleton* para gerenciar as conexões com os bancos vetoriais (como o `ChromaDB`), o que acaba gerando múltiplas conexões desnecessárias. Também não existe uma *Factory* central para instanciar os serviços de IA.
* **Padrões Estruturais:** O padrão *Adapter* foi bem aplicado. As diferentes APIs (OpenAI, Anthropic, Google) são adaptadas para funcionar com o contrato do `LlmService`, garantindo que o resto do sistema trabalhe apenas com o formato padronizado `LlmResponse`.
* **Padrões Comportamentais:** Na transição para a nova arquitetura baseada em agentes, o controle de fluxo foi delegado quase totalmente ao LLM. Não foi implementado um padrão como o *Chain of Responsibility* para validar as ações. Como resultado, o método `tool_registry.execute()` roda comandos diretamente a partir da resposta do modelo, o que é perigoso caso a IA sofra alguma alucinação.

---

## Plano de Resgate Técnico

### 1. Refatoração Conceitual: Proteção de Execução de Ferramentas

O maior problema de segurança e arquitetura encontrado no Vanna 2.0 é a execução direta de ferramentas baseada apenas no que o LLM decide. Para resolver isso, propomos implementar o padrão **Chain of Responsibility**.

A ideia é criar *middlewares* de execução (`ExecutionMiddleware`) que fiquem entre a resposta da IA e a chamada real da ferramenta. Por exemplo, antes de rodar qualquer comando no banco de dados, a requisição passa por um `SQLSanitizationMiddleware`. Se esse interceptador encontrar comandos como `DROP` ou `DELETE`, a execução é bloqueada imediatamente. O diagrama UML e os detalhes dessa refatoração estão na pasta `/diagramas` e no PDF principal.

### 2. Roadmap de Maturidade (MPS.BR - Nível G)

Para adequar o repositório aos requisitos básicos do Nível G do MPS.BR nos próximos 90 dias, sugerimos três ações práticas:

1. **Ação 1 - Gestão de Projetos (GPR):** Reduzir a dependência de um único mantenedor usando o *GitHub Projects* para organizar as tarefas e criar uma cadência previsível. É importante distribuir as permissões de *merge* para outros membros e documentar formalmente os riscos do projeto no repositório.
2. **Ação 2 - Gerência de Requisitos (GRE):** Evitar que decisões importantes fiquem espalhadas em comentários de Pull Requests. Sugerimos configurar *Issue Templates* com critérios de aceitação claros e usar ADRs (*Architecture Decision Records*) para registrar qualquer mudança que afete a estrutura do sistema.
3. **Ação 3 - Qualidade do Produto (QPR):** Configurar *pipelines* de CI/CD para automatizar os testes. Também recomendamos definir um *Definition of Done* (DoD) formal, exigindo que os PRs só sejam aprovados se passarem por análise estática de segurança (SAST) e atingirem uma cobertura mínima nos testes unitários.

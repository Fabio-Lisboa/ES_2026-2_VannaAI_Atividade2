# Refatoração Conceitual: Chain of Responsibility na Execução de Ferramentas

## Diagnóstico do Problema
O agente principal da versão 2.0 executa chamadas de ferramentas de maneira direta, confiando integralmente na saída textual do LLM. Essa abordagem não possui uma camada de interceptação e validação entre a inferência da IA e a execução real de queries no banco de dados.

## Padrão Proposto
Aplicação do padrão Chain of Responsibility através da implementação de Middlewares de Execução.

## Como Funciona a Solução
A arquitetura passa a tratar cada requisição de ferramenta como um objeto (`ToolExecutionRequest`) que transita por uma corrente de avaliadores.
1. O LLM solicita a execução de uma ferramenta.
2. A requisição é submetida ao `SQLSanitizationMiddleware`.
3. O interceptador inspeciona a string em `args.sql`.
4. Se o comando contiver instruções não permitidas (como DROP ou DELETE), a corrente é interrompida, retornando um erro imediato ao agente.
5. O método de execução física só é alcançado se todos os elos da corrente validarem a operação com sucesso.
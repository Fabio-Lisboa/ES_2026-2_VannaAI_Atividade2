# Padrões de Projeto (Eixo C - GoF)

## 1. Padrões Criacionais
A infraestrutura falha no gerenciamento eficiente de instâncias de comunicação externa. Não há implementação do padrão Singleton para conexões com bancos vetoriais, como o ChromaDB, o que permite a criação de clientes redundantes e aumenta o consumo de memória. Além disso, a injeção de dependência atual funciona como uma Factory implícita, mas falta uma classe centralizada para controlar a instanciação dos diferentes provedores de IA.

## 2. Padrões Estruturais
O padrão Adapter é empregado com sucesso na camada de integrações. O repositório lida com diversas APIs de terceiros que possuem contratos próprios. A interface `LlmService` atua como o alvo da adaptação. Todas as respostas externas são normalizadas para os modelos internos `LlmRequest` e `LlmResponse`, garantindo o baixo acoplamento.

## 3. Padrões Comportamentais
Na transição para a nova versão, o controle processual via condicionais foi substituído por um Agentic Loop. No entanto, a aplicação delega totalmente o controle de fluxo ao modelo de linguagem, sem a proteção de um padrão comportamental de validação. O método de execução de ferramentas é invocado de maneira cega a partir da saída da IA. Na ausência de um Chain of Responsibility para checar os comandos gerados, o sistema fica vulnerável a injeções de SQL acidentais resultantes de alucinações do modelo.
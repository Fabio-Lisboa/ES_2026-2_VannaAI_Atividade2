# Anatomia do Código e Dívida Técnica (Eixo B - SOLID e DRY)

## 1. O Teste da Troca (Princípio da Inversão de Dependência)
O projeto respeita o Princípio da Inversão de Dependência (DIP) na sua comunicação com serviços externos de IA. O núcleo da aplicação, representado pelo módulo Agent, não depende de implementações concretas, mas sim da interface `LlmService`. Isso significa que a substituição de um provedor exigiria modificações em apenas um ou dois arquivos específicos de integração, sem impacto sistêmico no código central.

## 2. Busca por "God Objects" (Princípio da Responsabilidade Única)
A inspeção identificou uma quebra severa do Princípio da Responsabilidade Única (SRP) na versão legacy do sistema. A classe `VannaBase` apresenta 2.125 linhas de código e 65 métodos. Ela assume simultaneamente sete responsabilidades primárias, incluindo gerenciamento de conexões de banco de dados, geração e extração de SQL, controle de prompts e treinamento de embeddings. 

## 3. Métricas de Duplicação (Princípio DRY)
Detectamos violações parciais do princípio DRY (Don't Repeat Yourself) na camada de integração de LLMs. Diferentes provedores implementam lógicas muito semelhantes para parsing de ferramentas e tratamento de parâmetros. Um exemplo claro é o método `_extract_tool_calls_from_message` presente no adaptador da OpenAI, cuja lógica de conversão de argumentos JSON poderia ser abstraída para uma camada utilitária compartilhada entre todos os serviços.
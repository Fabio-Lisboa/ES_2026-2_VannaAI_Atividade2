# Evidências: Anatomia do Código (Eixo B)

## 1. Busca por God Objects (Violação de SRP)
* **Arquivo Inspecionado:** `src/vanna/legacy/base/base.py`
* **Análise:** Classe aglutinando 2.125 linhas e 65 métodos. Responsabilidades múltiplas: banco de dados, geração SQL, extração de IA e manipulação de *embeddings*.
* **Evidência Visual:** `../analise/Eixo-B-Codigo/imagens/god_object/vannabase_2125_linhas.png`

## 2. Métricas de Duplicação (Violação Parcial DRY)
* **Trecho Inspecionado:** Método `_extract_tool_calls_from_message`.
* **Análise:** A lógica de *parsing* e tratamento de JSON para chamadas de ferramentas é duplicada entre implementações de provedores, como OpenAI e Anthropic.
* **Evidência Visual:** `../analise/Eixo-B-Codigo/imagens/metricas_dry/extract_tool_calls.png`
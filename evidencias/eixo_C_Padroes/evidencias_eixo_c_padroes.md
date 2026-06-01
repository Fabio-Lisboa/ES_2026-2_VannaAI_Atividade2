# Evidências: Padrões de Projeto (Eixo C)

## 1. Padrões Criacionais (Ausência de Singleton)
* **Trecho Inspecionado:** Inicialização do `PersistentClient` no módulo `chromadb/agent_memory.py`.
* **Análise:** Cada instância cria sua própria conexão com o banco de vetores, provocando sobrecarga de rede e consumo excessivo de memória por ausência de um mecanismo `Singleton` centralizado.
* **Evidência Visual:** `../analise/Eixo-C-Padroes/imagens/chromadb_no_singleton.png`

## 2. Padrões Comportamentais (Ausência de Chain of Responsibility)
* **Trecho Inspecionado:** `Agentic Loop` no arquivo `core/agent/agent.py`.
* **Análise:** O fluxo transfere todo o controle processual para a IA. O comando é executado imediatamente via `await self.tool_registry.execute()`, sem validação prévia de segurança.
* **Evidência Visual:** `../analise/Eixo-C-Padroes/imagens/execucao_cega_agent.png`
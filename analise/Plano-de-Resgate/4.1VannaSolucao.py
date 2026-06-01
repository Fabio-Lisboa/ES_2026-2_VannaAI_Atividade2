# 1. O Contexto do Pedido da Ferramenta
class ToolExecutionRequest:
    def __init__(self, tool_name, arguments, user_context):
        self.tool_name = tool_name
        self.arguments = arguments
        self.user_context = user_context
        self.is_blocked = False

# 2. A Corrente de Responsabilidade (Handler Base)
class ExecutionMiddleware:
    def __init__(self, next_middleware=None):
        self.next_middleware = next_middleware

    def handle(self, request: ToolExecutionRequest):
        if not request.is_blocked and self.next_middleware:
            return self.next_middleware.handle(request)

# 3. Os Elos da Corrente (Validações de Segurança e Negócio)
class RateLimitMiddleware(ExecutionMiddleware):
    def handle(self, request: ToolExecutionRequest):
        if check_quota(request.user_context) > LIMIT:
            request.is_blocked = True
            return "Erro: Limite de uso excedido."
        return super().handle(request)

class SQLSanitizationMiddleware(ExecutionMiddleware):
    def handle(self, request: ToolExecutionRequest):
        if request.tool_name == "run_sql":
            query = request.arguments.get('sql', '').upper()
            if "DROP" in query or "DELETE" in query:
                request.is_blocked = True
                return "Erro: AI tentou rodar query destrutiva!"
        return super().handle(request)

class FinalExecutionMiddleware(ExecutionMiddleware):
    def handle(self, request: ToolExecutionRequest):
        # Se chegou até aqui, a IA está autorizada a rodar a ferramenta
        return tool_registry.execute(request.tool_name, request.arguments)

# 4. Uso na Arquitetura Vanna 2.0
# Agora o Agente não ataca o banco diretamente. Ele passa pela corrente!
pipeline_seguranca = RateLimitMiddleware(SQLSanitizationMiddleware(FinalExecutionMiddleware()))

# Quando a IA pede para rodar algo:
resultado = pipeline_seguranca.handle(ToolExecutionRequest(
    tool_name="run_sql", 
    arguments={"sql": "DROP TABLE usuarios;"}, 
    user_context=current_user
))
# Resultado será o bloqueio feito pelo SQLSanitizationMiddleware!
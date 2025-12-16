

            #erros de orquestração
#traduzem erros de domínio
#agregam contexto
class ServiceError(Exception):
    """Erro genérico de serviço."""


class NotFoundError(ServiceError):
    """Recurso não encontrado."""


class BusinessRuleError(ServiceError):
    """Violação de regra de negócio (ex: sem exemplares disponíveis)."""

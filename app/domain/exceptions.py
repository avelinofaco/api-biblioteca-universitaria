       
             #regras do negócio

class DomainError(Exception):
    """Erro base de domínio."""


class UsuarioNaoEncontrado(DomainError):
    pass


class UsuarioComMultaPendente(DomainError):
    pass


class LimiteEmprestimosExcedido(DomainError):
    pass

class EmprestimoInvalido(DomainError):
    pass
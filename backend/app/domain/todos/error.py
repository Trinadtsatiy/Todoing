from backend.app.domain.common.error import DomainError


class TodoNotFoundError(DomainError):
    pass


class TodoAccessDeniedError(DomainError):
    pass
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from backend.app.domain.common.entity import Entity
from backend.app.domain.common.error import DomainValidationError
from backend.app.domain.users.user import UserId

from backend.app.domain.common.value_object import ValueObject


@dataclass(frozen=True)
class TodoId(ValueObject):
    value: UUID


@dataclass(frozen=True)
class TodoTitle(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("Требуется заголовок Todo.")

        if len(self.value) > 100:
            raise DomainValidationError("Заголовок Todo должно быть менее 100 символов")


@dataclass(frozen=True)
class TodoContent(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("Содержание Todo должно иметь хотя бы 1 символ.")

        if len(self.value) > 1000:
            raise DomainValidationError("Содержание Todo должно быть менее 1000 символов.")


@dataclass
class Todo(Entity):
    id: TodoId
    title: TodoTitle
    owner_id: UserId
    content: TodoContent
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        title: str,
        content: str,
        owner_id: UserId,
        created_at: datetime,
        updated_at: datetime,
    ) -> "Todo":
        return Todo(
            owner_id=owner_id,
            id=TodoId(value=uuid4()),
            title=TodoTitle(value=title),
            content=TodoContent(value=content),
            created_at=created_at,
            updated_at=updated_at,
        )

import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from backend.app.domain.common.entity import Entity
from backend.app.domain.common.error import DomainValidationError
from backend.app.domain.common.value_object import ValueObject


@dataclass(frozen=True)
class UserEmail(ValueObject):
    value: str

    def __post_init__(self) -> None:
        pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, self.value):
            raise DomainValidationError("Неверный формат почты. Почта должна быть в формате 'example@example.com'.")


@dataclass(frozen=True)
class UserFirstName(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("Имя должно содержать не менее 1 символа.")
        if len(self.value) > 100:
            raise DomainValidationError("Имя должно содержать меньше 100 символов.")
        if not self.value.isalpha():
            raise DomainValidationError("Имя должно состоять только из букв.")


@dataclass(frozen=True)
class UserLastName(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("Фамилия должна содержать не менее 1 символа.")
        if len(self.value) > 100:
            raise DomainValidationError("Фамилия должна содержать меньше 100 символов.")
        if not self.value.isalpha():
            raise DomainValidationError("Фамилия должна состоять только из букв.")


@dataclass(frozen=True)
class UserId(ValueObject):
    value: UUID


@dataclass
class User(Entity[UserId]):
    first_name: UserFirstName
    last_name: UserLastName
    email: UserEmail
    hashed_password: str

    @staticmethod
    def create(first_name: str, last_name: str, email: str, hashed_password: str) -> "User":
        return User(
            id=UserId(uuid4()),
            email=UserEmail(email),
            hashed_password=hashed_password,
            last_name=UserLastName(last_name),
            first_name=UserFirstName(first_name),
        )

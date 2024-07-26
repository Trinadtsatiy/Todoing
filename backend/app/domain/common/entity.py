from dataclasses import dataclass
from typing import Generic, TypeVar

from backend.app.domain.common.value_object import ValueObject

EntityId = TypeVar("EntityId", bound=ValueObject)


@dataclass
class Entity(Generic[EntityId]):
    id: EntityId

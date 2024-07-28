from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class UpdateTodoRequest:
    id: UUID
    title: str
    content: str | None = field(default=None)

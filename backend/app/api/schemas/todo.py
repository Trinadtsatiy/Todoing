from dataclasses import dataclass, field


@dataclass(frozen=True)
class UpdateTodoSchema:
    title: str
    content: str | None = field(default=None)

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateTodoRequest:
    title: str
    content: str

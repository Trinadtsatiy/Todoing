from dataclasses import dataclass

from backend.app.application.contracts.todos.todo_details_response import \
    TodoDetailsResponse


@dataclass(frozen=True)
class TodoListResponse:
    data: list[TodoDetailsResponse]
    count: int

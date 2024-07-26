from uuid import UUID

from backend.app.application.common.interactor import Interactor
from backend.app.application.contracts.todos.get_todos_request import \
    GetTodoListRequest
from backend.app.application.contracts.todos.todo_details_response import \
    TodoDetailsResponse
from backend.app.application.contracts.todos.todo_list_response import \
    TodoListResponse
from backend.app.domain.todos.error import TodoNotFoundError
from backend.app.domain.todos.repository import TodoRepository
from backend.app.domain.users.user import UserId


class GetTodoById(Interactor[UUID, TodoDetailsResponse]):
    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    async def __call__(self, request: UUID) -> TodoDetailsResponse:
        todo = await self.todo_repository.find_by_id(UserId(request))  # type: ignore

        if todo is None:
            raise TodoNotFoundError(f"Todo с id {request} не существует")

        return TodoDetailsResponse(
            id=todo.id.value,
            title=todo.title.value,
            content=todo.content.value,
            owner_id=todo.owner_id.value,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )


class GetTodoList(Interactor[GetTodoListRequest, TodoListResponse]):
    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    async def __call__(self, request: GetTodoListRequest) -> TodoListResponse:
        todos = await self.todo_repository.find_all(request.limit, request.offset)

        if not todos:
            return TodoListResponse([], 0)

        data = [
            TodoDetailsResponse(
                id=todo.id.value,
                title=todo.title.value,
                content=todo.content.value,
                owner_id=todo.owner_id.value,
                created_at=todo.created_at,
                updated_at=todo.updated_at,
            )
            for todo in todos
        ]

        return TodoListResponse(data, len(data))

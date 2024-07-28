from backend.app.application.common.date_time_provider import DateTimeProvider
from backend.app.application.common.id_provider import IdProvider
from backend.app.application.common.interactor import Interactor
from backend.app.application.common.unit_of_work import UnitOfWork
from backend.app.application.contracts.todos.todo_details_response import \
    TodoDetailsResponse
from backend.app.application.contracts.todos.update_todo_request import \
    UpdateTodoRequest
from backend.app.domain.todos.error import (TodoAccessDeniedError,
                                            TodoNotFoundError)
from backend.app.domain.todos.repository import TodoRepository
from backend.app.domain.todos.todo import TodoContent, TodoId, TodoTitle


class UpdateTodo(Interactor[UpdateTodoRequest, TodoDetailsResponse]):
    def __init__(
        self,
        uow: UnitOfWork,
        id_provider: IdProvider,
        todo_repository: TodoRepository,
        date_time_provider: DateTimeProvider,
    ) -> None:
        self.uow = uow
        self.id_provider = id_provider
        self.todo_repository = todo_repository
        self.date_time_provider = date_time_provider

    async def __call__(self, request: UpdateTodoRequest) -> TodoDetailsResponse:
        user_id = self.id_provider.get_current_user_id()

        todo = await self.todo_repository.find_by_id(TodoId(request.id))

        if todo is None:
            raise TodoNotFoundError(f"Todo с id {request.id} не существует")

        if todo.owner_id != user_id:
            raise TodoAccessDeniedError("Вы не создатель этой Todo")

        updated_at = self.date_time_provider.get_current_time()

        if not request.content:
            content = None
        else:
            content = TodoContent(request.content)

        await self.todo_repository.update(
            todo.id,
            content=content,
            updated_at=updated_at,
            title=TodoTitle(request.title),
        )

        await self.uow.commit()

        return TodoDetailsResponse(
            id=todo.id.value,
            title=request.title,
            content=request.content or todo.content.value,
            owner_id=todo.owner_id.value,
            created_at=todo.created_at,
            updated_at=updated_at,
        )

from backend.app.application.common.date_time_provider import DateTimeProvider
from backend.app.application.common.id_provider import IdProvider
from backend.app.application.common.interactor import Interactor
from backend.app.application.common.unit_of_work import UnitOfWork
from backend.app.application.contracts.todos.create_todo_request import \
    CreateTodoRequest
from backend.app.application.contracts.todos.todo_details_response import \
    TodoDetailsResponse
from backend.app.domain.todos.repository import TodoRepository
from backend.app.domain.todos.todo import Todo


class CreateTodo(Interactor[CreateTodoRequest, TodoDetailsResponse]):
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

    async def __call__(self, request: CreateTodoRequest) -> TodoDetailsResponse:
        user_id = self.id_provider.get_current_user_id()

        todo = Todo.create(
            owner_id=user_id,
            title=request.title,
            content=request.content,
            created_at=self.date_time_provider.get_current_time(),
            updated_at=self.date_time_provider.get_current_time(),
        )
        await self.todo_repository.create(todo)

        await self.uow.commit()

        return TodoDetailsResponse(
            id=todo.id.value,
            title=todo.title.value,
            content=todo.content.value,
            owner_id=todo.owner_id.value,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

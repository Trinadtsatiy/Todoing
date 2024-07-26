from uuid import UUID

from backend.app.application.common.id_provider import IdProvider
from backend.app.application.common.interactor import Interactor
from backend.app.application.common.unit_of_work import UnitOfWork
from backend.app.domain.todos.error import (TodoAccessDeniedError,
                                            TodoNotFoundError)
from backend.app.domain.todos.repository import TodoRepository
from backend.app.domain.todos.todo import TodoId


class DeleteTodo(Interactor[UUID, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        id_provider: IdProvider,
        todo_repository: TodoRepository,
    ) -> None:
        self.uow = uow
        self.id_provider = id_provider
        self.todo_repository = todo_repository

    async def __call__(self, request: UUID) -> None:
        user_id = self.id_provider.get_current_user_id()

        todo = await self.todo_repository.find_by_id(TodoId(request))

        if not todo:
            raise TodoNotFoundError(f"Todo с id {request}")

        if todo.owner_id != user_id:
            raise TodoAccessDeniedError("Вы не создатель этой Todo")

        await self.todo_repository.delete(todo.id)

        await self.uow.commit()

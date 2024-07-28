from datetime import datetime
from typing import Protocol

from backend.app.domain.todos.todo import Todo, TodoContent, TodoId, TodoTitle
from backend.app.domain.users.user import UserId


class TodoRepository(Protocol):
    async def create(self, todo: Todo) -> None:
        raise NotImplementedError

    async def find_all(self, limit: int = 20, offset: int = 0) -> list[Todo] | None:
        raise NotImplementedError

    async def find_by_id(self, id: TodoId) -> Todo | None:
        raise NotImplementedError

    async def find_by_owner_id(self, owner_id: UserId, limit: int = 20, offset: int = 0) -> list[Todo] | None:
        raise NotImplementedError

    async def update(
        self,
        id: TodoId,
        title: TodoTitle,
        updated_at: datetime,
        content: TodoContent | None = None,
    ) -> None:
        raise NotImplementedError

    async def delete(self, id: TodoId) -> None:
        raise NotImplementedError

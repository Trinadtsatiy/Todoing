from datetime import datetime

from psycopg import AsyncConnection
from psycopg.rows import dict_row

from backend.app.domain.todos.repository import TodoRepository
from backend.app.domain.todos.todo import Todo, TodoContent, TodoId, TodoTitle
from backend.app.domain.users.user import UserId
from backend.app.infra.persistence.repositories.mappers.todo_mapper import \
    todo_from_dict_to_entity


class PostgresqlTodoRepository(TodoRepository):
    __slots__ = ("connection",)

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def create(self, todo: Todo) -> None:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO todos (id, title, content, owner_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (
                    todo.id.value,
                    todo.title.value,
                    todo.content.value,
                    todo.owner_id.value,
                    todo.created_at,
                    todo.updated_at,
                ),
            )

    async def find_by_id(self, id: TodoId) -> Todo | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, title, content, owner_id, created_at, updated_at
                FROM todos
                WHERE id = %s;
                """,
                (id.value,),
            )

            result = await cursor.fetchone()

            if result is None:
                return None

            return todo_from_dict_to_entity(result)

    async def find_all(self, limit: int = 20, offset: int = 0) -> list[Todo] | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, title, content, owner_id, created_at, updated_at
                FROM todos LIMIT %s OFFSET %s;
                """,
                (limit, offset),
            )

            result = await cursor.fetchall()

            if not result:
                return None

            return [todo_from_dict_to_entity(row) for row in result]

    async def find_by_owner_id(self, owner_id: UserId, limit: int = 20, offset: int = 0) -> list[Todo] | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, title, content, owner_id, created_at, updated_at
                FROM todos
                WHERE owner_id = %s
                LIMIT %s OFFSET %s;
                """,
                (owner_id.value, limit, offset),
            )

            result = await cursor.fetchall()

            if not result:
                return None

            return [todo_from_dict_to_entity(row) for row in result]

    async def update(
        self,
        id: TodoId,
        title: TodoTitle,
        updated_at: datetime,
        content: TodoContent | None = None,
    ) -> None:
        async with self.connection.cursor() as cursor:
            if content is not None:
                query = """UPDATE todos SET title = %s, updated_at = %s, content = %s WHERE id = %s;"""
                await cursor.execute(query, (title.value, updated_at, content.value, id.value))

            else:
                query = """UPDATE todos SET title = %s, updated_at = %s WHERE id = %s;"""
                await cursor.execute(query, (title.value, updated_at, id.value))

    async def delete(self, id: TodoId) -> None:
        async with self.connection.cursor() as cursor:
            await cursor.execute("DELETE FROM todos WHERE id = %s;", (id.value,))

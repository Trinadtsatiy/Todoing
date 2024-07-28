from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from backend.app.api.dependencies.authentication import auth_required
from backend.app.api.schemas.todo import UpdateTodoSchema
from backend.app.application.contracts.todos.create_todo_request import \
    CreateTodoRequest
from backend.app.application.contracts.todos.get_todos_request import \
    GetTodoListRequest
from backend.app.application.contracts.todos.todo_details_response import \
    TodoDetailsResponse
from backend.app.application.contracts.todos.todo_list_response import \
    TodoListResponse
from backend.app.application.contracts.todos.update_todo_request import \
    UpdateTodoRequest
from backend.app.application.usecases.todos.create_todo import CreateTodo
from backend.app.application.usecases.todos.delete_todo import DeleteTodo
from backend.app.application.usecases.todos.get_todo import (GetTodoById,
                                                             GetTodoList)
from backend.app.application.usecases.todos.update_todo import UpdateTodo

todo_router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    route_class=DishkaRoute,
)


@todo_router.get("/", response_model=TodoListResponse)
async def get_todo_list(
    get_todo_list_request: Annotated[GetTodoListRequest, Depends()],
    get_todo_list_interactor: FromDishka[GetTodoList],
) -> TodoListResponse:
    return await get_todo_list_interactor(get_todo_list_request)


@todo_router.post(
    "/",
    status_code=201,
    response_model=TodoDetailsResponse,
    dependencies=[Depends(auth_required)],
)
async def create_todo(
    create_todo_request: CreateTodoRequest,
    create_todo_interactor: FromDishka[CreateTodo],
) -> TodoDetailsResponse:
    return await create_todo_interactor(create_todo_request)


@todo_router.get("/{todo_id}", response_model=TodoDetailsResponse)
async def get_todo_by_id(
    todo_id: UUID,
    get_todo_interactor: FromDishka[GetTodoById],
) -> TodoDetailsResponse:
    return await get_todo_interactor(todo_id)


@todo_router.patch(
    "/{todo_id}",
    response_model=TodoDetailsResponse,
    dependencies=[Depends(auth_required)],
)
async def update_todo(
    todo_id: UUID,
    update_todo_schema: UpdateTodoSchema,
    update_todo_interactor: FromDishka[UpdateTodo],
) -> TodoDetailsResponse:
    return await update_todo_interactor(
        UpdateTodoRequest(
            id=todo_id,
            title=update_todo_schema.title,
            content=update_todo_schema.content,
        )
    )


@todo_router.delete(
    "/{todo_id}",
    status_code=204,
    dependencies=[Depends(auth_required)],
)
async def delete_todo(
    todo_id: UUID,
    delete_todo_interactor: FromDishka[DeleteTodo],
) -> None:
    await delete_todo_interactor(todo_id)

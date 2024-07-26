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

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    route_class=DishkaRoute,
)


@post_router.get("/", response_model=TodoListResponse)
async def get_post_list(
    get_post_list_request: Annotated[GetTodoListRequest, Depends()],
    get_post_list_interactor: FromDishka[GetTodoList],
) -> TodoListResponse:
    return await get_post_list_interactor(get_post_list_request)


@post_router.post(
    "/",
    status_code=201,
    response_model=TodoDetailsResponse,
    dependencies=[Depends(auth_required)],
)
async def create_post(
    create_post_request: CreateTodoRequest,
    create_post_interactor: FromDishka[CreateTodo],
) -> TodoDetailsResponse:
    return await create_post_interactor(create_post_request)


@post_router.get("/{post_id}", response_model=TodoDetailsResponse)
async def get_post_by_id(
    post_id: UUID,
    get_post_interactor: FromDishka[GetTodoById],
) -> TodoDetailsResponse:
    return await get_post_interactor(post_id)


@post_router.patch(
    "/{post_id}",
    response_model=TodoDetailsResponse,
    dependencies=[Depends(auth_required)],
)
async def update_post(
    post_id: UUID,
    update_post_schema: UpdateTodoSchema,
    update_post_interactor: FromDishka[UpdateTodo],
) -> TodoDetailsResponse:
    return await update_post_interactor(
        UpdateTodoRequest(
            id=post_id,
            title=update_post_schema.title,
            content=update_post_schema.content,
        )
    )


@post_router.delete(
    "/{post_id}",
    status_code=204,
    dependencies=[Depends(auth_required)],
)
async def delete_post(
    post_id: UUID,
    delete_post_interactor: FromDishka[DeleteTodo],
) -> None:
    await delete_post_interactor(post_id)

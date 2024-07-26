from collections.abc import AsyncGenerator

from dishka import (AsyncContainer, Provider, Scope, from_context,
                    make_async_container, provide)
from fastapi import Request
from psycopg import AsyncConnection
from psycopg.conninfo import conninfo_to_dict

from backend.app.application.common.date_time_provider import DateTimeProvider
from backend.app.application.common.id_provider import IdProvider
from backend.app.application.common.jwt_processor import JwtTokenProcessor
from backend.app.application.common.password_hasher import PasswordHasher
from backend.app.application.common.unit_of_work import UnitOfWork
from backend.app.application.usecases.authentication.login import Login
from backend.app.application.usecases.authentication.register import Register
from backend.app.application.usecases.todos.create_todo import CreateTodo
from backend.app.application.usecases.todos.delete_todo import DeleteTodo
from backend.app.application.usecases.todos.get_todo import (GetTodoById,
                                                             GetTodoList)
from backend.app.application.usecases.todos.update_todo import UpdateTodo
from backend.app.application.usecases.users.get_current_user import \
    GetCurrentUser
from backend.app.domain.todos.repository import TodoRepository
from backend.app.domain.users.repository import UserRepository
from backend.app.infra.authentication.id_provider import JwtTokenIdProvider
from backend.app.infra.authentication.jwt_processor import \
    JoseJwtTokenProcessor
from backend.app.infra.authentication.jwt_settings import JwtSettings
from backend.app.infra.date_time_provider import (SystemDateTimeProvider,
                                                  Timezone)
from backend.app.infra.persistence.db_settings import DatabaseSettings
from backend.app.infra.persistence.repositories.todo_repository import \
    PostgresqlTodoRepository
from backend.app.infra.persistence.repositories.user_repository import \
    PostgresqlUserRepository
from backend.app.infra.persistence.unit_of_work import PostgresqlUnitOfWork
from backend.app.infra.security.password_hasher import Pbkdf2PasswordHasher
from backend.app.infra.settings import MainSettings
from backend.app.infra.utils.get_env_var import get_env_variable


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def jwt_settings(self) -> JwtSettings:
        return JwtSettings(
            secret=get_env_variable("JWT_SECRET_KEY"),
            algorithm=get_env_variable("JWT_ALGORITHM"),
            expires_in=int(get_env_variable("JWT_EXPIRES_IN")),
        )

    @provide(scope=Scope.APP)
    def db_settings(self) -> DatabaseSettings:
        return DatabaseSettings(
            host=get_env_variable("POSTGRES_HOST"),
            port=int(get_env_variable("POSTGRES_PORT")),
            user=get_env_variable("POSTGRES_USER"),
            password=get_env_variable("POSTGRES_PASSWORD"),
            database=get_env_variable("POSTGRES_DB"),
        )

    @provide(scope=Scope.APP)
    def main_settings(self, jwt_settings: JwtSettings, db_settings: DatabaseSettings) -> MainSettings:
        return MainSettings(
            jwt_settings=jwt_settings,
            db_settings=db_settings,
        )


class DatabaseConfigurationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncConnection)
    async def provide_db_connection(self, db_settings: DatabaseSettings) -> AsyncGenerator[AsyncConnection, None]:
        connection = await AsyncConnection.connect(
            **conninfo_to_dict(db_settings.uri),
        )
        yield connection
        await connection.close()


class DatabaseAdaptersProvider(Provider):
    scope = Scope.REQUEST

    unit_of_work = provide(PostgresqlUnitOfWork, provides=UnitOfWork)
    user_repository = provide(PostgresqlUserRepository, provides=UserRepository)
    todo_repository = provide(PostgresqlTodoRepository, provides=TodoRepository)


class AuthenticationAdaptersProvider(Provider):
    token_processor = provide(JoseJwtTokenProcessor, scope=Scope.APP, provides=JwtTokenProcessor)
    request = from_context(
        scope=Scope.REQUEST,
        provides=Request,
    )

    @provide(scope=Scope.REQUEST, provides=IdProvider)
    def id_provider(self, token_processor: JwtTokenProcessor, request: Request) -> IdProvider:
        return JwtTokenIdProvider(token_processor=token_processor, token=request.auth)


class SecurityProvider(Provider):
    scope = Scope.APP
    password_hasher = provide(Pbkdf2PasswordHasher, provides=PasswordHasher)


class DateTimeProvider(Provider):  # type: ignore
    @provide(scope=Scope.APP, provides=DateTimeProvider)
    def provide_date_time_provider(self) -> DateTimeProvider:
        return SystemDateTimeProvider(Timezone.UTC)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    login = provide(Login)
    register = provide(Register)
    get_current_user = provide(GetCurrentUser)
    create_todo = provide(CreateTodo)
    get_todo_by_id = provide(GetTodoById)
    get_todo_list = provide(GetTodoList)
    update_todo = provide(UpdateTodo)
    delete_todo = provide(DeleteTodo)


def create_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        AuthenticationAdaptersProvider(),
        SecurityProvider(),
        UseCasesProvider(),
        DateTimeProvider(),  # type: ignore
    )

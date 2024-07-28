from os import getenv

from backend.app.infra.utils.exceptions import MissingEnvVariableError


def get_env_variable(var: str, default: str | None = None) -> str:
    env = getenv(var)

    if env is None:
        if default is None:
            raise MissingEnvVariableError(var)

        return default

    return env

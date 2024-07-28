from dataclasses import dataclass

from backend.app.infra.authentication.jwt_settings import JwtSettings
from backend.app.infra.persistence.db_settings import DatabaseSettings


@dataclass(frozen=True)
class MainSettings:
    jwt_settings: JwtSettings
    db_settings: DatabaseSettings

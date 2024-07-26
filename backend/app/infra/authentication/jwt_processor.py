from datetime import timedelta
from uuid import UUID

from jwt import PyJWTError, decode, encode

from backend.app.application.common.date_time_provider import DateTimeProvider
from backend.app.application.common.jwt_processor import JwtTokenProcessor
from backend.app.domain.users.user import UserId
from backend.app.infra.authentication.jwt_settings import JwtSettings


class JoseJwtTokenProcessor(JwtTokenProcessor):
    def __init__(self, jwt_options: JwtSettings, date_time_provider: DateTimeProvider) -> None:
        self.jwt_options = jwt_options
        self.date_time_provider = date_time_provider

    def generate_token(self, user_id: UserId) -> str:
        issued_at = self.date_time_provider.get_current_time()
        expiration_time = issued_at + timedelta(hours=self.jwt_options.expires_in)

        claims = {
            "iat": issued_at,
            "exp": expiration_time,
            "sub": str(user_id.value),
        }

        return encode(claims, self.jwt_options.secret, self.jwt_options.algorithm)

    def validate_token(self, token: str) -> UserId | None:
        try:
            payload = decode(token, self.jwt_options.secret, [self.jwt_options.algorithm])

            return UserId(UUID(payload["sub"]))

        except (PyJWTError, ValueError, KeyError):
            return None

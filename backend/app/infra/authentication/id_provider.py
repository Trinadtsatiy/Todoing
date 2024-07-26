from backend.app.application.common.id_provider import IdProvider
from backend.app.application.common.jwt_processor import JwtTokenProcessor
from backend.app.domain.users.error import UserIsNotAuthorizedError
from backend.app.domain.users.user import UserId


class JwtTokenIdProvider(IdProvider):
    def __init__(self, token_processor: JwtTokenProcessor, token: str) -> None:
        self.token_processor = token_processor
        self.token = token

    def get_current_user_id(self) -> UserId:
        user_id = self.token_processor.validate_token(self.token)

        if user_id is None:
            raise UserIsNotAuthorizedError("Инвалидные credentials")

        return user_id

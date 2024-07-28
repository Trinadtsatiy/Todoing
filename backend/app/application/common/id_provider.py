from typing import Protocol

from backend.app.domain.users.user import UserId


class IdProvider(Protocol):
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError

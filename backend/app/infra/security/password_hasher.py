from backend.app.application.common.password_hasher import PasswordHasher
from passlib.handlers.pbkdf2 import pbkdf2_sha256


class Pbkdf2PasswordHasher(PasswordHasher):
    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha256.verify(password, hashed_password)

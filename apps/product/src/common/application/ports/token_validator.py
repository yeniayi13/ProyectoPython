from abc import ABC, abstractmethod
from src.common.domain.jwt_payload import JWTPayload


class TokenValidator(ABC):
    @abstractmethod
    def validate_token(self, token: str) -> JWTPayload:
        pass

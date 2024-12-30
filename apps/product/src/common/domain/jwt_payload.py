from pydantic import BaseModel, Field, validator
import time
from src.common.domain.roles import Roles

class JWTPayload(BaseModel):
    user_id: str = Field(..., description="ID del usuario asociado al token")
    expires: float = Field(..., description="Timestamp de expiración del token")
    role: Roles = Field(..., description="Rol del usuario asociado al token")

    @validator("expires")
    def validate_expiration(cls, value):
        if value <= time.time():
            raise ValueError("El token ha expirado")
        return value

    @validator("role", pre=True)
    def validate_role(cls, value):
        if isinstance(value, str):
            try:
                return Roles(value)
            except ValueError:
                raise ValueError(f"Rol inválido: {value}")
        return value

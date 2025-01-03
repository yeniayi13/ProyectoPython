from typing import List
from src.common.domain.roles import Roles
from src.common.domain.jwt_payload import JWTPayload
from src.common.application.ports.token_validator import TokenValidator

class RoleValidatorService:
    def __init__(self, token_validator: TokenValidator):
        self.token_validator = token_validator

    def validate_role(self, token: str, allowed_roles: List[str]) -> JWTPayload:
        print('allowed_roles:',allowed_roles)
        jwt_payload: JWTPayload = self.token_validator.validate_token(token)
        print('dentro de validate roles despues de jwtpay')
        print('jwt_payload:', jwt_payload)

        
        # Convertir allowed_roles a instancias de Roles
        allowed_roles_enum = [Roles(role) for role in allowed_roles]
        

        if jwt_payload.role not in allowed_roles_enum:
            raise ValueError("Acceso denegado: rol no permitido")
        return jwt_payload

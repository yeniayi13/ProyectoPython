from typing import List
from src.common.domain.roles import Roles
from fastapi import Depends, HTTPException, status, Request
from pydantic import ValidationError
from src.common.application.services.role_validator_service import RoleValidatorService
from src.common.infrastructure.adapters.jwt_token_validator import JWTTokenValidator

def get_role_validator_service() -> RoleValidatorService:
    token_validator = JWTTokenValidator()
    return RoleValidatorService(token_validator)

def get_token_from_header(request: Request):
    authorization: str = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o faltante",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.split(" ")[1]

def require_roles(allowed_roles: List[Roles]):
    def role_checker(
        token: str = Depends(get_token_from_header), 
        role_validator: RoleValidatorService = Depends(get_role_validator_service)
    ):
        try:
            role_validator.validate_role(token, [role.value for role in allowed_roles])

        except ValueError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: rol no permitido"
            )
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED , detail="El token contiene datos inválidos"
            )
    return role_checker

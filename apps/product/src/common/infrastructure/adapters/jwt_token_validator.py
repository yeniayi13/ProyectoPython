from typing import Dict
from src.common.infrastructure.config.config import get_settings
from pydantic import ValidationError
import jwt
from src.common.application.ports.token_validator import TokenValidator
from src.common.domain.jwt_payload import JWTPayload

settings = get_settings()

SECRET_KEY =  settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM

class JWTTokenValidator(TokenValidator):
    def decode_token(self, token: str) -> Dict:
        try:
            # Decodifica el token utilizando PyJWT
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_token
        except jwt.ExpiredSignatureError as e:
            print('ExpiredSignatureError:',e)
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError as e:
            print('InvalidTokenError:',e)
            raise ValueError("Token inválido")
        except Exception as e:
            print('Exception:',e)

    def validate_token(self, token: str) -> JWTPayload:
        decoded_payload = self.decode_token(token)
        try:
            # Valida el payload usando el esquema JWTPayload
            jwt_payload = JWTPayload(**decoded_payload) 
            return jwt_payload
        except ValidationError as e:
            print('ValidationError: ',e)
            raise ValueError(f"Token inválido: {e}")
        except Exception as e:
            print('Exception',e)
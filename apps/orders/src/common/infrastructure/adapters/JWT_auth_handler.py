from fastapi import Security
from src.common.application.ports.auth_handler import Auth_handler
from src.common.infrastructure.config.config import get_settings
from src.common.utils.errors import Error
from src.common.utils.result import Result
import time
import jwt
from fastapi.security import HTTPBearer, OAuth2PasswordBearer


settings = get_settings()

JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_SECRET = settings.JWT_SECRET

oauth2_scheme = OAuth2PasswordBearer("/auth/log_in")
security = HTTPBearer()



class JWT_auth_handler(Auth_handler):

    def sign(self, id:str, role:str)->str:
        payload = {
            'user_id' : id,
            'expires' : time.time() + 5000,
            'role': role
            }
        
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token
    
                     
    def decode(self, token:  HTTPBearer = Security(security))-> Result:
        try:
            decoded_token = jwt.decode(token.credentials, JWT_SECRET, algorithms= JWT_ALGORITHM)
            if decoded_token["expires"]  >= time.time():
                return Result.success(decoded_token)
            else: 
                return Result.failure(Error('JWTExpired','The time of your JWT has expired',401))
        except Exception as e:
            if 'Signature verification failed' in str(e):
                return Result.failure(Error('JWTVerificationFailed','Signature verification failed because of an invalid token',401)) 
            if 'Invalid crypto padding' in str(e):
                return Result.failure(Error('InvalidCryptoPadding','Your JWT token is not complete, check it please',401))  
            print('decodeJWT e: ',e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  

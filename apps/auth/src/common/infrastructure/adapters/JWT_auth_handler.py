import time
import jwt
from src.user.application.models.user import Roles
from src.common.application.ports.auth_handler import Auth_handler
from src.common.infrastructure.config.config import get_settings
from src.common.utils.errors import Error
from src.common.utils.result import Result

settings = get_settings()

JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_SECRET = settings.JWT_SECRET

class JWT_auth_handler(Auth_handler):

    def sign(self, id:str, role:str)->str:
        payload = {
            'user_id' : id,
            'expires' : time.time() + 900,
            'role': role
            }
        
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token
    
    def decode(self,token:str)-> Result:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms= JWT_ALGORITHM)
            if decoded_token["expires"]  >= time.time():
                return Result.success(decoded_token)
            else: 
                return Result.failure(Error('JWTExpired','The time of your JWT has expired',401))
        except Exception as e:
            print('Unable to decode the token')
            print()
            print(e) 
        

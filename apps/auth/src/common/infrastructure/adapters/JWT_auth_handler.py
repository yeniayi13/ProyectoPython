import time
import jwt
from src.user.application.models.user import Roles
from src.common.application.ports.auth_handler import Auth_handler
from src.common.infrastructure.config.config import get_settings

settings = get_settings()

JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_SECRET = settings.JWT_SECRET

class JWT_auth_handler(Auth_handler):

    def sign(self, id:str, role:str):
        payload = {
            'user_id' : id,
            'expires' : time.time() + 900,
            'role': role
            }
        
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token
    
    def decode(self,token:str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms= JWT_ALGORITHM)
            if decoded_token["expires"]  >= time.time():
                return decoded_token 
            else: 
                return {'code': 401, 'msg': 'The time of your JWT has expired'}
        except Exception as e:
            print('Unable to decode the token')
            print()
            print(e) 
        

from src.common.infrastructure.adapters.JWT_auth_handler import JWT_auth_handler
from src.common.utils.errors import Error
from src.common.utils.result import Result

auth = JWT_auth_handler()  

def verify_roles(role,roles:list) -> Result:
    if role in roles:
        return True
    return False
    

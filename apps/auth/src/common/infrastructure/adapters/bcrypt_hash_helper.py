from bcrypt import checkpw,hashpw,gensalt
from src.common.application.ports.hash_helper import Hash_helper

class Bcrypt_hash_helper(Hash_helper):

    @staticmethod
    def verify_password(password:str, hashed_password:str):
        
        if checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
        else:
            return False
        
    @staticmethod
    def get_password_hashed(password:str):
        encoded = hashpw(
            password.encode("utf-8"),
            gensalt()
        )
        decoded = encoded.decode('utf-8')
        return decoded
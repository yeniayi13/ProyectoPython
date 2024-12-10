import enum

class Roles(enum):
    SUPERADMIN ='superadmin'
    MANAGER = 'manager'
    CLIENT = 'client'



class User():
    id:str
    name:str
    last_name:str
    ci: str
    username:str
    email:str
    role: Roles

    def __init__(self, name, last_name, ci, username, email, role):
        pass
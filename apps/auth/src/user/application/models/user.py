from enum import Enum

class Roles(Enum):
    SUPERADMIN ='SUPERADMIN'
    MANAGER = 'MANAGER'
    CLIENT = 'CLIENT'



class User():
    id:str
    name:str
    last_name:str
    ci: str
    username:str
    email:str
    role: Roles

    def __init__(self, name:str, last_name:str, ci:str, username:str, email:str, role:Roles):
        self.name = name
        self.last_name = last_name
        self.ci = ci
        self.username = username
        self.email = email
        self.role =role
from pydantic import BaseModel
from src.user.application.models.user import Roles


class Create_manager_dto(BaseModel):
    first_name:str
    last_name:str
    c_i:str
    username:str
    email:str
    password:str
    role:Roles

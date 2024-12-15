from typing import Optional
from pydantic import BaseModel, Field
from src.user.application.models.user import Roles


class Create_superadmin_dto(BaseModel):
    id: Optional[str] = Field(default='')
    first_name:str
    last_name:str
    c_i:str
    username:str
    email:str
    password:str
    role:Roles

from pydantic import BaseModel, EmailStr
from src.user.application.models.user import Roles
from datetime import datetime

class User_in_create(BaseModel):
    id:str
    first_name:str
    last_name:str
    c_i:str
    username:str
    email:EmailStr
    password:str
    role:str
    created_at:datetime
    updated_at:datetime

class User_in_auth(BaseModel):
    id:str
    password:str
from typing import Union
from pydantic import BaseModel, EmailStr, Field
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

class User_in_modify(BaseModel): 
    first_name:Union[str,None] = Field(default= None)
    last_name:Union[str,None] = Field(default= None)
    c_i:Union[str,None] = Field(default= None)
    username:Union[str,None] = Field(default= None)
    email:Union[EmailStr,None] = Field(default= None)
    updated_at:datetime = Field(default= None)

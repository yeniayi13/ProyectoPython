from pydantic import BaseModel, EmailStr


class Client_in_create(BaseModel):
    id:str
    first_name:str
    last_name:str
    c_i:str
    email:EmailStr

class Client_in_update(BaseModel):
    first_name:str
    last_name:str
    c_i:str
    email:EmailStr

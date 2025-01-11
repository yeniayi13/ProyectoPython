from typing import Optional
from pydantic import BaseModel, Field



class Create_client_dto(BaseModel):
    id:str
    first_name:str
    last_name:str
    c_i:str
    email:str



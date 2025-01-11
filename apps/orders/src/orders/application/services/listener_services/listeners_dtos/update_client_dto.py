from pydantic import BaseModel


class Update_client_dto(BaseModel):
    id:str
    first_name:str
    last_name:str
    c_i:str
    email:str

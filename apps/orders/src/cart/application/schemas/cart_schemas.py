from pydantic import BaseModel


class Cart_in_modify(BaseModel):
    client_id:str
    product_id:str
    add:bool

class Cart_in_delete(BaseModel):
    client_id:str
    product_id:str

class Cart_in_response(BaseModel):
    name:str
    quantity:int
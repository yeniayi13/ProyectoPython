from pydantic import BaseModel, EmailStr


class Product_in_create(BaseModel):
    id:str
    name:str
    price:float
    quantity:int
    cost:float
    

class Product_in_update(BaseModel):
    name:str
    price:float
    quantity:int
    cost:float
    
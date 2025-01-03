from pydantic import BaseModel, EmailStr


class Product_in_create(BaseModel):
    id:str
    name:str
    price:float
    quantity:int
    

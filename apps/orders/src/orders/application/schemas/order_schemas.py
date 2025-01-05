
from pydantic import BaseModel


class Product_in_order(BaseModel):
    id:str
    quantity:int
    price:float
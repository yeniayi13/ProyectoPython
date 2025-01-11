from typing import Optional
from pydantic import BaseModel, Field



class Create_product_dto(BaseModel):
    id:str
    name:str
    price:float
    quantity:int
    cost:float






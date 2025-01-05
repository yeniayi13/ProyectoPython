
import datetime
from pydantic import BaseModel


class Product_in_order(BaseModel):
    id:str
    quantity:int
    price:float

class Order_in_response(BaseModel):
    id:str
    status:str
    total:float
    date:datetime.datetime

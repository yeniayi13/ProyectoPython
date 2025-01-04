from pydantic   import BaseModel, Field

class Modify_cart_quantity_dto(BaseModel):
     client_id: str 
     product_id: str
     add: bool


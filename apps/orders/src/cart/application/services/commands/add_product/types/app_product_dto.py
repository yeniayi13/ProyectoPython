from pydantic   import BaseModel, Field

class Add_product_dto(BaseModel):
     
     client_id: str 
     product_id: str
     quantity: int


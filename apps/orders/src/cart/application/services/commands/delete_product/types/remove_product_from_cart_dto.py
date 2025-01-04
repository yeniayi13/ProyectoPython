from pydantic   import BaseModel, Field

class Remove_product_from_cart_dto(BaseModel):
    client_id: str 
    product_id: str


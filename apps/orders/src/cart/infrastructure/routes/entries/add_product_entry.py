from pydantic   import BaseModel, Field

class Add_product_entry(BaseModel):
     #user_id: str =  Field(...,min_length=36, max_length=36)
     client_id: str =  Field(min_length=36, max_length=36,default='d9ffa241-e417-4f7f-9a78-93ef0172aa58')
     product_id: str =  Field(...,min_length=36, max_length=36)
     quantity: int =  Field(gt=0,default=1)  

     class Config:
        extra = 'forbid'


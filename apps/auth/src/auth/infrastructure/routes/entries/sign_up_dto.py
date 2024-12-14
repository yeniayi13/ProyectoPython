import re
from pydantic   import BaseModel, EmailStr, Field, field_validator

class Sign_up_dto(BaseModel):
     first_name: str =  Field(...,min_length=2, max_length=30)
     last_name: str=  Field(...,min_length=2, max_length=30)
     c_i: str =  Field(
         ...,
         min_length=10,
         max_length=10,
         pattern=r'^[VEJ]-\d{8}$' )
     username: str = Field(
         ...,
         min_length=6, 
         max_length=30
         )
     email: EmailStr = Field(...,min_length=6, max_length=50)
     password: str = Field(...,min_length=8)
     #password: str = Field(
      #   ...,
       #  pattern= r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$' 
        # )
     

     class Config:
        extra = 'forbid'

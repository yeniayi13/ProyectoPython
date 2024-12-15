from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Modify_client_dto(BaseModel):
     id: str =  Field(...)
     first_name:Optional[str] =  Field(min_length=2, max_length=30, default= None)
     last_name: Optional[str] =  Field(min_length=2, max_length=30, default= None)
     c_i: Optional[str] =  Field(
          min_length=10,
          max_length=10,
          pattern=r'^[VEJ]-\d{8}$',
          default= None 
          )
     username: Optional[str] = Field(
         min_length=6, 
         max_length=30,
         default= None
         )
     email: Optional[EmailStr] = Field(min_length=6, max_length=50, default= None)
     

     class Config:
        extra = 'ignore'

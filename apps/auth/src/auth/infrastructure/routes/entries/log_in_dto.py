from pydantic   import BaseModel, EmailStr, Field

class Log_in_dto(BaseModel):
     user: str = Field(...,min_length=6, max_length=50)
     password: str = Field(...,min_length=8)
     
     class Config:
        extra = 'forbid'

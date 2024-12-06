from sqlalchemy import DateTime, String, Integer, column
from user.application.models.user import User
from src.common.infrastructure.config.database.database import Base

class User_base(Base, User):
    __table_name__ = "users"
    
    id = column(String(150), primay_key = True)
    name = column(String(30))
    last_name = column(String(30))
    ci = column(String(8))
    username =column(String(30))
    email = column(String(50))
    pasword = column(String(250))
    role = column(String(10))
    created_at = column(DateTime)
    updated_at = column(DateTime)
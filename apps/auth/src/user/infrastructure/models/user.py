from sqlalchemy import CheckConstraint, Column, Date, Integer, String
from src.common.infrastructure.config.database.database import Base

class User(Base):
    __tablename__='users'
    id = Column(String(250), primary_key = True)
    first_name = Column(String(30),nullable = False)
    last_name = Column(String(30),nullable = False)
    c_i = Column(String(10),unique= True, nullable=False)
    username = Column(String(30), unique= True ,nullable = False)
    email = Column(String(50), unique= True, nullable = False)
    password = Column(String(250), nullable= False)
    role= Column(
        String(10),
        CheckConstraint(
            "role IN ('SUPERADMIN', 'MANAGER','CLIENT')",
            name='role_check'
        ),nullable= False, 
    )
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date)
    #created_at = Column(DateTime, default=datetime, nullable=False)
    #updated_at = Column(DateTime, default=datetime, onupdate=datetime, nullable=False)


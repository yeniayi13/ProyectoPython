from sqlalchemy import CheckConstraint, Column, Date, Integer, String
from src.common.infrastructure.config.database.database import Base

class User(Base):
    __tablename__='users'
    id = Column(String(250), primary_key = True)
    first_name = Column(String(50),nullable = False)
    last_name = Column(String(50),nullable = False)
    c_i = Column(String(10), nullable=False)
    username = Column(String(50),nullable = False)
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



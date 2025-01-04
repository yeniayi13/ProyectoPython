from src.common.infrastructure.config.database.database import Base,engine
from src.user.infrastructure.models import user

def create_tables():
    Base.metadata.create_all(bind=engine)
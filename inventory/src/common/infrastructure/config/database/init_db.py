from src.common.infrastructure.config.database.database import Base, engine
from src.inventory.infrastructure.models import Product, Inventory

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")


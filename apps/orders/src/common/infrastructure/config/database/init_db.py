from src.common.infrastructure.config.database.database import Base, engine
from src.orders.infrastructure.models.order import Order
from src.orders.infrastructure.models.order_items import OrderItem

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")

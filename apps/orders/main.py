from src.common.infrastructure.config.database.init_db import create_tables
from fastapi import FastAPI
from src.cart.infrastructure.routes.cart_routes import cart_routes
from src.orders.infrastructure.routes.orders_routes import order_routes


app = FastAPI(
    title='AuthService',
    description='This service is in charge of authenticating users of the platform',
    version='1.0',
    #on_startup='',
    #on_shutdown='',
    #middleware='',
    #lifespan= lifespan,
)

app.include_router(order_routes)
app.include_router(cart_routes)

def main():
    # Inicializar la base de datos y crear las tablas
    create_tables()
    print("Database initialized and tables created.")

#if __name__ == "__main__":
main()
   

import asyncio

from fastapi.security import OAuth2PasswordBearer
#from src.common.infrastructure.config.event_handler.event_handler_connection import get_channel, rabbitmq_connection
from src.common.infrastructure.config.database.init_db import create_tables
from fastapi import FastAPI, logger
from src.cart.infrastructure.routes.cart_routes import cart_routes
from src.common.utils.rabbitmq_client import RabbitMQClient
#from src.orders.infrastructure.listeners.order_listeners import start_consuming
from src.orders.infrastructure.routes.orders_routes import order_routes
from contextlib import asynccontextmanager



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

client_created_client = RabbitMQClient("amqp://guest:guest@localhost/")
client_updated_client = RabbitMQClient("amqp://guest:guest@localhost/")
product_created_client = RabbitMQClient("amqp://guest:guest@localhost/")
product_updated_client = RabbitMQClient("amqp://guest:guest@localhost/")

async def lifespan(app:FastAPI):
    print('Starting to Consume from RabbitMQ ')
    try:
        create_tables()
        print("Database initialized and tables created.")
        await client_created_client.start_consume("client_created")
        await product_created_client.start_consume("product_created")
        yield
        await client_created_client.close()
    except Exception as e:
        print(e)           


app = FastAPI(
    title='OrderService',
    description='This service is in charge of managing the orders',
    version='1.0',
    #on_startup='',
    #on_shutdown='',
    #middleware='',
    lifespan= lifespan,
)

app.include_router(order_routes)
app.include_router(cart_routes)


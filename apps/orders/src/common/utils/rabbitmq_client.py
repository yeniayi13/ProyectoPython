import asyncio
import json

from aio_pika import connect, IncomingMessage, Connection
from fastapi import Depends
from sqlalchemy.orm import Session

from src.common.infrastructure.config.database.database import get_db
from src.orders.application.services.listener_services.create_client_service import Create_client_service
from src.orders.application.services.listener_services.create_product_service import Create_product_service
from src.orders.application.services.listener_services.listeners_dtos.create_client_dto import Create_client_dto 
from src.orders.application.services.listener_services.listeners_dtos.update_client_dto import  Update_client_dto
from src.orders.application.services.listener_services.listeners_dtos.create_product_dto import Create_product_dto
from src.orders.application.services.listener_services.update_client_service import Update_client_service
from src.orders.application.services.listener_services.update_product_service import Update_product_service
from src.orders.infrastructure.repositories.client_postgres_repository import Client_postgres_repository
from src.orders.infrastructure.repositories.product_postgres_repository import Product_postgres_repository


class RabbitMQClient:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection: Connection = None
        self.consume_task: asyncio.Task = None

    async def connect(self, queue):
        if not self.connection:
            self.connection = await connect(self.amqp_url)
        print(f'Connection stablished with RabbitMQ in the {queue} queue')

    async def on_message(self, message: IncomingMessage) -> None:
        session = next(get_db())
        async with message.process():
            body = json.loads(message.body)
            if(message.routing_key == 'users.client_created'):
                dto = Create_client_dto(
                    id= body['id'],
                    first_name= body['first_name'],
                    last_name= body['last_name'],
                    c_i= body['C.I'],
                    email= body['email']
                )
                service = Create_client_service(Client_postgres_repository(session))
                response = await service.execute(dto)
                
                
            if(message.routing_key == 'users.client_modified'):
                print(body)
                dto = Update_client_dto(
                    id=body['id'],
                    first_name= body['first_name'],
                    last_name= body['last_name'],
                    c_i= body['C.I'],
                    email= body['email']
                )
                service = Update_client_service(Client_postgres_repository(session))
                response = await service.execute(dto)
            if(message.routing_key == 'products.product_created'):
                dto = Create_product_dto(
                    id=body['id'] ,
                    name=body['name'],
                    price=body['price'],
                    quantity=body['quantity'],
                    cost=body['cost']
                )
                service = Create_product_service(Product_postgres_repository(session))
                response = await service.execute(dto)

            if(message.routing_key == 'products.product_updated'):
                dto = Create_product_dto(
                    id=body['id'] ,
                    name=body['name'],
                    price=body['price'],
                    quantity=body['quantity'],
                    cost=body['cost']
                )
                service = Update_product_service(Product_postgres_repository(session))
                response = await service.execute(dto)

            try:
                if response.is_error():
                    print('Error:',response.get_error_message())
                    return None
                    #await message.nack()
                print(f'{message.routing_key.split('.')[1]} Event processed succesfully')
            except Exception as e:
                    print('Exception:',e)



    async def consume(self, queue_name: str):
        await self.connect(queue_name)
        channel = await self.connection.channel()
        queue = await channel.declare_queue(queue_name)
        await queue.consume(self.on_message, no_ack=False)        

    async def start_consume(self, queue_name: str):
        self.consume_task = asyncio.create_task(self.consume(queue_name))
        print(f'Starting to consume from {queue_name} queue')

    async def close(self):
        if self.consume_task:
            self.consume_task.cancel()
            try:
                await self.consume_task
            except asyncio.CancelledError as e :
                print(e)
            except Exception as unexpected_exception:
                print("Unexpected exception has occurred")
                print(unexpected_exception)
        if self.connection:
            await self.connection.close()
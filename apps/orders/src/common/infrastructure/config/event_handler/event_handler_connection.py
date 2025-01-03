import json
import pika
import pika.exceptions
import logging
from src.common.utils.result import Result
from src.orders.application.services.listener_services.create_client_service import Create_client_service
from src.orders.application.services.listener_services.listeners_dtos.create_client_dto import Create_client_dto
from src.orders.infrastructure.repositories.client_postgres_repository import Client_postgres_repository

connection_parameters = pika.ConnectionParameters('localhost')


#def client_created_callback(ch, method, properties, body):
#    
#    payload = json.loads(body)
#    print(payload)
#    dto = Create_client_dto(
#        id= payload['id'],
#        first_name=payload['first_name'],
#        last_name= payload['last_name'],
#        c_i=payload['C.I'],
#        email=payload['email'],
#        )
#    result:Result = await Create_client_service(Client_postgres_repository).execute(dto)
#
#    if result.is_succes():
#        ch.basic_ack(delivery_tag=method.delivery_tag)
#        print('event processed succesfully')
#    print(result.get_error_message())

    


async def rabbitmq_connection():
    try:
        print('Initializing connection with Message Queues')
        
        connection = pika.BlockingConnection(connection_parameters)
        client_created_channel = connection.channel()
        #client_created_channel.basic_consume(on_message_callback= await client_created_callback,queue='client_created')
        #client_created_channel.start_consuming()
        print('Connection stablished with rabbitmq')

    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Connection error: {e}")
        raise e
    except Exception as e:
        logging.error(f"Unkwon error: {e}")
        raise e

    



def get_channel():
    try:
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        yield channel
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Connection error: {e}")
        #return
    except pika.exceptions.StreamLostError:
        logging.error(f"Connection error: {e}")
        #return
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        #return
    finally:
        print('closing channel ...')
        channel.close() 
        connection.close()
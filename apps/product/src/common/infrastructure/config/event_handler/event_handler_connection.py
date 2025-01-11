import pika
import pika.exceptions
import logging
from src.common.infrastructure.config.config import get_settings

settings = get_settings()
RABBIT_HOST = settings.RABBIT_HOST
RABBIT_USER = settings.RABBIT_USER
RABBIT_PASSWORD = settings.RABBIT_PASSWORD

import socket

try:
    print(f"Resolving host: {RABBIT_HOST}")
    resolved_ip = socket.gethostbyname(RABBIT_HOST)
    print(f"Resolved IP: {resolved_ip}")
except socket.gaierror as e:
    print(f"Failed to resolve {RABBIT_HOST}: {e}")

print('AQUÍ ESTÁN TODAS LA VARIABLES DE ENTORNO')
print(settings)

try:
    print('Initializing connection with Message Queues in Product Service')
    print(f'RABBIT_HOST: {RABBIT_HOST}')
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
    connection_parameters = pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=5672,
        credentials=credentials
    )
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    exchange = channel.exchange_declare(
                exchange='products',
                exchange_type='direct'
                )

    product_created_queue = channel.queue_declare('product_created')
    product_updated_queue = channel.queue_declare('product_updated')
    product_delated_queue = channel.queue_declare('product_delated')

    channel.queue_bind(exchange='products', queue=product_created_queue.method.queue,routing_key='products.product_created')
    channel.queue_bind(exchange='products', queue=product_updated_queue.method.queue, routing_key='products.product_updated')
    channel.queue_bind(exchange='products', queue=product_delated_queue.method.queue, routing_key='products.product_deleted')
    
    print('Product Queues Ready')
except pika.exceptions.AMQPConnectionError as e:
    logging.error(f"Connection error: {e}")
    print('ERROR DE CONEXIÓN: ', e)
    raise e
except Exception as e:
    logging.error(f"Unkwon error: {e}")
    print('ERROR DESCONOCIDO: ', e)
    raise e

def get_channel():
    try:
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        print('yielding channel ...')
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